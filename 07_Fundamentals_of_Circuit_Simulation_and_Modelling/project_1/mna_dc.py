"""
ECSE 472 - Project 1
Linear DC analysis using Modified Nodal Analysis (MNA).

Usage:
    python mna_dc.py circuits/simple.cir

This implementation uses only the Python standard library. It does not call SPICE.
Supported elements: R, independent V/I sources, C, L, VCVS, CCVS, VCCS, CCCS.
Diodes and nonlinear devices are intentionally not implemented.
"""

# sys 用于读取命令行参数、输出错误信息和设置退出状态。
import sys


# 【01 数值转换】把网表中的文字换成数字：1k→1000，1e10 由 float 直接识别。
# 老师问 engineering suffix / numeric parsing，就定位这里。
def parse_value(text):
    """Parse a number with common SPICE engineering suffixes."""
    # 将 "1k"、"2m" 等字符串转换为实际数值；M/m 表示毫，兆使用 meg。
    text = text.strip()
    suffixes = {
        "t": 1e12, "g": 1e9, "meg": 1e6, "k": 1e3,
        "m": 1e-3, "u": 1e-6, "n": 1e-9, "p": 1e-12,
        "f": 1e-15,
    }
    lower = text.lower()

    # SPICE commonly treats 'M' as milli and 'MEG' as mega.
    # 匹配后缀后，去掉末尾后缀，将数字部分乘以对应倍率。
    for suffix in ("meg", "t", "g", "k", "m", "u", "n", "p", "f"):
        if lower.endswith(suffix):
            number = text[:-len(suffix)]
            try:
                return float(number) * suffixes[suffix]
            except ValueError:
                break
    # 无匹配后缀时直接转换；非法输入会抛出 ValueError，由 main 处理。
    return float(text)


# 【02 读取网表】文件只读取一次；去掉空行/注释，拆开元件行并检查 .dc/.end。
def read_netlist(filename):
    """Read a netlist; the first non-empty line is the circuit title."""
    # with 确保文件自动关闭；readlines 按行读入，此时每行仍是字符串。
    with open(filename, "r", encoding="utf-8") as file:
        raw_lines = file.readlines()

    # 去除两端空白，过滤空行及整行注释，保留有效行。
    lines = []
    for raw in raw_lines:
        line = raw.strip()
        if not line or line.startswith("*") or line.startswith("#"):
            continue
        lines.append(line)

    if not lines:
        raise ValueError("The netlist is empty.")

    # 清理后的首行作为标题；两个标志记录是否遇到 .dc 和 .end。
    title = lines[0]
    elements = []
    dc_enabled = False
    ended = False

    # 跳过标题；.end 用 break 结束循环，.dc 用 continue 跳到下一行。
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

        # 按空白拆成参数列表，如 ["R1", "n1", "n2", "100"]，尚未转成数值。
        parts = line.split()
        elements.append(parts)

    # 读取结束后检查必需命令和元件；这里只检查遇到过 .end。
    if not ended:
        raise ValueError('The netlist must end with ".end".')
    if not dc_enabled:
        raise ValueError('Linear DC analysis requested, but ".dc" is missing.')
    if not elements:
        raise ValueError("No circuit elements were found.")

    return title, elements


# 【03 判断类型】看元件名称前缀；完整受控源前缀优先于单字母。
def element_kind(name):
    """Recognize controlled-source prefixes before single-letter prefixes."""
    # 先识别完整受控源前缀，避免 VCVS 被当成 V、CCCS 被当成 C。
    upper = name.upper()
    for prefix in ("VCVS", "CCVS", "VCCS", "CCCS"):
        if upper.startswith(prefix):
            return prefix
    if not upper:
        raise ValueError("An element has an empty name.")
    # 未匹配受控源时，再用首字母识别 R/V/I/C/L。
    kind = upper[0]
    if kind in ("R", "V", "I", "C", "L"):
        return kind
    raise ValueError(f"Unsupported element type: {name}")


# 【04 整理与验证】把参数列表变成元件字典；检查重名、格式、数值和控制支路。
# 老师问 how many passes：读文件和整理元件是两个阶段；内存中的列表还会被多次遍历。
def parse_elements(raw_elements):
    """Convert tokens to dictionaries with validated fields."""
    elements = []
    # 集合记录小写名称，防止重名；R1 与 r1 视为同名。
    names = set()

    for parts in raw_elements:
        name = parts[0]
        if name.lower() in names:
            raise ValueError(f"Duplicate element name: {name}")
        names.add(name.lower())
        kind = element_kind(name)

        # R/C/L 格式：名称 p节点 n节点 数值；电阻后续使用电导 1/R。
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

        # 独立源允许省略 DC；V 定义 Vp-Vn，I 的正方向为 p→n。
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

        # 电压控制源：p/n 为输出端，cp/cn 为控制端，控制电压为 Vcp-Vcn。
        elif kind in ("VCVS", "VCCS"):
            if len(parts) != 6:
                raise ValueError(
                    f"{name}: expected NAME node+ node- control+ control- gain"
                )
            elements.append({
                "name": name, "kind": kind, "p": parts[1], "n": parts[2],
                "cp": parts[3], "cn": parts[4], "gain": parse_value(parts[5]),
            })

        # 电流控制源通过元件名称引用控制支路；此处只保存名称与增益。
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
    # 全部解析后再查引用，允许控制元件写在后面；找不到时 get 返回 None。
    by_name = {e["name"].lower(): e for e in elements}
    for e in elements:
        if e["kind"] in ("CCVS", "CCCS"):
            control = by_name.get(e["control"].lower())
            if control is None:
                raise ValueError(
                    f'{e["name"]}: controlling element "{e["control"]}" was not found'
                )
            # 当前实现只支持引用已有电流未知量的支路；可串联 0V 源测量支路电流。
            if control["kind"] not in ("V", "VCVS", "CCVS", "L"):
                raise ValueError(
                    f'{e["name"]}: current must be sensed through a voltage-defined branch '
                    "(V, VCVS, CCVS, or L)"
                )

    return elements


# 【05 建立方程】把所有元件的贡献累加成 A*x=z。
# 定位地图：A 左上 G，右上 B，左下 C，右下 D；这里没有单独创建这些分块。
# x 前 N 项是节点电压，后 M 项是支路电流；z 是右侧已知源向量。
# 注意：分块 B 与 Ax=b 中的小写 b 不同；分块 C 与电容元件 C 也不同。
def build_mna(elements):
    """Build A and z for A*x=z, using Python lists (no external libraries)."""
    # 【05a 找节点】找到要计算电压的节点；地电压已知，所以去掉地对应的未知量。
    # 收集非接地节点，包括控制端；节点 0 电压已知，不进入未知向量。
    nodes = []
    for e in elements:
        for key in ("p", "n", "cp", "cn"):
            node = e.get(key)
            if node is not None and node != "0" and node not in nodes:
                nodes.append(node)

    # 【05b 节点编号】节点名称→矩阵位置；顺序按网表中首次出现排列。
    # 索引从 0 开始；未知向量 x 先放节点电压，再放电压定义支路的电流。
    node_index = {node: i for i, node in enumerate(nodes)}
    # 【05c 额外电流】电压源/电感的电流不能直接由端电压确定，增加电流未知量。
    # V/VCVS/CCVS/L 需增加电流未知量，并各增加一条电压约束方程。
    voltage_defined = [
        e for e in elements if e["kind"] in ("V", "VCVS", "CCVS", "L")
    ]
    # 【05d 支路编号】把额外电流排在节点电压后面，供 stamp 找到对应行列。
    # 支路索引接在节点索引后；对应列是电流未知量，对应行是电压约束。
    branch_index = {
        e["name"].lower(): len(nodes) + i
        for i, e in enumerate(voltage_defined)
    }

    # 【05e 矩阵大小】已有节点间新增一个独立电压源，会多一行、一列。
    # N 个节点 + M 个支路电流，共 N+M 个未知量，建立同阶方阵。
    size = len(nodes) + len(voltage_defined)
    if size == 0:
        raise ValueError("The circuit has no unknowns.")

    # 先建立全零 A 和 z，再由各个元件逐项填入；此时没有开始求解。
    A = [[0.0 for _ in range(size)] for _ in range(size)]
    z = [0.0 for _ in range(size)]

    # 【05f 查编号】接地没有自己的方程行或电压列。
    # 接地返回 None；整数索引 0 仍是有效位置，与节点名称 "0" 不同。
    def node_idx(node):
        return None if node == "0" else node_index[node]

    # 【05g 填矩阵】+= 是累加多个元件的贡献，不是覆盖已有系数。
    # 跳过接地行/列；使用 +=，因为多个元件可向同一位置贡献系数。
    def add(row, col, value):
        if row is not None and col is not None:
            A[row][col] += value

    # 【05h 电阻 / G 块】将欧姆定律写进节点方程：对角加，交叉减。
    # 电阻 I=g(Vp-Vn)：两个对角位置 +g，两个交叉位置 -g。
    def stamp_conductance(p, n, conductance):
        ip, inn = node_idx(p), node_idx(n)
        add(ip, ip, conductance)
        add(inn, inn, conductance)
        add(ip, inn, -conductance)
        add(inn, ip, -conductance)

    # 【05i 电压支路】老师问 B matrix / add V / voltage stamp，优先看这里。
    # 支路电流正方向 p→n；先将 +Ib/-Ib 加入两端 KCL，再加入 Vp-Vn=voltage。
    def stamp_branch(p, n, branch, voltage=0.0):
        ip, inn = node_idx(p), node_idx(n)
        # 【B 块，右上】把支路电流接入节点方程：p 流出 +Ib，n 流出 -Ib。
        # 这里的 +1/-1 是系数，不是 1A；接地端由 add 自动跳过。
        add(ip, branch, 1.0)
        add(inn, branch, -1.0)
        # 【C 块，左下】新增电压约束行，左侧写成 Vp-Vn。
        add(branch, ip, 1.0)
        add(branch, inn, -1.0)
        # 【右侧 z / 小写 b】把已知电压放在右边，得到 Vp-Vn=voltage。
        z[branch] += voltage

    # 逐个累加 stamp；节点行采用流出电流在左侧、已知注入电流在右侧的约定。
    for e in elements:
        kind = e["kind"]
        p, n = e["p"], e["n"]

        # 【R】电阻值换成电导，调用上面的固定四项模板。
        if kind == "R":
            stamp_conductance(p, n, 1.0 / e["value"])

        # 【I / 右侧向量】独立电流源不增加未知量，不修改 A。
        # 已知电流只修改右侧 z：流出 p 为负注入，流入 n 为正注入。
        elif kind == "I":
            # Positive source current flows from p to n.
            ip, inn = node_idx(p), node_idx(n)
            if ip is not None:
                z[ip] -= e["value"]
            if inn is not None:
                z[inn] += e["value"]

        # 【V】查支路编号后调用 stamp_branch；电压值会传入 z。
        # 电压源电流由整体电路决定；加入支路电流及已知电压约束。
        elif kind == "V":
            branch = branch_index[e["name"].lower()]
            stamp_branch(p, n, branch, e["value"])

        # 【C 电容】直流稳态当作开路，pass 表示不填任何矩阵项。
        # DC 稳态 dV/dt=0，因此 Ic=0；开路不代表电容两端电压为零。
        elif kind == "C":
            # An ideal capacitor is an open circuit in DC steady state.
            pass

        # 【L 电感】直流稳态当作短路，即一个 0V 电压支路；仍需求电流。
        # DC 稳态 dI/dt=0，因此 Vl=0；用 0V 源等效短路并保留电流未知量。
        elif kind == "L":
            # An ideal inductor is a short circuit in DC steady state.
            branch = branch_index[e["name"].lower()]
            stamp_branch(p, n, branch, 0.0)

        # 【VCVS / C 块】输出是电压，由控制端电压差决定；在约束行补控制电压系数。
        # Vp-Vn=μ(Vcp-Vcn)，移项后控制节点系数为 -μ、+μ。
        elif kind == "VCVS":
            branch = branch_index[e["name"].lower()]
            stamp_branch(p, n, branch, 0.0)
            row = branch
            add(row, node_idx(e["cp"]), -e["gain"])
            add(row, node_idx(e["cn"]), e["gain"])

        # 【VCCS / G 块】输出是电流，直接用控制电压写进两个节点方程。
        # 输出电流 g(Vcp-Vcn) 直接加入两端 KCL；增益单位为 A/V。
        elif kind == "VCCS":
            cp, cn = node_idx(e["cp"]), node_idx(e["cn"])
            ip, inn = node_idx(p), node_idx(n)
            g = e["gain"]
            add(ip, cp, g)
            add(ip, cn, -g)
            add(inn, cp, -g)
            add(inn, cn, g)

        # 【CCVS / D 块】输出是电压，由已有支路电流控制；右下块加入 -gain。
        # Vp-Vn=rm·Icontrol，在约束行的控制电流列加入 -rm（单位 Ω）。
        elif kind == "CCVS":
            branch = branch_index[e["name"].lower()]
            stamp_branch(p, n, branch, 0.0)
            control_branch = branch_index[e["control"].lower()]
            add(branch, control_branch, -e["gain"])

        # 【CCCS / B 块】输出是电流，由已有支路电流控制；右上块补 +gain/-gain。
        # 输出电流 β·Icontrol，在 p/n 的 KCL 中分别加入 +β/-β。
        elif kind == "CCCS":
            control_branch = branch_index[e["control"].lower()]
            ip, inn = node_idx(p), node_idx(n)
            add(ip, control_branch, e["gain"])
            add(inn, control_branch, -e["gain"])

    return A, z, nodes, node_index, branch_index, voltage_defined


# 【06 解方程】用行交换、除法和相减做消元；矩阵大小不变，左侧变成单位矩阵。
# 老师问 pivot / normalize / elimination，就看本函数中的对应标签。
def solve_linear_system(A, b):
    """Solve A*x=b with Gaussian elimination and partial pivoting."""
    # 【06a 准备】把 A 和右侧 b 拼起来，计算时只改副本 M。
    # b 就是前面的 z；复制各行并拼接右侧，形成增广矩阵 [A|b]，保留原始 A。
    n = len(b)
    M = [A[i][:] + [b[i]] for i in range(n)]

    # 此实现对主元上下都消元，具体为带部分主元选择的 Gauss–Jordan 消元。
    for col in range(n):
        # 【06b 选主元 / partial pivoting】选本列绝对值最大的候选数。
        # 从当前行及下方选择本列绝对值最大的主元，减轻小主元导致的误差。
        pivot = max(range(col, n), key=lambda row: abs(M[row][col]))
        # 【06c 检查能否继续】主元太接近零就报错；阈值是固定的，不是按矩阵尺度调整。
        # 固定阈值判断奇异/近奇异；浮空节点或理想源约束冲突可能触发错误。
        if abs(M[pivot][col]) < 1e-14:
            raise ValueError(
                "The MNA matrix is singular. Check for floating nodes, "
                "conflicting ideal sources, or an underdetermined circuit."
            )
        # 【06d 换行 / row swap】交换整个方程，包含右侧，不改变方程组的解。
        # 将主元所在行交换到当前行。
        M[col], M[pivot] = M[pivot], M[col]

        # 【06e 主元变 1 / normalize】不是把矩阵变小，而是整行除以同一个数。
        # 整行除以主元，使当前主元变成 1，右侧也必须同步变化。
        pivot_value = M[col][col]
        for j in range(col, n + 1):
            M[col][j] /= pivot_value

        # 【06f 其他位置变 0 / elimination】逐列消掉其余行的当前列元素。
        # 用其他行减去 factor 倍主元行，将本列其余元素消成 0。
        for row in range(n):
            if row == col:
                continue
            factor = M[row][col]
            if factor == 0:
                continue
            for j in range(col, n + 1):
                M[row][j] -= factor * M[col][j]

    # 【06g 取答案】单位矩阵乘 x 就是 x，所以最后一列直接给出各未知量。
    # 左侧化为单位矩阵后，最后一列就是解向量，顺序与未知量索引一致。
    return [M[i][n] for i in range(n)]


# 【07 显示方程】打印原始 A 和 z，方便与手算 stamp 对照；这里不做求解。
def print_matrix(A, z):
    print("\nMNA matrix A:")
    for row in A:
        print("  [" + ", ".join(f"{value: .6g}" for value in row) + "]")
    print("Right-hand side z:")
    print("  [" + ", ".join(f"{value: .6g}" for value in z) + "]")


# 【08 总入口】串起读取、解析、建矩阵、求解和打印；看程序整体流程就看这里。
def main(netlist_path=None):
    """Run DC analysis from a netlist path or the command-line argument.

    Examples:
        python mna_dc.py circuits/simple.cir
        main("/content/simple_voltage_divider.cir")  # Google Colab
    """
    # 可直接传入路径，也可从命令行 sys.argv[1] 读取路径。
    if netlist_path is None:
        if len(sys.argv) != 2:
            print("Usage: python mna_dc.py circuit.cir")
            sys.exit(2)
        netlist_path = sys.argv[1]

    try:
        # 主流程：读网表 → 解析验证 → 构建 MNA → 求解 → 输出。
        title, raw_elements = read_netlist(netlist_path)
        elements = parse_elements(raw_elements)
        A, z, nodes, node_index, branch_index, voltage_defined = build_mna(elements)
        solution = solve_linear_system(A, z)

        print(f"Circuit: {title}")
        print(f"Elements: {len(elements)}")
        print(f"Non-ground nodes: {', '.join(nodes) if nodes else '(none)'}")
        print_matrix(A, z)

        print("\nDC operating-point solution:")
        # 节点索引取电压，支路索引取电流；负电流表示与 p→n 定义方向相反。
        for node in nodes:
            print(f"  V({node}) = {solution[node_index[node]]:.9g} V")
        # 【08a 输出电流】只打印有额外电流未知量的支路；负号表示实际方向反向。
        for element in voltage_defined:
            idx = branch_index[element["name"].lower()]
            print(
                f"  I({element['name']}) = {solution[idx]:.9g} A "
                "(positive from first node to second node)"
            )

        # 【08b 补算 CCCS 输出电流】它没有自己的未知量，用 gain×控制电流得到。
        # CCCS elements do not introduce their own MNA branch unknown.
        # Compute their output current from the controlling branch current.
        for element in elements:
            if element["kind"] == "CCCS":
                control_idx = branch_index[element["control"].lower()]
                current = element["gain"] * solution[control_idx]
                print(
                    f"  I({element['name']}) = {current:.9g} A "
                    "(positive from first node to second node)"
                )

    # 【08c 报错退出】把读取、参数或求解失败的信息显示给用户。
    # 捕获文件、输入和求解错误，输出到 stderr，并以非零状态结束。
    except (OSError, ValueError, KeyError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


# 【09 启动】直接运行文件时进入 main；在 Colab import 时不自动运行。
if __name__ == "__main__":
    main()
