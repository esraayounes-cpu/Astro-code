"""Plot SEDs"""

import matplotlib.pyplot as plt
import numpy as np

def plot_sed(sed, log_scale=True, title=None, xlim=None, ylim=None, **kwargs):
    """
    Plot a converted SED
    
    Parameters
    ----------
    sed : pandas.DataFrame
        DataFrame with columns: wavelength (or lambda_eff) and flux
    log_scale : bool, default=True
        Use log-log scale?
    title : str, optional
        Plot title
    xlim : tuple, optional
        x-axis limits
    ylim : tuple, optional
        y-axis limits
    **kwargs : additional arguments passed to plt.plot()
    
    Returns
    -------
    matplotlib.figure.Figure, matplotlib.axes.Axes
    """
    
    # Determine wavelength column name
    if 'wavelength' in sed.columns:
        wave_col = 'wavelength'
    elif 'lambda_eff' in sed.columns:
        wave_col = 'lambda_eff'
    else:
        raise ValueError("SED must contain 'wavelength' or 'lambda_eff' column")
    
    # Check flux column
    if 'flux' not in sed.columns:
        raise ValueError("SED must contain 'flux' column")
    
    wavelength = sed[wave_col]
    flux = sed['flux']
    has_errors = 'error' in sed.columns
    
    # Set limits
    if xlim is None:
        xlim = (wavelength.min(), wavelength.max())
    if ylim is None:
        if log_scale:
            positive_flux = flux[flux > 0]
            if len(positive_flux) > 0:
                ylim = (positive_flux.min(), flux.max())
            else:
                ylim = (1e-10, 1e-5)
        else:
            ylim = (0, (flux + sed.get('error', 0)).max())
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot
    if log_scale:
        ax.plot(np.log10(wavelength), np.log10(flux), 
                'o', markersize=8, **kwargs)
        ax.set_xlabel(r'$\log_{10}$ Wavelength (Å)')
        ax.set_ylabel(r'$\log_{10}$ Flux (erg s$^{-1}$ cm$^{-2}$ Å$^{-1}$)')
        ax.set_xlim(np.log10(xlim))
        ax.set_ylim(np.log10(ylim))
    else:
        # Add error bars if available
        if has_errors:
            ax.errorbar(wavelength, flux, yerr=sed['error'], 
                       fmt='o', capsize=4, capthick=1.5,
                       markersize=8, **kwargs)
        else:
            ax.plot(wavelength, flux, 'o', markersize=8, **kwargs)
        ax.set_xlabel('Wavelength (Å)')
        ax.set_ylabel(r'Flux (erg s$^{-1}$ cm$^{-2}$ Å$^{-1}$)')
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # Set title
    ax.set_title(title if title else 'SED Plot', fontsize=14)
    
    return fig, ax