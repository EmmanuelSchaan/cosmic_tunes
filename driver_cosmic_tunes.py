import sound
reload(sound)
from sound import *

import cmb
reload(cmb)
from cmb import *

##################################################################################
# Make noise!

sound = Sound()

# Gaussian white noise
f = lambda nu: 1.
sound.writeSound(f, duration=5., name="white")

# Gaussian Brownian noise, i.e. Gaussian red noise:
# random walk, integral of a white noise
f = lambda nu: 1./nu**2
sound.writeSound(f, duration=5., name="red")

# Gaussian Pink noise:
# because in between red and white...
f = lambda nu: 1./nu
sound.writeSound(f, duration=5., name="pink")

# Gaussian blue noise:
# Cerenkov radiation (blue flash of astronauts)
f = lambda nu: nu
sound.writeSound(f, duration=5., name="blue")

# Gaussian violet noise:
# acoustic noise underwater, preventing you from hearing the whales
f = lambda nu: nu**2
sound.writeSound(f, duration=5., name="violet")


##################################################################################
# CMB noise: Choose a 1d dimensionless power spectrum
# equal to the 2d dimensionless CMB power spectrum: l^2 C_l^2d = l C_l^1d

# Initialize CMB and foreground power spectra
cmb = StageIVCMB()

# remap frequencies to multipoles, with Lagrange interpolation polynomial
nuMin = 50.   # Hz
nuMax = 500.   # Hz
lMin = 10.
lMax = 5.e3
ell = lambda nu: lMax*(nu-nuMin)/(nuMax-nuMin) + lMin*(nuMax-nu)/(nuMax-nuMin)

# CMB noise
f = lambda nu: ell(nu) * cmb.flensedTT(ell(nu))
sound.writeSound(f, duration=5., name="lensed_cmb")

# kSZ noise
f = lambda nu: ell(nu) * cmb.fkSZ(ell(nu))
sound.writeSound(f, duration=5., name="ksz")





