from matplotlib.lines import lineStyles
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import pandas as pd

import metpy.calc as mpcalc
from metpy.cbook import get_test_data
from metpy.plots import Hodograph, SkewT
from metpy.units import units

path_RS_obs = '/home/newton/ienm2020/henona/Bureau/UE_2_MESO_NH/TPIENM_LANNEMEZAN_CNRM_RS-all_L1_20220919-2107_20220919-2107_V1.nc'
path_fichier_prep_mesoNH = '/home/newton/ienm2020/henona/Bureau/UE_2_MESO_NH/run_ref/001_prep_ideal_case/IDEAL_LANNEMEZAN.nc'

def plot_RS(fichier_obs,fichier_mod,Tmin=-30,Tmax=25,Ptop=200):

    data_mod = xr.open_dataset(fichier_mod)
    data0=xr.open_dataset(fichier_obs)  
    
    p=data0['pressure'].values * units.hPa
    p_mod = (data_mod['PABST'].values/100) * units.hPa

    #print(p)
    #print(p_mod)

    T = data0['temperature'].values * units.degK
    Theta_mod = data_mod['THT'].values * units.degK
    T_mod = mpcalc.temperature_from_potential_temperature(p_mod,Theta_mod)
    #print(T_mod)

    Hu = data0['humidity'].values/100
    Td=mpcalc.dewpoint_from_relative_humidity(T,Hu)
    mixing_ration_mod = data_mod['RVT'].values
    relative_humidity_mod = mpcalc.relative_humidity_from_mixing_ratio(p_mod,T_mod,mixing_ration_mod)
    Td_mod = mpcalc.dewpoint_from_relative_humidity(T_mod,relative_humidity_mod)

    #print(Td_mod)

    wind_speed = data0['windSpeed'].values* units('m/s')
    wind_dir = data0['windDirection'].values* units.degrees
    u, v = mpcalc.wind_components(wind_speed, wind_dir)
    u_mod = data_mod['UT'].values * units('m/s')
    v_mod = data_mod['VT'].values * units('m/s')
    
    T.ito(units.degC)
    Td.ito(units.degC)
    T_mod.ito(units.degC)
    Td_mod.ito(units.degC)
    
    
    fig=plt.figure(figsize=(7,7))


    skew = SkewT(fig,aspect=80.5)

    skew.ax.set_ylim(1000, Ptop)
    skew.ax.set_xlim(Tmin,Tmax)

    # Plot the data using normal plotting functions, in this case using
    # log scaling in Y, as dictated by the typical meteorological plot
    skew.plot(p, T, color='red', linewidth=2,label='T obs')
    skew.plot(p, Td, color='blue', linewidth=2,label='Td obs')
    skew.plot_barbs(p[0::75], u[0::75], v[0::75])
    skew.plot(p_mod[0], T_mod[0], color='red', linewidth=2,label='T mod',linestyle='dotted')
    skew.plot(p_mod[0], Td_mod[0], 'blue', linewidth=2,label='Td mod',linestyle='dotted')
    
    plt.legend()
    plt.title('RS Lannemezan '+str(data0.time.values[0])[:13])

    # Show the plot
    plt.savefig('/home/newton/ienm2020/henona/Bureau/UE_2_MESO_NH/RS_comparaison_etat_initial.jpg',dpi=500)

def plot_vent(fichier_obs,fichier_mod):
    data_mod = xr.open_dataset(fichier_mod)
    data0=xr.open_dataset(fichier_obs)
    z=data0['altitude'].values * units.m
    z_mod = (data_mod['level'].values+560) * units.m
    wind_speed = data0['windSpeed'].values* units('m/s')
    wind_dir = data0['windDirection'].values* units.degrees
    u, v = mpcalc.wind_components(wind_speed, wind_dir)
    u_mod = data_mod['UT'].values * units('m/s')
    v_mod = data_mod['VT'].values * units('m/s')
    plt.plot(u,z,color='red',label='U obs')
    plt.plot(v,z,color='green',label='V obs')
    plt.plot(u_mod[0],z_mod,color='red',label='U mod',linestyle='dotted')
    plt.plot(v_mod[0],z_mod,color='green',label='V mod',linestyle='dotted')
    plt.legend()
    plt.grid()
    plt.savefig('/home/newton/ienm2020/henona/Bureau/UE_2_MESO_NH/vent_comparaison_etat_initial.jpg',dpi=500)


#plot_RS(path_RS_obs,path_fichier_prep_mesoNH)
plot_vent(path_RS_obs,path_fichier_prep_mesoNH)
