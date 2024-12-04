import matplotlib
import matplotlib.pyplot as plt
import matplotlib.text
import matplotlib.cm
import numpy
import json
import os


# parameters of the plots
white = True

# Read the models spikecount data
path_to_file = os.path.abspath("./model_spikecounts.json")
with open(path_to_file, "r") as f:
    spike_counts_dict = json.load(f)
f.close()
# sort dict keys in alphabetical order
spike_counts_dict = dict(sorted(spike_counts_dict.items()))

# The stimuli that resulted in the spikecounts
#stimuli = [0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
stimuli = [0, 20, 40, 60, 80, 100, 150, 200, 250, 300, 350, 400, 500, 600, 700, 800, 900]


# The duration of the stimulation of the models in ms
stim_dur = 800

# The directory where the f-i plot should be saved
save_dir = os.path.abspath("./Models_fi_plots/")
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

plt.clf()

if white:
    edge_color = "black"
    edge_width = 0.5
    line_width = 2
    point_marker_size = 8
    stylized_marker_size = 9
    detailed_marker_size = 13
else:
    plt.style.use('dark_background')
    edge_color = None
    edge_width = None
    line_width = 1.5
    point_marker_size = 7
    stylized_marker_size = 7
    detailed_marker_size = 11

plt.tick_params(axis='both', which='major', labelsize=16)

fig, axs = plt.subplots(1, 3)

matplotlib.rcParams['axes.spines.right'] = False
matplotlib.rcParams['axes.spines.top'] = False
matplotlib.rcParams['axes.spines.left'] = False
matplotlib.rcParams['axes.spines.bottom'] = False

path_color_file = "/home/szabobogi/hippounit_standard_features/visualization/config/modelcolors_vibrant_final.json"
with open(path_color_file, "r") as f:
    model_colors_dict = json.load(f)
f.close()

# the morphology types of the models
point_models = sorted(["Neymotin 2011", "Neymotin 2013", "Sherif 2020", "Stacey(rb) 2009", "Stacey(vd) 2009", "Vladimirov 2013", "Hu(vd) 2018", "Hu(rb) 2018", "Hummos 2014"])
stylized_models = sorted(["Cutsuridis & Poirazi 2014", "Lee 2014", "Turi 2019", "Saudargiene 2015", "Bezaire 2016"])
detailed_models = sorted(["Saraga 2006", "Tzilivaki.1 2019", "Tzilivaki.2 2019", "Ferrante & Ascoli 2015", "Migliore 2018", "Tzilivaki.3 2019", "Tzilivaki.4 2019", "Tzilivaki.5 2019", "Chiovini 2014"])

for model in spike_counts_dict:

    if model == 'Cutsuridis & Poirazi 2014':
        model_color_name = 'Cuts&Poir 2015'
    elif model == "Ferrante & Ascoli 2015":
        model_color_name = "Ferr&Asco 2015"
    elif model == "Saraga 2006":
        model_color_name = "Saraga 2006 6.3C"
    else:
        model_color_name = model

    stimuli = [0, 20, 40, 60, 80, 100, 150, 200, 250, 300, 350, 400, 500, 600, 700, 800, 900]
    freq = [x//(stim_dur/1000) for x in spike_counts_dict[model]]
    freq_new = []
    stimuli_new = []

    for i in range(len(freq)):
        if freq[i] != 0:
            freq_new.append(freq[i])
            stimuli_new.append(stimuli[i])
        if freq[i] >= 150:
            break

    if stimuli_new[0] != 0:
        stimuli_new = [x-stimuli_new[0] for x in stimuli_new]

    if model in point_models:
        axs[0].plot(stimuli_new, freq_new, linestyle='-', linewidth=line_width, marker='o', markersize=point_marker_size, color = model_colors_dict[model_color_name], markeredgecolor=edge_color, markeredgewidth=edge_width, label=model, alpha=0.7)
    elif model in stylized_models:
        axs[1].plot(stimuli_new, freq_new, linestyle='-', linewidth=line_width, marker='^', markersize=stylized_marker_size, color = model_colors_dict[model_color_name], markeredgecolor=edge_color, markeredgewidth=edge_width, label=model, alpha=0.7)
    elif model in detailed_models:
        axs[2].plot(stimuli_new, freq_new, linestyle='-', linewidth=line_width, marker='*', markersize=detailed_marker_size, color = model_colors_dict[model_color_name], markeredgecolor=edge_color, markeredgewidth=edge_width, label=model, alpha=0.7)
    else:
        #dataframe.loc[model, "morphology"] = None
        print("No information about the morphology type of the model", model)
    #ax1.plot(stimuli, [x//(stim_dur/1000) for x in spike_counts_dict[model]], linestyle='-', marker=marker_type, markersize=marker_size, label=model)

# lgd = fig.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left', fontsize=12, markerscale=1)

for ax in axs.flat:
    ax.set_xlabel('Current from rheobase (pA)',loc="center", fontsize=16)
    ax.set_ylabel('Frequency (Hz)',loc="center", fontsize=16)
    # ax.set_xlim(0,600)
    ax.set_ylim(0,500)
    ax.set_ylim(0, 850)
    #ax.grid()

# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()

axs[0].set_title("Point models", fontsize=18, pad=10)
axs[1].set_title("Stylized models", fontsize=18, pad=10)
axs[2].set_title("Detailed models", fontsize=18, pad=10)

#fig.set_size_inches(14, 4.5)
fig.set_size_inches(20, 6)

if white:
    plt.savefig(os.path.join(save_dir, "F-i plots of the investigated models per morphologies white"))
else:
    plt.savefig(os.path.join(save_dir, "F-i plots of the investigated models per morphologies"))

# for a zoomed in version
for ax in axs.flat:
    ax.set_ylim(0,250)
    ax.set_xlim(0,850)
    ax.tick_params(axis='both', which='major', labelsize=14, length=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
if white:
    plt.savefig(os.path.join(save_dir, "F-i plots of the investigated models zoom per morphologies white"))
else:
    plt.savefig(os.path.join(save_dir, "F-i plots of the investigated models zoom per morphologies"))



save_plot_as_svg = os.path.join(save_dir, "Model_FI_plots_final_no_grid.svg")
plt.savefig(save_plot_as_svg, dpi=600, format='svg')





'''
if white:
    plt.savefig(os.path.join(save_dir, "F-i plots of the investigated models per morphologies white"), bbox_extra_artists=(lgd,), bbox_inches='tight')
else:
    plt.savefig(os.path.join(save_dir, "F-i plots of the investigated models per morphologies"), bbox_extra_artists=(lgd,), bbox_inches='tight')

# for a zoomed in version
for ax in axs.flat:
    ax.set_ylim(0,250)
if white:
    plt.savefig(os.path.join(save_dir, "F-i plots of the investigated models zoom per morphologies white"), bbox_extra_artists=(lgd,), bbox_inches='tight')
else:
    plt.savefig(os.path.join(save_dir, "F-i plots of the investigated models zoom per morphologies"), bbox_extra_artists=(lgd,), bbox_inches='tight')

'''


#plt.show()
