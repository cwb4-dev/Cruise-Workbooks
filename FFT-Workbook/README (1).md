# 🎵 FFT Learning Workbook

A hands-on guide to learning **Fast Fourier Transform (FFT)** by building real projects with code. Learn signal processing, audio analysis, image processing, and more through interactive examples.

Perfect for beginners who want to understand FFT by doing, not just reading theory.

---

## ✨ What You'll Learn

- **Audio Analysis** - Find frequencies in music and sound
- **Noise Filtering** - Clean up noisy signals
- **Image Processing** - Blur, enhance, and analyze images using FFT
- **Pattern Detection** - Discover hidden cycles in time series data
- **Pitch Detection** - Identify musical notes
- **Compression** - Learn how MP3 and JPG work
- **Spectrograms** - Visualize how frequencies change over time

---

## 🚀 Quick Start

### 1. Clone This Repository
```bash
git clone <repository-url>
cd fft-learning-workbook
```

### 2. Install Dependencies
```bash
pip install numpy scipy matplotlib librosa
```

### 3. Open with Claude Code
```bash
# Option A: Use Claude Code in terminal
claude-code FFT_Learning_Workbook.md

# Option B: Copy code blocks into Claude.ai or Claude Code
# Open the workbook and paste each code example into Claude
```

### 4. Pick a Use Case and Start Coding!

Each use case includes:
- ✅ Full working starter code
- ✅ Explanation of the concept
- ✅ "What to Try" challenges
- ✅ Expected output/plots

---

## 📚 Workbook Structure

The workbook includes **8 progressive use cases**:

| # | Use Case | Topic | Difficulty |
|---|----------|-------|------------|
| 1 | Simple Sine Wave | FFT Basics | ⭐ Beginner |
| 2 | Audio Frequency Analysis | Music & Sound | ⭐ Beginner |
| 3 | Noise Filtering | Signal Processing | ⭐⭐ Intermediate |
| 4 | Image Blur | 2D FFT | ⭐⭐ Intermediate |
| 5 | Periodic Patterns | Time Series | ⭐⭐ Intermediate |
| 6 | Spectrograms | Frequency Over Time | ⭐⭐ Intermediate |
| 7 | Pitch Detection | Audio Recognition | ⭐⭐⭐ Advanced |
| 8 | Compression | Data Reduction | ⭐⭐⭐ Advanced |

---

## 💡 How to Use This Workbook

### Recommended Learning Path

**Start Here:** Use Case 1 → 2 → 3 (builds foundation)

Then pick what interests you:
- **Love music?** → Use Cases 2, 6, 7
- **Interested in images?** → Use Case 4
- **Analyzing data?** → Use Cases 5, 8
- **Want it all?** → Do them in order!

### Workflow for Each Use Case

1. **Read the explanation** - Understand the concept
2. **Copy the code** - Paste into Claude Code
3. **Run it** - See the output/plot
4. **Modify it** - Try the "What to Try" challenges
5. **Experiment** - Change parameters and observe results

### Example: Use Case 1 (Sine Wave)

```python
# Copy this into Claude Code and run
import numpy as np
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt

# Create a simple sine wave
duration = 1.0
sample_rate = 1000
t = np.linspace(0, duration, sample_rate, endpoint=False)
frequency = 5  # Hz
signal = np.sin(2 * np.pi * frequency * t)

# Compute FFT
fft_values = fft(signal)
frequencies = fftfreq(len(signal), 1/sample_rate)

# Plot
plt.plot(t[:200], signal[:200])
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Sine Wave")
plt.show()
```

**What to try:**
- Change `frequency = 5` to `frequency = 20` and rerun
- What happens to the plot?

---

## 🎯 Learning Objectives

By the end of this workbook, you'll understand:

- [ ] What the Fourier Transform does (converts time → frequency)
- [ ] Why FFT is fast (O(n log n) vs O(n²))
- [ ] How to apply FFT to real problems
- [ ] Time domain vs frequency domain thinking
- [ ] How to filter, compress, and analyze signals
- [ ] Practical applications (audio, images, sensors, finance)

---

## 📋 Prerequisites

### Software Requirements
- **Python 3.7+**
- **Claude Code** (optional but recommended) or Claude.ai

### Required Libraries
```bash
pip install numpy scipy matplotlib librosa
```

- **NumPy** - Numerical computing
- **SciPy** - Scientific computing (includes FFT)
- **Matplotlib** - Plotting and visualization
- **Librosa** - Audio processing (optional, for real audio files)

### Knowledge Requirements
- Basic Python (loops, functions, imports)
- Basic math (sine waves, frequencies)
- **No advanced math required!** We explain as we go.

---

## 🔧 Using with Claude Code

### Option 1: Claude Code Terminal (Recommended)
```bash
# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Run the workbook
claude-code FFT_Learning_Workbook.md
```

### Option 2: Claude.ai Web Interface
1. Go to [claude.ai](https://claude.ai)
2. Open the workbook file in a text editor
3. Copy code blocks one at a time
4. Paste into Claude Code (the code execution feature)
5. Run and see results instantly

### Option 3: Jupyter Notebook
```bash
# Create a Jupyter notebook
pip install jupyter
jupyter notebook

# Copy each code block into cells and run
```

### Tips for Using with Claude
- **Run one code block at a time** - don't copy everything at once
- **Modify and experiment** - Claude Code lets you see results immediately
- **Ask Claude questions** - "Why did we use fft() here?" or "What if I change this parameter?"
- **Build incrementally** - start simple, add complexity gradually

---

## 📊 Example Projects Included

### Project 1: Audio Spectrum Analyzer
See frequencies in music:
```python
# Load an audio file
import librosa
y, sr = librosa.load("song.mp3")

# Analyze frequencies
from scipy.fft import fft
spectrum = fft(y[:sr*2])  # First 2 seconds

# Plot to visualize
```

### Project 2: Noise Filter
Remove unwanted frequencies:
```python
noisy_signal = signal + noise
filtered = apply_fft_filter(noisy_signal, cutoff_freq=20)
```

### Project 3: Image Blur using FFT
Blur images in frequency domain (see how JPEGs work):
```python
from scipy.fft import fft2, ifft2
blurred = blur_image_with_fft(image, radius=30)
```

---

## 🤔 Common Questions

### Q: Do I need to understand the math?
**A:** No! We focus on intuition and practical use. The math is there if you want it, but it's not required.

### Q: How long does this take?
**A:** 
- Quick overview: 2-3 hours
- Full workbook: 1-2 weeks (with experimentation)
- One use case: 20-30 minutes

### Q: Can I use this with my own data?
**A:** **Yes!** Many use cases include challenges to use real audio files, images, or data. Just load your files and apply the same FFT code.

### Q: What if the code doesn't work?
**A:** Check:
1. Is NumPy/SciPy installed? (`pip install scipy numpy matplotlib`)
2. Are you using the right sample rate/FFT length?
3. See "Troubleshooting" section in the workbook

### Q: Is this just audio?
**A:** No! FFT works for:
- 🎵 Audio & music
- 🖼️ Images
- 📈 Stock prices & sensor data
- 🌊 Seismic data
- 📡 Radio signals
- And more!

---

## 📖 Learning Resources

### Included in This Repo
- `FFT_Learning_Workbook.md` - All 8 use cases with code
- `README.md` - This file

### External Resources
- [3Blue1Brown FFT Video](https://www.youtube.com/watch?v=spUNpyF58BY) - Excellent visual explanation
- [NumPy FFT Documentation](https://numpy.org/doc/stable/reference/routines.fft.html)
- [SciPy Signal Processing](https://docs.scipy.org/doc/scipy/reference/signal.html)
- [Librosa (Audio Processing)](https://librosa.org/)

---

## 🛠️ Troubleshooting

### Installation Issues

**Problem:** `ModuleNotFoundError: No module named 'scipy'`
```bash
# Solution: Install requirements
pip install --upgrade scipy numpy matplotlib librosa
```

**Problem:** Plots not showing in Jupyter
```python
# Add this at the top of your notebook
%matplotlib inline
```

### Code Issues

**Problem:** "FFT values don't look right"
- ✅ Make sure sample rate is 2x your highest frequency
- ✅ Use `np.real(ifft(...))` when converting back
- ✅ Check for off-by-one errors in indexing

**Problem:** "Performance is slow"
- ✅ Make FFT length a power of 2: `len(signal) = 2^n`
- ✅ Use `scipy.fft` instead of `numpy.fft`
- ✅ Process in chunks for real-time applications

See the full troubleshooting guide in the workbook!

---

## 🎓 Skill Progression

```
Beginner
  ↓
[Use Case 1-2] → "I can analyze audio!"
  ↓
Intermediate
  ↓
[Use Case 3-6] → "I can filter signals and detect patterns!"
  ↓
Advanced
  ↓
[Use Case 7-8] → "I understand signal processing!"
  ↓
Expert
  ↓
[Build your own project] → "I can apply FFT anywhere!"
```

---

## 🚀 Next Steps After This Workbook

### Challenge Projects
1. **Build an EQ (Equalizer)** - Control different frequency ranges
2. **Pitch Shifter** - Make audio higher/lower pitched
3. **Real-time Visualizer** - Animate frequency content live
4. **Anomaly Detector** - Find when machinery acts weird
5. **Noise Profile Learner** - Learn and remove background noise

### Move to Production
- Learn about **windowing functions** (improve FFT accuracy)
- Explore **filters** (more sophisticated than simple cutoff)
- Study **wavelets** (alternative to FFT for some problems)
- Build **web apps** (Audio API for browser-based audio processing)

### Dive Deeper
- Quantum Fourier Transform (QFT) in quantum computing
- 2D/3D FFT for medical imaging
- GPU acceleration with CuPy or TensorFlow
- Real-time signal processing with JACK or PortAudio

---

## 💬 Contributing

Found a bug? Have a better explanation? Want to add a use case?

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingUseCase`)
3. Commit your changes (`git commit -m 'Add amazing use case'`)
4. Push to the branch (`git push origin feature/AmazingUseCase`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🎉 Getting Started Now

```bash
# 1. Clone
git clone <repository-url>
cd fft-learning-workbook

# 2. Install
pip install numpy scipy matplotlib librosa

# 3. Code!
claude-code FFT_Learning_Workbook.md
# OR copy code blocks into Claude.ai

# 4. Learn by doing
# Start with Use Case 1, run the code, modify parameters
# Move to Use Case 2 when you're comfortable
```

**Pick a use case, copy the code, run it, and start learning!** 🚀

---

## ⭐ Show Your Support

If this workbook helped you learn FFT, please:
- ⭐ Star this repository
- 📢 Share it with others learning signal processing
- 💬 Let us know what you built!

---

## 📬 Questions?

- Open an issue on GitHub
- Check the Troubleshooting section in the workbook
- Review the External Resources section above

Happy learning! 🎵🔊📊
