"""ECSE 472 Project 3: linear and nonlinear Backward Euler transient analysis."""

import argparse
import csv
import math
from pathlib import Path

DIODE_IS = 1e-14
DIODE_VT = 0.025


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


def parse_seconds(token):
    token = token.lower()
    value = parse_value(token.removesuffix("s"))
    if not math.isfinite(value) or value <= 0:
        raise ValueError("Transient times must be positive and finite")
    return value


def read_netlist(path):
    lines = [line.strip() for line in Path(path).read_text(encoding="utf-8-sig").splitlines()
             if line.strip()]
    if not lines:
        raise ValueError("Empty netlist")
    title = lines[0]
    raw, timing = [], None
    for line in lines[1:]:
        line = line.partition(";")[0].strip()
        if not line or line.startswith(("*", "#")):
            continue
        parts = line.split()
        directive = parts[0].lower()
        if line.lower() == ".end":
            break
        if directive == ".tran":
            if len(parts) != 3 or timing is not None:
                raise ValueError("Expected one .tran STOP STEP directive")
            timing = tuple(parse_seconds(token) for token in parts[1:])
        elif directive.startswith("."):
            raise ValueError(f"Unsupported directive: {line}")
        else:
            raw.append(parts)
    else:
        raise ValueError("Missing .end")
    if timing is None:
        raise ValueError("Missing .tran STOP STEP")
    return title, parse_elements(raw), timing[0], timing[1]


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
            if len(parts) == 6 and parts[3].upper() == "COS":
                amplitude, frequency = map(parse_value, parts[4:6])
                if not all(map(math.isfinite, (amplitude, frequency))) or frequency < 0:
                    raise ValueError(f"{name}: invalid cosine amplitude or frequency")
                elements.append({"name": name, "kind": kind, "p": parts[1], "n": parts[2],
                                 "value": 0.0, "amplitude": amplitude, "frequency": frequency})
                continue
            if len(parts) not in (4, 5):
                raise ValueError(
                    f"{name}: expected NAME node+ node- [DC] value"
                )
            if len(parts) == 5:
                if parts[3].upper() != "DC":
                    raise ValueError(f"{name}: expected DC value or COS amplitude frequency")
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
def build_mna(elements):
    """Assemble the static linear MNA model and storage matrix."""
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
            raise ValueError("The MNA system is singular; check floating nodes or sources.")
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


def transient_step(matrix, rhs, previous, diode_nodes, node_count):
    """Solve A*x + f_diode(x) = rhs at one time point."""
    if not diode_nodes:
        return solve_linear_system(matrix, rhs)

    x = previous.copy()
    for iteration in range(201):
        # Start with the linear BE residual and its Jacobian.
        residual = [sum(a * v for a, v in zip(row, x)) - b
                    for row, b in zip(matrix, rhs)]
        jacobian = [row.copy() for row in matrix]
        for p, n in diode_nodes:
            vp = 0.0 if p is None else x[p]
            vn = 0.0 if n is None else x[n]
            current, gd = diode_iv(vp - vn)
            if p is not None:
                residual[p] += current
                jacobian[p][p] += gd
            if n is not None:
                residual[n] -= current
                jacobian[n][n] += gd
            if p is not None and n is not None:
                jacobian[p][n] -= gd
                jacobian[n][p] -= gd

        converged = all(abs(r) <= (1e-11 if i < node_count else 1e-9)
                        for i, r in enumerate(residual))
        if converged:
            if iteration == 0:
                solve_linear_system(jacobian, [0.0] * len(x))  # check uniqueness
            return x
        if iteration == 200:
            break
        delta = solve_linear_system(jacobian, [-r for r in residual])
        x = [v + dv for v, dv in zip(x, delta)]
    raise ValueError("Newton did not converge after 200 full updates")


def simulate(elements, stop, step):
    """Return unknown labels and solved (time, state) pairs; storage starts at zero."""
    model = build_mna(elements)
    nodes, indices = model["nodes"], model["node_index"]
    labels = [f"V({n})" for n in nodes] + [f'I({e["name"]})' for e in model["voltage_defined"]]
    diodes = [(indices.get(e["p"]), indices.get(e["n"])) for e in elements if e["kind"] == "D"]
    sources = [e for e in elements if "frequency" in e]
    previous = [0.0] * len(labels)
    samples = []
    count = max(1, math.ceil(stop / step))
    for k in range(1, count + 1):
        time = min(k * step, stop)
        # Snap a numerically exact endpoint to stop; avoid a spurious tiny final step.
        if math.isclose(time, stop, rel_tol=1e-14):
            time = stop
        last_time = samples[-1][0] if samples else 0.0
        h = time - last_time
        source_rhs = model["B"].copy()
        for e in sources:
            value = e["amplitude"] * math.cos(math.tau * e["frequency"] * time)
            if e["kind"] == "V":
                source_rhs[model["branch_index"][e["name"].lower()]] += value
            else:
                if e["p"] != "0":
                    source_rhs[indices[e["p"]]] -= value
                if e["n"] != "0":
                    source_rhs[indices[e["n"]]] += value

        # (G + C/h) x_k + f_diode(x_k) = B(t_k) + (C/h) x_previous
        matrix = [[g + c / h for g, c in zip(grow, crow)]
                  for grow, crow in zip(model["G"], model["C"])]
        rhs = [b + sum(c * v for c, v in zip(row, previous)) / h
               for b, row in zip(source_rhs, model["C"])]
        try:
            previous = transient_step(matrix, rhs, previous, diodes, len(nodes))
        except (ValueError, OverflowError) as error:
            raise ValueError(f"At t={time:g} s: {error}") from error
        samples.append((time, previous))
        if time == stop:
            break
    return labels, samples


def plot_voltages(title, labels, samples):
    import matplotlib.pyplot as plt

    time = [t for t, _ in samples]
    fig, ax = plt.subplots(figsize=(9, 4.5))
    for i, label in enumerate(labels):
        if label.startswith("V("):
            color = {"V(n1)": "royalblue", "V(n2)": "black"}.get(label)
            ax.plot(time, [x[i] for _, x in samples], label=label, color=color)
    ax.set(title=title.lstrip("* "), xlabel="Time (s)", ylabel="Voltage (V)",
           xlim=(0, time[-1]))
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("netlist", type=Path)
    parser.add_argument("--csv", type=Path, help="Output CSV (default: netlist name with .csv)")
    parser.add_argument("--plot", action="store_true", help="Display node voltages using Matplotlib")
    args = parser.parse_args()
    try:
        title, elements, stop, step = read_netlist(args.netlist)
        labels, samples = simulate(elements, stop, step)
        output = args.csv or args.netlist.with_suffix(".csv")
        if output.resolve() == args.netlist.resolve():
            parser.error("CSV output must differ from the input netlist")
        with output.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(["time_s", *labels])
            for time, state in samples:
                writer.writerow([time, *state])
        print(f"{title}: {len(samples)} steps, final time {stop:g} s")
        for name, value in zip(labels, samples[-1][1]):
            print(f"  {name} = {value:.9g}")
        print(f"Waveform data: {output}")
        if args.plot:
            plot_voltages(title, labels, samples)
    except (OSError, ValueError, OverflowError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
