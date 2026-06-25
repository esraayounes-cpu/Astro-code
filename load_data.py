import numpy as np
import pandas as pd
from .sed_filters import SDSS_FILTERS

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
