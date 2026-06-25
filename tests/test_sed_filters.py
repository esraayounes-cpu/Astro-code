import pandas as pd
from galaxy_sed.sed_filters import SDSS_FILTERS


def test_sdss_filters_is_dataframe():
    assert isinstance(SDSS_FILTERS, pd.DataFrame)


def test_sdss_filters_has_expected_columns():
    expected_cols = ["band", "lambda_eff", "ab_zeropoint", "extinction_coeff"]
    assert list(SDSS_FILTERS.columns) == expected_cols


def test_sdss_filters_has_five_bands():
    assert len(SDSS_FILTERS) == 5
    assert list(SDSS_FILTERS["band"]) == ["u", "g", "r", "i", "z"]


def test_sdss_filter_wavelengths():
    expected_wavelengths = [3551, 4686, 6166, 7480, 8932]
    assert list(SDSS_FILTERS["lambda_eff"]) == expected_wavelengths


def test_sdss_filter_zeropoints():
    expected_zeropoints = [24.63, 25.11, 24.80, 24.77, 24.58]
    assert list(SDSS_FILTERS["ab_zeropoint"]) == expected_zeropoints


def test_sdss_filter_extinction_coeffs():
    expected_coeffs = [4.239, 3.303, 2.285, 1.698, 1.263]
    assert list(SDSS_FILTERS["extinction_coeff"]) == expected_coeffs