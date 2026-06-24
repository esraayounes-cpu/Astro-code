"""Master loader for SDSS data"""

from .load_sdss_fits import load_sdss_fits
from .convert_photometry import convert_sdss_photometry

def load_sdss(input_data, **kwargs):
    """
    Load SDSS data (auto-detects photometry or spectroscopy)
    
    Parameters
    ----------
    input_data : str or pandas.DataFrame
        Either a FITS file path or a DataFrame with SDSS magnitudes
    **kwargs : additional arguments passed to conversion functions
    
    Returns
    -------
    pandas.DataFrame
        A cleaned SED DataFrame
    """
    
    # Detect input type
    if isinstance(input_data, str):
        # It's a file path
        if input_data.lower().endswith('.fits'):
            return load_sdss_fits(input_data)
        else:
            raise ValueError("Unsupported file format. Use .fits files.")
    elif hasattr(input_data, 'columns'):  # DataFrame-like
        return convert_sdss_photometry(input_data, **kwargs)
    else:
        raise ValueError("Input must be a FITS file path or a DataFrame")