"""
Continuous Cauchy Wavelet Transform (CCWT) of EXAFS signal.

Ported into a reusable function from the original script by:
    Latif Ullah Khan, Beamline Scientist, BM08-XAFS/XRF Beamline, SESAME

Reference:
    Munoz M., Argoul P. et Farges F. (2003)
    Continuous Cauchy wavelet transform analyses of EXAFS spectra: a qualitative approach.
    American Mineralogist volume 88, pp. 694-700.
"""

import math
import numpy as np
from scipy.interpolate import griddata


class CCWTError(ValueError):
    """Raised when the CCWT computation cannot be completed with the given data/parameters."""


def compute_ccwt(kold, xold, n=200, ri=0.2, rf=6.0, na=200, kin=None, kfin=None, nt=256, z=8):
    """
    Compute the Continuous Cauchy Wavelet Transform of an EXAFS chi(k) signal.

    Parameters
    ----------
    kold, xold : 1D arrays
        Raw k and chi(k) values loaded from the data file.
    n : int
        Cauchy wavelet order.
    ri, rf : float
        Minimum / maximum R-space distance (Angstrom).
    na : int
        Number of R-space intervals.
    kin, kfin : float, optional
        Initial / final k value used for interpolation. Defaults to the data range.
    nt : int
        Number of interpolation points.
    z : int
        Zero-padding factor for the FFT.

    Returns
    -------
    dict with keys: knew, xnew, freq, ft_magnitude, r, wavelet_magnitude
    """
    kold = np.asarray(kold, dtype=float)
    xold = np.asarray(xold, dtype=float)

    if kold.size < 2:
        raise CCWTError("Data file must contain at least two points.")

    if kin is None:
        kin = float(kold[0])
    if kfin is None:
        kfin = float(kold[-1])
    if kfin <= kin:
        raise CCWTError("Final k value must be greater than initial k value.")
    if ri <= 0 or rf <= ri:
        raise CCWTError("R-space range must satisfy 0 < ri < rf.")
    if n < 2:
        raise CCWTError("Cauchy order n must be >= 2.")
    if na < 2:
        raise CCWTError("Number of R-space intervals (na) must be >= 2.")
    if not np.any(xold):
        raise CCWTError("The chi(k) column is all zeros; nothing to transform.")

    # Ensure k is sorted ascending for interpolation (np.interp requires it).
    if kold.size > 1 and not np.all(np.diff(kold) > 0):
        order = np.argsort(kold)
        kold, xold = kold[order], xold[order]
        if np.any(np.diff(kold) == 0):
            raise CCWTError("Data file has duplicate k values; please de-duplicate before uploading.")

    # EXAFS data interpolation
    pask = (kfin - kin) / nt
    knew = np.arange(kin, kfin, pask)
    xnew = np.interp(knew, kold, xold)

    if knew.size < 4:
        raise CCWTError("Too few points after interpolation; widen the k range.")

    # Wavelet transform analysis
    nk = len(knew)
    ZF = z * nk
    npt = ZF // 2
    freq = 1 / pask * np.arange(0, npt) / ZF
    omega = 2 * np.pi * freq

    # Fourier Transform calculation
    tff = np.fft.fft(xnew, ZF)
    TF = tff[:npt] / np.max(np.abs(tff))

    # Scale parameter
    r = np.linspace(ri, rf, na)
    a = n / (2 * r)

    # Characteristic values of the Cauchy wavelet
    s = sum(math.log(y) for y in range(1, n))

    # Cauchy wavelet calculation
    filtre = np.zeros((na, npt))
    for i in range(na):
        int_a = a[i] * omega
        int_a_safe = np.where(int_a == 0, 1, int_a)
        filtre[i] = np.where(
            int_a == 0, 0,
            np.exp(math.log(2 * np.pi) - s + n * np.log(int_a_safe) - int_a_safe)
        )

    myttf = tff[:npt]

    # Wavelet transform calculation
    to = np.array([np.fft.ifft(np.conj(filtre[i]) * myttf, ZF) for i in range(na)])

    Z = np.abs(to[:, :nk])
    X, Y = np.meshgrid(knew, r)
    points = np.array([X.flatten(), Y.flatten()]).T
    values = Z.flatten()
    zi = griddata(points, values, (X, Y), method='linear')
    zi = np.nan_to_num(zi, nan=0.0)

    return {
        "knew": knew,
        "xnew": xnew,
        "freq": freq,
        "ft_magnitude": np.abs(TF),
        "r": r,
        "wavelet_magnitude": zi,
    }
