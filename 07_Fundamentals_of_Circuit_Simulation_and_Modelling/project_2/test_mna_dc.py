"""Analytical regression checks for all nine legacy elements and diodes."""
import contextlib
import io
import math
from pathlib import Path
import tempfile
import unittest

from mna_dc import (DIODE_IS, DIODE_VT, build_mna, diode_iv, main,
                    parse_elements, read_netlist, solve_dc)


def analyze(body, **options):
    elements = parse_elements([line.split() for line in body.splitlines() if line.strip()])
    return solve_dc(elements, **options)


def voltage(result, node):
    return 0.0 if node == "0" else result["solution"][result["node_index"][node]]


def branch(result, name):
    return result["solution"][result["branch_index"][name.lower()]]


class ProjectTwoTests(unittest.TestCase):
    def test_deliverable_one_divider(self):
        r = analyze("Vin n1 0 DC 6\nR1 n1 n2 100\nR2 n2 0 50")
        self.assertAlmostEqual(voltage(r, "n1"), 6)
        self.assertAlmostEqual(voltage(r, "n2"), 2)
        self.assertAlmostEqual(branch(r, "Vin"), -0.04)

    def test_repository_project_one_example(self):
        r = analyze("V1 n1 0 DC 8\nI1 0 n3 DC 1m\nR1 n1 n2 1k\nR2 n2 n3 2k\nR3 n2 0 2k")
        self.assertAlmostEqual(voltage(r, "n2"), 6)
        self.assertAlmostEqual(voltage(r, "n3"), 8)
        self.assertAlmostEqual(branch(r, "V1"), -0.002)

    def test_independent_current_source(self):
        r = analyze("I1 0 a 1m\nR1 a 0 1k")
        self.assertAlmostEqual(voltage(r, "a"), 1)

    def test_capacitor_is_open_in_dc(self):
        r = analyze("I1 0 a 1m\nR1 a 0 1k\nC1 a 0 10u")
        self.assertAlmostEqual(voltage(r, "a"), 1)

    def test_inductor_is_short_in_dc(self):
        r = analyze("V1 a 0 1\nR1 a b 1k\nL1 b 0 1m")
        self.assertAlmostEqual(voltage(r, "b"), 0)
        self.assertAlmostEqual(branch(r, "L1"), 0.001)

    def test_vcvs(self):
        r = analyze("V1 a 0 2\nVCVS1 b 0 a 0 3\nR1 b 0 1k")
        self.assertAlmostEqual(voltage(r, "b"), 6)
        self.assertAlmostEqual(branch(r, "VCVS1"), -0.006)

    def test_vccs(self):
        r = analyze("V1 a 0 2\nVCCS1 b 0 a 0 1m\nR1 b 0 1k")
        self.assertAlmostEqual(voltage(r, "b"), -2)

    def test_ccvs(self):
        r = analyze("V1 a 0 2\nR1 a 0 1k\nCCVS1 b 0 V1 1k\nR2 b 0 1k")
        self.assertAlmostEqual(voltage(r, "b"), -2)
        self.assertAlmostEqual(branch(r, "CCVS1"), 0.002)

    def test_cccs(self):
        r = analyze("V1 a 0 2\nR1 a 0 1k\nCCCS1 b 0 V1 3\nR2 b 0 1k")
        self.assertAlmostEqual(voltage(r, "b"), 6)

    def test_deliverable_two_against_independent_scalar_root(self):
        r = analyze("Vin n1 0 DC 1\nD1 n1 n2\nR n2 0 50")
        low, high = 0.0, 1.0
        for _ in range(100):
            mid = (low + high) / 2
            if DIODE_IS * math.expm1((1 - mid) / DIODE_VT) > mid / 50:
                low = mid
            else:
                high = mid
        v2 = voltage(r, "n2")
        self.assertAlmostEqual(v2, (low + high) / 2, places=9)
        self.assertAlmostEqual(v2, 0.2673, places=4)
        self.assertAlmostEqual(branch(r, "Vin"), -v2 / 50, places=10)
        self.assertLessEqual(r["max_kcl_error"], 1e-11)
        self.assertLessEqual(r["max_constraint_error"], 1e-9)

    def test_diode_with_controlled_source(self):
        r = analyze("V1 ctrl 0 0.5\nVCVS1 a 0 ctrl 0 2\nD1 a b\nR1 b 0 50")
        self.assertAlmostEqual(voltage(r, "b"), 0.267314409, places=8)

    def test_current_driven_diode(self):
        r = analyze("I1 0 a 1m\nD1 a 0")
        self.assertAlmostEqual(voltage(r, "a"), DIODE_VT * math.log1p(1e-3 / DIODE_IS), places=8)

    def test_two_diodes(self):
        r = analyze("V1 a 0 2\nD1 a b\nD2 b c\nR1 c 0 1k")
        self.assertAlmostEqual(voltage(r, "a") - voltage(r, "b"),
                               voltage(r, "b") - voltage(r, "c"), places=8)
        self.assertLessEqual(r["max_kcl_error"], 1e-11)

    def test_reverse_biased_diode(self):
        r = analyze("V1 a 0 -1\nD1 a b\nR1 b 0 50")
        current = diode_iv(voltage(r, "a") - voltage(r, "b"))[0]
        self.assertAlmostEqual(current, -DIODE_IS, delta=1e-17)

    def test_diode_derivative(self):
        v, h = 0.65, 1e-7
        numerical = (diode_iv(v + h)[0] - diode_iv(v - h)[0]) / (2 * h)
        self.assertAlmostEqual(numerical / diode_iv(v)[1], 1, places=7)

    def test_grounded_and_floating_diode_companion_stamps(self):
        for p, n in (("a", "b"), ("a", "0"), ("0", "a")):
            with self.subTest(p=p, n=n):
                e = parse_elements([["D1", p, n]])
                initial = build_mna(e)
                nodes, idx = initial["nodes"], initial["node_index"]
                x = [0.05 if node == "a" else -0.02 for node in nodes]
                model = build_mna(e, x)
                vd = (0 if p == "0" else x[idx[p]]) - (0 if n == "0" else x[idx[n]])
                current, _ = diode_iv(vd)
                for node in nodes:
                    residual = sum(g * v for g, v in zip(model["G"][idx[node]], x)) - model["B"][idx[node]]
                    expected = current * ((1 if node == p else 0) - (1 if node == n else 0))
                    self.assertAlmostEqual(residual, expected, delta=1e-27)

    def test_title_can_start_with_asterisk(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "example.cir"
            path.write_text("* diode circuit\nVin a 0 1\nD1 a b\nR1 b 0 50\n.dc\n.end\n", encoding="utf-8")
            title, raw = read_netlist(path)
            self.assertEqual(title, "* diode circuit")
            self.assertEqual(len(raw), 3)
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                main(path)
            self.assertIn("V(a) = 1 V", stream.getvalue())
            self.assertIn("I(D1)", stream.getvalue())
            self.assertIn("G*x + C*dx/dt = B(t)", stream.getvalue())
            self.assertIn("C matrix", stream.getvalue())
            self.assertIn("B(t) vector", stream.getvalue())
            self.assertNotIn("D matrix", stream.getvalue())

    def test_missing_directives_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.cir"
            for text in ("Title\nV1 a 0 1\n.end\n", "Title\nV1 a 0 1\n.dc\n"):
                path.write_text(text, encoding="utf-8")
                with self.assertRaises(ValueError):
                    read_netlist(path)

    def test_floating_network_even_at_zero_residual(self):
        with self.assertRaisesRegex(ValueError, "singular|Singular"):
            analyze("R1 a b 1k\nR2 c 0 1k")

    def test_conflicting_voltage_sources(self):
        with self.assertRaises(ValueError):
            analyze("V1 a 0 1\nV2 a 0 2")

    def test_iteration_limit(self):
        with self.assertRaisesRegex(ValueError, "did not converge"):
            analyze("V1 a 0 1\nD1 a b\nR1 b 0 50", max_iterations=1)

    def test_invalid_elements(self):
        cases = ["D1 a 0 model", "R1 a 0 0", "V1 a 0 nan", "I1 a 0 inf",
                 "L1 a 0 -1", "VCVS1 a 0 b 0 inf", "CCCS1 a 0 missing 2",
                 "R1 a 0 1k\nr1 a 0 1k"]
        for body in cases:
            with self.subTest(body=body), self.assertRaises(ValueError):
                parse_elements([line.split() for line in body.splitlines()])


    def test_classroom_G_C_B_for_divider(self):
        elements = parse_elements([line.split() for line in (
            "Vin n1 0 6", "R1 n1 n2 100", "R2 n2 0 50")])
        model = build_mna(elements)
        self.assertEqual(model["G"], [[0.01, -0.01, 1.0],
                                      [-0.01, 0.03, 0.0],
                                      [1.0, 0.0, 0.0]])
        self.assertEqual(model["C"], [[0.0] * 3 for _ in range(3)])
        self.assertEqual(model["B"], [0.0, 0.0, 6.0])

    def test_grounded_capacitor_dynamic_stamp(self):
        model = build_mna(parse_elements([["C1", "a", "0", "2u"],
                                          ["R1", "a", "0", "1k"]]))
        self.assertEqual(model["G"], [[0.001]])
        self.assertEqual(model["C"], [[2e-6]])
        self.assertEqual(model["B"], [0.0])

    def test_two_terminal_capacitor_dynamic_stamp(self):
        elements = parse_elements([line.split() for line in (
            "V1 a 0 1", "R1 a b 1k", "R2 b 0 1k", "C1 a b 2u")])
        model = build_mna(elements)
        self.assertEqual(model["C"], [[2e-6, -2e-6, 0.0],
                                      [-2e-6, 2e-6, 0.0],
                                      [0.0, 0.0, 0.0]])

    def test_inductor_dynamic_stamp_and_constitutive_equation(self):
        model = build_mna(parse_elements([line.split() for line in (
            "V1 a 0 1", "R1 a b 1k", "L1 b 0 2m")]))
        row = model["branch_index"]["l1"]
        b_index = model["node_index"]["b"]
        self.assertEqual(model["C"][row][row], -0.002)
        self.assertEqual(model["G"][row][b_index], 1.0)
        # V_L = L*dI/dt = 0.002*2 = 0.004 V.
        x, dx = [0.0] * 4, [0.0] * 4
        x[b_index], dx[row] = 0.004, 2.0
        residual = sum(g * v for g, v in zip(model["G"][row], x))
        residual += sum(c * dv for c, dv in zip(model["C"][row], dx))
        self.assertAlmostEqual(residual, 0.0, places=12)

    def test_RC_equation_with_nonzero_time_derivative(self):
        model = build_mna(parse_elements([line.split() for line in (
            "I1 0 a 1.001m", "R1 a 0 1k", "C1 a 0 2u")]))
        # At V=1 V and dV/dt=0.5 V/s, source current is 1.001 mA.
        residual = model["G"][0][0] * 1.0 + model["C"][0][0] * 0.5 - model["B"][0]
        self.assertAlmostEqual(residual, 0.0, places=12)

    def test_storage_stamps_are_retained_in_DC(self):
        r = analyze("Vin n1 0 1\nR1 n1 n2 1k\nC1 n2 0 1u\nR2 n2 n3 100\nL1 n3 0 1m")
        self.assertAlmostEqual(voltage(r, "n2"), 1.0 / 11)
        self.assertAlmostEqual(voltage(r, "n3"), 0.0)
        self.assertEqual(r["C"][r["node_index"]["n2"]][r["node_index"]["n2"]], 1e-6)
        self.assertEqual(r["C"][r["branch_index"]["l1"]][r["branch_index"]["l1"]], -1e-3)


if __name__ == "__main__":
    unittest.main()
