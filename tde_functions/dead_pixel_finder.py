import numpy as np
import cmod_functions as cmod

#shot = 1100803006
#shotlist = [
#	1160616009,
#	1160616011,
#	1160616016,
#	1160616017,
#	1160616018,
#	1160616022,
#	1160616025,
#	1160616026,
#]
#shotlist = [1160616025,1160616027,1160616018]
shotlist = [1160616025]
#shotlist = [1120921007]
#shotlist = [1100803005, 1100803006, 1100803008, 1100803009, 1100803011, 1100803012, 1100803015, 1100803020]
#shotlist = [1160629026]
for shot in shotlist:
	time, frames = cmod.get_apd_frames(shot)
	tlen = frames.shape[0]
	offsets = np.mean(frames[:200],axis=0)
	offsets3=np.repeat(offsets[np.newaxis],tlen,axis=0)
	frames=offsets3-frames
	means = np.mean(frames,axis=0)
	dead_pix_arr = [means <= np.average(means)*0.05][0]

	# Flip the array along both dimensions
	dead_pix_arr = dead_pix_arr[::-1, ::-1]

	# Flip along only y direction
	#dead_pix_arr = dead_pix_arr[:, ::-1]
	print(dead_pix_arr)
	#print(f'{dead_pix_arr,np.shape(dead_pix_arr)=}')
	#print(f'{dead_pix_arr.shape=}')

	#filename = f'dead_pixels_shot_{shot}.npz'
	#foldername = '/home/helgeland/data/dead_pixels/'
	#np.savez(foldername + filename, dead_pix_arr=dead_pix_arr)

	print(f'shot {shot} is complete')
