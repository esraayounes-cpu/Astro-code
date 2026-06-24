import numpy as np
from astropy.io import fits

def load_sdss_fits(file_path):
    """
    Load and convert an SDSS spectroscopic FITS file
    
    Parameters
    ----------
    file_path : str
        Path to the SDSS spSpec FITS file
    
    Returns
    -------
    pandas.DataFrame
        DataFrame with columns: wavelength, flux, error
    """
    
    # Check if file exists
    import os
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Read the FITS file
    hdul = fits.open(file_path)
    
    # Extract header keywords for wavelength solution
    header = hdul[0].header
    
    coeff0 = header.get('COEFF0')
    coeff1 = header.get('COEFF1')
    
    if coeff0 is None or coeff1 is None:
        raise ValueError("COEFF0 or COEFF1 not found in header. Is this an SDSS spectrum?")
    
    # Extract flux and error arrays
    data = hdul[0].data
    flux = data[:, 0]
    error = data[:, 1]
    
    # Generate wavelength array
    n_pixels = len(flux)
    pixel_indices = np.arange(n_pixels)
    wavelength = 10**(coeff0 + coeff1 * pixel_indices)
    
    hdul.close()
    
    # Return as DataFrame
    import pandas as pd
    return pd.DataFrame({
        'wavelength': wavelength,
        'flux': flux,
        'error': error
    })