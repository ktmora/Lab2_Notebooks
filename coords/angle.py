# File: angle.py

import numpy as np
import ugradio

def to_rect(lon_deg, lat_deg):
    """
    lon, lat in DEGREES -> 3D unit vector (x,y,z).
    """
    lon = np.deg2rad(lon_deg)
    lat = np.deg2rad(lat_deg)

    x = np.zeros(3, dtype=float)
    x[0] = np.cos(lat) * np.cos(lon)
    x[1] = np.cos(lat) * np.sin(lon)
    x[2] = np.sin(lat)
    return x

def HA(l_deg, b_deg, elevation=0):
    """
    Galactic (l,b) in degrees -> local horizon-frame VECTOR (not yet alt/az angles).
    Returns a 3-vector in the final local frame.
    """

    # Galactic lon/lat -> Cartesian
    x_gal = to_rect(l_deg, b_deg)

    # Equatorial -> Galactic (J2000) rotation (your numbers, slightly more standard precision is OK too)
    EQ_TO_GAL = np.array([
        [-0.054876, -0.873437, -0.483835],
        [ 0.494109, -0.444830,  0.746982],
        [-0.867666, -0.198076,  0.455984],
    ], dtype=float)

    # Galactic -> Equatorial
    GAL_TO_EQ = np.linalg.inv(EQ_TO_GAL)
    x_eq = GAL_TO_EQ @ x_gal

    # LST
    lst = ugradio.timing.lst()  # often HOURS in ugradio
    # convert hours -> radians (robust heuristic)
    if lst > 2*np.pi:
        lst_rad = (lst / 24.0) * 2*np.pi
    else:
        lst_rad = lst

    # "RD_to_HD": rotate equatorial vector by +LST about z
    RD_to_HD = np.array([
        [ np.cos(lst_rad),  np.sin(lst_rad), 0.0],
        [-np.sin(lst_rad),  np.cos(lst_rad), 0.0],
        [ 0.0,              0.0,             1.0],
    ], dtype=float)

    x_hd = RD_to_HD @ x_eq

    # site latitude
    phi = np.deg2rad(37.8732)  # radians

    # "HD_to_AA": your matrix (keep it) but apply matrix @ vector
    HD_to_AA = np.array([
        [-np.sin(phi), 0.0,  np.cos(phi)],
        [ 0.0,        -1.0,  0.0],
        [ np.cos(phi), 0.0,  np.sin(phi)],
    ], dtype=float)

    x_local = HD_to_AA @ x_hd
    return x_local

v = HA(120, 0)
print("local vector:", v)

def vec_to_altaz():
	x, y, z = v
	alt = np.arcsin(np.clip(z, -1, 1))
	az = np.arctan2(y, x) % (2*np.pi)
	return np.rad2deg(alt), np.rad2deg(az)

alt_deg, az_deg = vec_to_altaz(HA(120, 0))
print("alt (deg):", alt_deg, "az (deg):", az_deg)


