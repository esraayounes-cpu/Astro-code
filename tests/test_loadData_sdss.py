import pandas as pd
import pytest

from your_package.load_sdss import load_sdss


def test_load_fits_file(monkeypatch):
    """A FITS path should call load_sdss_fits."""

    expected = pd.DataFrame({"flux": [1.0]})

    def mock_load_sdss_fits(path):
        assert path == "galaxy.fits"
        return expected

    monkeypatch.setattr(
        "your_package.load_sdss.load_sdss_fits",
        mock_load_sdss_fits,
    )

    result = load_sdss("galaxy.fits")

    pd.testing.assert_frame_equal(result, expected)


def test_load_dataframe(monkeypatch):
    """A DataFrame should call convert_sdss_photometry."""

    df = pd.DataFrame(
        {
            "u": [20.1],
            "g": [19.5],
            "r": [19.0],
        }
    )

    expected = pd.DataFrame({"flux": [42]})

    def mock_convert(data, **kwargs):
        assert data is df
        return expected

    monkeypatch.setattr(
        "your_package.load_sdss.convert_sdss_photometry",
        mock_convert,
    )

    result = load_sdss(df)

    pd.testing.assert_frame_equal(result, expected)


def test_kwargs_are_forwarded(monkeypatch):
    """Keyword arguments should be passed to convert_sdss_photometry."""

    df = pd.DataFrame({"u": [20]})

    def mock_convert(data, **kwargs):
        assert kwargs["unit"] == "Jy"
        return df

    monkeypatch.setattr(
        "your_package.load_sdss.convert_sdss_photometry",
        mock_convert,
    )

    load_sdss(df, unit="Jy")


def test_invalid_extension():
    """Unsupported file extensions should raise ValueError."""

    with pytest.raises(ValueError, match="Unsupported file format"):
        load_sdss("galaxy.csv")


def test_invalid_input_type():
    """Invalid input types should raise an exception."""

    with pytest.raises(ValueError, match="Input must"):
        load_sdss(12345)