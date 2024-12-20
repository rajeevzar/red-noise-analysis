These results was part of a paper puplished in Astronomy and Astrophysics in Manick et al. 2024 (see: https://ui.adsabs.harvard.edu/abs/2024A%26A...686A.249M/abstract) 
on the discovery of one of the very first nascent planets in Classical T Tauri stars. The star CI Tau in the case of this study. This was in a broader context of detecting the very first formed planets.

The research was carried out under the European SPIDI project (https://www.spidi-eu.org/). 

Press releases: 
https://www.univ-grenoble-alpes.fr/news/headlines/discovery-of-a-nascent-planet-in-close-orbit-around-a-young-star-1409005.kjsp

https://www.insu.cnrs.fr/fr/cnrsinfo/decouverte-dune-planete-naissante-en-orbite-proche-autour-dune-etoile-jeune

https://theconversation.com/lobservation-exceptionnelle-de-la-naissance-dune-planete-en-dehors-de-notre-systeme-solaire-238341



# Red Noise Analysis with Broken Power-Law Model

This project implements a method for analyzing red noise in time-series data using a broken power-law model. It calculates confidence intervals for detecting significant peaks in the power spectrum.

## Features
- Computes periodograms for input time-series data.
- Fits a broken power-law model to the power spectrum.
- Calculates confidence intervals to identify significant peaks.
- Generates visualizations of the results.

## Requirements
- Python 3.8 or later
- Required Python packages (in `requirements.txt`):
  - `numpy`
  - `matplotlib`
  - `scipy`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/your_repo_name.git


'''
Periodogram-Peak Significance Test in Red Noise
This project addresses a critical challenge in observational astrophysics: detecting periodic or quasi-periodic signals in noisy time-series data. This challenge becomes even more significant when periodic signals are masked by stellar activity, such as red noise, or spot modulation.

The implementation is based on the method proposed by Vaughan (2005) to identify significant periodic signals in power spectra by fitting a red noise model and computing false alarm probability (FAP) levels.

Time-series data, such as the light curves from stars, often exhibit power spectra dominated by red noise, where power increases at lower frequencies. Distinguishing true periodic signals from this noise requires precise statistical tools.

For example, the K2 light curve of CI Tau (EPIC247584113.dat ) shows a dominant red noise component, making the identification of its periodic signal at 25.7 days (a key focus of this study) challenging. The classical periodogram is used here to analyze the power spectrum and identify statistically significant peaks.

Methodology
The core of the analysis involves:

Classical Periodogram:

A method based on the Discrete Fourier Transform (DFT) to compute the power spectrum of a time-series.
Frequencies are considered up to the Nyquist frequency, beyond which they are ignored.
The periodogram output at each frequency is normalized and follows a chi-squared ($\chi^2$) distribution with two degrees of freedom.


Power Law Model:

The underlying power spectral density (PSD) of the red noise is modeled as $P(f) = Nf^{-\alpha}$.
Least-squares fitting is applied in log space to estimate parameters $\hat{N}$ and $\hat{\alpha}$ for the red noise continuum.
False Alarm Probability (FAP) Levels:

Using the null hypothesis (data generated with red noise and no periodic components), significant peaks in the periodogram are identified by computing FAP levels.

Significance Testing:

Confidence intervals (e.g., 0.1% and 0.01% FAP levels) are computed to highlight statistically significant peaks.

Key Findings
The 25.7-day period (of the planet) peak observed in the classical periodogram is significant beyond the 0.01% FAP level.
The peak is consistent with results from other methods like the Generalized Lomb-Scargle (GLS) periodogram, which identifies the same periodicity within uncertainties (24 ± 5 days).

Features:
Computes periodograms for time-series data.
Fits a red noise power law model to the periodogram.
Identifies significant periodic signals based on FAP thresholds.
Output
A visualization of the periodogram showing the power spectrum, fitted red noise model, and FAP thresholds.

'''