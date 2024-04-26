import argparse
import h5py
from itertools import count
from mayavi import mlab
from tvtk.api import tvtk
from tvtk.common import configure_input, configure_input_data


def view_anim_file(hdf5_animation_file):
	weights = None
	with h5py.File(hdf5_animation_file, 'r') as f:
		verts = f['verts'][()] #.value
		tris = f['tris'][()] #.value
		if 'weights' in f:
			weights = f['weights'][()] #.value
			
	pd = tvtk.PolyData(points=verts[0], polys=tris)
	normals = tvtk.PolyDataNormals(splitting=False)
	configure_input_data(normals, pd)
	
	# choose position and orientation
	actor = tvtk.Actor(mapper=tvtk.PolyDataMapper(), position=(0, 0, 0), orientation=(0, -90, 0))
	configure_input(actor.mapper, normals)
	actor.property.set(edge_color=(0.5, 0.5, 0.5), ambient=0.0,
		               specular=0.15, specular_power=128., shading=True, diffuse=0.8)

	fig = mlab.figure(bgcolor=(1,1,1), size=(1024, 1024))
	fig.scene.add_actor(actor)
	
	
	# Choose a view angle, and display the figure
	# mlab.view(90, 45, 7.5, [1.5, 0, 0])
	# mlab.savefig(filename='photofile.png')
	
	@mlab.animate(delay=40, ui=True)
	def animation():
		for i in count():
			if weights is not None:
				w_str = ",".join(["%0.2f"] * weights.shape[1])
				print ("Frame %d Weights = " + w_str) % tuple([i] + weights[i].tolist())
			frame = i % len(verts)
			pd.points = verts[frame]
			fig.scene.render()
			yield

	a = animation()
	fig.scene.z_minus_view()
	mlab.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Animation viewer for hdf5 mesh animationfiles '
                    '(use import scripts to convert other formats to hdf5)')
    parser.add_argument('input_filename')
    args = parser.parse_args()
    main(args.input_filename)

