def run_norm_ds(ds, radius):
	"""Returns the normalized dataset of a given dataset using run_norm from
	fppanalysis function by applying xarray apply_ufunc.

	Input:
	- ds: xarray Dataset
	- kwargs:
	- cut_off_freq: cut off frequency used to determine length of running window in run_norm.

	'run_norm' returns a tuple of time base and the signal. Therefore, apply_ufunc will
	return a tuple of two DataArray (corresponding to time base and the signal).
	To return a format like the original dataset, we create a new dataset of normalized frames and
	corresponding time computed from apply_ufunc.

	Description of apply_ufunc arguments.
		- first the function
		- then arguments in the order expected by 'run_norm'
		- input_core_dimensions: list of lists, where the number of inner sequences must match
		the number of input arrays to the function 'run_norm'. Each inner sequence specifies along which
		dimension to align the corresponding input argument. That means, here we want to normalize
		frames along time, hence 'time'.
		- output_core_dimensions: list of lists, where the number of inner sequences must match
		the number of output arrays to the function 'run_norm'.
		- exclude_dims: dimensions allowed to change size. This must be set for some reason.
		- vectorize must be set to True in order to for run_norm to be applied on all pixels.
	"""

	import xarray as xr
	from fppanalysis.running_moments import run_norm

	normalization = xr.apply_ufunc(
		run_norm,
		ds["frames"],
		radius,
		ds["time"],
		input_core_dims=[["time"], [], ["time"]],
		output_core_dims=[["time"], ["time"]],
		exclude_dims=set(("time",)),
		vectorize=True,
		)

	ds_normalized = xr.Dataset(
		data_vars=dict(
		frames=(["y", "x", "time"], normalization[0].data),
		),
		coords=dict(
			R=(["y", "x"], ds["R"].data),
			Z=(["y", "x"], ds["Z"].data),
			time=normalization[1].data[0, 0, :],
			),
		)

	return ds_normalized


def run_mean_ds(ds, radius):

	import xarray as xr
	from fppanalysis.running_moments import run_mean

	normalization = xr.apply_ufunc(
		run_mean,
		ds["frames"],
		radius,
		input_core_dims=[["time"], []],
		output_core_dims=[["time"]],
		exclude_dims=set(("time",)),
		vectorize=True,
		)

	ds_normalized = xr.Dataset(
		data_vars=dict(
			frames=(["y", "x", "time"], normalization.data),
			),
		coords=dict(
			R=(["y", "x"], ds["R"].data),
			Z=(["y", "x"], ds["Z"].data),
			time=ds["time"].values[radius:-radius],
			),
		)
	return ds_normalized
