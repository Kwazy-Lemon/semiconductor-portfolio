import math
from pathlib import Path
import unittest

from mna_tran import read_netlist, simulate


CIRCUITS = Path(__file__).parent / "circuits"


class TransientTests(unittest.TestCase):
    def test_linear_rc(self):
        _, elements, stop, step = read_netlist(CIRCUITS / "linear_rc.cir")
        labels, samples = simulate(elements, stop, step)
        self.assertEqual(len(samples), 50)
        for k, (time, state) in enumerate(samples, 1):
            self.assertAlmostEqual(time, k * step)
            expected = 1.0 - (1.0 + step / 0.001) ** (-k)
            self.assertAlmostEqual(state[labels.index("V(n2)")], expected, places=12)

    def test_rectifier_against_scalar_bisection(self):
        _, elements, stop, step = read_netlist(CIRCUITS / "half_wave_rectifier.cir")
        labels, samples = simulate(elements, stop, step)
        self.assertEqual(len(samples), 500)
        self.assertEqual(samples[-1][0], stop)
        previous = 0.0
        for k, (time, state) in enumerate(samples, 1):
            self.assertAlmostEqual(time, k * step)
            vin = math.cos(2 * math.pi * 60 * time)
            self.assertAlmostEqual(state[labels.index("V(n1)")], vin, places=11)
            # Independent scalar BE equation for node n2; monotone in vout.
            low, high = -1.0, 1.0
            for _ in range(60):
                mid = (low + high) / 2
                diode_current = 1e-14 * math.expm1((vin - mid) / 0.025)
                imbalance = mid / 50 + 100e-6 * (mid - previous) / step - diode_current
                if imbalance > 0:
                    high = mid
                else:
                    low = mid
            previous = (low + high) / 2
            self.assertAlmostEqual(state[labels.index("V(n2)")], previous, delta=1e-9)

    def test_partial_final_step(self):
        _, elements, _, step = read_netlist(CIRCUITS / "linear_rc.cir")
        labels, samples = simulate(elements, 1.5 * step, step)
        self.assertEqual([time for time, _ in samples], [step, 1.5 * step])
        expected = 1 - 1 / ((1 + step / 0.001) * (1 + 0.5 * step / 0.001))
        self.assertAlmostEqual(samples[-1][1][labels.index("V(n2)")], expected)


if __name__ == "__main__":
    unittest.main()
