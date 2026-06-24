import numpy as np
import pandas as pd
from .sed_filters import SDSS_FILTERS
from astropy.io import fits


def convert_sdss_photometry(data, extinguish=True, ebv_column='ebv'):
    """
    Convert SDSS photometric magnitudes to an SED
    
    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame containing SDSS magnitudes (umag, gmag, rmag, imag, zmag)
    extinguish : bool, default=True
        Apply Galactic extinction correction?
    ebv_column : str, default='ebv'
        Name of column containing E(B-V) values
    
    Returns
    -------
    pandas.DataFrame
        DataFrame with columns: band, lambda_eff, flux, error
    """
    
    # Required columns
    required = ['umag', 'gmag', 'rmag', 'imag', 'zmag']
    if not all(col in data.columns for col in required):
        raise ValueError(f"Data must contain columns: {required}")
    
    results = []
    
    # Loop through each band
    for i, row in SDSS_FILTERS.iterrows():
        band = row['band']
        lambda_eff = row['lambda_eff']
        zp = row['ab_zeropoint']
        
        # Get magnitude
        mag_col = f"{band}mag"
        mag = data[mag_col].iloc[0]
        
        # Get magnitude error
        err_col = f"{band}magerr"
        if err_col in data.columns:
            mag_err = data[err_col].iloc[0]
        else:
            mag_err = 0.05 # default if no error column
        
        # Apply extinction correction if requested
        if extinguish:
            if ebv_column in data.columns:
                ebv = data[ebv_column].iloc[0]
                ext_coeff = row['extinction_coeff']
                mag = mag - (ext_coeff * ebv)
        
        # Convert magnitude to flux (erg/s/cm^2/Å)
        flux = 10**(-0.4 * (mag + zp))
        
        # Propagate error
        flux_err = abs(flux * 0.4 * np.log(10) * mag_err)
        
        # Append to results
        results.append({
            'band': band,
            'wavelength': lambda_eff,
            'flux': flux,
            'error': flux_err
        })
    
    return pd.DataFrame(results)

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