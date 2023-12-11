def dead_pixel_finder(shot, foldername=None):
	"""Find dead pixels for a given shot number
 	"""

	import numpy as np
	import cmod_functions as cmod
	
	time, frames = cmod.get_apd_frames(shot)
	tlen = frames.shape[0]
	offsets = np.mean(frames[:200],axis=0)
	offsets3=np.repeat(offsets[np.newaxis],tlen,axis=0)
	frames=offsets3-frames
	means = np.mean(frames,axis=0)
	dead_pix_arr = [means <= np.average(means)*0.05][0]
	
	# Flip the array along both dimensions
	#dead_pix_arr = dead_pix_arr[::-1, ::-1]
	
	# Flip along only y direction
	dead_pix_arr = dead_pix_arr[:, ::-1]

	if foldername:
		filename = f'dead_pixels_shot_{shot}.npz'
		np.savez(foldername + filename, dead_pix_arr=dead_pix_arr)
	
	return dead_pix_arr

