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


def build_mna(elements):
    """Build A and z for A*x=z, using Python lists (no external libraries)."""
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

    size = len(nodes) + len(voltage_defined)
    if size == 0:
        raise ValueError("The circuit has no unknowns.")

    A = [[0.0 for _ in range(size)] for _ in range(size)]
    z = [0.0 for _ in range(size)]

    def node_idx(node):
        return None if node == "0" else node_index[node]

    def add(row, col, value):
        if row is not None and col is not None:
            A[row][col] += value

    def stamp_conductance(p, n, conductance):
        ip, inn = node_idx(p), node_idx(n)
        add(ip, ip, conductance)
        add(inn, inn, conductance)
        add(ip, inn, -conductance)
        add(inn, ip, -conductance)

    def stamp_branch(p, n, branch, voltage=0.0):
        ip, inn = node_idx(p), node_idx(n)
        add(ip, branch, 1.0)
        add(inn, branch, -1.0)
        add(branch, ip, 1.0)
        add(branch, inn, -1.0)
        z[branch] += voltage

    for e in elements:
        kind = e["kind"]
        p, n = e["p"], e["n"]

        if kind == "R":
            stamp_conductance(p, n, 1.0 / e["value"])

        elif kind == "I":
            # Positive source current flows from p to n.
            ip, inn = node_idx(p), node_idx(n)
            if ip is not None:
                z[ip] -= e["value"]
            if inn is not None:
                z[inn] += e["value"]

        elif kind == "V":
            branch = branch_index[e["name"].lower()]
            stamp_branch(p, n, branch, e["value"])

        elif kind == "C":
            # An ideal capacitor is an open circuit in DC steady state.
            pass

        elif kind == "L":
            # An ideal inductor is a short circuit in DC steady state.
            branch = branch_index[e["name"].lower()]
            stamp_branch(p, n, branch, 0.0)

        elif kind == "VCVS":
            branch = branch_index[e["name"].lower()]
            stamp_branch(p, n, branch, 0.0)
            row = branch
            add(row, node_idx(e["cp"]), -e["gain"])
            add(row, node_idx(e["cn"]), e["gain"])

        elif kind == "VCCS":
            cp, cn = node_idx(e["cp"]), node_idx(e["cn"])
            ip, inn = node_idx(p), node_idx(n)
            g = e["gain"]
            add(ip, cp, g)
            add(ip, cn, -g)
            add(inn, cp, -g)
            add(inn, cn, g)

        elif kind == "CCVS":
            branch = branch_index[e["name"].lower()]
            stamp_branch(p, n, branch, 0.0)
            control_branch = branch_index[e["control"].lower()]
            add(branch, control_branch, -e["gain"])

        elif kind == "CCCS":
            control_branch = branch_index[e["control"].lower()]
            ip, inn = node_idx(p), node_idx(n)
            add(ip, control_branch, e["gain"])
            add(inn, control_branch, -e["gain"])

    return A, z, nodes, node_index, branch_index, voltage_defined


def solve_linear_system(A, b):
    """Solve A*x=b with Gaussian elimination and partial pivoting."""
    n = len(b)
    M = [A[i][:] + [b[i]] for i in range(n)]

    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(M[row][col]))
        if abs(M[pivot][col]) < 1e-14:
            raise ValueError(
                "The MNA matrix is singular. Check for floating nodes, "
                "conflicting ideal sources, or an underdetermined circuit."
            )
        M[col], M[pivot] = M[pivot], M[col]

        pivot_value = M[col][col]
        for j in range(col, n + 1):
            M[col][j] /= pivot_value

        for row in range(n):
            if row == col:
                continue
            factor = M[row][col]
            if factor == 0:
                continue
            for j in range(col, n + 1):
                M[row][j] -= factor * M[col][j]

    return [M[i][n] for i in range(n)]


def print_matrix(A, z):
    print("\nMNA matrix A:")
    for row in A:
        print("  [" + ", ".join(f"{value: .6g}" for value in row) + "]")
    print("Right-hand side z:")
    print("  [" + ", ".join(f"{value: .6g}" for value in z) + "]")


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

    except (OSError, ValueError, KeyError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
