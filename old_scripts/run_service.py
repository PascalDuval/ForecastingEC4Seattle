from __future__ import annotations

import subprocess
import sys

if __name__ == "__main__":
    command = [
        sys.executable,
        "-m",
        "bentoml",
        "serve",
        "seattle_energy.service:EnergyService",
        "--port",
        "3000",
        "--production",
    ]
    subprocess.run(command, check=True)
