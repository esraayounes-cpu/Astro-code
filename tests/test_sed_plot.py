import pandas as pd
import pytest
from galaxy_sed.sed_plot import plot_sed


def test_plot_sed_with_wavelength_column():
    sed = pd.DataFrame({
        "wavelength": [3551, 4686, 6166, 7480, 8932],
        "flux": [1e-17, 2e-17, 3e-17, 2.5e-17, 2e-17]
    })

    fig, ax = plot_sed(sed)

    assert fig is not None
    assert ax is not None
    


def test_plot_sed_with_lambda_eff_column():
    sed = pd.DataFrame({
        "lambda_eff": [3551, 4686, 6166, 7480, 8932],
        "flux": [1e-17, 2e-17, 3e-17, 2.5e-17, 2e-17]
    })

    fig, ax = plot_sed(sed)

    assert fig is not None
    assert ax is not None




def test_plot_sed_missing_flux_column():
    sed = pd.DataFrame({
        "wavelength": [3551, 4686, 6166],
    })

    with pytest.raises(ValueError, match="SED must contain 'flux' column"):
        plot_sed(sed)


def test_plot_sed_missing_wavelength_column():
    sed = pd.DataFrame({
        "flux": [1e-17, 2e-17, 3e-17]
    })

    with pytest.raises(ValueError, match="SED must contain 'wavelength' or 'lambda_eff' column"):
        plot_sed(sed)

