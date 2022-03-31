# Author: Stefan Hofer
# Modified by: Astrid Bragstad Gjelsvik

import numpy as np
import seaborn as sns
import xarray as xr
import matplotlib.pyplot as plt
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'
#plt.rcParams.update({'font.size':16})


# CALIOP DATA
folder = '/tos-project2/NS9600K/shofer/'
data_folder = 'caliop_olimpia_new/netcdf_format/'

files_ann = ['bulk_slfs_annual.nc', 'ct_slfs_annual.nc']
files_seasonal = ['bulk_slfs_seasonal.nc', 'ct_slfs_seasonal.nc']

ann_bulk = xr.open_dataset(folder + data_folder + files_ann[0])
ann_ct = xr.open_dataset(folder + data_folder + files_ann[1])

# NORESM Data
folder_n = ['/projects/NS9600K/astridbg/data/model/noresm_rawdata/cases/NF2000climo_f19_tn14_meyers92_20220210/atm/hist/',
	    '/projects/NS9600K/astridbg/data/model/noresm_rawdata/cases/NF2000climo_f19_tn14_andenes21_20220222/atm/hist/']

data_n = ['NF2000climo_f19_tn14_meyers92_20220210.cam.h0*.nc',
	  'NF2000climo_f19_tn14_andenes21_20220222.cam.h0*.nc']


def preprocess(ds):
    ds_new = ds[['SLFXCLD_ISOTM', 'CT_SLFXCLD_ISOTM',
                 'CT_CLD_ISOTM', 'CLD_ISOTM']]
    return ds_new


list_cases = []
for i in range(2):
    case_one = xr.open_mfdataset(
        folder_n[i] + data_n[i], preprocess=preprocess)
    list_cases.append(case_one)
    print(i,": ",folder_n[i])


# =======================================================
# FUNCTIONS
# =======================================================


def arctic_slf_weighted(ds, s_bnd=66.6, n_bnd=90, ss_bnd=None, nn_bnd=None):
    '''Computes the mean of the CALIOP SLF in the Arctic,
    weighted by the size of the grid cell.
    '''
    ds_arctic = ds.sel(lat=slice(s_bnd, n_bnd))

    weighted_arctic = ds_arctic.weighted(ds_arctic.cell_weight)
    mean_arctic = weighted_arctic.mean(dim=['lat', 'lon']).SLF

    return mean_arctic


def arctic_slf_noresm(ds, s_bnd=66.6, n_bnd=90):
    '''Computes the mean SLF of NorESM2 input in the Arctic. Boundaries given by
    "s_bnd" and "n_bnd" variables.

    Defaults: s_bnd=66.6N
              n_bnd=90.0N
    '''
    lats = ds.lat.sel(lat=slice(s_bnd, n_bnd))
    # Select between boundaries given and delete first three months
    ds_arctic = ds.sel(lat=slice(s_bnd, n_bnd),
                       time=slice('2007-04-01', '2010-04-01'))
    weights_n = np.cos(np.deg2rad(lats))
    weighted = ds_arctic.weighted(weights_n)
    mean_arctic = weighted.mean(dim=['lat', 'lon', 'time'])

    mean_arctic['slf_ct'] = (mean_arctic.CT_SLFXCLD_ISOTM /
                             mean_arctic.CT_CLD_ISOTM)
    mean_arctic['slf_bulk'] = (mean_arctic.SLFXCLD_ISOTM /
                               mean_arctic.CLD_ISOTM)
    mean_arctic['isotherms_mpc'] = mean_arctic['isotherms_mpc'] - 273.15
    mean_arctic = mean_arctic.rename({'isotherms_mpc': 'isotherm'})

    return mean_arctic


def plot_slf_iso(ds, fig=False, axs=False):
    if axs == False:
        fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(4, 6))
    else:
        fig = fig
        axs = axs
    xr.plot.line(ds * 100, y='isotherm', yincrease=False, ax=axs)
    sns.despine()
    fig.tight_layout()

    return fig, axs


# ============= My own nudged runs ==========================
# This is the CALIOP data for the northern extratropics
et_n_bulk = arctic_slf_weighted(ann_bulk, s_bnd=30, n_bnd=82)
et_n_ct = arctic_slf_weighted(ann_ct, s_bnd=30, n_bnd=82)

# ==============================================================================
# PLOT THE TWO CASES
# ==============================================================================

# This plot is for the Stanford research statement
plt.close('all')
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(9, 5),dpi=300)
ax = axs.flatten()

i = 0
for case_one in list_cases:
    # First cases to compares between my runs and Jonah
    case_one_slf = arctic_slf_noresm(case_one, s_bnd=30, n_bnd=82)
    # =============================================================
    # =============== PLOTTING ROUTINE ============================
    # =============================================================
    xr.plot.line(case_one_slf.slf_bulk * 100, y='isotherm',
                 yincrease=False, label='Bulk Model', ax=ax[i], lw=2.5)
    xr.plot.line(et_n_bulk * 100, y='isotherm',
                 yincrease=False, ax=ax[i], color='black', label='Bulk Obs', lw=2.5, ls='dotted')

    xr.plot.line(case_one_slf.slf_ct * 100, y='isotherm',
                 yincrease=False, label='CT Model', ax=ax[i], lw=2.5)
    xr.plot.line(et_n_ct * 100, y='isotherm',
                 yincrease=False, ax=ax[i], color='black', label='CT Obs', lw=2.5, ls='dashdot')
    i += 1

sns.despine()
fig.tight_layout()


titles = ['CAM5', 'Andenes 2021']
i = 0
for ax in ax:
    ax.text(0.5, 0.95, titles[i], fontsize=26,
            transform=ax.transAxes, ha='center')
    ax.set_xlabel('SLF (%)', fontsize=18)
    ax.set_ylabel('Isotherm (C)', fontsize=18)
    ax.legend(frameon=False, loc='lower left')
    i += 1
fig.savefig(
    '/tos-project2/NS9600K/astridbg/master/figures/satellite_model_comparison/SLF_satellite_2cases.pdf',bbox_inces="tight")
