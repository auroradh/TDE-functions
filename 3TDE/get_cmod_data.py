def greenwald_fraction(shot, t_start, t_end, minor_radius=0.22):
	"""
	Calculate Greenwald fraction for a given shot and time window
	by extracting plasma parameters from mds tree using cmod_functions.
	"""
	import numpy as np
	import cmod_functions as cmod

	# Save all plasma parameters for each scan
	toroidal_magnetic_field_time, toroidal_magnetic_field = cmod.plasma_parameters.get_toroidal_magnetic_field(shot)
	plasma_current_time, plasma_current = cmod.plasma_parameters.get_plasma_current(shot)
	line_integrated_density_time, line_integrated_density = cmod.plasma_parameters.get_line_integrated_density(shot)
	line_averaged_density_time, line_averaged_density = cmod.plasma_parameters.get_line_averaged_density(shot)

	# Shift to Mega Amps before calculating average value
	plasma_current = plasma_current*1e-3

	# Calculate average values for plasma current and line averaged density
	plasma_current_sliced = plasma_current[(plasma_current_time < t_end) & (plasma_current_time > t_start)]
	averaged_plasma_current = plasma_current_sliced.mean()

	line_averaged_density_sliced = line_averaged_density[(line_averaged_density_time < t_end) & (line_averaged_density_time > t_start)]
	averaged_line_average_density = line_averaged_density_sliced.mean()

	# Calculate Greenwald density
	greenwald_density = np.abs(averaged_plasma_current) / (np.pi * minor_radius * minor_radius)
	# Greenwald density limit needs to be in terms of 10^20 m^-3
	greenwald_density = greenwald_density*1e-20

	# return Greenwald fraction
	return averaged_line_average_density / greenwald_density

def LCFS_limiter_positions(shot, t_start, t_end, num_time_steps=50):
	"""
	Finds maximum, minimum and mean value of radial position of 
	LCFS (last closed flux surface) and wall limiter positions. 
	Extracts the radial and poloidal positions of the last closed flux surface (LCFS) 
	and limiter shadow in major radius coordinates for given shots using EFIT.

	The functions 'calculate_splinted_LCFS' og 'calculated_splinted_limiter' 
	interpolates the spatial positions in order to obtain better resolution
	of the LCFS and the limiter shadow.

	Need to specify time window for the shot in order to extract 
	a given time point from where to calculate the LCFS. Since the LCFS is not stationary, 
	we make an average of the LCFS position by looking at 50 time points for TDE velocity plot. 
	Each 50 time point is saved as a npz file.

	Note: Dependency on https://github.com/sajidah-ahmed/cmod_functions. 

	Args:
	- shot: Shot number
	- t_start: start of time series
	- t_end: end of time series
	- num_time_steps: Number of points from where to find min, max and mean LCFS location

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

	time_points = np.linspace(t_start, t_end, num_time_steps=50)

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

	print(f'shot {shot} is complete')

	return R_LCFS_mean*100, R_LCFS_min*100, R_LCFS_max*100, Z_LCFS*100, R_limiter*100, Z_limiter*100