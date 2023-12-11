def LCFS_limiter_positions(shot, t_start, t_end, num_time_steps=50, foldername=None):
	"""
	Finds maximum, minimum and mean value of radial position of 
	LCFS (last closed flux surface) and wall limiter positions. 
	Extracts the radial and poloidal positions of the last closed flux surface (LCFS) 
	and limiter shadow in major radius coordinates for given shots using EFIT.

	The functions 'calculate_splinted_LCFS' and 'calculated_splinted_limiter' 
	interpolates the spatial positions in order to obtain better resolution
	of the LCFS and the limiter shadow.

	Need to specify time window for the shot in order to extract 
	a given time point from where to calculate the LCFS. Since the LCFS is not stationary, 
	we make an average of the LCFS position by looking at e.g. 50 time points for TDE velocity plot.

 	Note: Dependency on https://github.com/sajidah-ahmed/cmod_functions.

	Args:
	- shot: Shot number
	- t_start: start of time series
	- t_end: end of time series
	- num_time_steps: Number of points from where to find min, max and mean LCFS location
 	- foldername: To save variables in a npz file, specify the foldername

	Returns:
	- R_LCFS_mean: Mean value from all time points of R_LCFS in cm
	- R_LCFS_min: Minimum value from all time points of R_LCFS in cm
	- R_LCFS_max: Maximum value from all time points of R_LCFS in cm
	- Z_LCFS: Poloidal coordinates in cm
	- R_limiter: Major radius coordinates in cm
	- Z_limiter: Poloidal coordinates for limiter structure in cm
	"""

	import numpy as np
	import cmod_functions as cmod

	time_points = np.linspace(t_start, t_end, num_time_steps)

	# Poloidal coordinates consists of 100 points
	R_LCFS_multiple = np.zeros((100, num_time_steps))
	Z_LCFS_multiple = np.zeros((100, num_time_steps))

	for idx, time_point in enumerate(time_points):

		# Code from cmod_functions on github
		R_limiter, Z_limiter = cmod.get_limiter_coordinates(shot_number=shot)
		R_limiter, Z_limiter = cmod.calculate_splinted_limiter(R_limiter, Z_limiter)
		rbbbs, zbbbs, _, efit_time = cmod.get_separatrix_coordinates(shot_number=shot)
		R_LCFS, Z_LCFS = cmod.calculate_splinted_LCFS(
			# Time step is the point in time from where we want to extract the LCFS
			time_step=time_point,
			efit_time=efit_time,
			rbbbs=rbbbs,
			zbbbs=zbbbs)

		R_LCFS_multiple[:, idx] = R_LCFS
		Z_LCFS_multiple[:, idx] = Z_LCFS

	# Zeros consisting of Z points and number of time steps
	R = np.zeros((len(Z_limiter), num_time_steps))
	R_LCFS_mean = np.zeros((len(Z_limiter), 1))
	R_LCFS_min = np.zeros((len(Z_limiter), 1))
	R_LCFS_max = np.zeros((len(Z_limiter), 1))

	# Find max, min and mean R_LCFS for each Z location (100 points)
	for j in range(len(Z_limiter)):
		R_LCFS_mean[j, :] = np.mean(R_LCFS_multiple[j,:])
		R_LCFS_min[j, :] = min(R_LCFS_multiple[j,:])
		R_LCFS_max[j, :] = max(R_LCFS_multiple[j,:])

	# in centimeters
	R_LCFS_mean = R_LCFS_mean*100
	R_LCFS_min = R_LCFS_min*100
	R_LCFS_max = R_LCFS_max*100
	Z_LCFS = Z_LCFS*100
	R_limiter = R_limiter*100
	Z_limiter = Z_limiter*100

	print(f'shot {shot} is complete')

	if foldername:
		filename = f'LCFS_limiter_coordinates_{shot}.npz'
		np.savez(foldername + filename, R_limiter=R_limiter, Z_limiter=Z_limiter,
			R_LCFS=R_LCFS, Z_LCFS=Z_LCFS, R_LCFS_mean=R_LCFS_mean, R_LCFS_min=R_LCFS_min,
			R_LCFS_max=R_LCFS_max)

	return R_LCFS_mean, R_LCFS_min, R_LCFS_max, Z_LCFS, R_limiter, Z_limiter

