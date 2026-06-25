import numpy as np
import pandas as pd
import pytest
from astropy.io import fits

from galaxy_sed.data import convert_sdss_photometry, load_sdss_fits


def test_convert_sdss_photometry_basic():
    data = pd.DataFrame({
        "umag": [18.0],
        "gmag": [17.5],
        "rmag": [17.0],
        "imag": [16.8],
        "zmag": [16.7]
    })

    result = convert_sdss_photometry(data)

    # output should be a DataFrame with one row per SDSS band
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 5

    # expected columns
    assert list(result.columns) == ["band", "wavelength", "flux", "error"]

    # bands should be u,g,r,i,z
    assert list(result["band"]) == ["u", "g", "r", "i", "z"]

    # fluxes and errors should all be positive
    assert np.all(result["flux"] > 0)
    assert np.all(result["error"] > 0)


def test_convert_sdss_photometry_missing_columns():
    data = pd.DataFrame({
        "umag": [18.0],
        "gmag": [17.5]
    })

    with pytest.raises(ValueError, match="Data must contain columns"):
        convert_sdss_photometry(data)


def test_convert_sdss_photometry_with_errors_and_ebv():
    data = pd.DataFrame({
        "umag": [18.0],
        "gmag": [17.5],
        "rmag": [17.0],
        "imag": [16.8],
        "zmag": [16.7],
        "umagerr": [0.1],
        "gmagerr": [0.1],
        "rmagerr": [0.1],
        "imagerr": [0.1],
        "zmagerr": [0.1],
        "ebv": [0.02]
    })

    result = convert_sdss_photometry(data, extinguish=True)

    assert len(result) == 5
    assert np.all(result["flux"] > 0)
    assert np.all(result["error"] > 0)


def test_load_sdss_fits_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_sdss_fits("this_file_does_not_exist.fits")


def test_load_sdss_fits_reads_mock_file(tmp_path):
    # Create a fake SDSS-like FITS file
    flux = np.array([1.0, 2.0, 3.0])
    error = np.array([0.1, 0.2, 0.3])

    # your code expects data[:,0] = flux and data[:,1] = error
    arr = np.column_stack([flux, error])

    hdu = fits.PrimaryHDU(arr)
    hdu.header["COEFF0"] = 3.0
    hdu.header["COEFF1"] = 0.001

    file_path = tmp_path / "mock_sdss.fits"
    hdu.writeto(file_path)

    result = load_sdss_fits(str(file_path))

    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ["wavelength", "flux", "error"]
    assert len(result) == 3

    # check that flux/error were read correctly
    assert np.allclose(result["flux"], flux)
    assert np.allclose(result["error"], error)

    # check wavelength calculation
    expected_wavelength = 10 ** (3.0 + 0.001 * np.arange(3))
    assert np.allclose(result["wavelength"], expected_wavelength)

