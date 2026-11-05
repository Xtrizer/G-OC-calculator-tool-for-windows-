# ⚡ G-OC Calculator — GPU Overclock & Power Estimator with improvements in useing

![Platform](https://img.shields.io/badge/PLATFORM-WINDOWS_10%20%2F%2011-0078D6?style=for-the-badge&logo=windows)
![Release](https://img.shields.io/badge/RELEASE-V2.0.2--BETA4-2EA44F?style=for-the-badge)
![Status](https://img.shields.io/badge/STATUS-IN_DEVELOPMENT-E3B341?style=for-the-badge)
![License](https://img.shields.io/badge/LICENSE-MIT-8957E5?style=for-the-badge)

**Plan a GPU overclock before you touch a single slider.** G-OC Calculator estimates the memory bandwidth and compute gain of an overclock, how much extra power it will draw, whether your power supply can handle it, and whether your CPU and PCIe slot suit the card. It is free, open source, portable, and runs fully offline.

> **It is a calculator, not an overclocking tool.** The app never changes your GPU settings, clocks, voltage or BIOS. "APPLY OC" only runs the calculation.


## 📸 Screenshots

<img width="1281" height="992" alt="Screenshot 2026-11-04 213555" src="https://github.com/user-attachments/assets/d7fa5695-9a3f-4852-a723-d6b0fb12498a" />
<img width="1193" height="975" alt="Screenshot 2026-11-04 213514" src="https://github.com/user-attachments/assets/cc7ecf0b-445c-46e6-9a53-e63c54bedd4b" />
<img width="1251" height="989" alt="Screenshot 2026-11-04 213349" src="https://github.com/user-attachments/assets/ef0feea7-b740-4e6e-a9e3-a318302e56cc" />
<img width="1216" height="976" alt="Screenshot 2026-11-04 213337" src="https://github.com/user-attachments/assets/1e320b7d-47e5-42e7-b751-283eefdc57fe" />
<img width="1207" height="988" alt="Screenshot 2026-11-04 213325" src="https://github.com/user-attachments/assets/33ebd909-36b0-4d00-bf40-95ccbfc2a535" />
<img width="1179" height="972" alt="Screenshot 2026-11-04 213316" src="https://github.com/user-attachments/assets/7afe64ce-8b56-48df-b92d-5f88efd89c4d" />
<img width="1190" height="1003" alt="Screenshot 2026-11-04 213306" src="https://github.com/user-attachments/assets/fc5e0377-c94a-4856-b9df-2454f34477ea" />
<img width="1246" height="991" alt="Screenshot 2026-11-04 213133" src="https://github.com/user-attachments/assets/e680cfb9-5c5d-47e7-9cfa-ef8e31a5fe9e" />
<img width="1315" height="1011" alt="Screenshot 2026-11-04 213041" src="https://github.com/user-attachments/assets/fe6efde7-2018-4ac0-8a32-63f6d48a1247" />
<img width="1238" height="999" alt="Screenshot 2026-11-04 213020" src="https://github.com/user-attachments/assets/ff529817-42a2-4790-a24d-184049e620ea" />
<img width="1310" height="1046" alt="Screenshot 2026-11-04 212901" src="https://github.com/user-attachments/assets/ad57ba86-6993-450e-a146-207fb97fe999" />

The default theme changes its accent color to match your card: **NVIDIA (green)**, **AMD (red)**, **Intel (blue/purple)**. Ten themes are included (see *Themes* below).

## 🔑 Key Features

* 🚀 **Performance estimator.** Stock vs overclock for memory speed (Gbps), memory bandwidth (GB/s) and compute (TFLOPS), shown side by side with bars.
* ⚡ **PSU and power check.** Estimated GPU power at the new clocks and voltage, total system power, PSU load, recommended PSU wattage, power drawn from the wall using 80 Plus efficiency curves, and heat lost.
* 📚 **GPU CATEGORY (new in beta 4).** An offline list of 259 graphics cards (NVIDIA, AMD, Intel) sorted weakest to strongest. Tap a card and the fields fill in. 146 entries are cross-checked against published bandwidth and TFLOPS figures; the others are marked **UNVERIFIED** (community-sourced, compare with GPU-Z).
* 🧩 **COMPATIBILITY (new in beta 4).** Type a CPU (312 desktop models) and a GPU, at stock or overclocked clocks. It shows the PCIe generation and lanes (matched or reduced), the estimated PCIe loss, the estimated CPU bottleneck at 720p / 1080p / 1440p / 4K, GPU-limited headroom, what-if tables and a PSU hint. AGP / PCI / onboard graphics are reported as "does not fit". All of these numbers are **estimates** from a built-in model, not benchmarks.
* 🎨 **Themes (new in beta 4).** Default, Retro Silver, Windows XP, Windows 98, MSI, ASUS, Aero, Glass, White and Core Extreme. Use the small THEMES button in the top right corner.
* 🔍 **Hardware inspector.** Reads your GPU name, VRAM size and driver version from Windows, including secondary GPUs on Optimus laptops.
* 🛡️ **Locked-card detection.** Cards known to be non-overclockable (NVS, Quadro NVS, RX Vega 64) lock the input fields and show a clear alert.
* 💡 **Architecture guidance.** Notes for Fermi through Blackwell, RDNA and Intel Arc, plus special notes (for example the RX Vega 56 BIOS flash and its Samsung-memory requirement) and advice to raise clocks in small 10-15 MHz steps.
* 💾 **Presets.** Export and import your overclock settings to a file so you can switch between profiles quickly. A laptop profile is included.
* ⚠️ **Alerts.** Warnings for unrealistic gains, high voltage, PSU load above 80% / 90% / 100%, and laptop thermal limits.


## 📥 Download

1. Go to the **[latest release (v2.0.2-beta4)](https://github.com/Xtrizer/G-OC-calculator-tool-for-windows-/releases/tag/v2.0.2-beta4)**.
2. Download **`G-OC-calculator.exe`**.
3. *(Recommended)* [verify the download](#-verify-your-download).
4. Double-click the file. There is nothing to install.

All versions: [Releases page](https://github.com/Xtrizer/G-OC-calculator-tool-for-windows-/releases).


## 🖥️ Requirements

| | |
|---|---|
| **Operating system** | Windows 10 or Windows 11, 64-bit |
| **Install** | None. Portable single `.exe`. No Python, no admin rights needed |
| **Internet** | Not required |
| **Graphics driver** | Your GPU vendor's driver with **OpenGL 2.0 or newer**. The generic "Microsoft Basic Display Adapter" driver may fail to start the app |
| **Hardware detection** | Uses built-in Windows PowerShell. If detection fails, you can type every value by hand |
| **Disk space** | About 20 MB |

Beta 3 was tested on 5 different PCs. Beta 4 is a beta: please report any problem you find.


## 🔐 Verify your download

The executable is not code-signed, so Windows SmartScreen may show "Windows protected your PC". Check that the file is the one published here by comparing its SHA-256 fingerprint.

**`G-OC-calculator.exe`**

```
3dfc7cc71459be1e6cc7a002f80b4193a2bfa36100b6b754e5dfddcb582202f2
```

In PowerShell, run:

```powershell
Get-FileHash .\G-OC-calculator.exe -Algorithm SHA256
```

The hash must match exactly. If it does not, do not run the file. The same value is in [`SHA256SUMS.txt`](SHA256SUMS.txt).

If SmartScreen appears: click **More info**, then **Run anyway**. Antivirus programs sometimes flag single-file apps built with PyInstaller as false positives. If that happens, you can check the file on [VirusTotal](https://www.virustotal.com) before running it.


## 🔒 What the app does on your PC

* Runs **two read-only Windows PowerShell queries** (`Get-CimInstance Win32_PnPEntity` and `Win32_VideoController`) to read the GPU name, VRAM size and driver version.
* Contains **no networking code**. It does not connect to the internet or send any data anywhere. You can check this yourself: the full source is in [`main.py`](main.py).
* Does **not** change GPU clocks, voltage, fan speed or BIOS, and does not install drivers or services.
* Writes files only when you export a preset, press SAVE CONFIG, or change the theme (small `.json` files next to the program).

## 🧩 About the COMPATIBILITY estimates

CPU and GPU strength are rough gaming indexes (GTX 1060 6GB = 100) used only to compare parts, PCIe loss is a heuristic based on link bandwidth, card design (x4 / x8 / x16) and VRAM size, and overclock gains use simple scaling factors. They are **not benchmarks**. Real results depend on the game, RAM, BIOS, drivers and cooling.


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

Memory type multipliers: SDR ×1, DDR1 / DDR2 / DDR3 / DDR4 / GDDR2 / GDDR3 / GDDR4 ×2, GDDR5 ×4, GDDR5X and GDDR6 ×8, GDDR6X ×16, GDDR7 ×16, HBM / HBM2 / HBM3 ×2. Use the memory clock as shown in GPU-Z.


## ⚠️ Disclaimer

All figures are **theoretical estimates** based on hardware specifications. Real FPS gains and stability depend on your GPU's silicon quality, cooling and power limits, and are usually lower than the theoretical gain. Always raise clocks in small steps, stress-test each step, and watch temperatures.

Overclocking, raising voltage and flashing a BIOS can damage hardware and void warranties. Use this tool at your own risk. See the [license](LICENSE).


## 🛠️ Build from source

The app is a single Python file built with [Kivy](https://kivy.org). It was built with Python 3.12.

```powershell
py -3.12 -m pip install -r requirements.txt pyinstaller
py -3.12 -m PyInstaller --onefile --windowed --name G-OC-calculator main.py
```

The `.exe` appears in `dist\`. To just run it without building: `py -3.12 main.py`.

> PyInstaller builds are not bit-for-bit reproducible, so an exe you build yourself will have a different SHA-256 from the one published in the releases.


## 📄 License

Released under the **MIT License**. See [LICENSE](LICENSE). The released `.exe` also bundles Kivy (MIT), Python (PSF License), SDL2 (zlib) and the PyInstaller bootloader (GPL-2.0 with the bootloader exception).


## 💬 Community and feedback

* 📢 **Telegram group:** [Join G-OC Community](https://t.me/+3nGi0kP7A3wyMWI8)
* 📷 **Instagram:** [@xtrizer_ghost](https://instagram.com/xtrizer_ghost)
* 🐞 **Found a bug or have a request?** [Open an issue](https://github.com/Xtrizer/G-OC-calculator-tool-for-windows-/issues). Please include your GPU model, Windows version and a screenshot.
* 🤝 **Pull requests are welcome**, especially for GPU data, architecture notes and bug fixes.
* ⭐ If the tool helped you, a star on this repository helps other people find it.
