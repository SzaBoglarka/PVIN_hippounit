import os
from neuron import h
import neuron
import efel
import json


class SpikecountGenerator:
    def __init__(
        self, model_name, path_to_mechanisms, path_to_hoc, soma_reference, template=False, template_name=None
    ):
        """Initialize self attributes and paths"""
        self.model_name = model_name
        h.nrn_load_dll(path_to_mechanisms)
        h.load_file(path_to_hoc)
        if template:
            exec("cell = h." + template_name + "()")
            exec("print(type(cell))")
            #exec("self.soma = cell." + soma_reference)
            self.soma = "cell." + soma_reference
            print(self.soma)
        else:
            self.soma = "h." + soma_reference

    def set_efel_settings(self, temperature=None, threshold=None, der_threshold=None, down_der_threshold=None, h_dt=None):
        """Here the default settings of efel can be changed"""
        #print(efel.__version__)
        efel.reset()
        if temperature is not None:
            h.celsius = temperature
        if threshold is not None:
            efel.set_double_setting('Threshold', threshold)
        if der_threshold is not None:
            efel.set_derivative_threshold(der_threshold)
        if down_der_threshold is not None:
            efel.set_double_setting('DownDerivativeThreshold', down_der_threshold)
        if h_dt is not None:
            h.dt = h_dt
        # h.celsius = 34
        # efel.setDoubleSetting('Threshold', 0)

    def runstim_and_countspikes(self, stim_delay, stim_dur, h_tstop, stimuli, h_voltagebase=-65):
        """Run the simulation of the model and extract the spikecounts"""
        traces = []
        spike_counts = []
        for stim in stimuli:
            h.finitialize(h_voltagebase)
            h.fcurrent()
            stim = h.IClamp(0.5, sec=cell.soma)
            #exec("stim = h.IClamp(0.5, sec=Bwb[0].soma)")
            stim.amp = stim
            stim.delay = stim_delay
            stim.dur = stim_dur
            h.tstop = h_tstop
            rec_t = h.Vector().record(h._ref_t)
            exec('rec_v = h.Vector().record(' + self.soma + '(0.5)._ref_v)')
            h.run()
            trace = {}
            trace["T"] = rec_t
            trace["V"] = rec_v
            trace["stim_start"] = [stim.delay]
            trace["stim_end"] = [stim.delay + stim.dur]
            traces = [trace]
            traces_results = efel.getFeatureValues(traces, ["Spikecount_stimint"])
            #print(traces_results[0]['Spikecount_stimint'][0])
            spike_counts.append(int(traces_results[0]['Spikecount_stimint'][0]))
        return spike_counts

    def save_spikecount_results(self, path_to_results_file):
        """Saves the extracted spikecount results to the given json file"""
        savedir = os.path.abspath(path_to_results_file)
        with open(savedir, "r") as f:                   # loading the results file
            spike_counts_dict = json.load(f)
        print(model_name, ":", spike_counts)
        spike_counts_dict[model_name] = spike_counts
        json_object = json.dumps(spike_counts_dict)     # serializing json
        with open(savedir, "w") as outfile:             # writing the new results
            outfile.write(json_object)


# load the model
h.load_file('stdrun.hoc')
model_name = "Stacey (vd) 2009"
path_to_mechanisms = 'C:/Users/DELL 111/Documents/KOKI/CA1 Stacey 2009/nrnmech.dll'
path_to_hoc = 'C:/Users/DELL 111/Documents/KOKI/CA1 Stacey 2009/Bwb_vd.hoc'
soma_reference = 'soma'
use_template = True
template_name = 'Bwb'

test_model = SpikecountGenerator(model_name, path_to_mechanisms, path_to_hoc, soma_reference, use_template, template_name)
test_model.set_efel_settings(temperature=34, threshold=0)
stimuli = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6]
test_model.runstim_and_countspikes(stim_delay=200, stim_dur=800, h_tstop=1200, stimuli=stimuli)



