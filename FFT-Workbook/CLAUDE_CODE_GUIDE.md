# FFT Learning Workbook: Claude Code Guide

**Learn Fast Fourier Transform by using Claude Code with effective prompting.**

Before starting: Complete [SETUP.md](SETUP.md) first to get your environment running.

---

## Table of Contents

1. [How to Use This Guide](#how-to-use-this-guide)
2. [Claude Code Prompting Tips](#claude-code-prompting-tips)
3. [Use Cases 1-8](#use-cases-1-8)
4. [Challenges & Projects](#challenges--projects)
5. [Key Concepts](#key-concepts)

---

## How to Use This Guide

### The Process

1. **Read the concept** - Understand what you're learning
2. **Copy the prompt** - Use the Claude Code prompt provided
3. **Run in Claude Code** - Paste into Claude Code and execute
4. **See the output** - Plots, numbers, results
5. **Try the challenges** - Modify and experiment
6. **Build your understanding** - Keep tweaking until it clicks

### Running Code with Claude Code

```bash
# SSH to your droplet
ssh claude-do

# Attach to your session
tmux attach -t claude

# Create a new Python file
nano use_case_1.py

# (Paste the code from Claude Code prompt)
# Then save: Ctrl+O, Enter, Ctrl+X

# Run with Claude Code
claude-code use_case_1.py
```

Or use Claude Code directly:

```bash
# Start Claude Code with a new file
claude-code my_experiment.py

# It will open the code in Claude
# Paste your Python code
# Run it
```

---

## Claude Code Prompting Tips

### Tip 1: Be Specific About What You Want

**Good prompt:**
```
Create a Python script that:
1. Generates a 5 Hz sine wave for 1 second
2. Computes the FFT using scipy.fft
3. Plots both time domain (original) and frequency domain (FFT result)
4. Shows the peak frequency found
```

**Vague prompt:**
```
Make an FFT example
```

### Tip 2: Show Expected Output

**Good:**
```
Create code that finds the dominant frequency in audio.
Expected output: A plot with frequency on X-axis, magnitude on Y-axis.
Also print: "Peak frequency: X Hz"
```

**Less helpful:**
```
Find frequencies in audio
```

### Tip 3: Ask for Variations

**Good:**
```
Create the sine wave code, then show me how to modify it to:
1. Use a 20 Hz sine wave instead
2. Add multiple frequencies (5 Hz + 10 Hz)
3. Add noise to the signal
```

**Basic:**
```
Make sine wave code
```

### Tip 4: Request Explanations

```
Create FFT code that:
1. Computes the Fourier transform
2. Extracts positive frequencies
3. Finds the peak

Also explain in comments:
- Why we only look at positive frequencies
- What fftfreq does
- Why we use np.abs() on the FFT result
```

### Tip 5: Ask for Error Handling

```
Create code that:
1. Loads an audio file
2. Handles if file doesn't exist
3. Checks if it's a valid audio format
4. Prints helpful error messages
```

---

## USE CASES 1-8

### USE CASE 1: Simple Sine Wave (Foundation)

**Concept:** Create a sine wave, compute its FFT, see frequency in frequency domain

**Difficulty:** ⭐ Beginner | **Time:** 15 min

**Claude Code Prompt:**

```
Create a Python script that:

1. Generates a sine wave:
   - Duration: 1 second
   - Sample rate: 1000 Hz
   - Frequency: 5 Hz

2. Computes the FFT using scipy.fft

3. Creates two plots side-by-side:
   - Top: Time domain (first 200 samples of original signal)
   - Bottom: Frequency domain (magnitude spectrum for positive frequencies)
   
4. Prints the detected peak frequency

Use comments to explain:
- Why we use linspace() with endpoint=False
- What fftfreq() does
- Why we only plot positive frequencies

Make it visual and easy to understand for beginners.
```

**What to Try (Challenges):**

```
Try these modifications and observe what changes:

1. Change frequency to 20 Hz
   frequency = 20

2. Add a second sine wave
   signal = np.sin(2*np.pi*5*t) + 0.5*np.sin(2*np.pi*10*t)

3. Increase sample rate
   sample_rate = 2000

4. Create multiple frequencies in one signal
   frequencies = [5, 10, 15]
   signal = sum(np.sin(2*np.pi*f*t) for f in frequencies)
```

---

### USE CASE 2: Audio Frequency Analysis (Music)

**Concept:** Analyze which frequencies are present in music/sound

**Difficulty:** ⭐ Beginner | **Time:** 20 min

**Claude Code Prompt:**

```
Create a Python script that analyzes musical notes using FFT:

1. Define musical note frequencies:
   - C: 261.63 Hz
   - E: 329.63 Hz
   - G: 391.99 Hz
   - A: 440.00 Hz

2. Generate a simple melody:
   - Play C for 0-1 seconds
   - Play E for 1-2 seconds
   - Play G for 2-3 seconds
   
3. Compute FFT and create visualization:
   - Plot frequency spectrum
   - Mark the note frequencies with red dashed lines
   - Label each note on the plot
   
4. Print detected frequencies with note names

Include helper function:
freq_to_note(frequency) - converts frequency to nearest note name

This shows how FFT can identify musical notes!
```

**What to Try:**

```
Experiments:

1. Create a chord (play all notes at once):
   signal = sin(C) + sin(E) + sin(G)
   
2. Try different note combinations
   
3. Add amplitude to notes:
   signal = 0.8*sin(C) + 0.5*sin(E) + 0.3*sin(G)
   Does magnitude change in FFT?
   
4. Create your own melody sequence
```

**Challenge:** Load a real audio file

```
pip3 install librosa

Then use:
import librosa
y, sr = librosa.load("song.mp3")
# Analyze with FFT
```

---

### USE CASE 3: Noise Filtering (Clean Signals)

**Concept:** Remove unwanted frequencies from noisy data

**Difficulty:** ⭐⭐ Intermediate | **Time:** 25 min

**Claude Code Prompt:**

```
Create a Python script demonstrating noise filtering with FFT:

1. Generate test data:
   - Clean signal: 5 Hz sine wave
   - Add noise: 50 Hz sine wave (unwanted)
   - Result: Noisy signal

2. Create 3 subplots showing:
   - Top: Noisy signal (time domain)
   - Middle: Filtered signal (time domain)
   - Bottom: Frequency domain comparison
     (both before and after filtering on same plot)

3. Implement filtering:
   - Compute FFT
   - Zero out frequencies above 20 Hz
   - Inverse FFT back to time domain
   
4. Calculate improvement:
   - Mean squared error before filtering
   - Mean squared error after filtering
   - Print: "X times better after filtering"

Show how FFT reveals and removes noise!
```

**What to Try:**

```
1. Change filter cutoff:
   filtered_fft[np.abs(frequencies) > 15] = 0
   (lower number = more aggressive)
   
2. Add multiple noise frequencies:
   noise = 0.2*sin(50Hz) + 0.2*sin(80Hz)
   
3. Try a gradual filter instead of sharp cutoff:
   mask = 1 / (1 + (frequencies/20)**2)
   
4. Increase noise level:
   noise = np.random.normal(0, 1, len(t))
   Can FFT still find the signal?
```

---

### USE CASE 4: Image Blur (2D FFT)

**Concept:** FFT works on images! High frequencies = edges. Remove them = blur.

**Difficulty:** ⭐⭐ Intermediate | **Time:** 20 min

**Claude Code Prompt:**

```
Create a Python script showing 2D FFT for image processing:

1. Load built-in image:
   from scipy.datasets import face
   img = face(gray=True)

2. Compute 2D FFT and shift zero frequency to center

3. Create 4 subplots:
   - Top-left: Original image
   - Top-right: FFT magnitude (log scale) with frequencies in center
   - Bottom-left: Filter mask (circular)
   - Bottom-right: Blurred result

4. Implement circular low-pass filter:
   - Keep only frequencies within radius R
   - Zero out everything else
   - Inverse FFT to get blurred image

5. Make it interactive:
   - Show result for different radius values
   - Explain: larger radius = less blur

Demonstrate how filtering in frequency domain blurs images!
```

**What to Try:**

```
1. Change radius values:
   radius = 10, 30, 50, 100
   Observe: larger = less blur
   
2. Try inverted mask:
   mask = ~mask
   (Keep edges, remove center)
   
3. Load your own image:
   from PIL import Image
   img = np.array(Image.open('photo.jpg').convert('L'))
   
4. Create other filter shapes:
   - Square mask
   - Ring mask (only mid-range frequencies)
   - Gradual falloff instead of sharp edges
```

---

### USE CASE 5: Periodic Patterns (Time Series)

**Concept:** Find hidden cycles in data (stock prices, sensors, etc.)

**Difficulty:** ⭐⭐ Intermediate | **Time:** 25 min

**Claude Code Prompt:**

```
Create a Python script to detect periodic patterns in time series data:

1. Generate synthetic data with:
   - Trend: slowly increasing
   - Periodic: repeats every 7 days (weekly pattern)
   - Noise: random variation
   - Combined: trend + periodic + noise

2. Create 2 subplots:
   - Top: Time series data (looks random to human eyes)
   - Bottom: Frequency domain (FFT reveals the pattern!)
   
3. Find dominant frequency:
   - Use FFT to find strongest frequency
   - Convert to period: period = 1/frequency
   - Print detected period
   
4. Show the hidden pattern:
   - Extract the periodic component
   - Plot it on top of original data

Demonstrates: FFT reveals hidden cycles!

Use case: Stock prices, sensor readings, weather, etc.
```

**What to Try:**

```
1. Change periodic pattern:
   periodic = 5*sin(7-day cycle) → 5*sin(30-day cycle)
   Can you detect the new period?
   
2. Add multiple cycles:
   periodic = 5*sin(7-day) + 3*sin(30-day)
   Can FFT find both?
   
3. Increase noise:
   noise = np.random.normal(0, 2, ...)
   At what noise level can't you detect the pattern?
   
4. Try real data:
   - Stock prices from yfinance
   - Temperature data
   - Sensor readings
```

---

### USE CASE 6: Spectrograms (Frequency Over Time)

**Concept:** Music changes over time. Show frequency content changing moment-by-moment.

**Difficulty:** ⭐⭐ Intermediate | **Time:** 20 min

**Claude Code Prompt:**

```
Create a Python script showing spectrograms (frequency changing over time):

1. Generate a chirp signal:
   - Frequency increases from 200 Hz to 800 Hz over 3 seconds
   - Creates a "woop" sound that goes up in pitch
   
2. Compute STFT (Short-Time Fourier Transform):
   - This is like taking FFT of small time windows
   - Shows how frequency changes over time
   - from scipy.signal import spectrogram

3. Create 2 subplots:
   - Top: Time domain waveform
   - Bottom: Spectrogram (frequency on Y, time on X, color = power)
   
4. Visual cues:
   - Color bar showing magnitude
   - Title explaining it's a rising pitch
   - Ylabel: Frequency (Hz)

Show how FFT changes over time!
```

**What to Try:**

```
1. Change frequency range:
   from 100 Hz to 2000 Hz
   
2. Create your own chirp pattern:
   Down-up-down frequency changes
   
3. Combine with Use Case 2:
   Play musical notes that change over time
   
4. Load real audio and create spectrogram:
   import librosa
   y, sr = librosa.load('audio.mp3')
   from scipy.signal import spectrogram
   plt.specgram(y, Fs=sr)
```

---

### USE CASE 7: Pitch Detection (Audio Recognition)

**Concept:** Identify the main frequency/pitch in audio

**Difficulty:** ⭐⭐⭐ Advanced | **Time:** 30 min

**Claude Code Prompt:**

```
Create a Python script to detect pitch (dominant frequency) in audio:

1. Generate a realistic note:
   - Frequency: A4 (440 Hz - concert pitch)
   - Add harmonics (overtones) to make realistic:
     * 2nd harmonic: 2 × 440
     * 3rd harmonic: 3 × 440
   - Add noise to make challenging
   
2. Compute FFT and find peaks:
   - Use scipy.signal.find_peaks()
   - Find top 5 dominant frequencies
   
3. Convert frequencies to note names:
   - Create function: freq_to_note(frequency)
   - Show: "440 Hz = A4 (concert pitch)"
   
4. Visualization:
   - Plot frequency spectrum
   - Mark detected peaks with red dots
   - Label with note names
   
5. Print results:
   - Detected note
   - Expected note
   - How close we got

This is how tuners and pitch detection work!
```

**What to Try:**

```
1. Change the note:
   note_freq = 262  # Middle C
   note_freq = 880  # High A
   
2. Increase complexity:
   - More harmonics
   - More noise
   - How many peaks can you detect?
   
3. Load real audio:
   import librosa
   y, sr = librosa.load('voice.wav')
   
4. Build a simple tuner:
   - Show if note is sharp/flat
   - Display cents off from correct pitch
```

---

### USE CASE 8: Compression (Keep Important Frequencies)

**Concept:** Remove unimportant frequencies to save space (like MP3/JPG)

**Difficulty:** ⭐⭐⭐ Advanced | **Time:** 30 min

**Claude Code Prompt:**

```
Create a Python script showing data compression with FFT:

1. Create a complex signal:
   - Multiple frequencies with different strengths:
     * 10 * sin(5 Hz) - strong
     * 3 * sin(20 Hz) - medium
     * 1 * sin(50 Hz) - weak
     * 0.5 * sin(100 Hz) - very weak

2. Compression algorithm:
   - Compute FFT
   - Keep only top N frequency components
   - Zero out the rest
   - Inverse FFT back to time domain

3. Create 4 subplots:
   - Original signal (time)
   - Compressed signal (time)
   - All frequencies (magnitude spectrum)
   - Kept frequencies only
   
4. Calculate compression ratio:
   - Original size vs compressed size
   - Error between original and compressed
   
5. Print results:
   "Compression: 10x smaller with error = X"

Show how MP3/JPG compression works!
```

**What to Try:**

```
1. Change number of kept frequencies:
   n_keep = 3, 6, 10, 20
   How quality vs file size?
   
2. Threshold instead of count:
   Keep frequencies above 10% of max magnitude
   
3. Gradual compression:
   Instead of zero, reduce magnitude gradually
   
4. Try on image (2D):
   Load image
   Compute 2D FFT
   Keep only top frequencies
   Inverse FFT and compare
```

---

## CHALLENGES & PROJECTS

### Challenge 1: Build an Equalizer

Create sliders that control different frequency ranges:

```
Claude Code Prompt:

Create a Python script with an interactive equalizer:

1. Load audio file (or generate test audio)

2. Create frequency bands:
   - Bass: 20-250 Hz
   - Mids: 250-2000 Hz
   - Treble: 2000+ Hz

3. For each band, boost/cut by specific amount:
   - Boost bass by 10 dB
   - Keep mids neutral
   - Reduce treble by 5 dB

4. Implement using FFT:
   - FFT of audio
   - Multiply frequency ranges by gain
   - Inverse FFT back to audio

5. Output:
   - Before and after waveforms
   - Before and after spectrograms

This is how real equalizers work!
```

### Challenge 2: Pitch Shifter

Change audio pitch without changing speed:

```
Claude Code Prompt:

Create a simple pitch shifter:

1. Load audio (or generate test tone)

2. Shift frequencies up by 5 semitones:
   - FFT of audio
   - Shift all frequencies higher (multiply by 2^(5/12))
   - Inverse FFT

3. Compare:
   - Original audio
   - Pitch-shifted audio
   
4. Try different semitone shifts: -12, -5, 0, +5, +12

Note: Simple approach, professional shifters use more sophisticated techniques.
```

### Challenge 3: Real-time Spectrum Analyzer

Animate the frequency spectrum live:

```
Claude Code Prompt:

Create a real-time spectrum analyzer:

1. Continuously generate audio data (or record from mic)

2. Compute FFT of each chunk

3. Animate using matplotlib:
   - Update plot each frame
   - Show live frequency spectrum
   - Like a music visualizer

4. Use:
   import matplotlib.animation as animation
   ani = animation.FuncAnimation(...)
```

### Challenge 4: Anomaly Detector

Find when signals behave abnormally:

```
Claude Code Prompt:

Create an anomaly detection system:

1. Generate "normal" machinery signal:
   - Periodic at 60 Hz (normal operation)
   - Small noise variations

2. Add anomalies:
   - Frequency shifts to 55 Hz or 65 Hz
   - New frequencies appear
   - Harmonic changes

3. Detect anomalies:
   - Learn normal FFT pattern
   - Compare new data to normal
   - Flag when different
   
4. Print: "Anomaly detected at timestamp X"

Use case: Equipment monitoring, vibration analysis
```

### Challenge 5: Noise Profile Learner

Learn and remove background noise:

```
Claude Code Prompt:

Create a noise removal system:

1. Record background noise (e.g., fan, air conditioning)
   - Compute FFT of pure noise
   - Learn the noise profile

2. Record speech/music with that noise
   - Compute FFT
   - Subtract noise profile
   - Inverse FFT

3. Compare:
   - Noisy audio (before)
   - Cleaned audio (after)
   
4. Measure improvement (SNR, error, etc)

Use case: Voice calls, podcast recording
```

---

## KEY CONCEPTS

### The Fourier Transform Intuition

**Simple explanation:**
- Take a signal (audio, data, image)
- FFT tells you: "What frequencies are in this?"
- Result: A spectrum showing strength of each frequency

**Math summary:**
- Time domain: How signal changes over time
- Frequency domain: What frequencies are present
- FFT: Fast way to convert between them

### Why FFT is Fast

- **Naive approach:** O(n²) multiplications
- **FFT:** O(n log n) multiplications
- **Speedup:** 1000x faster for n=1000!

### Key Parameters

**Sample Rate:** How many samples per second
- Must be 2x highest frequency you want to capture
- Audio: 44,100 Hz (captures up to 22 kHz - human hearing limit)
- Example: If you want 5 kHz, need sample rate ≥ 10 kHz

**FFT Length:** How many samples to analyze
- Longer = better frequency resolution (more detail)
- Power of 2 is fastest: 256, 512, 1024, 2048, 4096
- Trade-off: More detail vs more computation

**Window Function:** Reduce edge artifacts
- Simple version: Multiply signal by Hann window
- `signal = signal * np.hanning(len(signal))`

### Common Gotchas

**1. Only plot positive frequencies**
```python
positive_idx = frequencies > 0
plot(frequencies[positive_idx], magnitude[positive_idx])
```

**2. Use np.real() when inverse FFTing**
```python
result = np.real(ifft(fft_values))  # Not just ifft()
```

**3. FFT gives complex numbers**
```python
magnitude = np.abs(fft_result)  # Convert to magnitude
phase = np.angle(fft_result)    # Or extract phase
```

**4. DC component (frequency 0) is large**
```python
# Skip first value in plotting
plot(freqs[1:], magnitude[1:])
```

---

## Prompting Template for Claude Code

Use this template when you want to create new FFT code:

```
Create a Python script that:

WHAT (what should it do?):
1. [Generate/Load data]
2. [Compute/Process with FFT]
3. [Visualize/Output results]

WHY (explain the concept):
- Explain what FFT reveals here
- Why this matters
- Real-world applications

HOW (implementation details):
- Use numpy, scipy, matplotlib
- Use comments to explain key lines
- Show equations if relevant

SHOW (visualization):
- What plots to create
- Labels and titles
- What numbers to print

CHALLENGE (how to extend it):
- Suggest 3-4 variations to try
- Ask "What if you...?"
```

---

## Learning Path Summary

```
Week 1:
  Day 1-2: Use Case 1 (Basics)
  Day 3-4: Use Case 2 (Audio, most intuitive)
  Day 5: Use Case 3 (Filtering)

Week 2:
  Pick your interest:
  - Audio path: Cases 6, 7
  - Image path: Case 4
  - Data path: Cases 5, 8

Week 3:
  Build a Challenge Project:
  - Equalizer, Pitch Shifter, Visualizer, etc.

Week 4+:
  Apply to your own data:
  - Your audio files
  - Your sensor data
  - Your images
```

---

## Resources

- [3Blue1Brown FFT Video](https://www.youtube.com/watch?v=spUNpyF58BY) - Best visual explanation
- [NumPy FFT Docs](https://numpy.org/doc/stable/reference/routines.fft.html)
- [SciPy Signal](https://docs.scipy.org/doc/scipy/reference/signal.html)
- [Librosa Docs](https://librosa.org/) - Audio processing
- [Matplotlib Tutorial](https://matplotlib.org/stable/tutorials/index.html)

---

## Next Steps

1. ✅ Complete [SETUP.md](SETUP.md) - Environment ready
2. ✅ Run Use Case 1 - See FFT basics work
3. ✅ Try the challenges - Modify code, experiment
4. ✅ Build a project - Equalizer, visualizer, etc.
5. ✅ Apply to your data - Make it personal

**Ready? Start with Use Case 1!** 🚀

Use Claude Code to generate the code, run it, see the results, modify it, learn!
