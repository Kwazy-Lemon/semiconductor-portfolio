"""
ECSE 472 - Project 2
Linear and nonlinear DC analysis using Modified Nodal Analysis (MNA).
Based on project_1/mna_dc.py; Project 1 remains an independent snapshot.

Usage:
    python mna_dc.py circuits/simple.cir

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


# 【建立 MNA】直接建立完整 A，不单独创建 G/B/C/D 分块；右侧向量叫 z。
# 未知量顺序：先节点电压，后 V/VCVS/CCVS/L 的支路电流。
def build_mna(elements, operating_point=None):
    """Build A*x=z; with an operating point, include diode companion stamps.

    Without an operating point, D contributes nodes but no matrix entries.
    This gives the fixed linear part used to evaluate the true residual.
    """
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
    branch_index = {
        e["name"].lower(): len(nodes) + i
        for i, e in enumerate(voltage_defined)
    }

    # 【初始化】建立 (N+M) 阶全零矩阵 A，以及同长度的右侧向量 z。
    size = len(nodes) + len(voltage_defined)
    if size == 0:
        raise ValueError("The circuit has no unknowns.")

    A = [[0.0 for _ in range(size)] for _ in range(size)]
    z = [0.0 for _ in range(size)]

    # 【查节点编号】地返回 None，表示没有对应的未知电压位置。
    def node_idx(node):
        return None if node == "0" else node_index[node]

    # 【填入矩阵】跳过接地项，其他位置用 += 累加元件贡献。
    def add(row, col, value):
        if row is not None and col is not None:
            A[row][col] += value

    # 【电阻模板 / G 块】对角 +g、交叉 -g；来自 I=g(Vp-Vn)。
    def stamp_conductance(p, n, conductance):
        ip, inn = node_idx(p), node_idx(n)
        add(ip, ip, conductance)
        add(inn, inn, conductance)
        add(ip, inn, -conductance)
        add(inn, ip, -conductance)

    # 【电压支路模板：老师问 B matrix / add V 时看这里】
    # 前两次 add：B 块，把 +Ib/-Ib 加入两端节点方程。
    # 后两次 add：C 块，写出 Vp-Vn；最后 z += voltage 填入已知电压。
    def stamp_branch(p, n, branch, voltage=0.0):
        ip, inn = node_idx(p), node_idx(n)
        add(ip, branch, 1.0)
        add(inn, branch, -1.0)
        add(branch, ip, 1.0)
        add(branch, inn, -1.0)
        z[branch] += voltage

    # 【逐个元件填 stamp】以下各分支按类型修改 A 或 z。
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
                z[ip] -= ieq
            if inn is not None:
                z[inn] += ieq

        # 【I 电流源】只改右侧 z；电流 p→n，所以 p 减、n 加。
        elif kind == "I":
            # Positive source current flows from p to n.
            ip, inn = node_idx(p), node_idx(n)
            if ip is not None:
                z[ip] -= e["value"]
            if inn is not None:
                z[inn] += e["value"]

        # 【V 电压源】找到电流编号，把电源电压传给 stamp_branch。
        elif kind == "V":
            branch = branch_index[e["name"].lower()]
            stamp_branch(p, n, branch, e["value"])

        # 【C 电容】直流稳态开路，电流为零，不填矩阵。
        elif kind == "C":
            # An ideal capacitor is an open circuit in DC steady state.
            pass

        # 【L 电感】直流稳态短路，用 0V 电压支路表示，保留电流未知量。
        elif kind == "L":
            # An ideal inductor is a short circuit in DC steady state.
            branch = branch_index[e["name"].lower()]
            stamp_branch(p, n, branch, 0.0)

        # 【VCVS / C 块】Vp-Vn=gain*(Vcp-Vcn)，在电压约束行补控制电压系数。
        elif kind == "VCVS":
            branch = branch_index[e["name"].lower()]
            stamp_branch(p, n, branch, 0.0)
            row = branch
            add(row, node_idx(e["cp"]), -e["gain"])
            add(row, node_idx(e["cn"]), e["gain"])

        # 【VCCS / G 块】输出电流=gain*(Vcp-Vcn)，直接加入两端节点方程。
        elif kind == "VCCS":
            cp, cn = node_idx(e["cp"]), node_idx(e["cn"])
            ip, inn = node_idx(p), node_idx(n)
            g = e["gain"]
            add(ip, cp, g)
            add(ip, cn, -g)
            add(inn, cp, -g)
            add(inn, cn, g)

        # 【CCVS / D 块】Vp-Vn=gain*Icontrol，在约束行的控制电流列加入 -gain。
        elif kind == "CCVS":
            branch = branch_index[e["name"].lower()]
            stamp_branch(p, n, branch, 0.0)
            control_branch = branch_index[e["control"].lower()]
            add(branch, control_branch, -e["gain"])

        # 【CCCS / B 块】输出电流=gain*Icontrol，在两端节点行补 +gain/-gain。
        elif kind == "CCCS":
            control_branch = branch_index[e["control"].lower()]
            ip, inn = node_idx(p), node_idx(n)
            add(ip, control_branch, e["gain"])
            add(inn, control_branch, -e["gain"])

    return A, z, nodes, node_index, branch_index, voltage_defined


# 【解方程】b 就是 z；复制并拼成增广矩阵 [A|b]，不修改原始 A。
# 消元不改变矩阵大小，只把左侧化成单位矩阵。
def solve_linear_system(A, b):
    """Solve A*x=b with Gaussian elimination and partial pivoting."""
    n = len(b)
    M = [A[i][:] + [b[i]] for i in range(n)]
    # Row scaling avoids treating small conductances as absolute zero.
    for row in M:
        scale = max(map(abs, row[:-1]), default=0.0)
        if scale == 0.0 or not math.isfinite(scale):
            raise ValueError("Singular or non-finite MNA matrix; check circuit topology.")
        for j in range(n + 1):
            row[j] /= scale

    for col in range(n):
        # 【选主元并换行】挑本列绝对值最大的候选数；太接近零就报错。
        pivot = max(range(col, n), key=lambda row: abs(M[row][col]))
        if abs(M[pivot][col]) < 1e-14:
            raise ValueError(
                "The MNA matrix is singular. Check for floating nodes, "
                "conflicting ideal sources, or an underdetermined circuit."
            )
        M[col], M[pivot] = M[pivot], M[col]

        # 【变成 1】整行除以主元，右侧也同步除。
        pivot_value = M[col][col]
        for j in range(col, n + 1):
            M[col][j] /= pivot_value

        # 【消成 0】其他行减去 factor 倍主元行，消掉本列其余元素。
        for row in range(n):
            if row == col:
                continue
            factor = M[row][col]
            if factor == 0:
                continue
            for j in range(col, n + 1):
                M[row][j] -= factor * M[col][j]

    # 【取答案】左边成为单位矩阵后，最后一列就是电压/电流的解。
    solution = [M[i][n] for i in range(n)]
    if not all(math.isfinite(v) for v in solution):
        raise ValueError("The linear solution is non-finite.")
    return solution



def diode_iv(voltage):
    """Shockley current (anode -> cathode) and differential conductance."""
    exponent = voltage / DIODE_VT
    if exponent > 700:
        raise OverflowError("Diode voltage exceeds the floating-point range.")
    return (DIODE_IS * math.expm1(exponent),
            DIODE_IS / DIODE_VT * math.exp(exponent))


# 【非线性 DC】保留项目一的所有线性印章，每次只更新二极管的工作点。
def solve_dc(elements, max_iterations=200, current_tolerance=1e-11,
             voltage_tolerance=1e-9):
    """Solve the true DC equations using damped Newton iterations.

    KCL rows are checked in amperes; voltage-constraint rows in volts.
    No hidden ground conductance or clipped diode curve is introduced.
    """
    if max_iterations <= 0:
        raise ValueError("max_iterations must be positive.")
    if not all(math.isfinite(t) and t > 0
               for t in (current_tolerance, voltage_tolerance)):
        raise ValueError("Tolerances must be positive and finite.")

    linear_A, linear_z, nodes, node_index, branch_index, voltage_defined = build_mna(elements)
    size, node_count = len(linear_z), len(nodes)
    diodes = [e for e in elements if e["kind"] == "D"]

    def node_voltage(x, node):
        return 0.0 if node == "0" else x[node_index[node]]

    def residual(x):
        # Use the original diode currents, independently of Ieq cancellation.
        values = [sum(a * v for a, v in zip(row, x)) - rhs
                  for row, rhs in zip(linear_A, linear_z)]
        for e in diodes:
            vd = node_voltage(x, e["p"]) - node_voltage(x, e["n"])
            current, _ = diode_iv(vd)
            if e["p"] != "0":
                values[node_index[e["p"]]] += current
            if e["n"] != "0":
                values[node_index[e["n"]]] -= current
        return values

    def residual_norm(values):
        if not all(math.isfinite(v) for v in values):
            return math.inf
        return max((abs(v) / (current_tolerance if i < node_count else voltage_tolerance)
                    for i, v in enumerate(values)), default=0.0)

    x = [0.0] * size
    for iteration in range(max_iterations + 1):
        A, z, _, _, _, _ = build_mna(elements, x)
        values = residual(x)
        norm = residual_norm(values)
        if norm <= 1.0:
            # Zero residual is possible even in an underdetermined circuit.
            solve_linear_system(A, [0.0] * size)
            return {
                "solution": x, "A": A, "z": z, "nodes": nodes,
                "node_index": node_index, "branch_index": branch_index,
                "voltage_defined": voltage_defined, "iterations": iteration,
                "max_kcl_error": max(map(abs, values[:node_count]), default=0.0),
                "max_constraint_error": max(map(abs, values[node_count:]), default=0.0),
            }
        if iteration == max_iterations:
            break

        # A is the Jacobian from the linearized MNA stamps.
        # J*delta=-F is equivalent to J*x_new=z for an undamped step.
        delta = solve_linear_system(A, [-v for v in values])
        alpha = 1.0
        for e in diodes:
            change = node_voltage(delta, e["p"]) - node_voltage(delta, e["n"])
            if change > 0.1:
                alpha = min(alpha, 0.1 / change)

        # Limit the step, not the physical exponential model.
        for _ in range(60):
            trial = [v + alpha * step for v, step in zip(x, delta)]
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


# 【打印矩阵】显示最终工作点线性化的 A 和 z，不进行计算。
def print_matrix(A, z):
    print("\nMNA matrix A:")
    for row in A:
        print("  [" + ", ".join(f"{value: .6g}" for value in row) + "]")
    print("Right-hand side z:")
    print("  [" + ", ".join(f"{value: .6g}" for value in z) + "]")


# 【主流程】取文件路径→读取→解析→建矩阵→求解→打印；出错则显示错误并退出。
# 输出负电流表示方向与“第一个节点→第二个节点”相反。
def main(netlist_path=None):
    """Run DC analysis from a netlist path or the command-line argument.

    Examples:
        python mna_dc.py circuits/simple.cir
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
        solution, A, z = result["solution"], result["A"], result["z"]
        nodes, node_index = result["nodes"], result["node_index"]
        branch_index, voltage_defined = result["branch_index"], result["voltage_defined"]

        print(f"Circuit: {title}")
        print(f"Elements: {len(elements)}")
        print(f"Non-ground nodes: {', '.join(nodes) if nodes else '(none)'}")
        if any(e["kind"] == "D" for e in elements):
            print("Diode parameters: Is=1e-15 A, Vt=0.025 V")
            print("The printed MNA equation is linearized at the final operating point.")
        print(f'Newton updates: {result["iterations"]}')
        print_matrix(A, z)

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
