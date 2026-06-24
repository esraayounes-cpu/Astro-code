import pandas as pd

SDSS_FILTERS = pd.DataFrame({
    'band': ['u', 'g', 'r', 'i', 'z'],
    'lambda_eff': [3551, 4686, 6166, 7480, 8932], # Angstroms
    'ab_zeropoint': [24.63, 25.11, 24.80, 24.77, 24.58],
    'extinction_coeff': [4.239, 3.303, 2.285, 1.698, 1.263]
})