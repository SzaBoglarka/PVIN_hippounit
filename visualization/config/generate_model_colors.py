import os
import numpy
import collections
import json
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


#try:
#	colormap = plt.cm.spectral      #http://matplotlib.org/1.2.1/examples/pylab_examples/show_colormaps.html
#except:
#	colormap = plt.cm.nipy_spectral
#plt.gca().set_prop_cycle(plt.cycler('color', colormap(numpy.linspace(0.1, 0.9, len(list(data_dict.keys())))))) 

# the models in morph categories
path_morph_categs_file = "/home/szabobogi/hippounit_standard_features/hippounit/Abrazolas/__files_to_make_uniform_figures/models_in_morph_cats_with_new_names.json"
with open(path_morph_categs_file, "r") as f:
    model_morph_dict = json.load(f)
f.close() 

morphs = ["stylized_models", "detailed_models", "point_models"]
morphs_to_plot = ["stylized_models", "point_models", "detailed_models"]
model_colors_new = {}

"""
j = 0.09
k = 0.85
for morph in morphs:
    print(morph)
    #colormap = plt.cm.nipy_spectral
    colormap = plt.cm.hsv
    model_morph_dict[morph].sort()
    i = 0
    for model in model_morph_dict[morph]:
        print(model)
        model_colors_new[model] = colormap(numpy.linspace(j, k, len(model_morph_dict[morph])))[i].tolist()
        i = i + 1
    j = j - 0.04
    k = k + 0.04
"""

j = 0.09
k = 0.99
for morph in morphs:
    print(morph)
    #colormap = plt.cm.nipy_spectral
    colormap = plt.cm.hsv
    model_morph_dict[morph].sort()
    i = 0
    for model in model_morph_dict[morph]:
        print(model)
        model_colors_new[model] = colormap(numpy.linspace(j, k, len(model_morph_dict[morph])))[i].tolist()
        i = i + 1
    j = j - 0.04
    k = k - 0.04


"""
colormap = plt.cm.rainbow
model_morph_dict[morphs[0]].sort()
i = 0
for model in model_morph_dict[morphs[0]]:
    print(model)
    model_colors_new[model] = colormap(numpy.linspace(0.05, 0.94, len(model_morph_dict[morphs[0]])))[i].tolist()
    i = i + 1

colormap = plt.cm.rainbow
model_morph_dict[morphs[1]].sort()
i = 0
for model in model_morph_dict[morphs[1]]:
    print(model)
    model_colors_new[model] = colormap(numpy.linspace(0.1, 0.89, len(model_morph_dict[morphs[1]])))[i].tolist()
    i = i + 1

colormap = plt.cm.rainbow
model_morph_dict[morphs[2]].sort()
i = 0
for model in model_morph_dict[morphs[2]]:
    print(model)
    model_colors_new[model] = colormap(numpy.linspace(0, 0.99, len(model_morph_dict[morphs[2]])))[i].tolist()
    i = i + 1
"""

#print(model_colors_new)

# save the colors of the models
path_to_colors_file = '/home/szabobogi/hippounit_standard_features/hippounit/Abrazolas/__files_to_make_uniform_figures/modelcolors_vibrant_final_regi.json'

json_object = json.dumps(model_colors_new)
with open(path_to_colors_file, "w") as f:
    f.write(json_object)
f.close()

