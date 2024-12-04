import os
from neuron import h
import neuron
import efel
import json

# load the model
h.load_file('stdrun.hoc')
model_name = "Bezaire 2016"
h.nrn_load_dll('/home/szabobogi/BC_modells/CA1_Bezaire_2016_(Lee)/x86_64/libnrnmech.so')
h.load_file('/home/szabobogi/BC_modells/CA1_Bezaire_2016_(Lee)/class_pvbasketcell.hoc')
save_dir = '../Bezaire/'
cell = h.pvbasketcell()

print(efel.__version__)
efel.reset()
h.celsius = 34
#h.celsius = 6.3



efel.set_double_setting('Threshold', -10)

traces = []
stimuli = [0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
spike_counts = []

for stim_amp in stimuli:
    h.finitialize(-65)
    h.fcurrent()
    stim = h.IClamp(0.5, sec=cell.soma[0])
    stim.amp = stim_amp
    stim.delay = 200
    stim.dur = 800
    h.tstop = 1200
    rec_t = h.Vector().record(h._ref_t)
    rec_v = h.Vector().record(cell.soma[0](0.5)._ref_v)
    h.run()

    trace = {}
    trace["T"] = rec_t
    trace["V"] = rec_v
    trace["stim_start"] = [stim.delay]
    trace["stim_end"] = [stim.delay + stim.dur]
    traces = [trace]
    traces_results = efel.get_feature_values(traces, ["Spikecount_stimint"])
    # print(traces_results[0]['Spikecount_stimint'][0])
    spike_counts.append(int(traces_results[0]['Spikecount_stimint'][0]))

    #plt.figure()
    #plt.plot(rec_t,rec_v)
    #plt.show()


# Writing to sample.json
savedir = os.path.abspath("../model_spikecounts.json")
if not os.path.exists(savedir):
    os.makedirs(savedir)

with open(savedir, "r") as f:
    spike_counts_dict = json.load(f)

print(model_name, ":", spike_counts)
spike_counts_dict[model_name] = spike_counts

# Serializing json
json_object = json.dumps(spike_counts_dict)

with open(savedir, "w") as outfile:
    outfile.write(json_object)


