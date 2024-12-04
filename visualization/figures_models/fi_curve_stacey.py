import os
from neuron import h
import neuron
import efel
import json
from matplotlib import pyplot as plt

# load the model
h.load_file('stdrun.hoc')
model_name = "Stacey (vd) 2009"
h.nrn_load_dll('/home/szabobogi/BC_modells/CA1_Stacey_2009/x86_64/libnrnmech.so')
h.load_file('/home/szabobogi/BC_modells/CA1_Stacey_2009/Bwb_vd.hoc')
cell = h.Bwb()
save_dir = './Stacey_vd_2009/'


print(efel.__version__)
efel.reset()
h.celsius = 34
#h.celsius = 6.3
efel.set_double_setting('Threshold', -10)

traces = []
stimuli = [0.08]
spike_counts = []

for stim_amp in stimuli:
    h.finitialize(-65)
    h.fcurrent()
    stim = h.IClamp(0.5, sec=cell.soma)
    stim.amp = stim_amp
    stim.delay = 200
    stim.dur = 800
    h.tstop = 1200
    rec_t = h.Vector().record(h._ref_t)
    rec_v = h.Vector().record(cell.soma(0.5)._ref_v)
    h.run()

    '''
    trace = {}
    trace["T"] = rec_t
    trace["V"] = rec_v
    trace["stim_start"] = [stim.delay]
    trace["stim_end"] = [stim.delay + stim.dur]
    traces = [trace]
    traces_results = efel.getFeatureValues(traces, ["Spikecount_stimint"])
    # print(traces_results[0]['Spikecount_stimint'][0])
    spike_counts.append(int(traces_results[0]['Spikecount_stimint'][0]))
    '''

    plt.figure(figsize=(20, 8))
    plt.xlim()
    plt.plot(rec_t, rec_v, color='black')
    plt.axis('off')
    plt.title("Stacey(vd) 2009")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_plot_as_svg = os.path.join(save_dir, f"{stim_amp}.svg")
    plt.savefig(save_plot_as_svg, dpi=600, format='svg')
    plt.close()



'''
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
'''

