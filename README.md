# ⚡ G-OC Calculator — GPU Overclock & Power Estimator

![Platform](https://img.shields.io/badge/PLATFORM-WINDOWS_10%20%2F%2011-0078D6?style=for-the-badge&logo=windows)
![Release](https://img.shields.io/badge/RELEASE-V2.0.1--BETA3-2EA44F?style=for-the-badge)
![Status](https://img.shields.io/badge/STATUS-IN_DEVELOPMENT-E3B341?style=for-the-badge)
![License](https://img.shields.io/badge/LICENSE-MIT-8957E5?style=for-the-badge)

**Plan a GPU overclock before you touch a single slider.** G-OC Calculator estimates the memory bandwidth and compute gain of an overclock, how much extra power it will draw, and whether your power supply can handle it. It is free, open source, portable, and runs fully offline.

> **It is a calculator, not an overclocking tool.** The app never changes your GPU settings, clocks, voltage or BIOS. "APPLY OC" only runs the calculation.

---

## 📸 Screenshots

<img width="1045" height="1039" alt="G-OC Calculator, AMD theme" src="https://github.com/user-attachments/assets/a968c326-0a58-4cd5-a6fa-4b7e3cd4f835" />

The interface changes its accent color to match your card: **NVIDIA (green)**, **AMD (red)**, **Intel (blue/purple)**.

---

## 🔑 Key Features

* 🚀 **Performance estimator.** Stock vs overclock for memory speed (Gbps), memory bandwidth (GB/s) and compute (TFLOPS), shown side by side with bars.
* ⚡ **PSU and power check.** Estimated GPU power at the new clocks and voltage, total system power, PSU load, recommended PSU wattage, power drawn from the wall using 80 Plus efficiency curves, and heat lost.
* 🔍 **Hardware inspector.** Reads your GPU name, VRAM size and driver version from Windows, including secondary GPUs on Optimus laptops.
* 🛡️ **Locked-card detection.** Cards known to be non-overclockable (NVS, Quadro NVS, RX Vega 64) lock the input fields and show a clear alert.
* 💡 **Architecture guidance.** Notes for Fermi through Blackwell, RDNA and Intel Arc, plus special notes (for example the RX Vega 56 BIOS flash and its Samsung-memory requirement) and advice to raise clocks in small 10-15 MHz steps.
* 💾 **Presets.** Export and import your overclock settings to a file so you can switch between profiles quickly. A laptop profile is included.
* ⚠️ **Alerts.** Warnings for unrealistic gains, high voltage, PSU load above 80% / 90% / 100%, and laptop thermal limits.

---

## 📥 Download

1. Go to the **[latest release (v2.0.1-beta3)](https://github.com/Xtrizer/G-OC-calculator-tool-for-windows-/releases/tag/v2.0.1-beta3)**.
2. Download **`G-OC-Calculator.beta.3.exe`** (about 18.6 MB).
3. *(Recommended)* [verify the download](#-verify-your-download).
4. Double-click the file. There is nothing to install.

All versions: [Releases page](https://github.com/Xtrizer/G-OC-calculator-tool-for-windows-/releases).

---

## 🖥️ Requirements

| | |
|---|---|
| **Operating system** | Windows 10 or Windows 11, 64-bit |
| **Install** | None. Portable single `.exe`. No Python, no admin rights needed |
| **Internet** | Not required |
| **Graphics driver** | Your GPU vendor's driver with **OpenGL 2.0 or newer**. The generic "Microsoft Basic Display Adapter" driver may fail to start the app |
| **Hardware detection** | Uses built-in Windows PowerShell. If detection fails, you can type every value by hand |
| **Disk space** | About 20 MB |

Tested on 5 different PCs without problems.

---

## 🔐 Verify your download

The executable is not code-signed, so Windows SmartScreen may show "Windows protected your PC". Check that the file is the one published here by comparing its SHA-256 fingerprint.

**`G-OC-Calculator.beta.3.exe`**

```
d6eab0154542987b0369e52d7b8dc31505050790d74290d3da548e6f164d9fbf
```

In PowerShell, run:

```powershell
Get-FileHash .\G-OC-Calculator.beta.3.exe -Algorithm SHA256
```

The hash must match exactly. If it does not, do not run the file. The same value is in [`SHA256SUMS.txt`](SHA256SUMS.txt).

If SmartScreen appears: click **More info**, then **Run anyway**. Antivirus programs sometimes flag single-file apps built with PyInstaller as false positives. If that happens, you can check the file on [VirusTotal](https://www.virustotal.com) before running it.

---

## 🔒 What the app does on your PC

* Runs **two read-only Windows PowerShell queries** (`Get-CimInstance Win32_PnPEntity` and `Win32_VideoController`) to read the GPU name, VRAM size and driver version.
* Contains **no networking code**. It does not connect to the internet or send any data anywhere. You can check this yourself: the full source is in [`main.py`](main.py).
* Does **not** change GPU clocks, voltage, fan speed or BIOS, and does not install drivers or services.
* Writes a file only when you export a preset.

---

## 🧮 How the numbers are calculated

| Result | Formula |
|---|---|
| Memory data rate (Gbps) | memory clock (MHz) × type multiplier ÷ 1000 |
| Memory bandwidth (GB/s) | data rate × bus width (bit) ÷ 8 |
| Compute (TFLOPS) | shader cores × 2 × core clock (MHz) ÷ 1,000,000 |
| GPU power after OC | stock power × (new clock ÷ old clock) × (new voltage ÷ old voltage)² |
| System power | GPU + CPU + 75 W (motherboard, RAM, drives, fans) |
| PSU load | system power ÷ PSU rating. Warnings above 80%, 90% and 100% |
| Recommended PSU | system power ÷ 0.8, rounded up to the next 50 W |
| Wall power | system power ÷ PSU efficiency (80 Plus curve, interpolated by load) |

Memory type multipliers: DDR2 / DDR3 / GDDR3 ×2, GDDR5 ×4, GDDR5X and GDDR6 ×8, GDDR6X ×16, GDDR7 ×32, HBM / HBM2 / HBM3 ×2. Use the memory clock as shown in GPU-Z.

---

## ⚠️ Disclaimer

All figures are **theoretical estimates** based on hardware specifications. Real FPS gains and stability depend on your GPU's silicon quality, cooling and power limits, and are usually lower than the theoretical gain. Always raise clocks in small steps, stress-test each step, and watch temperatures.

Overclocking, raising voltage and flashing a BIOS can damage hardware and void warranties. Use this tool at your own risk. See the [license](LICENSE).

---

## 🛠️ Build from source

The app is a single Python file built with [Kivy](https://kivy.org). It was built with Python 3.12.

```powershell
py -3.12 -m pip install -r requirements.txt pyinstaller
py -3.12 -m PyInstaller --onefile --windowed --name G-OC-Calculator main.py
```

The `.exe` appears in `dist\`. To just run it without building: `py -3.12 main.py`.

> PyInstaller builds are not bit-for-bit reproducible, so an exe you build yourself will have a different SHA-256 from the one published in the releases.

---

## 📄 License

Released under the **MIT License**. See [LICENSE](LICENSE). The released `.exe` also bundles Kivy (MIT), Python (PSF License), SDL2 (zlib) and the PyInstaller bootloader (GPL-2.0 with the bootloader exception).

---

## 💬 Community and feedback

* 📢 **Telegram group:** [Join G-OC Community](https://t.me/+3nGi0kP7A3wyMWI8)
* 📷 **Instagram:** [@xtrizer_ghost](https://instagram.com/xtrizer_ghost)
* 🐞 **Found a bug or have a request?** [Open an issue](https://github.com/Xtrizer/G-OC-calculator-tool-for-windows-/issues). Please include your GPU model, Windows version and a screenshot.
* 🤝 **Pull requests are welcome**, especially for GPU data, architecture notes and bug fixes.
* ⭐ If the tool helped you, a star on this repository helps other people find it.
