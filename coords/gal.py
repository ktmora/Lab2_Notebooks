
# File: gal.py

# Hopefully the function below will take in galatic coordinates and return local coordinates in azimuth and altitude

import numpy as np
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
import astropy.units as u
import time

def to_AA(l_deg, b_deg, *, lat_obs=37.87, lon_obs=-122.27, height_m=0, obstime=None):
    """
    Convert Galactic (l,b) in degrees -> (Alt, Az) for an observer in Berkeley.

    Parameters
    ----------
    l_deg, b_deg : float
        Galactic longitude l and latitude b in degrees.
    lat_obs, lon_obs : float
        Observer latitude/longitude in degrees.
    height_m : float
        Observer height in meters.
    obstime : astropy.time.Time or None
        If None, uses current UTC time.

    Returns
    -------
    alt, az : astropy.coordinates.Angle
        Altitude and azimuth angles (use .deg for degrees).
    """

    # Galactic to ICRS (RA, dec)
    coord_gal = SkyCoord(l=l_deg * u.deg, b=b_deg * u.deg, frame="galactic")
    coord_icrs = coord_gal.icrs

    # Observer location
    location = EarthLocation(lat=lat_obs * u.deg, lon=lon_obs * u.deg, height=height_m * u.m)

    # Time
    if obstime is None:
        obstime = Time.now()

    # ICRS -> AltAz
    altaz = coord_icrs.transform_to(AltAz(obstime=obstime, location=location))

    return altaz.alt, altaz.az

# alt, az = to_AA(120, 0)
# print("Alt (deg):", alt.deg)
# print("Az  (deg):", az.deg)
