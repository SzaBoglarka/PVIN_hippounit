import numpy
import os
from neuron import h
import neuron
import efel
import json

h.load_file('stdrun.hoc')
model_name = "Saraga 2006 34C"
h.nrn_load_dll('C:/Users/DELL 111/Documents/KOKI/CA1 Saraga 2006/nrnmech.dll')
h.load_file('C:/Users/DELL 111/Documents/KOKI/CA1 Saraga 2006/cella.hoc')
#cell = h.cNACnoljp2()

print(efel.__version__)
efel.reset()
h.celsius = 34
#h.celsius = 6.3
efel.setDoubleSetting('Threshold', 0)

traces = []
stimuli = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6]
spike_counts = []

for stim_amp in stimuli:
    h.finitialize(-65)
    h.fcurrent()
    stim = h.IClamp(0.5, sec=h.somaa)
    stim.amp = stim_amp
    stim.delay = 200
    stim.dur = 800
    h.tstop = 1200
    rec_t = h.Vector().record(h._ref_t)
    rec_v = h.Vector().record(h.somaa(0.5)._ref_v)
    h.run()

    trace = {}
    trace["T"] = rec_t
    trace["V"] = rec_v
    trace["stim_start"] = [stim.delay]
    trace["stim_end"] = [stim.delay + stim.dur]
    traces = [trace]
    traces_results = efel.getFeatureValues(traces, ["Spikecount_stimint"])
    # print(traces_results[0]['Spikecount_stimint'][0])
    spike_counts.append(int(traces_results[0]['Spikecount_stimint'][0]))

    #plt.figure()
    #plt.plot(rec_t,rec_v)
    #plt.show()


# Writing to sample.json
savedir = os.path.abspath("C:/Users/DELL 111/Documents/Boglárka nagyon komoly mappája/KOKI PV BC/Abrak keszitese/spikecounts34.json")
with open(savedir, "r") as f:
    spike_counts_dict = json.load(f)

print(model_name, ":", spike_counts)
spike_counts_dict[model_name] = spike_counts

# Serializing json
json_object = json.dumps(spike_counts_dict)

with open(savedir, "w") as outfile:
    outfile.write(json_object)


