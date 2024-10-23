from pathlib import Path

import numpy as np

from matplotlib import pyplot as plt
from capacitor_real import cap_real_self

runtime = 100

fig = plt.figure(figsize=(9, 8), layout="tight")

plt.plot(cap_real_self[0]["time"], cap_real_self[0]["voltage"], label="100uF MLCC1 (RC, 1k)")
plt.plot(cap_real_self[1]["time"], cap_real_self[1]["voltage"], label="100uF MLCC2 (RC, 1k)")
plt.plot(cap_real_self[2]["time"], cap_real_self[2]["voltage"], label="100uF Tantal (RC, 1k)")

plt.suptitle(f"Self-Discharge of Capacitors")
plt.xlabel("time [s]")
plt.ylabel("voltage [V]")
plt.xticks(np.arange(0.0, runtime+0.1, 5))
plt.yticks(np.arange(0.0, 5.6, 0.5))
plt.ylim(bottom=0.0) #, top=1.0)
plt.grid(True)
plt.legend(loc="lower right")
plt.tight_layout()
# force direct values on axis
for ax in fig.get_axes():
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
plt.savefig(Path(__file__).with_suffix(".svg"))  # PNG / SVG
plt.close(fig)
