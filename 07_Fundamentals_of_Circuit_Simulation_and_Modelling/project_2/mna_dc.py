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


# 【课堂形式】线性电路：G*x + C*dx/dt = B(t)。
# G 是完整静态 MNA 系数矩阵；C 是储能矩阵；B 是激励向量。
# 未知量顺序：先节点电压，后 V/VCVS/CCVS/L 的支路电流。
def build_mna(elements, operating_point=None):
    """Build G*x + C*dx/dt = B(t); optionally linearize the diodes.

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

    # 【初始化】G 和 C 都是 (N+M)×(N+M)，B 的长度是 N+M。
    size = len(nodes) + len(voltage_defined)
    if size == 0:
        raise ValueError("The circuit has no unknowns.")

    G = [[0.0 for _ in range(size)] for _ in range(size)]
    C = [[0.0 for _ in range(size)] for _ in range(size)]
    B = [0.0 for _ in range(size)]

    # 【查节点编号】地返回 None，表示没有对应的未知电压位置。
    def node_idx(node):
        return None if node == "0" else node_index[node]

    # 【填入矩阵】跳过接地项，其他位置用 += 累加元件贡献。
    def add(row, col, value):
        if row is not None and col is not None:
            G[row][col] += value

    # 【电阻模板 / G 静态矩阵】对角 +g、交叉 -g；来自 I=g(Vp-Vn)。
    def stamp_conductance(p, n, conductance):
        ip, inn = node_idx(p), node_idx(n)
        add(ip, ip, conductance)
        add(inn, inn, conductance)
        add(ip, inn, -conductance)
        add(inn, ip, -conductance)

    # 【电压支路模板：电压源的静态系数全部进入 G】
    # 前两次 add：G 中的电流列，把 +Ib/-Ib 加入两端节点方程。
    # 后两次 add：G 中的电压约束行，写出 Vp-Vn；最后 B += voltage 填入已知电压。
    def stamp_branch(p, n, branch, voltage=0.0):
        ip, inn = node_idx(p), node_idx(n)
        add(ip, branch, 1.0)
        add(inn, branch, -1.0)
        add(branch, ip, 1.0)
        add(branch, inn, -1.0)
        B[branch] += voltage

    # 【逐个元件填 stamp】以下各分支按类型修改 G、C 或 B。
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
                B[ip] -= ieq
            if inn is not None:
                B[inn] += ieq

        # 【I 电流源】只改激励向量 B；电流 p→n，所以 p 减、n 加。
        elif kind == "I":
            # Positive source current flows from p to n.
            ip, inn = node_idx(p), node_idx(n)
            if ip is not None:
                B[ip] -= e["value"]
            if inn is not None:
                B[inn] += e["value"]

        # 【V 电压源】找到电流编号，把电源电压传给 stamp_branch。
        elif kind == "V":
            branch = branch_index[e["name"].lower()]
            stamp_branch(p, n, branch, e["value"])

        # 【电容】i = capacitance*d(Vp-Vn)/dt，印章只进入动态矩阵 C。
        elif kind == "C":
            ip, inn = node_idx(p), node_idx(n)
            capacitance = e["value"]
            if ip is not None:
                C[ip][ip] += capacitance
            if inn is not None:
                C[inn][inn] += capacitance
            if ip is not None and inn is not None:
                C[ip][inn] -= capacitance
                C[inn][ip] -= capacitance

        # 【L 电感】直流稳态短路，用 0V 电压支路表示，保留电流未知量。
        elif kind == "L":
            # An ideal inductor is a short circuit in DC steady state.
            branch = branch_index[e["name"].lower()]
            stamp_branch(p, n, branch, 0.0)
            # Vp - Vn - L*dI/dt = 0，所以动态系数为 -L。
            C[branch][branch] -= e["value"]

        # 【VCVS / G 中的电压约束行】Vp-Vn=gain*(Vcp-Vcn)，在电压约束行补控制电压系数。
        elif kind == "VCVS":
            branch = branch_index[e["name"].lower()]
            stamp_branch(p, n, branch, 0.0)
            row = branch
            add(row, node_idx(e["cp"]), -e["gain"])
            add(row, node_idx(e["cn"]), e["gain"])

        # 【VCCS / G 静态矩阵】输出电流=gain*(Vcp-Vcn)，直接加入两端节点方程。
        elif kind == "VCCS":
            cp, cn = node_idx(e["cp"]), node_idx(e["cn"])
            ip, inn = node_idx(p), node_idx(n)
            g = e["gain"]
            add(ip, cp, g)
            add(ip, cn, -g)
            add(inn, cp, -g)
            add(inn, cn, g)

        # 【CCVS / G 中的控制电流系数】Vp-Vn=gain*Icontrol，在约束行的控制电流列加入 -gain。
        elif kind == "CCVS":
            branch = branch_index[e["name"].lower()]
            stamp_branch(p, n, branch, 0.0)
            control_branch = branch_index[e["control"].lower()]
            add(branch, control_branch, -e["gain"])

        # 【CCCS / G 中的电流列】输出电流=gain*Icontrol，在两端节点行补 +gain/-gain。
        elif kind == "CCCS":
            control_branch = branch_index[e["control"].lower()]
            ip, inn = node_idx(p), node_idx(n)
            add(ip, control_branch, e["gain"])
            add(inn, control_branch, -e["gain"])

    return {
        "G": G, "C": C, "B": B,
        "nodes": nodes, "node_index": node_index,
        "branch_index": branch_index, "voltage_defined": voltage_defined,
    }


# 【线性求解】求 G*x=B；系数矩阵和右端向量分开保存。
def solve_linear_system(G, B):
    """Gaussian elimination with row scaling and partial pivoting."""
    G, B = [row[:] for row in G], B[:]
    size = len(B)
    for row in range(size):
        scale = max(map(abs, G[row]), default=0.0)
        if scale == 0.0 or not math.isfinite(scale):
            raise ValueError("Singular or non-finite G; check circuit topology.")
        for col in range(size):
            G[row][col] /= scale
        B[row] /= scale

    for col in range(size):
        pivot = max(range(col, size), key=lambda row: abs(G[row][col]))
        if abs(G[pivot][col]) < 1e-14:
            raise ValueError("The DC system is singular; check floating nodes or sources.")
        G[col], G[pivot] = G[pivot], G[col]
        B[col], B[pivot] = B[pivot], B[col]
        value = G[col][col]
        for k in range(size):
            G[col][k] /= value
        B[col] /= value
        for row in range(size):
            if row == col:
                continue
            factor = G[row][col]
            if factor == 0.0:
                continue
            for k in range(size):
                G[row][k] -= factor * G[col][k]
            B[row] -= factor * B[col]

    if not all(math.isfinite(value) for value in B):
        raise ValueError("The solution is non-finite.")
    return B



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

    # 课堂方程：G*x + C*dx/dt + f_diode(x) = B(t)。
    # DC 工作点令 dx/dt=0；C 仍然建立、保存和打印。
    linear = build_mna(elements)
    G_linear, B_source = linear["G"], linear["B"]
    nodes, node_index = linear["nodes"], linear["node_index"]
    size, node_count = len(B_source), len(nodes)
    diodes = [e for e in elements if e["kind"] == "D"]

    def node_voltage(x, node):
        return 0.0 if node == "0" else x[node_index[node]]

    def residual(x):
        # Use the original diode currents, independently of Ieq cancellation.
        values = [sum(a * v for a, v in zip(row, x)) - rhs
                  for row, rhs in zip(G_linear, B_source)]
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
        # 在当前电压线性化二极管，得到牛顿雅可比矩阵。
        current_model = build_mna(elements, x)
        G_newton = current_model["G"]
        values = residual(x)
        norm = residual_norm(values)
        if norm <= 1.0:
            # Zero residual is possible even in an underdetermined circuit.
            solve_linear_system(G_newton, [0.0] * size)
            return {
                **linear, "solution": x, "iterations": iteration,
                "max_kcl_error": max(map(abs, values[:node_count]), default=0.0),
                "max_constraint_error": max(map(abs, values[node_count:]), default=0.0),
            }
        if iteration == max_iterations:
            break

        # G_newton = G_linear + d(f_diode)/dx；这不是动态矩阵 C。
        delta = solve_linear_system(G_newton, [-v for v in values])
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


# 【打印课堂方程】始终显示原始 G、动态矩阵 C 和独立源激励 B。
def print_mna_model(result):
    print("\nLinear model: G*x + C*dx/dt = B(t)")
    print("With diodes: G*x + C*dx/dt + f_diode(x) = B(t)")
    print("DC operating point: dx/dt = 0")
    labels = result["nodes"] + [
        "I(" + element["name"] + ")" for element in result["voltage_defined"]
    ]
    print("Unknown order: " + ", ".join(labels))
    size = len(result["B"])
    for name, meaning in (("G", "static coefficients"), ("C", "storage coefficients")):
        print(f"\n{name} matrix ({size} x {size}, {meaning}):")
        for row in result[name]:
            print("  [" + ", ".join(f"{value: .6g}" for value in row) + "]")
    print("\nB(t) vector (independent sources evaluated at DC):")
    print("  [" + ", ".join(f"{value: .6g}" for value in result["B"]) + "]")


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
            print("Diode nonlinear terms are evaluated separately from the static G matrix.")
        print(f'Newton updates: {result["iterations"]}')
        print_mna_model(result)

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
