"""
ECSE 472 - Project 1
Linear DC analysis using Modified Nodal Analysis (MNA).

Usage:
    python mna_dc.py circuits/simple.cir

This implementation uses only the Python standard library. It does not call SPICE.
Supported elements: R, independent V/I sources, C, L, VCVS, CCVS, VCCS, CCCS.
Diodes and nonlinear devices are intentionally not implemented.
"""

import sys


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
        if not line or line.startswith("*") or line.startswith("#"):
            continue
        lines.append(line)

    if not lines:
        raise ValueError("The netlist is empty.")

    title = lines[0]
    elements = []
    dc_enabled = False
    ended = False

    for line in lines[1:]:
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
    if kind in ("R", "V", "I", "C", "L"):
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

        if kind in ("R", "C", "L"):
            if len(parts) != 4:
                raise ValueError(f"{name}: expected NAME node+ node- value")
            value = parse_value(parts[3])
            if kind == "R" and value == 0:
                raise ValueError(f"{name}: resistance cannot be zero")
            if kind in ("R", "C") and value < 0:
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
def build_mna(elements):
    """Build A and z for A*x=z, using Python lists (no external libraries)."""
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
    return [M[i][n] for i in range(n)]


# 【打印矩阵】显示原始方程的 A 和 z，不进行计算。
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
        A, z, nodes, node_index, branch_index, voltage_defined = build_mna(elements)
        solution = solve_linear_system(A, z)

        print(f"Circuit: {title}")
        print(f"Elements: {len(elements)}")
        print(f"Non-ground nodes: {', '.join(nodes) if nodes else '(none)'}")
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

    except (OSError, ValueError, KeyError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


# 【启动】直接运行文件时调用 main；import 时不自动运行。
if __name__ == "__main__":
    main()
