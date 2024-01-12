"""This script makes xarray format of W7X HDF5 files."""

import numpy as np
import xarray as xr
import h5py

def vector_rotation(vector,beta):
    """ 
    Code from Seung-Gyou Baek from 'test_tde.py'
    """

    beta_rad = beta*(np.pi/180)
    M = np.zeros((2,2))
    M[0,0] = np.cos(beta_rad)
    M[1,0] = np.sin(beta_rad)
    M[0,1] = -np.sin(beta_rad)
    M[1,1] = np.cos(beta_rad)
    vector_prime = M.dot(vector)

    return vector_prime

def rad_pol_positions(filename):
    """
    Create radial and poloidal positions of the pixels. 

    Code from Seung-Gyou Baek in 'test_tde.py'

    """
    z_arr = filename['z_arr']/10. # in centimeters, shape = (16,8), (row, column)
    r_arr = filename['r_arr']/10. # in centimeters, (16,8), (row,column) 
    pol_arr = z_arr*0.0
    rad_arr = r_arr*0.0
    nrows = r_arr.shape[0]
    ncols = r_arr.shape[1]
    fov_angle = 21.485

    for j in range(ncols):
        for i in range(nrows):
            vector_prime = vector_rotation([(r_arr[i,j]-r_arr[15,0]),z_arr[i,j]-z_arr[15,0]],\
                                            fov_angle)
            pol_arr[i,j] = vector_prime[1]
            rad_arr[i,j] = vector_prime[0]

    return z_arr, r_arr, pol_arr, rad_arr


def create_xarray_from_hdf5(filename, R_arr, Z_arr):
    """
    Creates an xarray dataset from the W7X HDF5 files.
    
    Code from Seung-Gyou Baek in 'test_tde.py'

        Input: 
            - filename: string, .h5 file
            - R_arr: radial positions of pixels
            - Z_arr: poloidal positions of pixels
        Returns:
            - ds: xarray dataset
    """
    f = h5py.File(filename,'r')
    frames  = f['frames'][()]
    times = f['dimensions'][()] # times are in units of nanoseconds
    time=(times-times[0])/1.e9 - 0.992 # in seconds

    scale = f['scale'][()]
    offset = f['offset'][()]
    # I want to take 1001 samples to be consistent with the IDL script
    offsets = np.sum(frames[0:1001,:,:],axis=0)/1001.

    # make the brightness unit from int to float
    # in order to apply the scale and offset factors
    bri = frames.astype(float) 
    for i in range(bri[:,0,0].shape[0]): #(frames, row, column)
        bri[i,:,:] = -scale * (offsets - bri[i,:,:])

    return xr.Dataset(
        {"frames": (["time", "y", "x"], bri)},
        coords={"R": (["y", "x"], R_arr), "Z": (["y", "x"], Z_arr), "time": (["time"], time)},
    )
    

if __name__ == "__main__":
    shot = 221214013
    filename = '/Users/ahe104/Box/W7X_data/W7X_gpi_h5_files/'+str(shot).strip()+'.h5'
    rad_pol_filename = np.load('/Users/ahe104/Box/W7X_data/rz_arrays/rz_arrs.npz')
    z_arr, r_arr, pol_arr, rad_arr = rad_pol_positions(rad_pol_filename)
    ds = create_xarray_from_hdf5(filename, r_arr, z_arr)
