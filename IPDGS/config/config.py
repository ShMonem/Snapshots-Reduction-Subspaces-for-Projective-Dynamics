"""
Configuration for bases computation.
Options for bases type and different properties can be changed in the "config.json"

"""

import json
import os

with open("IPDGS/config/bases_config.json") as fp:
    config = json.load(fp)
fp.close()

# testing state
vertPos_testing = config['computeState']['testingComputations']   # _Released / _Debugging

# set data sources and parameters
name = config["object"]["mesh"]
experiment = config["object"]["experiment"]     # name of you simulations  
# "first"/"avarage": used for standerization step
vertPos_rest_shape = config["vertexPos_bases"]["rest_shape"]
# pre alignment done to frames, can be '_centered' or '_alignedRigid'
preAlignement = config["vertexPos_bases"]["preAlignement"]


vertPos_maxFrames = config["vertexPos_bases"]["max_numFrames"]       # number of snapshots used in computations (NO. files you have)
snapshots_format = config["snapshots"]["format"]
snapshots_folder = config["snapshots"]["snaps_folder"]     # where snapshots are stored
animation_folder = config["snapshots"]["anims_folder"]     # where animations will be stored and found

snapshots_anim_ready = config["snapshots"]["anim_folder_ready"]     # read .off or .ply and convert it to .h5
visualize_snapshots = config["snapshots"]["visualize_aligned_animations"]  # visualize aligned snapshots
# notice that data should be put in place so that all .py can have access too!
input_snapshots_pattern = "input_data/" + name + "/" + experiment + "/" + snapshots_folder + "/pos_*" +  snapshots_format
input_animation_dir 	= "input_data/" + name + "/" + experiment + "/" + animation_folder + "/" + str(vertPos_maxFrames) + ".h5"
input_aligned_animation_dir 	= "input_data/" + name + "/" + experiment + "/" + animation_folder + "/" + str(vertPos_maxFrames) + preAlignement + ".h5"
"""
1st: vertex position reduction parameters
"""
assert  config["vertexPos_bases"]["PCA"]["compute"] == "Yes"

if config["vertexPos_bases"]["splocs"]["compute"] == "Yes":
	vertPos_bases_type = "SPLOCS" 
else:
	vertPos_bases_type = "PCA"
# store singVals to file during computations: True/False
store_vertPos_PCA_sing_val = config["vertexPos_bases"]["PCA"]["store_sing_val"]



vertPos_numFrames = config["vertexPos_bases"]["numFrames"]            # number of snapshots used in computations
vertPos_numComponents = config["vertexPos_bases"]["PCA"]["numComponents"]    # number of bases to be computed

if config["snapshots"]["read_all_from_first"] == "Yes":
	frame_increament = 1
else:
	frame_increament = vertPos_maxFrames//vertPos_numFrames 
	assert frame_increament <= 10    # max number of frame increament

# local support and splocs parameters (better not change them!)
# minimum geodesic distance for support map, d_min_in splocs paper
vertPos_smooth_min_dist = config["vertexPos_bases"]["support"]["min_dist"]
# maximum geodesic distance for support map, d_max in splocs paper: higher --> less sparsity & faster convergence
vertPos_smooth_max_dist = config["vertexPos_bases"]["support"]["max_dist"]

    
# masses file if required to pre-process snapshots
# if not found, then libigl is necessary to compute masses
vertPos_masses_file = "input_data/" + name + "/" + name + "_vertPos_massMatrix.bin"
    


# set bases parameters
standarize, massWeight, orthogonal, support = False, False, False, False
if config['vertexPos_bases']['standarized'] == '_Standarized':  # '_Standarized'/ '_nonStandarized'
    q_standarize = True
if config['vertexPos_bases']['massWeighted'] == '_Volkwein':     # 'Volkwein' / '_nonWeighted'
    q_massWeight = True
if config['vertexPos_bases']['orthogonalized'] == '_Orthogonalized':  # '_Orthogonalized'/'_nonOrthogonalized'
    q_orthogonal = True
if config['vertexPos_bases']["PCA"]['supported'] == '_Localized':    # '_Localized'/'_Global'
    q_support = 'local'
else:
    q_support = 'global'

if config["vertexPos_bases"]["PCA"]["store_sing_val"] == "Yes":
    q_store_sing_val = True
else:
    q_store_sing_val = False

# set storage directories
# find the workspace
script_dir = os.path.dirname(os.path.abspath(__file__))

vertPos_bases_name_extention = vertPos_bases_type + preAlignement + config['vertexPos_bases']['massWeighted'] +\
							 config['vertexPos_bases']['standarized'] + config['vertexPos_bases']["PCA"]['supported'] +  \
							 config['vertexPos_bases']['orthogonalized'] + vertPos_testing

vertPos_singVals_file =  "results/" + name + "/q_bases/" + vertPos_bases_type + preAlignement + config['vertexPos_bases']['massWeighted'] + \
                         config['vertexPos_bases']['standarized'] + config['vertexPos_bases']["PCA"]['supported']  + \
                         "/using_" + str(vertPos_numFrames)+ "outOf" + str(vertPos_maxFrames)+"_Frames_/"

vertPos_output_animation = "results/" + name + "/q_animationFiles/" + vertPos_bases_name_extention + "/" + experiment +\
                           "/using_" + str(vertPos_numFrames) + "outOf" + str(vertPos_maxFrames)+ "_Frames_" + \
                           'computed_' + str(vertPos_numComponents) + "_bases.h5"

vertPos_output_bases_ext = "results/" + name +"/q_bases/" + vertPos_bases_name_extention + "/" + experiment + \
                           "/using_" + str(vertPos_numFrames)+ "outOf"+ str(vertPos_maxFrames)+ "_Frames_/"
                            #+ str(vertPos_numComponents) + "_bases.h5"
        
vertPos_singVals_dir = os.path.join(script_dir, vertPos_singVals_file)
vertPos_output_animation_dir = os.path.join(script_dir, vertPos_output_animation)
vertPos_output_bases_dir = os.path.join(script_dir,vertPos_output_bases_ext)

# SPLOCS paramers

splocs_max_itrs = config["vertexPos_bases"]["splocs"]["max_itrs"]
splocs_admm_num_itrs = config["vertexPos_bases"]["splocs"]["admm_num_itrs"]
splocs_lambda = config["vertexPos_bases"]["splocs"]["lambda"]
splocs_rho = config["vertexPos_bases"]["splocs"]["rho"]

