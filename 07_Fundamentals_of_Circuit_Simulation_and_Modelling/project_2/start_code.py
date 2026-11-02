"""Run the Deliverable 2 example from any working directory."""
from pathlib import Path
from mna_dc import main

if __name__ == "__main__":
    main(str(Path(__file__).resolve().parent / "circuits" / "diode.cir"))
