import numpy as np
import matplotlib.pyplot as plt

def visualise_sed(wavelengths, flux, flux_errors=None, redshift=0,
                  object_name=None, save_path=None, show=True):

    wavelengths = np.asarray(wavelengths)
    flux = np.asarray(flux)

    if redshift > 0:
        wavelengths = wavelengths / (1 + redshift)
        xlabel = "Rest Wavelength (Angstroms)"
        title = f"Galaxy SED: {object_name or ''} (z = {redshift:.3f})"
    else:
        xlabel = "Observed Wavelength (Angstroms)"
        title = f"Galaxy SED: {object_name or ''}".strip()

    fig, ax = plt.subplots(figsize=(10, 6))

    if flux_errors is not None:
        ax.errorbar(wavelengths, flux, yerr=np.asarray(flux_errors),
                     fmt='o', capsize=5, color='black', ecolor='gray')
    else:
        ax.scatter(wavelengths, flux, color='black', s=80)

    ax.set_xlabel(xlabel)
    ax.set_ylabel("Flux Density (mJy)")
    ax.set_title(title)

    if max(wavelengths) / min(wavelengths) > 10:
        ax.set_xscale('log')
        ax.set_yscale('log')

    ax.grid(alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    if show:
        plt.show()

    return fig, ax