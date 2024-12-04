import numpy as np
from neuron import h
from neuron.units import mV, ms, um
import matplotlib
import matplotlib.pyplot as plt
import efel
import os


# load the model
h.load_file('stdrun.hoc')
model_name = "Cutsuridis & Poirazi 2014"
h.nrn_load_dll('/home/szabobogi/BC_modells/CA1_Cutsuridis_Poirazi_2015/x86_64/libnrnmech.so')
h.load_file('/home/szabobogi/BC_modells/CA1_Cutsuridis_Poirazi_2015/CA1BC_modified.hoc')
save_dir = '../CutsPoir/'
cell = h.CA1BasketCell()

stim_amp = 0.6 * mV
h.celsius = 34

# run the simulation
h.fcurrent()
stim = h.IClamp(0.5, sec=cell.soma)
stim.amp = stim_amp
stim.delay = 200 * ms
stim.dur = 800 * ms
h.tstop = 1200 * ms

time_vector = h.Vector().record(h._ref_t)
voltage_vector = h.Vector().record(cell.soma(0.5)._ref_v)
h.finitialize(-65 * mV)
#print("h.dt :", h.dt)

h.run()

trace = {}
trace["T"] = time_vector
trace["V"] = voltage_vector
trace["stim_start"] = [stim.delay]
trace["stim_end"] = [stim.delay + stim.dur]
traces = [trace]

matplotlib.rcParams['axes.spines.right'] = False
matplotlib.rcParams['axes.spines.top'] = False
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(time_vector, voltage_vector, )
ax.axis('off')
ax.set_title(f"{model_name}", fontsize=22)
ax.text(50, 50, f"{stim_amp} nA", fontsize=20)
ax.set_ylabel("mV")
ax.set_xlabel("ms")
ax.set_xlim(0, 1200)
ax.set_ylim(-90, 60)
plt.tight_layout(pad=1.5)

# add inset axes
x1, x2, y1, y2 = 860, 900, -90, 60  # subregion of the original image
zoomin_axes = ax.inset_axes(
    [0.89, 0.25, 0.11, 0.6],
    xlim=(x1, x2), ylim=(y1, y2), xticklabels=[], yticklabels=[])
zoomin_axes.tick_params(top=False, bottom=False, left=False, right=False)
zoomin_axes.plot(time_vector, voltage_vector)
ax.indicate_inset_zoom(zoomin_axes, edgecolor="black")

if not os.path.exists(save_dir):
    os.makedirs(save_dir)
save_plot_as_svg = os.path.join(save_dir, f"{stim_amp}.svg")
plt.savefig(save_plot_as_svg, dpi=600, format='svg')
plt.close()

print("done")
