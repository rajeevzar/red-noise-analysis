import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import periodogram
from scipy.optimize import curve_fit
import math

# Configure Matplotlib settings
plt.rcParams.update({'font.size': 26})
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Avenir'


def broken_conf(signal, step_len, confidence_level=0.95, show=False):
    """
    Generate confidence intervals for a signal containing white and colored noise.

    Parameters:
    -----------
    signal : ndarray
        The input signal, evenly spaced in time (1D array).
    step_len : float
        Cadence (time step) of the input signal.
    confidence_level : float, optional
        Confidence level for detecting significant peaks (default is 0.95).
    show : bool, optional
        If True, generates plots of the results.

    Returns:
    --------
    frequencies : ndarray
        Frequency array from the periodogram.
    power_spectrum : ndarray
        Power spectrum from the periodogram.
    confidence_interval : ndarray
        Fitted confidence interval.
    max_period : float
        The largest period exceeding the confidence level.
    fitted_model : ndarray
        Fitted power-law model for the spectrum.
    """
    if not 0 < confidence_level <= 1:
        raise ValueError("Confidence level must be between 0 and 1.")

    # Compute periodogram
    frequencies, power_spectrum = periodogram(signal, fs=1.0 / step_len, scaling='spectrum')
    power_spectrum = power_spectrum[:len(frequencies) // 2]
    frequencies = frequencies[:len(frequencies) // 2]
    power_spectrum /= np.mean(power_spectrum)

    # Logarithmic transformation
    log_frequencies, log_power = zip(*[
        (math.log10(freq), math.log10(power))
        for freq, power in zip(frequencies, power_spectrum) if freq > 0
    ])
    # print("log_frequencies:", log_frequencies)
    # print("log_power:", log_power)
    # Define the piecewise linear model
    def linbreak(x, slope, intercept1, intercept2):
        return np.piecewise(
            x,
            [x < (intercept1 - intercept2) / slope, x >= (intercept1 - intercept2) / slope],
            [lambda x: intercept1 - slope * x, lambda x: intercept2]
        )

    # Fit the power spectrum with the model
    popt, _ = curve_fit(linbreak, log_frequencies, log_power, p0=[1.0, 0.01, 0.1])
    fitted_model = 10 ** linbreak(log_frequencies, *popt)

    # Calculate confidence interval
    num_frequencies = len(frequencies)
    chi2_threshold = -2.0 * np.log(1.0 - confidence_level ** (1 / num_frequencies))
    confidence_interval = [val * chi2_threshold * 0.5 for val in fitted_model]

    # Align array lengths
    min_length = min(len(frequencies), len(power_spectrum), len(confidence_interval))
    frequencies = frequencies[:min_length]
    power_spectrum = power_spectrum[:min_length]
    confidence_interval = confidence_interval[:min_length]

    # Detect significant peaks
    significant_frequencies = [
        1.0 / frequencies[i] for i in range(len(frequencies))
        if power_spectrum[i] > confidence_interval[i]
    ]
    max_period = max(significant_frequencies, default=0.0)

    # Optional: Plot the results
    if show:
        plt.figure(figsize=(10, 8))
        plt.loglog(frequencies, power_spectrum, '-k', label='Power Spectrum')
        plt.loglog(frequencies, fitted_model[:min_length], 'r', label='Fitted Model')
        plt.loglog(frequencies, confidence_interval, 'r--', label=f'CI ({confidence_level * 100:.1f}%)')
        plt.xlabel('Frequency (1/d)')
        plt.ylabel('Power')
        plt.legend()
        plt.show()

    return frequencies, power_spectrum, confidence_interval, max_period, fitted_model



# Example usage
if __name__ == "__main__":
    # Load signal data
    jd, flux = np.loadtxt('EPIC247584113.dat', unpack=True)

    # Calculate confidence intervals for different confidence levels
    freq_90, power_90, ci_90, period_90, model_90 = broken_conf(flux, step_len=1.0, confidence_level=0.90, show=False)
    freq_95, power_95, ci_95, period_95, model_95 = broken_conf(flux, step_len=1.0, confidence_level=0.95, show=False)
    freq_99, power_99, ci_99, period_99, model_99 = broken_conf(flux, step_len=1.0, confidence_level=0.99, show=False)

    # Plot the results
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(freq_90, power_90, '-k', label='Power Spectrum')
    ax.plot(freq_90, model_90, 'r', label='Fitted Model')
    ax.plot(freq_90, ci_90, 'r--', alpha=0.3, label='90% CI')
    ax.plot(freq_90, ci_99, 'r--', alpha=1.0, label='99% CI')
    ax.set_ylim(-0.1, 6)
    ax.set_xlim(0.0148, 0.2)
    ax.set_xlabel('Frequency (1/d)')
    ax.set_ylabel('Power')
    ax.legend()
    plt.tight_layout()
    plt.savefig('rednoise_pgm.pdf')
    # plt.show()
    
