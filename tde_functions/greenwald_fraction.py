def greenwald_fraction(shot, t_start, t_end, minor_radius=0.22):
	"""
	Calculate Greenwald fraction for a given shot and time window
	by extracting plasma parameters from mds tree using cmod_functions.
	"""
	import numpy as np
	import cmod_functions as cmod

	# Extract plasma parameters from cmod_functions
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

	# return the Greenwald fraction
	return averaged_line_average_density / greenwald_density
