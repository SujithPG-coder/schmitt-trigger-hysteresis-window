"""Plot ngspice results for the Schmitt trigger (run the two .cir files first)."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "docs" / "images"
OUT.mkdir(parents=True, exist_ok=True)

# Transient response to a noisy sine
d = np.loadtxt(HERE / "schmitt_transient.dat")
t, vin, vout, vcmp = d[:, 0] * 1e3, d[:, 1], d[:, 3], d[:, 5]
fig, ax = plt.subplots(3, 1, figsize=(11, 8), sharex=True)
ax[0].plot(t, vin, color="#3b75af", lw=0.6)
ax[0].axhline(3, color="#d1495b", ls="--", lw=1, label="VUT = 3 V")
ax[0].axhline(1, color="#2a9d8f", ls="--", lw=1, label="VLT = 1 V")
ax[0].set_ylabel("Vin (V)"); ax[0].set_title("Noisy input (10 V, 100 Hz sine + white noise)")
ax[0].legend(loc="upper right"); ax[0].grid(alpha=0.3)
ax[1].plot(t, vcmp, color="#888888", lw=0.8)
ax[1].set_ylabel("Vout (V)")
ax[1].set_title("Plain comparator (no hysteresis) - noise causes false switching")
ax[1].grid(alpha=0.3)
ax[2].plot(t, vout, color="#d1495b", lw=1.2)
ax[2].set_ylabel("Vout (V)"); ax[2].set_xlabel("Time (ms)")
ax[2].set_title("Schmitt trigger (1 V - 3 V window) - one clean transition per crossing")
ax[2].grid(alpha=0.3)
fig.tight_layout(); fig.savefig(OUT / "sim_transient.png", dpi=120); plt.close(fig)

# Hysteresis loop
d = np.loadtxt(HERE / "hysteresis_loop.dat")
vin, vout = d[:, 1], d[:, 3]
half = len(vin) // 2
fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(vin[:half], vout[:half], color="#d1495b", lw=2, label="Vin increasing")
ax.plot(vin[half:], vout[half:], color="#3b75af", lw=2, ls="--", label="Vin decreasing")
ax.axvspan(1, 3, color="#f4a261", alpha=0.15, label="Hysteresis window (1 V - 3 V)")
ax.set_xlabel("Vin (V)"); ax.set_ylabel("Vout (V)")
ax.set_title("Transfer characteristic - inverting Schmitt trigger")
ax.legend(loc="center right"); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(OUT / "sim_hysteresis_loop.png", dpi=120); plt.close(fig)
print("Figures saved to", OUT)
