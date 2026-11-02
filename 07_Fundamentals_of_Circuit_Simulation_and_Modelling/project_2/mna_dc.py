"""
ECSE 472 - Project 2
Linear and nonlinear DC analysis using Modified Nodal Analysis (MNA).
Based on project_1/mna_dc.py; Project 1 remains an independent snapshot.

Usage:
    python mna_dc.py circuits/diode.cir

This implementation uses only the Python standard library. It does not call SPICE.
Supported elements: R, independent V/I sources, C, L, VCVS, CCVS, VCCS, CCCS.
Adds Shockley diodes and damped Newton-Raphson iteration.
"""

import math
import sys

DIODE_IS = 1e-15  # A
DIODE_VT = 0.025  # V


# 【数值转换】1k→1000；1e10 直接由 float 转换。输入微单位使用 u。
def parse_value(text):
    """Parse a number with common SPICE engineering suffixes."""
    text = text.strip()
    suffixes = {
        "t": 1e12, "g": 1e9, "meg": 1e6, "k": 1e3,
        "m": 1e-3, "u": 1e-6, "n": 1e-9, "p": 1e-12,
        "f": 1e-15,
    }
    lower = text.lower()

    # SPICE commonly treats 'M' as milli and 'MEG' as mega.
    for suffix in ("meg", "t", "g", "k", "m", "u", "n", "p", "f"):
        if lower.endswith(suffix):
            number = text[:-len(suffix)]
            try:
                return float(number) * suffixes[suffix]
            except ValueError:
                break
    return float(text)


# 【读取网表】读取文件，过滤空行/注释，提取标题，识别 .dc/.end，拆开元件行。
def read_netlist(filename):
    """Read a netlist; the first non-empty line is the circuit title."""
    with open(filename, "r", encoding="utf-8") as file:
        raw_lines = file.readlines()

    lines = []
    for raw in raw_lines:
        line = raw.strip()
        if not line:
            continue
        lines.append(line)

    if not lines:
        raise ValueError("The netlist is empty.")

    title = lines[0]
    elements = []
    dc_enabled = False
    ended = False

    for line in lines[1:]:
        if line.startswith(("*", "#")):
            continue
        line = line.split(";", 1)[0].strip()
        if not line:
            continue
        lower = line.lower()
        if lower == ".end":
            ended = True
            break
        if lower == ".dc":
            dc_enabled = True
            continue
        if lower.startswith("."):
            raise ValueError(f"Unsupported directive: {line}")

        parts = line.split()
        elements.append(parts)

    if not ended:
        raise ValueError('The netlist must end with ".end".')
    if not dc_enabled:
        raise ValueError('Linear DC analysis requested, but ".dc" is missing.')
    if not elements:
        raise ValueError("No circuit elements were found.")

    return title, elements


# 【识别类型】先认四种受控源前缀，再认 R/V/I/C/L，避免前缀混淆。
def element_kind(name):
    """Recognize controlled-source prefixes before single-letter prefixes."""
    upper = name.upper()
    for prefix in ("VCVS", "CCVS", "VCCS", "CCCS"):
        if upper.startswith(prefix):
            return prefix
    if not upper:
        raise ValueError("An element has an empty name.")
    kind = upper[0]
    if kind in ("R", "V", "I", "C", "L", "D"):
        return kind
    raise ValueError(f"Unsupported element type: {name}")


# 【解析元件】检查重名和参数，把每行存成包含名称、类型、节点和数值的字典。
# 电压控制源用两个控制节点；电流控制源用控制支路名称，最后统一检查引用。
def parse_elements(raw_elements):
    """Convert tokens to dictionaries with validated fields."""
    elements = []
    names = set()

    for parts in raw_elements:
        name = parts[0]
        if name.lower() in names:
            raise ValueError(f"Duplicate element name: {name}")
        names.add(name.lower())
        kind = element_kind(name)

        if kind == "D":
            if len(parts) != 3:
                raise ValueError(f"{name}: expected NAME anode cathode")
            elements.append({
                "name": name, "kind": kind, "p": parts[1], "n": parts[2],
            })

        elif kind in ("R", "C", "L"):
            if len(parts) != 4:
                raise ValueError(f"{name}: expected NAME node+ node- value")
            value = parse_value(parts[3])
            if kind == "R" and value == 0:
                raise ValueError(f"{name}: resistance cannot be zero")
            if kind in ("R", "C", "L") and value < 0:
                raise ValueError(f"{name}: value cannot be negative")
            elements.append({
                "name": name, "kind": kind, "p": parts[1],
                "n": parts[2], "value": value,
            })

        elif kind in ("V", "I"):
            if len(parts) not in (4, 5):
                raise ValueError(
                    f"{name}: expected NAME node+ node- [DC] value"
                )
            if len(parts) == 5:
                if parts[3].upper() != "DC":
                    raise ValueError(f"{name}: only DC source values are supported")
                value_text = parts[4]
            else:
                value_text = parts[3]
            elements.append({
                "name": name, "kind": kind, "p": parts[1],
                "n": parts[2], "value": parse_value(value_text),
            })

        elif kind in ("VCVS", "VCCS"):
            if len(parts) != 6:
                raise ValueError(
                    f"{name}: expected NAME node+ node- control+ control- gain"
                )
            elements.append({
                "name": name, "kind": kind, "p": parts[1], "n": parts[2],
                "cp": parts[3], "cn": parts[4], "gain": parse_value(parts[5]),
            })

        elif kind in ("CCVS", "CCCS"):
            if len(parts) != 5:
                raise ValueError(
                    f"{name}: expected NAME node+ node- controlling_voltage_source gain"
                )
            elements.append({
                "name": name, "kind": kind, "p": parts[1], "n": parts[2],
                "control": parts[3], "gain": parse_value(parts[4]),
            })

    for element in elements:
        for field in ("value", "gain"):
            if field in element and not math.isfinite(element[field]):
                raise ValueError(f'{element["name"]}: {field} must be finite')

    # Validate current-controlled source references after all elements are known.
    by_name = {e["name"].lower(): e for e in elements}
    for e in elements:
        if e["kind"] in ("CCVS", "CCCS"):
            control = by_name.get(e["control"].lower())
            if control is None:
                raise ValueError(
                    f'{e["name"]}: controlling element "{e["control"]}" was not found'
                )
            if control["kind"] not in ("V", "VCVS", "CCVS", "L"):
                raise ValueError(
                    f'{e["name"]}: current must be sensed through a voltage-defined branch '
                    "(V, VCVS, CCVS, or L)"
                )

    return elements


# 【建立分块 MNA】直接建立 G、B、C、D，以及 i_vector、e_vector。
# 未知量顺序：先节点电压，后 V/VCVS/CCVS/L 的支路电流。
def build_mna_blocks(elements, operating_point=None):
    """Stamp G*v+B*j=i and C*v+D*j=e, keeping all blocks separate."""
    # 【节点与编号】收集非接地节点并编号，再给额外支路电流编号。
    # N 个节点、M 个支路电流，对应 N+M 个未知量。
    nodes = []
    for e in elements:
        for key in ("p", "n", "cp", "cn"):
            node = e.get(key)
            if node is not None and node != "0" and node not in nodes:
                nodes.append(node)

    node_index = {node: i for i, node in enumerate(nodes)}
    voltage_defined = [
        e for e in elements if e["kind"] in ("V", "VCVS", "CCVS", "L")
    ]
    branch_number = {
        e["name"].lower(): i
        for i, e in enumerate(voltage_defined)
    }

    # 【初始化】G: N×N；B: N×M；C: M×N；D: M×M。
    size = len(nodes) + len(voltage_defined)
    if size == 0:
        raise ValueError("The circuit has no unknowns.")

    N, M = len(nodes), len(voltage_defined)
    G = [[0.0 for _ in range(N)] for _ in range(N)]
    B = [[0.0 for _ in range(M)] for _ in range(N)]
    C = [[0.0 for _ in range(N)] for _ in range(M)]
    # 矩阵块 D 是电压约束中的电流系数；与二极管元件 D 无关。
    # 独立电压源在这里填零；CCVS 会填入控制支路电流的系数。
    D = [[0.0 for _ in range(M)] for _ in range(M)]
    i_vector = [0.0 for _ in range(N)]
    e_vector = [0.0 for _ in range(M)]

    # 【查节点编号】地返回 None，表示没有对应的未知电压位置。
    def node_idx(node):
        return None if node == "0" else node_index[node]

    # 【填入矩阵】跳过接地项，其他位置用 += 累加元件贡献。
    def add(matrix, row, col, value):
        if row is not None and col is not None:
            matrix[row][col] += value

    # 【电阻模板 / G 块】对角 +g、交叉 -g；来自 I=g(Vp-Vn)。
    def stamp_conductance(p, n, conductance):
        ip, inn = node_idx(p), node_idx(n)
        add(G, ip, ip, conductance)
        add(G, inn, inn, conductance)
        add(G, ip, inn, -conductance)
        add(G, inn, ip, -conductance)

    # 【电压支路模板：老师问 B matrix / add V 时看这里】
    # 前两次 add：B 块，把 +Ib/-Ib 加入两端节点方程。
    # 后两次 add：C 块，写出 Vp-Vn；最后 e_vector += voltage 填入已知电压。
    def stamp_branch(p, n, branch, voltage=0.0):
        ip, inn = node_idx(p), node_idx(n)
        add(B, ip, branch, 1.0)
        add(B, inn, branch, -1.0)
        add(C, branch, ip, 1.0)
        add(C, branch, inn, -1.0)
        e_vector[branch] += voltage

    # 【逐个元件填 stamp】以下各分支按类型修改对应的分块或右端向量。
    for e in elements:
        kind = e["kind"]
        p, n = e["p"], e["n"]

        # 【R 电阻】1.0/value 就是计算 1/R，再调用电阻模板。
        if kind == "R":
            stamp_conductance(p, n, 1.0 / e["value"])

        # 【D 二极管】在当前工作点线性化：Id ≈ gd*Vd + Ieq。
        # 电导印章与电阻相同；Ieq 从阳极 p 流向阴极 n。
        elif kind == "D" and operating_point is not None:
            ip, inn = node_idx(p), node_idx(n)
            vp = 0.0 if ip is None else operating_point[ip]
            vn = 0.0 if inn is None else operating_point[inn]
            current, gd = diode_iv(vp - vn)
            ieq = current - gd * (vp - vn)
            stamp_conductance(p, n, gd)
            if ip is not None:
                i_vector[ip] -= ieq
            if inn is not None:
                i_vector[inn] += ieq

        # 【I 电流源】只改 i_vector；电流 p→n，所以 p 减、n 加。
        elif kind == "I":
            # Positive source current flows from p to n.
            ip, inn = node_idx(p), node_idx(n)
            if ip is not None:
                i_vector[ip] -= e["value"]
            if inn is not None:
                i_vector[inn] += e["value"]

        # 【V 电压源】找到电流编号，把电源电压传给 stamp_branch。
        elif kind == "V":
            branch = branch_number[e["name"].lower()]
            stamp_branch(p, n, branch, e["value"])

        # 【C 电容】直流稳态开路，电流为零，不填矩阵。
        elif kind == "C":
            # An ideal capacitor is an open circuit in DC steady state.
            pass

        # 【L 电感】直流稳态短路，用 0V 电压支路表示，保留电流未知量。
        elif kind == "L":
            # An ideal inductor is a short circuit in DC steady state.
            branch = branch_number[e["name"].lower()]
            stamp_branch(p, n, branch, 0.0)

        # 【VCVS / C 块】Vp-Vn=gain*(Vcp-Vcn)，在电压约束行补控制电压系数。
        elif kind == "VCVS":
            branch = branch_number[e["name"].lower()]
            stamp_branch(p, n, branch, 0.0)
            row = branch
            add(C, row, node_idx(e["cp"]), -e["gain"])
            add(C, row, node_idx(e["cn"]), e["gain"])

        # 【VCCS / G 块】输出电流=gain*(Vcp-Vcn)，直接加入两端节点方程。
        elif kind == "VCCS":
            cp, cn = node_idx(e["cp"]), node_idx(e["cn"])
            ip, inn = node_idx(p), node_idx(n)
            g = e["gain"]
            add(G, ip, cp, g)
            add(G, ip, cn, -g)
            add(G, inn, cp, -g)
            add(G, inn, cn, g)

        # 【CCVS / D 块】Vp-Vn=gain*Icontrol，在约束行的控制电流列加入 -gain。
        elif kind == "CCVS":
            branch = branch_number[e["name"].lower()]
            stamp_branch(p, n, branch, 0.0)
            control_branch = branch_number[e["control"].lower()]
            add(D, branch, control_branch, -e["gain"])

        # 【CCCS / B 块】输出电流=gain*Icontrol，在两端节点行补 +gain/-gain。
        elif kind == "CCCS":
            control_branch = branch_number[e["control"].lower()]
            ip, inn = node_idx(p), node_idx(n)
            add(B, ip, control_branch, e["gain"])
            add(B, inn, control_branch, -e["gain"])

    # 支路编号 0...M-1 用于 B/C/D；解向量中的支路位置从 N 开始。
    branch_index = {name: N + k for name, k in branch_number.items()}
    return {
        "G": G, "B": B, "C": C, "D": D,
        "i_vector": i_vector, "e_vector": e_vector,
        "nodes": nodes, "node_index": node_index,
        "branch_index": branch_index, "voltage_defined": voltage_defined,
    }


# 【直接分块求解】四块分别保存并消元，不创建完整矩阵或增广矩阵。
def solve_block_system(G, B, C, D, i_vector, e_vector):
    """Solve G*v+B*j=i and C*v+D*j=e by row operations on separate blocks."""
    G, B = [row[:] for row in G], [row[:] for row in B]
    C, D = [row[:] for row in C], [row[:] for row in D]
    i_vector, e_vector = i_vector[:], e_vector[:]
    N, M = len(i_vector), len(e_vector)
    size = N + M

    # 每行的左右两部分仍在各自的矩阵中，这里只返回引用。
    def row_parts(row):
        return (G[row], B[row]) if row < N else (C[row - N], D[row - N])

    def rhs(row):
        return i_vector[row] if row < N else e_vector[row - N]

    def set_rhs(row, value):
        if row < N:
            i_vector[row] = value
        else:
            e_vector[row - N] = value

    def entry(row, col):
        left, right = row_parts(row)
        return left[col] if col < N else right[col - N]

    # 【行缩放】分别缩放左右两部分。
    for row in range(size):
        left, right = row_parts(row)
        scale = max(max(map(abs, left), default=0.0),
                    max(map(abs, right), default=0.0))
        if scale == 0.0 or not math.isfinite(scale):
            raise ValueError("Singular or non-finite MNA blocks; check circuit topology.")
        for k in range(N):
            left[k] /= scale
        for k in range(M):
            right[k] /= scale
        set_rhs(row, rhs(row) / scale)

    for col in range(size):
        # 【选主元】也允许交换上下两组的方程，无须求 G 的逆矩阵。
        pivot = max(range(col, size), key=lambda row: abs(entry(row, col)))
        if abs(entry(pivot, col)) < 1e-14:
            raise ValueError("The MNA system is singular; check floating nodes or sources.")
        if pivot != col:
            left_a, right_a = row_parts(col)
            left_b, right_b = row_parts(pivot)
            left_a[:], left_b[:] = left_b[:], left_a[:]
            right_a[:], right_b[:] = right_b[:], right_a[:]
            value = rhs(col)
            set_rhs(col, rhs(pivot))
            set_rhs(pivot, value)

        # 【主元变成 1】两个矩阵行部分分别除以主元。
        left, right = row_parts(col)
        pivot_value = entry(col, col)
        for k in range(N):
            left[k] /= pivot_value
        for k in range(M):
            right[k] /= pivot_value
        set_rhs(col, rhs(col) / pivot_value)

        # 【消元】分别更新 G/C、B/D 中的行部分。
        for row in range(size):
            if row == col:
                continue
            factor = entry(row, col)
            if factor == 0.0:
                continue
            row_left, row_right = row_parts(row)
            for k in range(N):
                row_left[k] -= factor * left[k]
            for k in range(M):
                row_right[k] -= factor * right[k]
            set_rhs(row, rhs(row) - factor * rhs(col))

    solution = i_vector + e_vector  # 解向量：先 v，后 j。
    if not all(math.isfinite(value) for value in solution):
        raise ValueError("The solution is non-finite.")
    return solution


def diode_iv(voltage):
    """Shockley current (anode -> cathode) and differential conductance."""
    exponent = voltage / DIODE_VT
    if exponent > 700:
        raise OverflowError("Diode voltage exceeds the floating-point range.")
    return (DIODE_IS * math.expm1(exponent),
            DIODE_IS / DIODE_VT * math.exp(exponent))


# 【牛顿迭代】固定线性部分和当前工作点始终使用分块形式。
def solve_dc(elements, max_iterations=200, current_tolerance=1e-11,
             voltage_tolerance=1e-9):
    """Solve DC operating points using separate G, B, C, D blocks."""
    if max_iterations <= 0:
        raise ValueError("max_iterations must be positive.")
    if not all(math.isfinite(t) and t > 0
               for t in (current_tolerance, voltage_tolerance)):
        raise ValueError("Tolerances must be positive and finite.")

    linear = build_mna_blocks(elements)
    nodes, node_index = linear["nodes"], linear["node_index"]
    N, M = len(nodes), len(linear["e_vector"])
    size = N + M
    diodes = [element for element in elements if element["kind"] == "D"]

    def node_voltage(x, node):
        return 0.0 if node == "0" else x[node_index[node]]

    def residual(x):
        v, j = x[:N], x[N:]
        node_residual, branch_residual = [], []
        for row in range(N):
            value = sum(g * voltage for g, voltage in zip(linear["G"][row], v))
            value += sum(b * current for b, current in zip(linear["B"][row], j))
            node_residual.append(value - linear["i_vector"][row])
        for row in range(M):
            value = sum(c * voltage for c, voltage in zip(linear["C"][row], v))
            value += sum(d * current for d, current in zip(linear["D"][row], j))
            branch_residual.append(value - linear["e_vector"][row])
        for element in diodes:
            vd = node_voltage(x, element["p"]) - node_voltage(x, element["n"])
            current, _ = diode_iv(vd)
            if element["p"] != "0":
                node_residual[node_index[element["p"]]] += current
            if element["n"] != "0":
                node_residual[node_index[element["n"]]] -= current
        return node_residual + branch_residual

    def residual_norm(values):
        if not all(math.isfinite(value) for value in values):
            return math.inf
        return max((abs(value) / (current_tolerance if k < N else voltage_tolerance)
                    for k, value in enumerate(values)), default=0.0)

    x = [0.0] * size
    for iteration in range(max_iterations + 1):
        blocks = build_mna_blocks(elements, x)
        G, B, C, D = blocks["G"], blocks["B"], blocks["C"], blocks["D"]
        values = residual(x)
        norm = residual_norm(values)
        if norm <= 1.0:
            solve_block_system(G, B, C, D, [0.0] * N, [0.0] * M)
            return {
                **blocks, "solution": x, "iterations": iteration,
                "max_kcl_error": max(map(abs, values[:N]), default=0.0),
                "max_constraint_error": max(map(abs, values[N:]), default=0.0),
            }
        if iteration == max_iterations:
            break

        # 分块修正方程：G*dv+B*dj=-F_node；C*dv+D*dj=-F_branch。
        node_rhs = [-value for value in values[:N]]
        branch_rhs = [-value for value in values[N:]]
        delta = solve_block_system(G, B, C, D, node_rhs, branch_rhs)
        alpha = 1.0
        for element in diodes:
            change = node_voltage(delta, element["p"]) - node_voltage(delta, element["n"])
            if change > 0.1:
                alpha = min(alpha, 0.1 / change)

        for _ in range(60):
            trial = [value + alpha * step for value, step in zip(x, delta)]
            try:
                trial_norm = residual_norm(residual(trial))
            except OverflowError:
                trial_norm = math.inf
            if trial_norm <= 1.0 or trial_norm < norm * (1.0 - 1e-4 * alpha):
                x = trial
                break
            alpha *= 0.5
        else:
            raise ValueError("Newton backtracking failed; check circuit topology or parameters.")
    raise ValueError(f"DC analysis did not converge after {max_iterations} iterations.")


def print_mna_blocks(result):
    """Print each block and each right-hand-side vector separately."""
    N, M = len(result["nodes"]), len(result["voltage_defined"])
    print("\nBlock equations: G*v + B*j = i; C*v + D*j = e")
    print("v: node voltages; j: voltage-defined branch currents")
    print("Node order: " + (", ".join(result["nodes"]) or "(none)"))
    print("Branch order: " + (", ".join(e["name"] for e in result["voltage_defined"]) or "(none)"))
    for name, rows, cols in (("G", N, N), ("B", N, M), ("C", M, N), ("D", M, M)):
        print(f"\n{name} matrix ({rows} x {cols}):")
        for row in result[name]:
            print("  [" + ", ".join(f"{value: .6g}" for value in row) + "]")
        if rows == 0:
            print("  (no rows)")
    print("\ni vector (node-current RHS):")
    print("  [" + ", ".join(f"{value: .6g}" for value in result["i_vector"]) + "]")
    print("e vector (voltage-constraint RHS):")
    print("  [" + ", ".join(f"{value: .6g}" for value in result["e_vector"]) + "]")


# 【主流程】取文件路径→读取→解析→建矩阵→求解→打印；出错则显示错误并退出。
# 输出负电流表示方向与“第一个节点→第二个节点”相反。
def main(netlist_path=None):
    """Run DC analysis from a netlist path or the command-line argument.

    Examples:
        python mna_dc.py circuits/diode.cir
        main("/content/simple_voltage_divider.cir")  # Google Colab
    """
    if netlist_path is None:
        if len(sys.argv) != 2:
            print("Usage: python mna_dc.py circuit.cir")
            sys.exit(2)
        netlist_path = sys.argv[1]

    try:
        title, raw_elements = read_netlist(netlist_path)
        elements = parse_elements(raw_elements)
        result = solve_dc(elements)
        solution = result["solution"]
        nodes, node_index = result["nodes"], result["node_index"]
        branch_index, voltage_defined = result["branch_index"], result["voltage_defined"]

        print(f"Circuit: {title}")
        print(f"Elements: {len(elements)}")
        print(f"Non-ground nodes: {', '.join(nodes) if nodes else '(none)'}")
        if any(e["kind"] == "D" for e in elements):
            print("Diode parameters: Is=1e-15 A, Vt=0.025 V")
            print("The printed blocks are linearized at the final operating point.")
        print(f'Newton updates: {result["iterations"]}')
        print_mna_blocks(result)

        print("\nDC operating-point solution:")
        for node in nodes:
            print(f"  V({node}) = {solution[node_index[node]]:.9g} V")
        for element in voltage_defined:
            idx = branch_index[element["name"].lower()]
            print(
                f"  I({element['name']}) = {solution[idx]:.9g} A "
                "(positive from first node to second node)"
            )

        # CCCS elements do not introduce their own MNA branch unknown.
        # Compute their output current from the controlling branch current.
        # 【补算 CCCS 电流】它没有自己的未知量，用增益乘控制支路电流。
        for element in elements:
            if element["kind"] == "CCCS":
                control_idx = branch_index[element["control"].lower()]
                current = element["gain"] * solution[control_idx]
                print(
                    f"  I({element['name']}) = {current:.9g} A "
                    "(positive from first node to second node)"
                )

        # 【补算元件电流】没有独立支路未知量的元件由工作点求出电流。
        def voltage(node):
            return 0.0 if node == "0" else solution[node_index[node]]

        for element in elements:
            kind = element["kind"]
            v = voltage(element["p"]) - voltage(element["n"])
            if kind == "R":
                current = v / element["value"]
            elif kind == "I":
                current = element["value"]
            elif kind == "C":
                current = 0.0
            elif kind == "D":
                current = diode_iv(v)[0]
            elif kind == "VCCS":
                current = element["gain"] * (voltage(element["cp"]) - voltage(element["cn"]))
            else:
                continue
            print(f'  I({element["name"]}) = {current:.9g} A '
                  "(positive from first node to second node)")

        print(f'Maximum KCL residual: {result["max_kcl_error"]:.3e} A')
        print(f'Maximum voltage-constraint residual: {result["max_constraint_error"]:.3e} V')

    except (OSError, ValueError, KeyError, OverflowError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


# 【启动】直接运行文件时调用 main；import 时不自动运行。
if __name__ == "__main__":
    main()
