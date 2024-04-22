import os
import cProfile
import pstats
from IPDGS.classes.posComponents import posComponents
from external.splocs.inout import convert_sequence_to_hdf5, load_off, load_ply
from external.splocs.align_rigid import align
from external.splocs.view_animation import view_anim_file
from functools import partial
from IPDGS.config.config import vertPos_numFrames, snapshots_format, frame_increament, input_snapshots_pattern, \
                                input_animation_dir, input_aligned_animation_dir, visualize_snapshots
root_folder = os.getcwd()
profiler = cProfile.Profile()


def main():

    # in case input_animation_dir hasn ot been created yet:

    # read snapshots: list of meshes in .off or .ply format
    output_filename = input_animation_dir
    if not os.path.exists(input_aligned_animation_dir):
        # Create a new directory because it does not exist
        os.makedirs(output_filename)
        print("A directory is created to store snapshots animations!")
    else:
        print("Warning! an old the store directory already exists: \n", output_filename,
              "\n make sure you are not over-writing! ")

    print("Frame increament: ", frame_increament)
    if snapshots_format == ".off":
        convert_sequence_to_hdf5(input_snapshots_pattern, partial(load_off, no_colors=True),
                                 output_filename, vertPos_numFrames, frame_increament)
    elif snapshots_format == ".ply":
        convert_sequence_to_hdf5(input_snapshots_pattern, load_ply, output_filename,
                                 vertPos_numFrames, frame_increament)
    else:
        print("Yet, only .off/.ply mesh files are supported for snapshots!")
        return
    align(output_filename, input_aligned_animation_dir)

    if visualize_snapshots:
        view_anim_file(input_aligned_animation_dir)
    # read snapshots and bases computation
    # bases = posComponents()


if __name__ == '__main__':

    # parser = argparse.ArgumentParser(
    # 	description='Find Deformation Bases')
    # parser.add_argument('input_animation_file')
    # parser.add_argument('output_components_file')
    # parser.add_argument('-a', '--output_anim',
    # 					help='Output animation file (will also save the component weights)')
    # args = parser.parse_args()
    # main(args.input_animation_file,
    # 	args.output_components_file,
    # 	args.output_anim)

    profiler.enable()
    main()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('tottime')
    # stats.print_stats()