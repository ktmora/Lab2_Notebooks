# File: angle.py

import numpy as np


def to_rect(long, lat):
	"""
	This function takes in latitude and longitude and converts said angles to rectangular coodinates in a 3-element vector called x.
	"""

	# Initialize 3-coordinate x vector 
	x = np.array([0, 0, 0])

	# Assign values to x vector from (lat, long)
	x[0] = np.cos(lat) * np.cos(long) 
	x[1] = np.cos(lat) * np.sin(long)
	x[2] = np.sin(lat)

	return x


def HA(x, desired_galactic_coords = (120, 0), rev=False):
	"""
	Converts spherical coordinates to rectangular, then uses those coordinates to give the correct local coordinates based off the desired galactic coordinates.  
	"""
	# Applying the rotation matrix R (NEED TO SPECIFY WHAT THIS IS)
	xp = np.dot(R, x)

	# Convert xp (x-primed) to new set of spherical coordinates (long', lat')
	longp = np.arctan2(xp[1], xp[0])
	latp = np.arcsin(xp[2])

	if rev == True:
	# Inverse (from prime to unprimed values)
	iR = np.linalg.inv(R)
	x = np.dot(iR, xp)

	else:
	xp = np.dot(R, x)

	return

	# Different Rotation Matricies (R)


	# Equatorial to Galactic
	# Needs to be reversed to go from Galactic to equatorial
	eq_to_gal = np.array([ [-0.054876, -0.873437, -0.483835], [0.494109, -0.444830, 0.746982], [-0.867666, -0.198076, 0.455984] ])

	# Equatorial to topical: (Ra, Dec) to (Ha, Dec)
        RD_to_HD = np.array([ [np.cos(LST), np.sin(LST, 0], [np.sin(LST), -1*np.cos(LST), 0], [0, 0, 1]])

	# Topical to Local: aka (Ha, Dec) to (Azimuth, Altitude)
        # Becauase (Ha, Dec) are Earth-based coords,this conversion only depends on your terestrial latitude (phi)
        phi = 37.8732 # for NHC
        HD_to_AA = np.array([ [-1*np.sin(phi), 0, np.cos(phi)], [0, -1, 0], [np.cos(phi), 0, np.sin(phi)] ])

