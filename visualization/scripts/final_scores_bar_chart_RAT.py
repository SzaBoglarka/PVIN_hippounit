try:
    import cPickle as pickle
except:
    import pickle
import gzip
#from hippounit import plottools
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.artist import Artist
import os
import numpy
import collections
import json
import pandas as pd


# base directory of the validation results
base_dir= '/home/szabobogi/hippounit_standard_features/validation_results_RAT/results/'
# give save directory and save the figure(s)
save_dir= '/home/szabobogi/hippounit_standard_features/visualization/figures_RAT/Final_scores_barchart/'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
figname = 'final_scores_barchart_RAT'


data_dict=collections.OrderedDict()
fc = 0      # to count the number of finalscores

# the morphology types of the models
point_models = sorted(["Neymotin_2011", "Neymotin_2013", "Sherif_2020", "Stacey(rb)_2009", "Stacey(vd)_2009", "Vladimirov_2013", "Hu(vd)_2018", "Hu(rb)_2018", "Hummos_2014"])
stylized_models = sorted(["Cuts&Poir_2015", "Lee_2014", "Turi_2019", "Saudargiene_2015", "Bezaire_2016"])
detailed_models = sorted(["Saraga_2006_6.3_cels", "Tzilivaki1_2019_0.1_dt", "Tzilivaki4_2019_0.1_dt", "Ferr&Asco_2015", "Migliore_2018", "Tzilivaki3_2019_0.1_dt", "Tzilivaki2_2019_0.1_dt", "Tzilivaki5_2019_0.1_dt", "Chiovini_2014"])

# parameters of the plots
white = True
zoomed = False

# read the finalscore values of the models
for tests in os.listdir(base_dir):
	#data_dict['Tests'].append(tests)
	if "somaticfeat" in tests:
#		data_dict[tests] = []
		data_dict = {}
		data_dict["point"] = {}
		data_dict["stylized"] = {}
		data_dict["detailed"] = {}

		models_names = os.listdir(base_dir+tests)	
		models_names.sort()
		#print(models_names)

		for model in models_names:
			if os.path.exists(base_dir + tests + '/' + model):
				#print(model)
				for files in os.listdir(base_dir+tests + '/' +model):
					if 'final_score' in files:
						with open(base_dir+tests + '/' +model +'/' + files) as f:
							final_score = json.load(f, object_pairs_hook=collections.OrderedDict)
							for key in final_score.keys():
#								data_dict.append(float(final_score[key]))
#								data_dict[model] = float(final_score[key])
								if model in point_models:
									data_dict["point"][model] = float(final_score[key])
								elif model in stylized_models:
									data_dict["stylized"][model] = float(final_score[key])
								elif model in detailed_models:
									data_dict["detailed"][model] = float(final_score[key])
								else:
									print("No information about the morphology type of the model", model)
								fc = fc+1
			else:
#				data_dict[tests].append(float('nan')) # add nans for the models where the data is missing
				data_dict[models] = float('nan')

print("finalscores db = ",fc)

# the model names we want to see on the plots
new_names_dict= {
    "Neymotin_2011" : "Neymotin 2011",
    "Neymotin_2013" : "Neymotin 2013",
    "Stacey(rb)_2009" : "Stacey(rb) 2009", 
    "Stacey(vd)_2009" : "Stacey(vd) 2009", 
    "Vladimirov_2013" : "Vladimirov 2013", 
    "Hu(rb)_2018" : "Hu(rb) 2018", 
    #"Hu(vd)_2018" : "Hu(vd) 2018",
    #"Sherif_2020" : "Sherif 2020",
    "Hummos_2014" : "Hummos 2014", 
    "Cuts&Poir_2015" : "Cuts&Poir 2015",
    "Lee_2014" : "Lee 2014",
    "Turi_2019" : "Turi 2019",
    "Saudargiene_2015" : "Saudargiene 2015",
    "Bezaire_2016" : "Bezaire 2016",
    "Ferr&Asco_2015" : "Ferr&Asco 2015", 
    "Migliore_2018" : "Migliore 2018", 
    "Saraga_2006_6.3_cels" : "Saraga 2006 6.3C", 
    "Chiovini_2014" : "Chiovini 2014",
    "Tzilivaki1_2019" : "Tzilivaki.1 2019 no set dt", 
    "Tzilivaki2_2019" : "Tzilivaki.2 2019 no set dt", 
    "Tzilivaki3_2019" : "Tzilivaki.3 2019 no set dt", 
    "Tzilivaki4_2019" : "Tzilivaki.4 2019 no set dt",
    "Tzilivaki5_2019" : "Tzilivaki.5 2019 no set dt", 
    "Tzilivaki1_2019_0.1_dt" : "Tzilivaki.1 2019",
    "Tzilivaki2_2019_0.1_dt" : "Tzilivaki.2 2019",
    "Tzilivaki3_2019_0.1_dt" : "Tzilivaki.3 2019",
    "Tzilivaki4_2019_0.1_dt" : "Tzilivaki.4 2019",
    "Tzilivaki5_2019_0.1_dt" : "Tzilivaki.5 2019"
}

# the model colors we want to see on the plots
path_color_file = '/home/szabobogi/hippounit_standard_features/visualization/config/modelcolors_vibrant_final.json'
with open(path_color_file, "r") as f:
    model_colors_dict = json.load(f)
f.close()

final_data_dict = {}        # which has all the information in a way wewant to plot

# fill up the final_dict in the appropriate order
data_dict["point"] = dict(sorted(data_dict["point"].items()))       # sort the data_dict
for key, value in data_dict["point"].items():
    if key in new_names_dict:
        name = new_names_dict[key]
        try:
            final_data_dict[name] = {}
            final_data_dict[name]["color"] = model_colors_dict[name]
            final_data_dict[name]["finalscore"] = value
            final_data_dict[name]["morph"] = "point"
        except:
            print("no color info about", name)
            final_data_dict.pop(name)
            pass
data_dict["stylized"] = dict(sorted(data_dict["stylized"].items()))
for key, value in data_dict["stylized"].items():
    if key in new_names_dict:
        name = new_names_dict[key]
        try:
            final_data_dict[name] = {}
            final_data_dict[name]["color"] = model_colors_dict[name]
            final_data_dict[name]["finalscore"] = value
            final_data_dict[name]["morph"] = "stylized"
        except:
            print("no color info about", name)
            final_data_dict.pop(name)
            pass
data_dict["detailed"] = dict(sorted(data_dict["detailed"].items()))
for key, value in data_dict["detailed"].items():
    if key in new_names_dict:
        name = new_names_dict[key]
        try:
            final_data_dict[name] = {}
            final_data_dict[name]["color"] = model_colors_dict[name]
            final_data_dict[name]["finalscore"] = value
            final_data_dict[name]["morph"] = "detailed"
        except:
            print("no color info about", name)
            final_data_dict.pop(name)
            pass

# create the vectors for the barplot
final_scores = []
colors = []
for key, value in final_data_dict.items():
    final_scores.append(final_data_dict[key]["finalscore"])
    colors.append(final_data_dict[key]["color"])

# parameters of the bar plot and the figure
index = (numpy.arange(len(final_scores)))
#bar_width = 0.25
opacity = 0.8

#plt.figure()
plt.figure(figsize=(8,7))
if white:
    color_chars = "black"
    edge_color = "black"
    bar_width = 0.35
    plt.style.use("seaborn-whitegrid")
    grid_color = 'black'
    grid_width = 0.05
else:
    plt.style.use('dark_background')
    color_chars = "white"
    edge_color = None
    bar_width = 0.33
    grid_color = 'white'
    grid_width = 0.1
matplotlib.rcParams['axes.spines.right'] = False
matplotlib.rcParams['axes.spines.top'] = False
matplotlib.rcParams['axes.spines.left'] = False
matplotlib.rcParams['axes.spines.bottom'] = False
plt.clf()
font_size = 15
plt.grid(linewidth=grid_width, zorder=1, axis='y', color=grid_color)
plt.grid(linewidth=0, zorder=1, axis='x')
plt.tick_params(axis='both', which='major', labelsize=font_size)
plt.ylabel('Final Score', fontsize=font_size)
#plt.xticks(index + bar_width, models_names, rotation=90)
plt.xticks(index, final_data_dict.keys(), rotation=90, fontsize=font_size)
plt.tick_params(top=False, bottom=False, left=False, right=False)
#lgd=plt.legend(bbox_to_anchor=(1.0, 1.0), loc = 'upper left')

# plot the data
plt.bar(index, final_scores, bar_width, alpha=opacity, color = colors, zorder = 2, edgecolor = edge_color)

# separating the different morph groups
plt.axvline(x = 6.5, color = color_chars, linestyle = '--', linewidth=1)
plt.axvline(x = 11.5, color = color_chars, linestyle = '--', linewidth=1)

plt.ylim(0, 8)

"""
# separate the diff morphs if we include saraga
point_text = plt.text(-0.5, 46.6, 'point', fontsize = 9, color = color_chars)            # the hight is 46.6 and 5.63 in case of zoom
stylized_text = plt.text(7, 46.6, 'stylized', fontsize = 9, color = color_chars)
detailed_text = plt.text(12, 46.6, 'detailed', fontsize = 9, color = color_chars)
"""

# separate the diff morphs with texts
plt.text(2.2, 7.5, 'point', fontsize = 12, color = color_chars)
plt.text(8.3, 7.5, 'stylized', fontsize = 12, color = color_chars)
plt.text(15.7, 7.5, 'detailed', fontsize = 12, color = color_chars)

'''
# mark the diff morph tzpes with the markers
plt.plot(2.75, 5.5, marker='o', markersize=12, markeredgewidth=1, markeredgecolor='black', markerfacecolor='none')
plt.plot(9, 5.5, marker='^', markersize=12, markeredgewidth=1, markeredgecolor='black', markerfacecolor='none')
plt.plot(16.5, 5.5, marker='*', markersize=15, markeredgewidth=1, markeredgecolor='black', markerfacecolor='none')
'''

# if want to mark the bars with the morph types uncomment this section
'''
i = 0
for model in final_data_dict:
    if final_data_dict[model]["morph"] == "point":
        plt.plot(i, final_data_dict[model]["finalscore"] + 0.5, marker='o', markersize=5, color=final_data_dict[model]["color"])    # add 2.5 and add 0.5 to good zoomed figure
    elif final_data_dict[model]["morph"] == "stylized":
        plt.plot(i, final_data_dict[model]["finalscore"] + 0.5, marker='^', markersize=5, color=final_data_dict[model]["color"])
    elif final_data_dict[model]["morph"] == "detailed":
        plt.plot(i, final_data_dict[model]["finalscore"] + 0.5, marker='*', markersize=7, color=final_data_dict[model]["color"])
    i = i+1
'''


if white:
    figname = figname
else:
    figname = 'figname' + '_black'
save_plot_as_svg = os.path.join(save_dir, f"{figname}.svg")
#plt.savefig(save_dir + 'final_scores_barchart_standard', bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.savefig(save_plot_as_svg, bbox_inches='tight', dpi=600, format='svg')

"""
if zoomed:
    Artist.remove(point_text)
    Artist.remove(stylized_text)
    Artist.remove(detailed_text)

    plt.text(-0.5,5.63, 'point', fontsize = 9, color = color_chars)            # the hight is 46.6 and 5.63 in case of zoom
    plt.text(7, 5.63, 'stylized', fontsize = 9, color = color_chars)
    plt.text(12, 5.63, 'detailed', fontsize = 9, color = color_chars)

    plt.ylim(0, 6)  # set the zoom
    #plt.savefig(save_dir + 'final_scores_barchart_standard_ZOOM', bbox_extra_artists=(lgd,), bbox_inches='tight')
    if white:
        #figname = 'final_scores_barchart_standard_diff_morph_ZOOM_white'
        figname = 'final_scores_barchart_standard_diff_morph_ZOOM_white_final'
    else:
        figname = 'final_scores_barchart_standard_diff_morph_ZOOM_final'
    plt.savefig(save_dir + figname, bbox_inches='tight')
"""

