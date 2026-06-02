# FFT Learning Workbook: A Hands-On Guide

Welcome! This workbook guides you through learning FFT (Fast Fourier Transform) by building real projects. Each section has starter code you can modify and experiment with.

**Best way to use this:** Copy each code block into Claude Code, run it, modify it, and watch what happens.

---

## Setup & Prerequisites

### Required Libraries
```bash
pip install numpy scipy matplotlib librosa
```

### Quick Test - Verify Installation
```python
import numpy as np
from scipy.fft import fft
import matplotlib.pyplot as plt

print("✓ NumPy version:", np.__version__)
print("✓ Installation successful!")
```

---

## Use Case 1: Simple Sine Wave (The Absolute Basics)

**What you'll learn:** How FFT converts time-domain signals to frequency-domain

### The Concept
A sine wave oscillates back and forth. FFT tells us the **frequency** (how fast it oscillates). This is the foundation for everything else.

### Starter Code
```python
import numpy as np
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt

# Create a simple sine wave
duration = 1.0  # 1 second
sample_rate = 1000  # samples per second
t = np.linspace(0, duration, sample_rate, endpoint=False)

# Create a 5 Hz sine wave
frequency = 5  # Hz
signal = np.sin(2 * np.pi * frequency * t)

# Compute FFT
fft_values = fft(signal)
frequencies = fftfreq(len(signal), 1/sample_rate)

# Only look at positive frequencies (first half)
positive_freq_idx = frequencies > 0
positive_freqs = frequencies[positive_freq_idx]
positive_fft = np.abs(fft_values[positive_freq_idx])

# Plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

# Time domain
ax1.plot(t[:200], signal[:200])  # Show first 200 samples
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Amplitude")
ax1.set_title("Time Domain: Original Signal")
ax1.grid(True, alpha=0.3)

# Frequency domain
ax2.plot(positive_freqs[:100], positive_fft[:100])
ax2.set_xlabel("Frequency (Hz)")
ax2.set_ylabel("Magnitude")
ax2.set_title("Frequency Domain: FFT Result")
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print(f"Peak frequency found at: {positive_freqs[np.argmax(positive_fft[:100])]} Hz")
print(f"Expected frequency: {frequency} Hz")
```

### What To Try
- [ ] Change `frequency = 5` to `frequency = 20` and rerun. What changes in the plot?
- [ ] Add a second sine wave: `signal = np.sin(2*np.pi*5*t) + 0.5*np.sin(2*np.pi*10*t)`
- [ ] What happens if you increase `sample_rate` to 2000?

---

## Use Case 2: Audio Frequency Analysis (Music)

**What you'll learn:** Analyzing real audio files and visualizing their frequency content

### The Concept
Music has many frequencies playing simultaneously (bass, drums, melody, etc.). FFT separates them so we can see which are strongest.

### Starter Code - Generate Synthetic Music
```python
import numpy as np
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt

# Musical note frequencies (Hz)
notes = {
    'C': 261.63,
    'D': 293.66,
    'E': 329.63,
    'G': 391.99,
    'A': 440.00
}

# Create a simple melody
duration = 3.0
sample_rate = 44100
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Play C, then E, then G (a C major chord)
signal = np.zeros_like(t)

# First note: C (0-1 second)
mask1 = t < 1.0
signal[mask1] = np.sin(2 * np.pi * notes['C'] * t[mask1])

# Second note: E (1-2 seconds)
mask2 = (t >= 1.0) & (t < 2.0)
signal[mask2] = np.sin(2 * np.pi * notes['E'] * (t[mask2] - 1.0))

# Third note: G (2-3 seconds)
mask3 = t >= 2.0
signal[mask3] = np.sin(2 * np.pi * notes['G'] * (t[mask3] - 2.0))

# Compute FFT
fft_values = fft(signal)
frequencies = fftfreq(len(signal), 1/sample_rate)

# Get positive frequencies
positive_freq_idx = frequencies > 0
positive_freqs = frequencies[positive_freq_idx]
positive_fft = np.abs(fft_values[positive_freq_idx])

# Plot
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(positive_freqs[:2000], positive_fft[:2000])
ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("Magnitude")
ax.set_title("Frequency Spectrum of Simple Melody")
ax.grid(True, alpha=0.3)

# Mark the note frequencies
for note_name, note_freq in notes.items():
    ax.axvline(note_freq, color='red', linestyle='--', alpha=0.5, label=note_name if note_name == 'C' else '')

plt.tight_layout()
plt.show()

print("Expected peaks at:", list(notes.values()))
```

### What To Try
- [ ] Add amplitude: `signal[mask1] = 0.8 * np.sin(...)`  Does magnitude change?
- [ ] Create a chord by adding notes together: `signal = sin(C) + sin(E) + sin(G)`
- [ ] Can you identify which notes are playing by looking at the peaks?

### Challenge: Load Real Audio
```python
# Install: pip install librosa soundfile
import librosa

# Load an audio file
audio_path = "your_audio_file.mp3"  # Change this to your file
y, sr = librosa.load(audio_path, sr=None)

# Take a short chunk (first 2 seconds)
chunk = y[:sr*2]

# Compute FFT
fft_values = fft(chunk)
frequencies = fftfreq(len(chunk), 1/sr)

# Plot
positive_freq_idx = frequencies > 0
plt.figure(figsize=(12, 5))
plt.plot(frequencies[positive_freq_idx][:5000], np.abs(fft_values[positive_freq_idx][:5000]))
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("Real Audio Spectrum")
plt.grid(True, alpha=0.3)
plt.show()
```

---

## Use Case 3: Noise Filtering (Clean Signals)

**What you'll learn:** Removing unwanted frequencies from noisy data

### The Concept
Noise is usually high-frequency garbage. We can identify it in the frequency domain, remove it, and convert back to time domain. Magic!

### Starter Code
```python
import numpy as np
from scipy.fft import fft, ifft, fftfreq
import matplotlib.pyplot as plt

# Create a clean signal: 5 Hz sine wave
duration = 1.0
sample_rate = 1000
t = np.linspace(0, duration, sample_rate, endpoint=False)
clean_signal = np.sin(2 * np.pi * 5 * t)

# Add high-frequency noise
noise = 0.3 * np.sin(2 * np.pi * 50 * t)  # 50 Hz noise
noisy_signal = clean_signal + noise

# Compute FFT
fft_values = fft(noisy_signal)
frequencies = fftfreq(len(noisy_signal), 1/sample_rate)

# Create a filter: zero out frequencies above 20 Hz
filtered_fft = fft_values.copy()
filtered_fft[np.abs(frequencies) > 20] = 0

# Convert back to time domain
filtered_signal = np.real(ifft(filtered_fft))

# Plot
fig, axes = plt.subplots(3, 1, figsize=(12, 8))

# Time domain - noisy
axes[0].plot(t, noisy_signal, label='Noisy')
axes[0].plot(t, clean_signal, label='Clean (original)', linestyle='--')
axes[0].set_ylabel("Amplitude")
axes[0].set_title("Noisy Signal (5 Hz signal + 50 Hz noise)")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Time domain - filtered
axes[1].plot(t, filtered_signal, label='Filtered')
axes[1].plot(t, clean_signal, label='Clean (original)', linestyle='--')
axes[1].set_ylabel("Amplitude")
axes[1].set_title("After Filtering (Noise Removed)")
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# Frequency domain
positive_freq_idx = frequencies > 0
axes[2].plot(frequencies[positive_freq_idx], np.abs(fft_values[positive_freq_idx]), label='Before', alpha=0.7)
axes[2].plot(frequencies[positive_freq_idx], np.abs(filtered_fft[positive_freq_idx]), label='After', alpha=0.7)
axes[2].set_xlabel("Frequency (Hz)")
axes[2].set_ylabel("Magnitude")
axes[2].set_title("Frequency Domain")
axes[2].set_xlim([0, 100])
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Calculate how much better the filtered signal is
error_noisy = np.mean((noisy_signal - clean_signal) ** 2)
error_filtered = np.mean((filtered_signal - clean_signal) ** 2)
print(f"Error (noisy): {error_noisy:.6f}")
print(f"Error (filtered): {error_filtered:.6f}")
print(f"Improvement: {error_noisy/error_filtered:.1f}x better")
```

### What To Try
- [ ] Change the filter cutoff: `filtered_fft[np.abs(frequencies) > 15] = 0` (lower = more aggressive)
- [ ] Add multiple noise frequencies: `noise = 0.2*sin(50Hz) + 0.2*sin(80Hz)`
- [ ] Try a gradual filter instead of sharp cutoff (low-pass filter with smooth rolloff)

---

## Use Case 4: Simple Image Blur (2D FFT)

**What you'll learn:** FFT works on images too! High frequencies = sharp edges. Remove them = blur.

### Starter Code
```python
import numpy as np
from scipy.fft import fft2, ifft2, fftshift, ifftshift
import matplotlib.pyplot as plt
from scipy.datasets import face  # Built-in test image

# Load a grayscale image
img = face(gray=True)

# Compute 2D FFT
img_fft = fft2(img)
img_fft_shifted = fftshift(img_fft)  # Shift zero frequency to center (nicer visualization)

# Create a filter: circular mask to keep only center frequencies
rows, cols = img.shape
crow, ccol = rows // 2, cols // 2
radius = 30  # Experiment with this

# Create mask
Y, X = np.ogrid[:rows, :cols]
mask = (X - ccol)**2 + (Y - crow)**2 <= radius**2

# Apply filter
img_fft_filtered = img_fft_shifted.copy()
img_fft_filtered[~mask] = 0

# Convert back
img_fft_filtered_unshifted = ifftshift(img_fft_filtered)
img_filtered = np.real(ifft2(img_fft_filtered_unshifted))

# Plot
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

axes[0, 0].imshow(img, cmap='gray')
axes[0, 0].set_title("Original Image")
axes[0, 0].axis('off')

# Log scale for better visualization
axes[0, 1].imshow(np.log1p(np.abs(img_fft_shifted)), cmap='gray')
axes[0, 1].set_title("FFT Magnitude (log scale)")
axes[0, 1].axis('off')

axes[1, 0].imshow(mask, cmap='gray')
axes[1, 0].set_title(f"Filter Mask (radius={radius})")
axes[1, 0].axis('off')

axes[1, 1].imshow(img_filtered, cmap='gray', vmin=0, vmax=255)
axes[1, 1].set_title("Filtered (Blurred)")
axes[1, 1].axis('off')

plt.tight_layout()
plt.show()
```

### What To Try
- [ ] Increase `radius` to 50, 100. What happens?
- [ ] Try an inverted mask: `mask = ~mask` (keep edges, remove center)
- [ ] Load your own image: `from PIL import Image; img = np.array(Image.open('photo.jpg').convert('L'))`

---

## Use Case 5: Find Periodic Patterns in Data (Time Series)

**What you'll learn:** Detect hidden cycles in stock prices, sensor data, etc.

### Starter Code
```python
import numpy as np
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt

# Create synthetic data with a hidden cycle
duration = 100  # days
days = np.arange(duration)

# Trend + periodic pattern
trend = 0.1 * days  # Slowly increasing trend
periodic = 5 * np.sin(2 * np.pi * days / 7)  # Repeats every 7 days (weekly)
noise = np.random.normal(0, 0.5, duration)  # Random noise

data = 100 + trend + periodic + noise

# Compute FFT
fft_values = fft(data)
frequencies = fftfreq(len(data), 1)  # 1 sample per day

# Get positive frequencies
positive_freq_idx = frequencies > 0
positive_freqs = frequencies[positive_freq_idx]
positive_fft = np.abs(fft_values[positive_freq_idx])

# Find dominant frequency
dominant_freq = positive_freqs[np.argmax(positive_fft)]
dominant_period = 1 / dominant_freq if dominant_freq > 0 else 0

# Plot
fig, axes = plt.subplots(2, 1, figsize=(12, 8))

# Time domain
axes[0].plot(days, data, 'o-', markersize=3)
axes[0].set_xlabel("Days")
axes[0].set_ylabel("Value")
axes[0].set_title("Time Series Data (Stock Price, Sensor, etc.)")
axes[0].grid(True, alpha=0.3)

# Frequency domain
axes[1].plot(positive_freqs[1:50], positive_fft[1:50])  # Skip DC component
axes[1].set_xlabel("Frequency (1/days)")
axes[1].set_ylabel("Magnitude")
axes[1].set_title("FFT: What Cycles are Hidden in This Data?")
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print(f"Dominant period found: {dominant_period:.2f} days")
print(f"Expected period: 7 days")
```

### What To Try
- [ ] Change the periodic pattern: `periodic = 5 * np.sin(2 * np.pi * days / 30)` (30-day cycle)
- [ ] Add multiple cycles: `periodic = 5*sin(7-day) + 3*sin(30-day)`
- [ ] Increase noise: `noise = np.random.normal(0, 2, duration)` - can FFT still find the pattern?

---

## Use Case 6: Audio Spectrogram (Frequency Over Time)

**What you'll learn:** Music changes over time. Spectrograms show frequency content changing moment-to-moment.

### Starter Code
```python
import numpy as np
from scipy.fft import fft, fftfreq
from scipy import signal as scipy_signal
import matplotlib.pyplot as plt

# Create a chirp: frequency changes over time (low to high)
duration = 3.0
sample_rate = 8000
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Frequency increases from 200 Hz to 800 Hz
freq_start = 200
freq_end = 800
instantaneous_freq = np.linspace(freq_start, freq_end, len(t))
phase = 2 * np.pi * np.cumsum(instantaneous_freq) / sample_rate
audio = np.sin(phase)

# Method 1: Simple STFT (Short-Time Fourier Transform)
freqs, times, Sxx = scipy_signal.spectrogram(audio, sample_rate, nperseg=256)

# Plot
fig, axes = plt.subplots(2, 1, figsize=(12, 8))

# Waveform
axes[0].plot(t[:1000], audio[:1000])
axes[0].set_xlabel("Time (s)")
axes[0].set_ylabel("Amplitude")
axes[0].set_title("Audio Waveform (Chirp: Frequency Increasing Over Time)")
axes[0].grid(True, alpha=0.3)

# Spectrogram
im = axes[1].pcolormesh(times, freqs, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap='viridis')
axes[1].set_ylabel("Frequency (Hz)")
axes[1].set_xlabel("Time (s)")
axes[1].set_title("Spectrogram: Frequency Content Over Time")
axes[1].set_ylim([0, 1000])
plt.colorbar(im, ax=axes[1], label="Power (dB)")

plt.tight_layout()
plt.show()
```

### What To Try
- [ ] Change the chirp range: `freq_start = 100; freq_end = 2000`
- [ ] Create a melody that changes: manually define frequency vs time
- [ ] Load real audio and create a spectrogram of it

---

## Use Case 7: Find The Dominant Frequency (Pitch Detection)

**What you'll learn:** Identify the main frequency/pitch in audio

### Starter Code
```python
import numpy as np
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt

# Create a musical note: A4 (440 Hz, the "concert A")
duration = 0.5
sample_rate = 44100
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

note_freq = 440  # Hz
signal = np.sin(2 * np.pi * note_freq * t)

# Add some harmonics (overtones) - makes it sound more realistic
signal += 0.3 * np.sin(2 * np.pi * note_freq * 2 * t)  # 2nd harmonic
signal += 0.2 * np.sin(2 * np.pi * note_freq * 3 * t)  # 3rd harmonic

# Add a bit of noise
signal += 0.05 * np.random.normal(0, 1, len(signal))

# Compute FFT
fft_values = fft(signal)
frequencies = fftfreq(len(signal), 1/sample_rate)

# Get positive frequencies
positive_freq_idx = frequencies > 0
positive_freqs = frequencies[positive_freq_idx]
positive_fft = np.abs(fft_values[positive_freq_idx])

# Find peaks (dominant frequencies)
from scipy.signal import find_peaks
peaks, _ = find_peaks(positive_fft, height=np.max(positive_fft)*0.1)

# Sort peaks by magnitude
top_peaks = peaks[np.argsort(positive_fft[peaks])[-5:]]  # Top 5
top_peak_freqs = positive_freqs[top_peaks]
top_peak_mags = positive_fft[top_peaks]

# Musical note reference
note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
def freq_to_note(freq):
    """Convert frequency to nearest note name"""
    A4 = 440
    C0 = A4 * pow(2, -4.75)
    h = 12 * np.log2(freq / C0)
    octave = int(h) // 12
    note = int(h) % 12
    cents = (h - int(h)) * 100
    return f"{note_names[note]}{octave} ({freq:.1f} Hz)"

# Plot
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(positive_freqs[:2000], positive_fft[:2000], label='Spectrum')
ax.scatter(top_peak_freqs, top_peak_mags, color='red', s=100, label='Detected Peaks', zorder=5)
ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("Magnitude")
ax.set_title("Pitch Detection: Finding Dominant Frequencies")
ax.grid(True, alpha=0.3)
ax.legend()
ax.set_xlim([0, 2000])
plt.tight_layout()
plt.show()

print("Detected notes (top frequencies):")
for freq in sorted(top_peak_freqs, reverse=True):
    print(f"  {freq_to_note(freq)}")
print(f"\nExpected: {freq_to_note(note_freq)}")
```

### What To Try
- [ ] Change the note: `note_freq = 262` (middle C)
- [ ] Record yourself humming and analyze the pitch
- [ ] Can you build a simple tuner app?

---

## Use Case 8: Compression (Keep Only Important Frequencies)

**What you'll learn:** Remove unimportant frequencies to save storage space (like MP3)

### Starter Code
```python
import numpy as np
from scipy.fft import fft, ifft, fftfreq
import matplotlib.pyplot as plt

# Create a complex signal: multiple frequencies
duration = 1.0
sample_rate = 1000
t = np.linspace(0, duration, sample_rate, endpoint=False)

# Mix of different frequencies with different magnitudes
signal = (
    10 * np.sin(2 * np.pi * 5 * t) +     # Strong 5 Hz
    3 * np.sin(2 * np.pi * 20 * t) +     # Medium 20 Hz
    1 * np.sin(2 * np.pi * 50 * t) +     # Weak 50 Hz
    0.5 * np.sin(2 * np.pi * 100 * t)    # Very weak 100 Hz
)

# Compute FFT
fft_values = fft(signal)
frequencies = fftfreq(len(signal), 1/sample_rate)

# Compression: keep only top N frequencies
n_keep = 6  # Keep only top 6 components
magnitude = np.abs(fft_values)
top_n_indices = np.argsort(magnitude)[-n_keep:]

# Create compressed signal
fft_compressed = np.zeros_like(fft_values)
fft_compressed[top_n_indices] = fft_values[top_n_indices]
signal_compressed = np.real(ifft(fft_compressed))

# Calculate compression ratio
original_size = len(signal)  # How much data needed
compressed_size = n_keep * 2  # Real + Imaginary for each kept frequency
compression_ratio = original_size / compressed_size

# Plot
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Original signal
axes[0, 0].plot(t[:200], signal[:200])
axes[0, 0].set_title("Original Signal")
axes[0, 0].set_ylabel("Amplitude")
axes[0, 0].grid(True, alpha=0.3)

# Compressed signal
axes[0, 1].plot(t[:200], signal_compressed[:200])
axes[0, 1].set_title(f"Compressed Signal (kept {n_keep} frequencies)")
axes[0, 1].set_ylabel("Amplitude")
axes[0, 1].grid(True, alpha=0.3)

# FFT magnitude - all
positive_freq_idx = frequencies > 0
axes[1, 0].bar(frequencies[positive_freq_idx][:200], magnitude[positive_freq_idx][:200], width=0.5)
axes[1, 0].set_title("All Frequency Components")
axes[1, 0].set_xlabel("Frequency (Hz)")
axes[1, 0].set_ylabel("Magnitude")
axes[1, 0].grid(True, alpha=0.3, axis='y')

# FFT magnitude - kept only
fft_comp_mag = np.abs(fft_compressed)
axes[1, 1].bar(frequencies[positive_freq_idx][:200], fft_comp_mag[positive_freq_idx][:200], width=0.5)
axes[1, 1].set_title(f"Kept Components (top {n_keep})")
axes[1, 1].set_xlabel("Frequency (Hz)")
axes[1, 1].set_ylabel("Magnitude")
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

# Error metrics
error = np.mean((signal - signal_compressed) ** 2)
print(f"Compression ratio: {compression_ratio:.1f}x")
print(f"Mean squared error: {error:.6f}")
print(f"Frequencies kept: {np.sort(frequencies[top_n_indices])}")
```

### What To Try
- [ ] Change `n_keep = 3` or `n_keep = 10` - better quality or smaller size?
- [ ] Calculate the quality vs file size tradeoff
- [ ] This is basically how JPG and MP3 compression works!

---

## Challenge Projects

### Project 1: Build a Simple Equalizer
Create sliders that control the strength of different frequency ranges and hear the effect in real-time.

### Project 2: Pitch Shifter
Use FFT to shift all frequencies up or down (make audio higher or lower pitched)

### Project 3: Real-Time Audio Visualizer
Use `librosa` and `matplotlib.animation` to create a real-time frequency display

### Project 4: Anomaly Detector
Use FFT to detect when machinery or sensors behave abnormally (frequency changes unexpectedly)

### Project 5: Noise Profile Learner
Record background noise, learn its frequency profile with FFT, then remove it from recordings

---

## Key Formulas & Concepts

### The Big Picture
- **Time Domain:** How a signal changes over time
- **Frequency Domain:** What frequencies are present and how strong
- **FFT:** The algorithm that converts between them (≈ 1000x faster than naive version)

### Basic Workflow
```
Signal → FFT → Frequency Components → Modify → Inverse FFT → Modified Signal
```

### Common Parameters
- **Sample Rate (Hz):** How many samples per second (higher = capture higher frequencies)
- **Nyquist Frequency:** Highest frequency you can capture = Sample Rate / 2
- **FFT Length:** Determines frequency resolution (longer = more detail)
- **Window Function:** Apply before FFT to reduce edge artifacts (beyond scope here, but important!)

---

## Troubleshooting

**I see strange frequencies/noise in my FFT:**
- Check your sample rate is high enough (2x your highest frequency)
- Add a window function: `signal * np.hanning(len(signal))`
- Increase FFT length

**My filtered signal looks weird:**
- Try a smoother filter instead of hard cutoff
- Check that your inverse FFT is using `np.real()`

**Performance is slow:**
- Make sure FFT length is a power of 2: `len(signal) = 2^n` (very important!)
- Use `scipy.fft` instead of `numpy.fft`

---

## Next Steps

1. **Pick one use case** that interests you
2. **Run the starter code** in Claude Code
3. **Modify one parameter** and observe what changes
4. **Add complexity** - more signals, more noise, different frequencies
5. **Build your own project** combining multiple concepts

Happy FFT learning! 🎵🔊📊

---

## Resources

- [NumPy FFT docs](https://numpy.org/doc/stable/reference/routines.fft.html)
- [SciPy signal processing](https://docs.scipy.org/doc/scipy/reference/signal.html)
- [Librosa (audio)](https://librosa.org/)
- [3Blue1Brown FFT video](https://www.youtube.com/watch?v=spUNpyF58BY) - excellent intuitive explanation
