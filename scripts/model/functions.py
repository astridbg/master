

def fix_cam_time(ds):
    # Author: Marte Sofie Buraas / Ada Gjermundsen    

    """ NorESM raw CAM h0 files has incorrect time variable output,
    thus it is necessary to use time boundaries to get the correct time
    If the time variable is not corrected, none of the functions involving time
    e.g. yearly_avg, seasonal_avg etc. will provide correct information

    Parameters
    ----------
    ds : xarray.DaraSet

    Returns
    -------
    ds_weighted : xarray.DaraSet with corrected time
    """
    from cftime import DatetimeNoLeap

    months = ds.time_bnds.isel(nbnd=0).dt.month.values
    years = ds.time_bnds.isel(nbnd=0).dt.year.values
    dates = [DatetimeNoLeap(year, month, 15) for year, month in zip(years, months)]
    ds = ds.assign_coords(time=dates)
    return ds

def computeWeightedMean(ds):

    # Author: Anne Fouilloux
    import numpy as np

    # Compute weights based on the xarray you pass
    weights = np.cos(np.deg2rad(ds.lat))
    weights.name = "weights"
    # Compute weighted mean
    air_weighted = ds.weighted(weights)
    weighted_mean = air_weighted.mean(("lon", "lat"))
    return weighted_mean
