def plot_velocity_estimation(
        shot, # At this point, shot is only used for the title
        t_start, 
        t_end, 
        movie_data, 
        dead_pix_arr, 
        LCFS_limiter_foldername,
        title=None,
    ):
    """
    Input:
    - shot: shot number
    - f_GW: Greenwald fraction [string]
    - t_start: start time of shot
    - t_end: end time of shot
    - movie_data: movie data generated from https://github.com/uit-cosmo/velocity-estimation
    - dead_pix_arr: array containing dead pixels
    """
    import numpy as np
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    from pathlib import Path
    import cosmoplots

    axes_size = cosmoplots.set_rcparams_dynamo(plt.rcParams, num_cols=1, ls="thin")
    plt.rcParams["mathtext.fontset"] = "custom"

    fig = plt.figure()
    ax = fig.add_axes(axes_size)
  
    # Extract velocities
    vx = movie_data.get_vx()
    vy = movie_data.get_vy()
    confidences = movie_data.get_confidences()
    R = movie_data.get_R()
    Z = movie_data.get_Z()

    # Mark dead and alive pixels
    true_indices = np.where(dead_pix_arr)
    false_indices = np.where(dead_pix_arr == False)
    dead_pixels_R = R[true_indices]
    dead_pixles_Z = Z[true_indices]
    alive_pixels_R = R[false_indices]
    alive_pixels_Z = Z[false_indices]

    # Define the default vmin and vmax values
    norm = mpl.colors.Normalize(vmin=0, vmax=1)

    # Plot dead and alive pixels
    ax.scatter(dead_pixels_R, dead_pixles_Z, marker='x', color='midnightblue', s=1, linewidth=0.5)
    ax.scatter(alive_pixels_R, alive_pixels_Z, marker=".", color='midnightblue', s=0.5)
  
    # Plot LCFS and limiter
    LCFS_limiter_data = np.load(LCFS_limiter_foldername)

    R_limiter = LCFS_limiter_data['R_limiter']
    Z_limiter = LCFS_limiter_data['Z_limiter']
    R_LCFS = LCFS_limiter_data['R_LCFS']
    Z_LCFS = LCFS_limiter_data['Z_LCFS']
    R_LCFS_mean = LCFS_limiter_data['R_LCFS_mean']
    R_LCFS_min = LCFS_limiter_data['R_LCFS_min']
    R_LCFS_max = LCFS_limiter_data['R_LCFS_max']

    # Plot LCFS and limiter
    ax.plot(R_LCFS_mean, Z_LCFS, color="black", linestyle=":", linewidth=0.5)
    ax.plot(R_limiter, Z_limiter, color="black", linestyle=":", linewidth=0.5)
    ax.fill_betweenx(
        Z_LCFS.ravel(),
        R_LCFS_min.ravel(),
        R_LCFS_max.ravel(),
        alpha=0.2,
        color="lightsteelblue",
    )

    # Plot the velocity field
    qiv = ax.quiver(
        R,
        Z,
        vx,
        vy,
        confidences,
        scale=210000,
        scale_units="xy",
        angles="xy",
        norm=norm,
    )

    # Plot arrows representing magnitude
    qk = ax.quiverkey(
        qiv, 0.63, 1.025, 100000, r"$1000$ m/s", labelpos="E", coordinates="axes", fontproperties={'size':6}, labelsep=0.02
    )
    qk = ax.quiverkey(
        qiv, 0.2, 1.025, 50000, r"$500$ m/s", labelpos="E", coordinates="axes", fontproperties={'size':6}, labelsep=0.02
    )

    # Plot colorbar
    cbar = fig.colorbar(qiv, format="%.1f")
    cbar.ax.set_ylabel(r"max $\widehat{R}_{\widetilde{{\Phi}}}$", rotation=270, labelpad=13)
    ax.set_xlabel(r"$R$ / cm")
    ax.set_ylabel(r"$Z$ / cm")
    ax.set_aspect("equal")
    ax.set_ylim(min(Z[:,0]) - 0.5, max(Z[:,0] + 0.5))
    ax.set_xlim([min(R[0]) - 0.5, max(R[0]) + 0.5])
    plt.xticks(np.arange(round(min(R[0])), round(max(R[0]))+1, 1))
    plt.yticks(np.arange(round(min(Z[:,0])), round(max(Z[:,0]))+1, 1))

    ax.set_title(rf"Shot {shot} -- {title}" , fontsize=6,  x=0.5, y=1.05)
    plt.suptitle(r'time = 'f'{t_start} - {t_end} s', fontsize=4, horizontalalignment='center', x=0.59, y=1.01)

    plt.show()
