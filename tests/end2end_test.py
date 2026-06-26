import pandas as pd

from galaxy_sed import load_sdss, plot_sed


def test_complete_photometry_workflow():
 

    df = pd.DataFrame({
        "umag": [18.1],
        "gmag": [17.5],
        "rmag": [17.0],
        "imag": [16.8],
        "zmag": [16.6],
        "umagerr": [0.03],
        "gmagerr": [0.02],
        "rmagerr": [0.02],
        "imagerr": [0.02],
        "zmagerr": [0.03],
        "ebv": [0.05]
    })

    # Step 1: Load and convert
    sed = loadData_sdss(df)

    # Step 2: Verify output
    assert len(sed) == 5
    assert "band" in sed.columns
    assert "wavelength" in sed.columns
    assert "flux" in sed.columns
    assert "error" in sed.columns

    assert (sed["flux"] > 0).all()
    assert (sed["error"] > 0).all()

    # Step 3: Plot
    fig, ax = plot_sed(sed)

    assert fig is not None
    assert ax is not None
