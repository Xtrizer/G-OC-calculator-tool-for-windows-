"""OC//CALC v2.0.2-beta4 - Extreme Overclock & Experiment Suite (built-in offline GPU list)."""
import math
import json
import re
import threading
import os
import subprocess
import platform

from kivy.app import App
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.graphics import Color, Ellipse, Line, Rectangle, Triangle
from kivy.metrics import dp, sp
from kivy.resources import resource_find
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import NumericProperty

# ---- built-in list (gpu_db.py, generated) ----
GPUS = [
    {'vendor': 'NVIDIA', 'name': 'NVIDIA RIVA TNT2 M64', 'arch': 'Celsius', 'year': 1999, 'mem': 'SDR', 'vram': 0.032, 'bus': 64, 'mem_clock': 140, 'core_clock': 125, 'cores': 2, 'power': 12, 'perf': 0.4, 'tier': 'unverified', 'legacy': True, 'pcie_gen': None, 'pcie_lanes': None},
    {'vendor': 'Intel', 'name': 'Intel Extreme Graphics (865G)', 'arch': 'Intel GMA', 'year': 2003, 'mem': 'DDR1', 'vram': 0.096, 'bus': 64, 'mem_clock': 200, 'core_clock': 200, 'cores': 2, 'power': 15, 'perf': 0.5, 'tier': 'unverified', 'legacy': True, 'pcie_gen': None, 'pcie_lanes': None},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce 2 GTS', 'arch': 'Celsius', 'year': 2000, 'mem': 'DDR1', 'vram': 0.032, 'bus': 128, 'mem_clock': 166, 'core_clock': 200, 'cores': 4, 'power': 15, 'perf': 0.6, 'tier': 'unverified', 'legacy': True, 'pcie_gen': None, 'pcie_lanes': None},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce 2 MX 200', 'arch': 'Celsius', 'year': 2001, 'mem': 'DDR1', 'vram': 0.064, 'bus': 64, 'mem_clock': 166, 'core_clock': 175, 'cores': 2, 'power': 15, 'perf': 0.6, 'tier': 'unverified', 'legacy': True, 'pcie_gen': None, 'pcie_lanes': None},
    {'vendor': 'AMD', 'name': 'ATI Radeon 7000', 'arch': 'Rage / R100', 'year': 2001, 'mem': 'DDR1', 'vram': 0.064, 'bus': 64, 'mem_clock': 150, 'core_clock': 150, 'cores': 1, 'power': 15, 'perf': 0.7, 'tier': 'unverified', 'legacy': True, 'pcie_gen': None, 'pcie_lanes': None},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce 2 MX 400', 'arch': 'Celsius', 'year': 2001, 'mem': 'DDR1', 'vram': 0.064, 'bus': 128, 'mem_clock': 183, 'core_clock': 200, 'cores': 2, 'power': 18, 'perf': 0.8, 'tier': 'unverified', 'legacy': True, 'pcie_gen': None, 'pcie_lanes': None},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce 2 Ultra', 'arch': 'Celsius', 'year': 2000, 'mem': 'DDR1', 'vram': 0.064, 'bus': 128, 'mem_clock': 230, 'core_clock': 250, 'cores': 4, 'power': 20, 'perf': 0.8, 'tier': 'unverified', 'legacy': True, 'pcie_gen': None, 'pcie_lanes': None},
    {'vendor': 'AMD', 'name': 'ATI Radeon 7500', 'arch': 'Rage / R100', 'year': 2001, 'mem': 'DDR1', 'vram': 0.128, 'bus': 128, 'mem_clock': 230, 'core_clock': 290, 'cores': 2, 'power': 20, 'perf': 0.9, 'tier': 'unverified', 'legacy': True, 'pcie_gen': None, 'pcie_lanes': None},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce 4 MX 440', 'arch': 'Kelvin', 'year': 2002, 'mem': 'DDR1', 'vram': 0.128, 'bus': 128, 'mem_clock': 200, 'core_clock': 270, 'cores': 2, 'power': 22, 'perf': 1.0, 'tier': 'unverified', 'legacy': True, 'pcie_gen': None, 'pcie_lanes': None},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce FX 5200', 'arch': 'Rankine', 'year': 2003, 'mem': 'DDR2', 'vram': 0.128, 'bus': 128, 'mem_clock': 200, 'core_clock': 250, 'cores': 4, 'power': 15, 'perf': 1.0, 'tier': 'unverified', 'legacy': True, 'pcie_gen': None, 'pcie_lanes': None},
    {'vendor': 'AMD', 'name': 'ATI Radeon 8500', 'arch': 'R300 / R400', 'year': 2001, 'mem': 'DDR1', 'vram': 0.128, 'bus': 128, 'mem_clock': 275, 'core_clock': 275, 'cores': 4, 'power': 26, 'perf': 1.1, 'tier': 'unverified', 'legacy': True, 'pcie_gen': None, 'pcie_lanes': None},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce 3', 'arch': 'Kelvin', 'year': 2001, 'mem': 'DDR1', 'vram': 0.064, 'bus': 128, 'mem_clock': 230, 'core_clock': 200, 'cores': 4, 'power': 29, 'perf': 1.2, 'tier': 'unverified', 'legacy': True, 'pcie_gen': None, 'pcie_lanes': None},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce 3 Ti 200', 'arch': 'Kelvin', 'year': 2001, 'mem': 'DDR1', 'vram': 0.064, 'bus': 128, 'mem_clock': 200, 'core_clock': 175, 'cores': 4, 'power': 28, 'perf': 1.2, 'tier': 'unverified', 'legacy': True, 'pcie_gen': None, 'pcie_lanes': None},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce FX 5600 Ultra', 'arch': 'Rankine', 'year': 2003, 'mem': 'DDR1', 'vram': 0.128, 'bus': 128, 'mem_clock': 350, 'core_clock': 350, 'cores': 4, 'power': 30, 'perf': 1.3, 'tier': 'unverified', 'legacy': True, 'pcie_gen': None, 'pcie_lanes': None},
    {'vendor': 'AMD', 'name': 'ATI Radeon 9500 Pro', 'arch': 'R300 / R400', 'year': 2002, 'mem': 'DDR1', 'vram': 0.128, 'bus': 128, 'mem_clock': 275, 'core_clock': 275, 'cores': 4, 'power': 35, 'perf': 1.4, 'tier': 'unverified', 'legacy': True, 'pcie_gen': None, 'pcie_lanes': None},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce 4 Ti 4200', 'arch': 'Kelvin', 'year': 2002, 'mem': 'DDR1', 'vram': 0.128, 'bus': 128, 'mem_clock': 222, 'core_clock': 250, 'cores': 4, 'power': 35, 'perf': 1.4, 'tier': 'unverified', 'legacy': True, 'pcie_gen': None, 'pcie_lanes': None},
    {'vendor': 'Intel', 'name': 'Intel GMA 900 (915G)', 'arch': 'Intel GMA', 'year': 2004, 'mem': 'DDR1', 'vram': 0.128, 'bus': 128, 'mem_clock': 333, 'core_clock': 333, 'cores': 4, 'power': 18, 'perf': 1.5, 'tier': 'unverified', 'legacy': True, 'pcie_gen': None, 'pcie_lanes': None},
    {'vendor': 'Intel', 'name': 'Intel GMA 950 (945G)', 'arch': 'Intel GMA', 'year': 2005, 'mem': 'DDR2', 'vram': 0.224, 'bus': 128, 'mem_clock': 400, 'core_clock': 400, 'cores': 4, 'power': 20, 'perf': 1.6, 'tier': 'unverified', 'legacy': True, 'pcie_gen': None, 'pcie_lanes': None},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce 4 Ti 4600', 'arch': 'Kelvin', 'year': 2002, 'mem': 'DDR1', 'vram': 0.128, 'bus': 128, 'mem_clock': 325, 'core_clock': 300, 'cores': 4, 'power': 38, 'perf': 1.6, 'tier': 'unverified', 'legacy': True, 'pcie_gen': None, 'pcie_lanes': None},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce FX 5700 Ultra', 'arch': 'Rankine', 'year': 2003, 'mem': 'GDDR2', 'vram': 0.128, 'bus': 128, 'mem_clock': 450, 'core_clock': 475, 'cores': 4, 'power': 35, 'perf': 1.7, 'tier': 'unverified', 'legacy': True, 'pcie_gen': None, 'pcie_lanes': None},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce 6200', 'arch': 'Curie', 'year': 2004, 'mem': 'DDR1', 'vram': 0.128, 'bus': 64, 'mem_clock': 266, 'core_clock': 350, 'cores': 4, 'power': 25, 'perf': 1.8, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 1, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce FX 5800 Ultra', 'arch': 'Rankine', 'year': 2003, 'mem': 'GDDR2', 'vram': 0.128, 'bus': 128, 'mem_clock': 500, 'core_clock': 500, 'cores': 4, 'power': 60, 'perf': 1.8, 'tier': 'unverified', 'legacy': True, 'pcie_gen': None, 'pcie_lanes': None},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce 6600', 'arch': 'Curie', 'year': 2004, 'mem': 'DDR1', 'vram': 0.128, 'bus': 128, 'mem_clock': 250, 'core_clock': 300, 'cores': 8, 'power': 35, 'perf': 1.9, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 1, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'ATI Radeon 9700 Pro', 'arch': 'R300 / R400', 'year': 2002, 'mem': 'DDR1', 'vram': 0.128, 'bus': 256, 'mem_clock': 310, 'core_clock': 325, 'cores': 8, 'power': 50, 'perf': 2.0, 'tier': 'unverified', 'legacy': True, 'pcie_gen': None, 'pcie_lanes': None},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce FX 5900 Ultra', 'arch': 'Rankine', 'year': 2003, 'mem': 'DDR1', 'vram': 0.256, 'bus': 256, 'mem_clock': 425, 'core_clock': 450, 'cores': 4, 'power': 55, 'perf': 2.0, 'tier': 'unverified', 'legacy': True, 'pcie_gen': None, 'pcie_lanes': None},
    {'vendor': 'AMD', 'name': 'ATI Radeon 9800 Pro', 'arch': 'R300 / R400', 'year': 2003, 'mem': 'DDR1', 'vram': 0.128, 'bus': 256, 'mem_clock': 340, 'core_clock': 380, 'cores': 8, 'power': 55, 'perf': 2.1, 'tier': 'unverified', 'legacy': True, 'pcie_gen': None, 'pcie_lanes': None},
    {'vendor': 'AMD', 'name': 'ATI Radeon X300', 'arch': 'R300 / R400', 'year': 2004, 'mem': 'DDR1', 'vram': 0.128, 'bus': 64, 'mem_clock': 200, 'core_clock': 325, 'cores': 4, 'power': 25, 'perf': 2.2, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 1, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce 6600 GT', 'arch': 'Curie', 'year': 2004, 'mem': 'GDDR3', 'vram': 0.128, 'bus': 128, 'mem_clock': 500, 'core_clock': 500, 'cores': 8, 'power': 47, 'perf': 2.2, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 1, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'ATI Radeon X600 Pro', 'arch': 'R300 / R400', 'year': 2004, 'mem': 'DDR1', 'vram': 0.128, 'bus': 128, 'mem_clock': 300, 'core_clock': 400, 'cores': 4, 'power': 30, 'perf': 2.3, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 1, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'ATI Radeon X700 Pro', 'arch': 'R300 / R400', 'year': 2004, 'mem': 'GDDR2', 'vram': 0.256, 'bus': 128, 'mem_clock': 430, 'core_clock': 425, 'cores': 8, 'power': 45, 'perf': 2.4, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 1, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce 6800 Ultra', 'arch': 'Curie', 'year': 2004, 'mem': 'GDDR3', 'vram': 0.256, 'bus': 256, 'mem_clock': 550, 'core_clock': 400, 'cores': 16, 'power': 115, 'perf': 2.4, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 1, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce 6800 GT', 'arch': 'Curie', 'year': 2004, 'mem': 'GDDR3', 'vram': 0.256, 'bus': 256, 'mem_clock': 500, 'core_clock': 350, 'cores': 16, 'power': 100, 'perf': 2.5, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 1, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'ATI Radeon X800 Pro', 'arch': 'R300 / R400', 'year': 2004, 'mem': 'GDDR3', 'vram': 0.256, 'bus': 256, 'mem_clock': 450, 'core_clock': 475, 'cores': 12, 'power': 55, 'perf': 2.6, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 1, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'ATI Radeon X800 XT', 'arch': 'R300 / R400', 'year': 2004, 'mem': 'GDDR2', 'vram': 0.256, 'bus': 256, 'mem_clock': 560, 'core_clock': 500, 'cores': 16, 'power': 75, 'perf': 2.6, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 1, 'pcie_lanes': 16},
    {'vendor': 'Intel', 'name': 'Intel GMA X3100 (GM965)', 'arch': 'Intel GMA', 'year': 2007, 'mem': 'DDR2', 'vram': 0.384, 'bus': 128, 'mem_clock': 400, 'core_clock': 500, 'cores': 8, 'power': 15, 'perf': 2.7, 'tier': 'unverified', 'legacy': True, 'pcie_gen': None, 'pcie_lanes': None},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce 7300 GT', 'arch': 'Curie', 'year': 2006, 'mem': 'GDDR2', 'vram': 0.256, 'bus': 128, 'mem_clock': 333, 'core_clock': 350, 'cores': 8, 'power': 30, 'perf': 2.7, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 1, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce 7600 GT', 'arch': 'Curie', 'year': 2006, 'mem': 'GDDR3', 'vram': 0.256, 'bus': 128, 'mem_clock': 700, 'core_clock': 560, 'cores': 12, 'power': 35, 'perf': 2.8, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 1, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'ATI Radeon X1300 Pro', 'arch': 'R500 / TeraScale', 'year': 2005, 'mem': 'DDR2', 'vram': 0.256, 'bus': 128, 'mem_clock': 400, 'core_clock': 600, 'cores': 2, 'power': 31, 'perf': 2.9, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 1, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce 7900 GT', 'arch': 'Curie', 'year': 2006, 'mem': 'GDDR3', 'vram': 0.256, 'bus': 256, 'mem_clock': 660, 'core_clock': 450, 'cores': 24, 'power': 75, 'perf': 2.9, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 1, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'ATI Radeon X1650 Pro', 'arch': 'R500 / TeraScale', 'year': 2006, 'mem': 'GDDR2', 'vram': 0.256, 'bus': 128, 'mem_clock': 690, 'core_clock': 600, 'cores': 12, 'power': 44, 'perf': 3.0, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 1, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'ATI Radeon X1800 XL', 'arch': 'R500 / TeraScale', 'year': 2005, 'mem': 'GDDR3', 'vram': 0.256, 'bus': 256, 'mem_clock': 500, 'core_clock': 500, 'cores': 16, 'power': 75, 'perf': 3.1, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 1, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'ATI Radeon X1950 XTX', 'arch': 'R500 / TeraScale', 'year': 2006, 'mem': 'GDDR4', 'vram': 0.512, 'bus': 256, 'mem_clock': 1000, 'core_clock': 650, 'cores': 48, 'power': 125, 'perf': 3.1, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 1, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce 7800 GTX', 'arch': 'Curie', 'year': 2005, 'mem': 'GDDR3', 'vram': 0.256, 'bus': 256, 'mem_clock': 600, 'core_clock': 430, 'cores': 24, 'power': 110, 'perf': 3.2, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 1, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce 7900 GTX', 'arch': 'Curie', 'year': 2006, 'mem': 'GDDR3', 'vram': 0.512, 'bus': 256, 'mem_clock': 800, 'core_clock': 650, 'cores': 24, 'power': 120, 'perf': 3.3, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 1, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce 8400 GS', 'arch': 'Tesla', 'year': 2007, 'mem': 'DDR2', 'vram': 0.256, 'bus': 64, 'mem_clock': 400, 'core_clock': 520, 'cores': 16, 'power': 25, 'perf': 3.3, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce 8600 GT', 'arch': 'Tesla', 'year': 2007, 'mem': 'GDDR3', 'vram': 0.256, 'bus': 128, 'mem_clock': 700, 'core_clock': 540, 'cores': 32, 'power': 43, 'perf': 3.4, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'ATI Radeon HD 2400 Pro', 'arch': 'R500 / TeraScale', 'year': 2007, 'mem': 'DDR2', 'vram': 0.256, 'bus': 64, 'mem_clock': 400, 'core_clock': 525, 'cores': 40, 'power': 25, 'perf': 3.5, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 1, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'ATI Radeon HD 2600 XT', 'arch': 'R500 / TeraScale', 'year': 2007, 'mem': 'GDDR3', 'vram': 0.256, 'bus': 128, 'mem_clock': 700, 'core_clock': 800, 'cores': 120, 'power': 45, 'perf': 3.5, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 1, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce 8800 GT', 'arch': 'Tesla', 'year': 2007, 'mem': 'GDDR3', 'vram': 0.512, 'bus': 256, 'mem_clock': 900, 'core_clock': 600, 'cores': 112, 'power': 105, 'perf': 3.6, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce 8800 GTS 512', 'arch': 'Tesla', 'year': 2007, 'mem': 'GDDR3', 'vram': 0.512, 'bus': 256, 'mem_clock': 972, 'core_clock': 650, 'cores': 128, 'power': 135, 'perf': 3.7, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce 9600 GT', 'arch': 'Tesla', 'year': 2008, 'mem': 'GDDR3', 'vram': 0.512, 'bus': 256, 'mem_clock': 900, 'core_clock': 650, 'cores': 64, 'power': 95, 'perf': 3.7, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'ATI Radeon HD 3450', 'arch': 'R500 / TeraScale', 'year': 2008, 'mem': 'DDR2', 'vram': 0.256, 'bus': 64, 'mem_clock': 500, 'core_clock': 600, 'cores': 40, 'power': 30, 'perf': 3.8, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'ATI Radeon HD 3850', 'arch': 'R500 / TeraScale', 'year': 2007, 'mem': 'GDDR3', 'vram': 0.512, 'bus': 256, 'mem_clock': 828, 'core_clock': 668, 'cores': 320, 'power': 75, 'perf': 3.9, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'ATI Radeon HD 3870', 'arch': 'R500 / TeraScale', 'year': 2007, 'mem': 'GDDR4', 'vram': 0.512, 'bus': 256, 'mem_clock': 1126, 'core_clock': 775, 'cores': 320, 'power': 106, 'perf': 3.9, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce 9800 GTX', 'arch': 'Tesla', 'year': 2008, 'mem': 'GDDR3', 'vram': 0.512, 'bus': 256, 'mem_clock': 1100, 'core_clock': 675, 'cores': 128, 'power': 140, 'perf': 4.0, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA Quadro 400', 'arch': 'Fermi', 'year': 2011, 'mem': 'DDR3', 'vram': 0.512, 'bus': 64, 'mem_clock': 790, 'core_clock': 450, 'cores': 48, 'power': 32, 'perf': 4, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'ATI Radeon HD 4670', 'arch': 'R500 / TeraScale', 'year': 2008, 'mem': 'GDDR3', 'vram': 0.512, 'bus': 128, 'mem_clock': 1000, 'core_clock': 750, 'cores': 320, 'power': 59, 'perf': 4.1, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'ATI Radeon HD 4830', 'arch': 'R500 / TeraScale', 'year': 2008, 'mem': 'GDDR3', 'vram': 0.512, 'bus': 256, 'mem_clock': 900, 'core_clock': 575, 'cores': 640, 'power': 95, 'perf': 4.1, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'ATI Radeon HD 4850', 'arch': 'R500 / TeraScale', 'year': 2008, 'mem': 'GDDR3', 'vram': 0.512, 'bus': 256, 'mem_clock': 993, 'core_clock': 625, 'cores': 800, 'power': 110, 'perf': 4.2, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'ATI Radeon HD 4870', 'arch': 'R500 / TeraScale', 'year': 2008, 'mem': 'GDDR5', 'vram': 1, 'bus': 256, 'mem_clock': 900, 'core_clock': 750, 'cores': 800, 'power': 150, 'perf': 4.3, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 260', 'arch': 'Tesla', 'year': 2008, 'mem': 'GDDR3', 'vram': 0.896, 'bus': 448, 'mem_clock': 999, 'core_clock': 576, 'cores': 192, 'power': 171, 'perf': 4.3, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 280', 'arch': 'Tesla', 'year': 2008, 'mem': 'GDDR3', 'vram': 1, 'bus': 512, 'mem_clock': 1107, 'core_clock': 602, 'cores': 240, 'power': 236, 'perf': 4.4, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GT 210', 'arch': 'Fermi', 'year': 2009, 'mem': 'DDR3', 'vram': 1, 'bus': 64, 'mem_clock': 500, 'core_clock': 589, 'cores': 16, 'power': 30, 'perf': 4.5, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'ATI Radeon HD 5450', 'arch': 'GCN / TeraScale', 'year': 2010, 'mem': 'DDR3', 'vram': 1, 'bus': 64, 'mem_clock': 500, 'core_clock': 650, 'cores': 80, 'power': 20, 'perf': 4.6, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GT 520', 'arch': 'Fermi', 'year': 2011, 'mem': 'DDR3', 'vram': 1, 'bus': 64, 'mem_clock': 898, 'core_clock': 810, 'cores': 48, 'power': 29, 'perf': 4.7, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GT 610', 'arch': 'Fermi', 'year': 2012, 'mem': 'DDR3', 'vram': 1, 'bus': 64, 'mem_clock': 900, 'core_clock': 810, 'cores': 48, 'power': 29, 'perf': 4.7, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GT 705', 'arch': 'Fermi', 'year': 2014, 'mem': 'DDR3', 'vram': 1, 'bus': 64, 'mem_clock': 898, 'core_clock': 810, 'cores': 48, 'power': 29, 'perf': 4.8, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GT 620', 'arch': 'Fermi', 'year': 2012, 'mem': 'DDR3', 'vram': 1, 'bus': 64, 'mem_clock': 900, 'core_clock': 700, 'cores': 96, 'power': 30, 'perf': 4.9, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GT 710', 'arch': 'Kepler', 'year': 2014, 'mem': 'DDR3', 'vram': 1, 'bus': 64, 'mem_clock': 900, 'core_clock': 954, 'cores': 192, 'power': 19, 'perf': 5, 'tier': 'checked', 'legacy': False, 'pcie_gen': 2, 'pcie_lanes': 8},
    {'vendor': 'AMD', 'name': 'AMD Radeon R5 240', 'arch': 'GCN / TeraScale', 'year': 2013, 'mem': 'DDR3', 'vram': 1, 'bus': 64, 'mem_clock': 900, 'core_clock': 730, 'cores': 320, 'power': 30, 'perf': 5.3, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GT 720', 'arch': 'Kepler', 'year': 2014, 'mem': 'DDR3', 'vram': 2, 'bus': 64, 'mem_clock': 900, 'core_clock': 797, 'cores': 192, 'power': 19, 'perf': 5.7, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 2, 'pcie_lanes': 8},
    {'vendor': 'AMD', 'name': 'AMD Radeon R5 340X', 'arch': 'GCN / TeraScale', 'year': 2015, 'mem': 'DDR3', 'vram': 2, 'bus': 64, 'mem_clock': 900, 'core_clock': 825, 'cores': 320, 'power': 30, 'perf': 6.0, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GT 630 OEM', 'arch': 'Fermi', 'year': 2012, 'mem': 'GDDR5', 'vram': 1, 'bus': 128, 'mem_clock': 800, 'core_clock': 810, 'cores': 96, 'power': 65, 'perf': 6.3, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GT 730 (DDR3, 64-bit)', 'arch': 'Kepler', 'year': 2014, 'mem': 'DDR3', 'vram': 2, 'bus': 64, 'mem_clock': 900, 'core_clock': 902, 'cores': 384, 'power': 38, 'perf': 7, 'tier': 'checked', 'legacy': False, 'pcie_gen': 2, 'pcie_lanes': 8},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA Quadro 600', 'arch': 'Fermi', 'year': 2010, 'mem': 'DDR3', 'vram': 1, 'bus': 128, 'mem_clock': 800, 'core_clock': 640, 'cores': 96, 'power': 40, 'perf': 7, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GT 630', 'arch': 'Kepler', 'year': 2012, 'mem': 'DDR3', 'vram': 2, 'bus': 128, 'mem_clock': 900, 'core_clock': 875, 'cores': 384, 'power': 50, 'perf': 8, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GT 640', 'arch': 'Kepler', 'year': 2012, 'mem': 'GDDR3', 'vram': 2, 'bus': 128, 'mem_clock': 891, 'core_clock': 900, 'cores': 384, 'power': 65, 'perf': 11, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon R7 430', 'arch': 'GCN / TeraScale', 'year': 2016, 'mem': 'GDDR5', 'vram': 2, 'bus': 64, 'mem_clock': 1100, 'core_clock': 780, 'cores': 384, 'power': 50, 'perf': 12, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA Quadro 2000', 'arch': 'Fermi', 'year': 2010, 'mem': 'GDDR5', 'vram': 1, 'bus': 128, 'mem_clock': 1300, 'core_clock': 625, 'cores': 192, 'power': 62, 'perf': 14, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon HD 6670', 'arch': 'GCN / TeraScale', 'year': 2011, 'mem': 'GDDR5', 'vram': 1, 'bus': 128, 'mem_clock': 1000, 'core_clock': 800, 'cores': 480, 'power': 66, 'perf': 15, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA Quadro P400', 'arch': 'Pascal', 'year': 2017, 'mem': 'GDDR5', 'vram': 2, 'bus': 64, 'mem_clock': 1500, 'core_clock': 1228, 'cores': 256, 'power': 30, 'perf': 17, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon R7 250', 'arch': 'GCN / TeraScale', 'year': 2013, 'mem': 'GDDR5', 'vram': 1, 'bus': 128, 'mem_clock': 1150, 'core_clock': 1000, 'cores': 384, 'power': 65, 'perf': 18, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 550 Ti', 'arch': 'Fermi', 'year': 2011, 'mem': 'GDDR5', 'vram': 1, 'bus': 192, 'mem_clock': 1026, 'core_clock': 900, 'cores': 192, 'power': 116, 'perf': 18, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon HD 7750', 'arch': 'GCN / TeraScale', 'year': 2012, 'mem': 'GDDR5', 'vram': 1, 'bus': 128, 'mem_clock': 1125, 'core_clock': 800, 'cores': 512, 'power': 55, 'perf': 20, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon R7 450', 'arch': 'GCN / TeraScale', 'year': 2016, 'mem': 'GDDR5', 'vram': 4, 'bus': 128, 'mem_clock': 1125, 'core_clock': 850, 'cores': 384, 'power': 65, 'perf': 22, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GT 1030', 'arch': 'Pascal', 'year': 2017, 'mem': 'GDDR5', 'vram': 2, 'bus': 64, 'mem_clock': 1500, 'core_clock': 1468, 'cores': 384, 'power': 30, 'perf': 22, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 4},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 460 SE', 'arch': 'Fermi', 'year': 2010, 'mem': 'GDDR5', 'vram': 1, 'bus': 256, 'mem_clock': 850, 'core_clock': 650, 'cores': 288, 'power': 150, 'perf': 22, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 650', 'arch': 'Kepler', 'year': 2012, 'mem': 'GDDR5', 'vram': 1, 'bus': 128, 'mem_clock': 1250, 'core_clock': 1058, 'cores': 384, 'power': 64, 'perf': 22, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA Quadro K2000', 'arch': 'Kepler', 'year': 2013, 'mem': 'GDDR5', 'vram': 2, 'bus': 128, 'mem_clock': 1000, 'core_clock': 954, 'cores': 384, 'power': 51, 'perf': 22, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GT 740', 'arch': 'Kepler', 'year': 2014, 'mem': 'GDDR5', 'vram': 2, 'bus': 128, 'mem_clock': 1250, 'core_clock': 993, 'cores': 384, 'power': 64, 'perf': 25, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA Quadro K620', 'arch': 'Maxwell', 'year': 2014, 'mem': 'DDR3', 'vram': 2, 'bus': 128, 'mem_clock': 900, 'core_clock': 954, 'cores': 384, 'power': 45, 'perf': 25, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 460', 'arch': 'Fermi', 'year': 2010, 'mem': 'GDDR5', 'vram': 1, 'bus': 256, 'mem_clock': 900, 'core_clock': 675, 'cores': 336, 'power': 160, 'perf': 26, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 550', 'arch': 'GCN / TeraScale', 'year': 2017, 'mem': 'GDDR5', 'vram': 4, 'bus': 128, 'mem_clock': 1750, 'core_clock': 1183, 'cores': 512, 'power': 50, 'perf': 27, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 8},
    {'vendor': 'AMD', 'name': 'AMD Radeon Pro WX 3100', 'arch': 'GCN / TeraScale', 'year': 2017, 'mem': 'GDDR5', 'vram': 4, 'bus': 128, 'mem_clock': 1500, 'core_clock': 925, 'cores': 512, 'power': 50, 'perf': 28, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'ATI Radeon HD 6850', 'arch': 'GCN / TeraScale', 'year': 2010, 'mem': 'GDDR5', 'vram': 1, 'bus': 256, 'mem_clock': 1000, 'core_clock': 775, 'cores': 960, 'power': 127, 'perf': 29, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon HD 7770', 'arch': 'GCN / TeraScale', 'year': 2012, 'mem': 'GDDR5', 'vram': 1, 'bus': 128, 'mem_clock': 1125, 'core_clock': 1000, 'cores': 640, 'power': 80, 'perf': 30, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA Quadro P600', 'arch': 'Pascal', 'year': 2017, 'mem': 'GDDR5', 'vram': 2, 'bus': 128, 'mem_clock': 1500, 'core_clock': 1506, 'cores': 384, 'power': 40, 'perf': 30, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA Quadro T400', 'arch': 'Turing', 'year': 2021, 'mem': 'GDDR6', 'vram': 4, 'bus': 64, 'mem_clock': 1250, 'core_clock': 420, 'cores': 384, 'power': 30, 'perf': 30, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 650 Ti', 'arch': 'Kepler', 'year': 2012, 'mem': 'GDDR5', 'vram': 1, 'bus': 128, 'mem_clock': 1350, 'core_clock': 928, 'cores': 768, 'power': 110, 'perf': 31, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 750', 'arch': 'Maxwell', 'year': 2014, 'mem': 'GDDR5', 'vram': 1, 'bus': 128, 'mem_clock': 1250, 'core_clock': 1085, 'cores': 512, 'power': 55, 'perf': 32, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'ATI Radeon HD 6870', 'arch': 'GCN / TeraScale', 'year': 2010, 'mem': 'GDDR5', 'vram': 1, 'bus': 256, 'mem_clock': 1050, 'core_clock': 900, 'cores': 1120, 'power': 151, 'perf': 34, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 560 Ti', 'arch': 'Fermi', 'year': 2011, 'mem': 'GDDR5', 'vram': 1, 'bus': 256, 'mem_clock': 1002, 'core_clock': 822, 'cores': 384, 'power': 170, 'perf': 34, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'Intel', 'name': 'Intel Arc A310', 'arch': 'Intel Graphics', 'year': 2022, 'mem': 'GDDR6', 'vram': 4, 'bus': 64, 'mem_clock': 1938, 'core_clock': 2000, 'cores': 768, 'power': 75, 'perf': 35, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 470', 'arch': 'Fermi', 'year': 2010, 'mem': 'GDDR5', 'vram': 1.25, 'bus': 320, 'mem_clock': 837, 'core_clock': 607, 'cores': 448, 'power': 215, 'perf': 35, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon R7 260X', 'arch': 'GCN / TeraScale', 'year': 2013, 'mem': 'GDDR5', 'vram': 2, 'bus': 128, 'mem_clock': 1625, 'core_clock': 1100, 'cores': 896, 'power': 115, 'perf': 36, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon R7 360', 'arch': 'GCN / TeraScale', 'year': 2015, 'mem': 'GDDR5', 'vram': 2, 'bus': 128, 'mem_clock': 1625, 'core_clock': 1050, 'cores': 768, 'power': 85, 'perf': 36.5, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon HD 7790', 'arch': 'GCN / TeraScale', 'year': 2013, 'mem': 'GDDR5', 'vram': 1, 'bus': 128, 'mem_clock': 1500, 'core_clock': 1000, 'cores': 896, 'power': 85, 'perf': 38, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 750 Ti', 'arch': 'Maxwell', 'year': 2014, 'mem': 'GDDR5', 'vram': 2, 'bus': 128, 'mem_clock': 1350, 'core_clock': 1085, 'cores': 640, 'power': 60, 'perf': 38, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA Quadro K4000', 'arch': 'Kepler', 'year': 2013, 'mem': 'GDDR5', 'vram': 3, 'bus': 192, 'mem_clock': 1404, 'core_clock': 810, 'cores': 768, 'power': 80, 'perf': 38, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon HD 6950', 'arch': 'GCN / TeraScale', 'year': 2010, 'mem': 'GDDR5', 'vram': 2, 'bus': 256, 'mem_clock': 1250, 'core_clock': 800, 'cores': 1408, 'power': 200, 'perf': 40, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon HD 7850', 'arch': 'GCN / TeraScale', 'year': 2012, 'mem': 'GDDR5', 'vram': 2, 'bus': 256, 'mem_clock': 1200, 'core_clock': 860, 'cores': 1024, 'power': 130, 'perf': 40, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 6300', 'arch': 'RDNA 1/2/3', 'year': 2023, 'mem': 'GDDR6', 'vram': 2, 'bus': 32, 'mem_clock': 1750, 'core_clock': 1500, 'cores': 384, 'power': 32, 'perf': 40, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 4},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 480', 'arch': 'Fermi', 'year': 2010, 'mem': 'GDDR5', 'vram': 1.5, 'bus': 384, 'mem_clock': 924, 'core_clock': 700, 'cores': 480, 'power': 250, 'perf': 40, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 650 Ti Boost', 'arch': 'Kepler', 'year': 2013, 'mem': 'GDDR5', 'vram': 2, 'bus': 192, 'mem_clock': 1500, 'core_clock': 1033, 'cores': 768, 'power': 134, 'perf': 40, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 570', 'arch': 'Fermi', 'year': 2010, 'mem': 'GDDR5', 'vram': 1.25, 'bus': 320, 'mem_clock': 950, 'core_clock': 732, 'cores': 480, 'power': 219, 'perf': 42, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 460', 'arch': 'GCN / TeraScale', 'year': 2016, 'mem': 'GDDR5', 'vram': 4, 'bus': 128, 'mem_clock': 1750, 'core_clock': 1200, 'cores': 896, 'power': 75, 'perf': 45, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 660', 'arch': 'Kepler', 'year': 2012, 'mem': 'GDDR5', 'vram': 2, 'bus': 192, 'mem_clock': 1500, 'core_clock': 1033, 'cores': 960, 'power': 140, 'perf': 45, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA Quadro P1000', 'arch': 'Pascal', 'year': 2017, 'mem': 'GDDR5', 'vram': 4, 'bus': 128, 'mem_clock': 1502, 'core_clock': 1266, 'cores': 640, 'power': 47, 'perf': 45, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon HD 6970', 'arch': 'GCN / TeraScale', 'year': 2010, 'mem': 'GDDR5', 'vram': 2, 'bus': 256, 'mem_clock': 1375, 'core_clock': 880, 'cores': 1536, 'power': 250, 'perf': 46, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 580', 'arch': 'Fermi', 'year': 2010, 'mem': 'GDDR5', 'vram': 1.5, 'bus': 384, 'mem_clock': 1002, 'core_clock': 772, 'cores': 512, 'power': 244, 'perf': 46, 'tier': 'unverified', 'legacy': True, 'pcie_gen': 2, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon R9 270', 'arch': 'GCN / TeraScale', 'year': 2014, 'mem': 'GDDR5', 'vram': 2, 'bus': 256, 'mem_clock': 1400, 'core_clock': 925, 'cores': 1280, 'power': 150, 'perf': 47, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 1050', 'arch': 'Pascal', 'year': 2016, 'mem': 'GDDR5', 'vram': 2, 'bus': 128, 'mem_clock': 1750, 'core_clock': 1455, 'cores': 640, 'power': 75, 'perf': 48, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon Pro WX 4100', 'arch': 'GCN / TeraScale', 'year': 2016, 'mem': 'GDDR5', 'vram': 4, 'bus': 128, 'mem_clock': 1500, 'core_clock': 1100, 'cores': 1024, 'power': 50, 'perf': 50, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 560', 'arch': 'GCN / TeraScale', 'year': 2017, 'mem': 'GDDR5', 'vram': 4, 'bus': 128, 'mem_clock': 1750, 'core_clock': 1275, 'cores': 1024, 'power': 80, 'perf': 50, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 950', 'arch': 'Maxwell', 'year': 2015, 'mem': 'GDDR5', 'vram': 2, 'bus': 128, 'mem_clock': 1650, 'core_clock': 1188, 'cores': 768, 'power': 90, 'perf': 50, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon HD 7870', 'arch': 'GCN / TeraScale', 'year': 2012, 'mem': 'GDDR5', 'vram': 2, 'bus': 256, 'mem_clock': 1200, 'core_clock': 1000, 'cores': 1280, 'power': 175, 'perf': 52, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 1630', 'arch': 'Turing', 'year': 2022, 'mem': 'GDDR6', 'vram': 4, 'bus': 64, 'mem_clock': 1500, 'core_clock': 1785, 'cores': 512, 'power': 75, 'perf': 52, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 760', 'arch': 'Kepler', 'year': 2013, 'mem': 'GDDR5', 'vram': 2, 'bus': 256, 'mem_clock': 1500, 'core_clock': 1033, 'cores': 1152, 'power': 170, 'perf': 52, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon R9 270X', 'arch': 'GCN / TeraScale', 'year': 2013, 'mem': 'GDDR5', 'vram': 2, 'bus': 256, 'mem_clock': 1400, 'core_clock': 1050, 'cores': 1280, 'power': 180, 'perf': 55, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'Intel', 'name': 'Intel Arc A380', 'arch': 'Intel Graphics', 'year': 2022, 'mem': 'GDDR6', 'vram': 6, 'bus': 96, 'mem_clock': 1938, 'core_clock': 2050, 'cores': 1024, 'power': 75, 'perf': 55, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 8},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 660 Ti', 'arch': 'Kepler', 'year': 2012, 'mem': 'GDDR5', 'vram': 2, 'bus': 192, 'mem_clock': 1500, 'core_clock': 1058, 'cores': 1344, 'power': 150, 'perf': 55, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 1050 Ti', 'arch': 'Pascal', 'year': 2016, 'mem': 'GDDR5', 'vram': 4, 'bus': 128, 'mem_clock': 1750, 'core_clock': 1392, 'cores': 768, 'power': 75, 'perf': 58, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 670', 'arch': 'Kepler', 'year': 2012, 'mem': 'GDDR5', 'vram': 2, 'bus': 256, 'mem_clock': 1500, 'core_clock': 980, 'cores': 1344, 'power': 170, 'perf': 60, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon HD 7950', 'arch': 'GCN / TeraScale', 'year': 2012, 'mem': 'GDDR5', 'vram': 3, 'bus': 384, 'mem_clock': 1250, 'core_clock': 800, 'cores': 1792, 'power': 200, 'perf': 63, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 960', 'arch': 'Maxwell', 'year': 2015, 'mem': 'GDDR5', 'vram': 2, 'bus': 128, 'mem_clock': 1750, 'core_clock': 1178, 'cores': 1024, 'power': 120, 'perf': 63, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon R9 280', 'arch': 'GCN / TeraScale', 'year': 2014, 'mem': 'GDDR5', 'vram': 3, 'bus': 384, 'mem_clock': 1250, 'core_clock': 933, 'cores': 1792, 'power': 250, 'perf': 66, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon R9 380', 'arch': 'GCN / TeraScale', 'year': 2015, 'mem': 'GDDR5', 'vram': 4, 'bus': 256, 'mem_clock': 1425, 'core_clock': 970, 'cores': 1792, 'power': 190, 'perf': 66, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 680', 'arch': 'Kepler', 'year': 2012, 'mem': 'GDDR5', 'vram': 2, 'bus': 256, 'mem_clock': 1500, 'core_clock': 1058, 'cores': 1536, 'power': 195, 'perf': 66, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 6400', 'arch': 'RDNA 1/2/3', 'year': 2022, 'mem': 'GDDR6', 'vram': 4, 'bus': 64, 'mem_clock': 2000, 'core_clock': 2321, 'cores': 768, 'power': 53, 'perf': 68, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 4},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 1650 (GDDR5)', 'arch': 'Turing', 'year': 2019, 'mem': 'GDDR5', 'vram': 4, 'bus': 128, 'mem_clock': 2000, 'core_clock': 1665, 'cores': 896, 'power': 75, 'perf': 70, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 770', 'arch': 'Kepler', 'year': 2013, 'mem': 'GDDR5', 'vram': 2, 'bus': 256, 'mem_clock': 1750, 'core_clock': 1085, 'cores': 1536, 'power': 230, 'perf': 70, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA Quadro P2000', 'arch': 'Pascal', 'year': 2017, 'mem': 'GDDR5', 'vram': 5, 'bus': 160, 'mem_clock': 1753, 'core_clock': 1072, 'cores': 1024, 'power': 75, 'perf': 70, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA Quadro T1000', 'arch': 'Turing', 'year': 2019, 'mem': 'GDDR6', 'vram': 4, 'bus': 128, 'mem_clock': 1250, 'core_clock': 1350, 'cores': 896, 'power': 50, 'perf': 70, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon HD 7970', 'arch': 'GCN / TeraScale', 'year': 2011, 'mem': 'GDDR5', 'vram': 3, 'bus': 384, 'mem_clock': 1375, 'core_clock': 925, 'cores': 2048, 'power': 250, 'perf': 72, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon R9 380X', 'arch': 'GCN / TeraScale', 'year': 2015, 'mem': 'GDDR5', 'vram': 4, 'bus': 256, 'mem_clock': 1425, 'core_clock': 970, 'cores': 2048, 'power': 190, 'perf': 74, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 1650 (GDDR6)', 'arch': 'Turing', 'year': 2020, 'mem': 'GDDR6', 'vram': 4, 'bus': 128, 'mem_clock': 1500, 'core_clock': 1590, 'cores': 896, 'power': 75, 'perf': 74, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon R9 280X', 'arch': 'GCN / TeraScale', 'year': 2013, 'mem': 'GDDR5', 'vram': 3, 'bus': 384, 'mem_clock': 1500, 'core_clock': 1000, 'cores': 2048, 'power': 250, 'perf': 78, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon HD 7970 GHz Edition', 'arch': 'GCN / TeraScale', 'year': 2012, 'mem': 'GDDR5', 'vram': 3, 'bus': 384, 'mem_clock': 1500, 'core_clock': 1050, 'cores': 2048, 'power': 250, 'perf': 80, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 780', 'arch': 'Kepler', 'year': 2013, 'mem': 'GDDR5', 'vram': 3, 'bus': 384, 'mem_clock': 1500, 'core_clock': 900, 'cores': 2304, 'power': 250, 'perf': 83, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX Titan', 'arch': 'Kepler', 'year': 2013, 'mem': 'GDDR5', 'vram': 6, 'bus': 384, 'mem_clock': 1500, 'core_clock': 876, 'cores': 2688, 'power': 250, 'perf': 85, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA Quadro M4000', 'arch': 'Maxwell', 'year': 2015, 'mem': 'GDDR5', 'vram': 8, 'bus': 256, 'mem_clock': 1502, 'core_clock': 773, 'cores': 1664, 'power': 120, 'perf': 85, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 1060 3GB', 'arch': 'Pascal', 'year': 2016, 'mem': 'GDDR5', 'vram': 3, 'bus': 192, 'mem_clock': 2000, 'core_clock': 1708, 'cores': 1152, 'power': 120, 'perf': 90, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 470', 'arch': 'GCN / TeraScale', 'year': 2016, 'mem': 'GDDR5', 'vram': 4, 'bus': 256, 'mem_clock': 1650, 'core_clock': 1206, 'cores': 2048, 'power': 120, 'perf': 91, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon R9 290', 'arch': 'GCN / TeraScale', 'year': 2013, 'mem': 'GDDR5', 'vram': 4, 'bus': 512, 'mem_clock': 1250, 'core_clock': 947, 'cores': 2560, 'power': 250, 'perf': 93, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 570', 'arch': 'GCN / TeraScale', 'year': 2017, 'mem': 'GDDR5', 'vram': 4, 'bus': 256, 'mem_clock': 1750, 'core_clock': 1244, 'cores': 2048, 'power': 150, 'perf': 94, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 6500 XT', 'arch': 'RDNA 1/2/3', 'year': 2022, 'mem': 'GDDR6', 'vram': 4, 'bus': 64, 'mem_clock': 2250, 'core_clock': 2815, 'cores': 1024, 'power': 107, 'perf': 95, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 4},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 780 Ti', 'arch': 'Kepler', 'year': 2013, 'mem': 'GDDR5', 'vram': 3, 'bus': 384, 'mem_clock': 1750, 'core_clock': 928, 'cores': 2880, 'power': 250, 'perf': 95, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 970', 'arch': 'Maxwell', 'year': 2014, 'mem': 'GDDR5', 'vram': 4, 'bus': 256, 'mem_clock': 1750, 'core_clock': 1178, 'cores': 1664, 'power': 145, 'perf': 95, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX Titan Black', 'arch': 'Kepler', 'year': 2014, 'mem': 'GDDR5', 'vram': 6, 'bus': 384, 'mem_clock': 1750, 'core_clock': 980, 'cores': 2880, 'power': 250, 'perf': 97, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon R9 290X', 'arch': 'GCN / TeraScale', 'year': 2013, 'mem': 'GDDR5', 'vram': 4, 'bus': 512, 'mem_clock': 1250, 'core_clock': 1000, 'cores': 2816, 'power': 290, 'perf': 98, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 480 (8GB)', 'arch': 'GCN / TeraScale', 'year': 2016, 'mem': 'GDDR5', 'vram': 8, 'bus': 256, 'mem_clock': 2000, 'core_clock': 1266, 'cores': 2304, 'power': 150, 'perf': 99, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 1060 6GB', 'arch': 'Pascal', 'year': 2016, 'mem': 'GDDR5', 'vram': 6, 'bus': 192, 'mem_clock': 2000, 'core_clock': 1708, 'cores': 1280, 'power': 120, 'perf': 100, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 1650 Super', 'arch': 'Turing', 'year': 2019, 'mem': 'GDDR6', 'vram': 4, 'bus': 128, 'mem_clock': 1500, 'core_clock': 1725, 'cores': 1280, 'power': 100, 'perf': 103, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 580', 'arch': 'GCN / TeraScale', 'year': 2017, 'mem': 'GDDR5', 'vram': 8, 'bus': 256, 'mem_clock': 2000, 'core_clock': 1340, 'cores': 2304, 'power': 185, 'perf': 104, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 3050 (6GB)', 'arch': 'Ampere', 'year': 2024, 'mem': 'GDDR6', 'vram': 6, 'bus': 96, 'mem_clock': 1500, 'core_clock': 1470, 'cores': 2304, 'power': 70, 'perf': 105, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 980', 'arch': 'Maxwell', 'year': 2014, 'mem': 'GDDR5', 'vram': 4, 'bus': 256, 'mem_clock': 1750, 'core_clock': 1216, 'cores': 2048, 'power': 165, 'perf': 106, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon R9 390', 'arch': 'GCN / TeraScale', 'year': 2015, 'mem': 'GDDR5', 'vram': 8, 'bus': 512, 'mem_clock': 1500, 'core_clock': 1000, 'cores': 2560, 'power': 275, 'perf': 108, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 5500 XT (8GB)', 'arch': 'RDNA 1/2/3', 'year': 2019, 'mem': 'GDDR6', 'vram': 8, 'bus': 128, 'mem_clock': 1750, 'core_clock': 1845, 'cores': 1408, 'power': 130, 'perf': 112, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 8},
    {'vendor': 'AMD', 'name': 'AMD Radeon R9 390X', 'arch': 'GCN / TeraScale', 'year': 2015, 'mem': 'GDDR5', 'vram': 8, 'bus': 512, 'mem_clock': 1500, 'core_clock': 1050, 'cores': 2816, 'power': 275, 'perf': 113, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 590', 'arch': 'GCN / TeraScale', 'year': 2018, 'mem': 'GDDR5', 'vram': 8, 'bus': 256, 'mem_clock': 2000, 'core_clock': 1545, 'cores': 2304, 'power': 225, 'perf': 114, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 1660', 'arch': 'Turing', 'year': 2019, 'mem': 'GDDR5', 'vram': 6, 'bus': 192, 'mem_clock': 2000, 'core_clock': 1785, 'cores': 1408, 'power': 120, 'perf': 115, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon R9 Nano', 'arch': 'GCN / TeraScale', 'year': 2015, 'mem': 'HBM', 'vram': 4, 'bus': 4096, 'mem_clock': 500, 'core_clock': 1000, 'cores': 4096, 'power': 175, 'perf': 118, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon R9 Fury', 'arch': 'GCN / TeraScale', 'year': 2015, 'mem': 'HBM', 'vram': 4, 'bus': 4096, 'mem_clock': 500, 'core_clock': 1000, 'cores': 3584, 'power': 275, 'perf': 120, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 1660 Super', 'arch': 'Turing', 'year': 2019, 'mem': 'GDDR6', 'vram': 6, 'bus': 192, 'mem_clock': 1750, 'core_clock': 1785, 'cores': 1408, 'power': 125, 'perf': 126, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 1660 Ti', 'arch': 'Turing', 'year': 2019, 'mem': 'GDDR6', 'vram': 6, 'bus': 192, 'mem_clock': 1500, 'core_clock': 1770, 'cores': 1536, 'power': 120, 'perf': 128, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon R9 Fury X', 'arch': 'GCN / TeraScale', 'year': 2015, 'mem': 'HBM', 'vram': 4, 'bus': 4096, 'mem_clock': 500, 'core_clock': 1050, 'cores': 4096, 'power': 275, 'perf': 130, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 3050 (8GB)', 'arch': 'Ampere', 'year': 2022, 'mem': 'GDDR6', 'vram': 8, 'bus': 128, 'mem_clock': 1750, 'core_clock': 1777, 'cores': 2560, 'power': 130, 'perf': 130, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 1070', 'arch': 'Pascal', 'year': 2016, 'mem': 'GDDR5', 'vram': 8, 'bus': 256, 'mem_clock': 2000, 'core_clock': 1683, 'cores': 1920, 'power': 150, 'perf': 135, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 980 Ti', 'arch': 'Maxwell', 'year': 2015, 'mem': 'GDDR5', 'vram': 6, 'bus': 384, 'mem_clock': 1750, 'core_clock': 1075, 'cores': 2816, 'power': 250, 'perf': 135, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 5600 XT', 'arch': 'RDNA 1/2/3', 'year': 2020, 'mem': 'GDDR6', 'vram': 6, 'bus': 192, 'mem_clock': 1500, 'core_clock': 1560, 'cores': 2304, 'power': 150, 'perf': 140, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX Vega 56', 'arch': 'GCN / TeraScale', 'year': 2017, 'mem': 'HBM2', 'vram': 8, 'bus': 2048, 'mem_clock': 800, 'core_clock': 1471, 'cores': 3584, 'power': 210, 'perf': 140, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'Intel', 'name': 'Intel Arc A580', 'arch': 'Intel Graphics', 'year': 2023, 'mem': 'GDDR6', 'vram': 8, 'bus': 256, 'mem_clock': 2000, 'core_clock': 1700, 'cores': 3072, 'power': 175, 'perf': 140, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX Titan X (Maxwell)', 'arch': 'Maxwell', 'year': 2015, 'mem': 'GDDR5', 'vram': 12, 'bus': 384, 'mem_clock': 1750, 'core_clock': 1075, 'cores': 3072, 'power': 250, 'perf': 140, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 2060', 'arch': 'Turing', 'year': 2019, 'mem': 'GDDR6', 'vram': 6, 'bus': 192, 'mem_clock': 1750, 'core_clock': 1680, 'cores': 1920, 'power': 160, 'perf': 140, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 7600S', 'arch': 'RDNA 1/2/3', 'year': 2023, 'mem': 'GDDR6', 'vram': 8, 'bus': 128, 'mem_clock': 2000, 'core_clock': 1500, 'cores': 1792, 'power': 75, 'perf': 150, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 8},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 1070 Ti', 'arch': 'Pascal', 'year': 2017, 'mem': 'GDDR5', 'vram': 8, 'bus': 256, 'mem_clock': 2000, 'core_clock': 1683, 'cores': 2432, 'power': 180, 'perf': 158, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 2060 Super', 'arch': 'Turing', 'year': 2019, 'mem': 'GDDR6', 'vram': 8, 'bus': 256, 'mem_clock': 1750, 'core_clock': 1650, 'cores': 2176, 'power': 175, 'perf': 160, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 5700', 'arch': 'RDNA 1/2/3', 'year': 2019, 'mem': 'GDDR6', 'vram': 8, 'bus': 256, 'mem_clock': 1750, 'core_clock': 1725, 'cores': 2304, 'power': 180, 'perf': 165, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX Vega 64', 'arch': 'GCN / TeraScale', 'year': 2017, 'mem': 'HBM2', 'vram': 8, 'bus': 2048, 'mem_clock': 945, 'core_clock': 1546, 'cores': 4096, 'power': 295, 'perf': 165, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'Intel', 'name': 'Intel Arc A750', 'arch': 'Intel Graphics', 'year': 2022, 'mem': 'GDDR6', 'vram': 8, 'bus': 256, 'mem_clock': 2000, 'core_clock': 2050, 'cores': 3584, 'power': 225, 'perf': 165, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 4050 Laptop', 'arch': 'Ada Lovelace', 'year': 2023, 'mem': 'GDDR6', 'vram': 6, 'bus': 96, 'mem_clock': 2000, 'core_clock': 1605, 'cores': 2560, 'power': 95, 'perf': 165, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 8},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 2070', 'arch': 'Turing', 'year': 2018, 'mem': 'GDDR6', 'vram': 8, 'bus': 256, 'mem_clock': 1750, 'core_clock': 1620, 'cores': 2304, 'power': 175, 'perf': 170, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'Intel', 'name': 'Intel Arc A770 (8GB)', 'arch': 'Intel Graphics', 'year': 2022, 'mem': 'GDDR6', 'vram': 8, 'bus': 256, 'mem_clock': 2000, 'core_clock': 2100, 'cores': 4096, 'power': 225, 'perf': 175, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 1080', 'arch': 'Pascal', 'year': 2016, 'mem': 'GDDR5X', 'vram': 8, 'bus': 256, 'mem_clock': 1250, 'core_clock': 1733, 'cores': 2560, 'power': 180, 'perf': 175, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 5700 XT', 'arch': 'RDNA 1/2/3', 'year': 2019, 'mem': 'GDDR6', 'vram': 8, 'bus': 256, 'mem_clock': 1750, 'core_clock': 1905, 'cores': 2560, 'power': 225, 'perf': 180, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'Intel', 'name': 'Intel Arc A770 (16GB)', 'arch': 'Intel Graphics', 'year': 2022, 'mem': 'GDDR6', 'vram': 16, 'bus': 256, 'mem_clock': 2188, 'core_clock': 2100, 'cores': 4096, 'power': 225, 'perf': 180, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 3060 (12GB)', 'arch': 'Ampere', 'year': 2021, 'mem': 'GDDR6', 'vram': 12, 'bus': 192, 'mem_clock': 1875, 'core_clock': 1777, 'cores': 3584, 'power': 170, 'perf': 180, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 6600', 'arch': 'RDNA 1/2/3', 'year': 2021, 'mem': 'GDDR6', 'vram': 8, 'bus': 128, 'mem_clock': 1750, 'core_clock': 2491, 'cores': 1792, 'power': 132, 'perf': 185, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 8},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 7700S', 'arch': 'RDNA 1/2/3', 'year': 2023, 'mem': 'GDDR6', 'vram': 8, 'bus': 128, 'mem_clock': 2250, 'core_clock': 2200, 'cores': 2048, 'power': 100, 'perf': 190, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 8},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 2070 Super', 'arch': 'Turing', 'year': 2019, 'mem': 'GDDR6', 'vram': 8, 'bus': 256, 'mem_clock': 1750, 'core_clock': 1770, 'cores': 2560, 'power': 215, 'perf': 190, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA Titan X (Pascal)', 'arch': 'Pascal', 'year': 2016, 'mem': 'GDDR5X', 'vram': 12, 'bus': 384, 'mem_clock': 1250, 'core_clock': 1531, 'cores': 3584, 'power': 250, 'perf': 195, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 6600 XT', 'arch': 'RDNA 1/2/3', 'year': 2021, 'mem': 'GDDR6', 'vram': 8, 'bus': 128, 'mem_clock': 2000, 'core_clock': 2589, 'cores': 2048, 'power': 160, 'perf': 200, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 8},
    {'vendor': 'AMD', 'name': 'AMD Radeon VII', 'arch': 'GCN / TeraScale', 'year': 2019, 'mem': 'HBM2', 'vram': 16, 'bus': 4096, 'mem_clock': 1000, 'core_clock': 1750, 'cores': 3840, 'power': 300, 'perf': 200, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'Intel', 'name': 'Intel Arc B570', 'arch': 'Intel Graphics', 'year': 2025, 'mem': 'GDDR6', 'vram': 10, 'bus': 160, 'mem_clock': 2375, 'core_clock': 2500, 'cores': 2304, 'power': 150, 'perf': 200, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 8},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 5050', 'arch': 'Blackwell', 'year': 2025, 'mem': 'GDDR6', 'vram': 8, 'bus': 128, 'mem_clock': 2500, 'core_clock': 2572, 'cores': 2560, 'power': 130, 'perf': 200, 'tier': 'checked', 'legacy': False, 'pcie_gen': 5, 'pcie_lanes': 8},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 7600', 'arch': 'RDNA 1/2/3', 'year': 2023, 'mem': 'GDDR6', 'vram': 8, 'bus': 128, 'mem_clock': 2250, 'core_clock': 2655, 'cores': 2048, 'power': 165, 'perf': 205, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 8},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce GTX 1080 Ti', 'arch': 'Pascal', 'year': 2017, 'mem': 'GDDR5X', 'vram': 11, 'bus': 352, 'mem_clock': 1375, 'core_clock': 1582, 'cores': 3584, 'power': 250, 'perf': 205, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 2080', 'arch': 'Turing', 'year': 2018, 'mem': 'GDDR6', 'vram': 8, 'bus': 256, 'mem_clock': 1750, 'core_clock': 1710, 'cores': 2944, 'power': 215, 'perf': 210, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA Titan Xp', 'arch': 'Pascal', 'year': 2017, 'mem': 'GDDR5X', 'vram': 12, 'bus': 384, 'mem_clock': 1425, 'core_clock': 1582, 'cores': 3840, 'power': 250, 'perf': 210, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 6650 XT', 'arch': 'RDNA 1/2/3', 'year': 2022, 'mem': 'GDDR6', 'vram': 8, 'bus': 128, 'mem_clock': 2188, 'core_clock': 2635, 'cores': 2048, 'power': 180, 'perf': 212, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 8},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 7600 XT', 'arch': 'RDNA 1/2/3', 'year': 2024, 'mem': 'GDDR6', 'vram': 16, 'bus': 128, 'mem_clock': 2250, 'core_clock': 2755, 'cores': 2048, 'power': 190, 'perf': 214, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 8},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 4060', 'arch': 'Ada Lovelace', 'year': 2023, 'mem': 'GDDR6', 'vram': 8, 'bus': 128, 'mem_clock': 2125, 'core_clock': 2460, 'cores': 3072, 'power': 115, 'perf': 215, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 8},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 2080 Super', 'arch': 'Turing', 'year': 2019, 'mem': 'GDDR6', 'vram': 8, 'bus': 256, 'mem_clock': 1938, 'core_clock': 1815, 'cores': 3072, 'power': 250, 'perf': 220, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 6700', 'arch': 'RDNA 1/2/3', 'year': 2023, 'mem': 'GDDR6', 'vram': 10, 'bus': 160, 'mem_clock': 2000, 'core_clock': 2450, 'cores': 2304, 'power': 175, 'perf': 232, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 3060 Ti', 'arch': 'Ampere', 'year': 2020, 'mem': 'GDDR6', 'vram': 8, 'bus': 256, 'mem_clock': 1750, 'core_clock': 1665, 'cores': 4864, 'power': 200, 'perf': 235, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA TITAN V', 'arch': 'Volta', 'year': 2017, 'mem': 'HBM2', 'vram': 12, 'bus': 3072, 'mem_clock': 850, 'core_clock': 1200, 'cores': 5120, 'power': 250, 'perf': 240, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'Intel', 'name': 'Intel Arc B580', 'arch': 'Intel Graphics', 'year': 2024, 'mem': 'GDDR6', 'vram': 12, 'bus': 192, 'mem_clock': 2375, 'core_clock': 2670, 'cores': 2560, 'power': 190, 'perf': 245, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 8},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 6700 XT', 'arch': 'RDNA 1/2/3', 'year': 2021, 'mem': 'GDDR6', 'vram': 12, 'bus': 192, 'mem_clock': 2000, 'core_clock': 2581, 'cores': 2560, 'power': 230, 'perf': 250, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 4070 Laptop', 'arch': 'Ada Lovelace', 'year': 2023, 'mem': 'GDDR6', 'vram': 8, 'bus': 128, 'mem_clock': 2000, 'core_clock': 1605, 'cores': 4608, 'power': 140, 'perf': 250, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 8},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 5060', 'arch': 'Blackwell', 'year': 2025, 'mem': 'GDDR7', 'vram': 8, 'bus': 128, 'mem_clock': 1750, 'core_clock': 2497, 'cores': 3840, 'power': 145, 'perf': 255, 'tier': 'checked', 'legacy': False, 'pcie_gen': 5, 'pcie_lanes': 8},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 3070', 'arch': 'Ampere', 'year': 2020, 'mem': 'GDDR6', 'vram': 8, 'bus': 256, 'mem_clock': 1750, 'core_clock': 1725, 'cores': 5888, 'power': 220, 'perf': 260, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 4060 Ti (8GB)', 'arch': 'Ada Lovelace', 'year': 2023, 'mem': 'GDDR6', 'vram': 8, 'bus': 128, 'mem_clock': 2250, 'core_clock': 2535, 'cores': 4352, 'power': 160, 'perf': 260, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 8},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 6750 XT', 'arch': 'RDNA 1/2/3', 'year': 2022, 'mem': 'GDDR6', 'vram': 12, 'bus': 192, 'mem_clock': 2250, 'core_clock': 2600, 'cores': 2560, 'power': 250, 'perf': 262, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 4060 Ti (16GB)', 'arch': 'Ada Lovelace', 'year': 2023, 'mem': 'GDDR6', 'vram': 16, 'bus': 128, 'mem_clock': 2250, 'core_clock': 2535, 'cores': 4352, 'power': 165, 'perf': 262, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 8},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 2080 Ti', 'arch': 'Turing', 'year': 2018, 'mem': 'GDDR6', 'vram': 11, 'bus': 352, 'mem_clock': 1750, 'core_clock': 1545, 'cores': 4352, 'power': 250, 'perf': 270, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 3070 Ti', 'arch': 'Ampere', 'year': 2021, 'mem': 'GDDR6X', 'vram': 8, 'bus': 256, 'mem_clock': 1188, 'core_clock': 1770, 'cores': 6144, 'power': 290, 'perf': 280, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA Titan RTX', 'arch': 'Turing', 'year': 2018, 'mem': 'GDDR6', 'vram': 24, 'bus': 384, 'mem_clock': 1750, 'core_clock': 1770, 'cores': 4608, 'power': 280, 'perf': 285, 'tier': 'checked', 'legacy': False, 'pcie_gen': 3, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 7700 XT', 'arch': 'RDNA 1/2/3', 'year': 2023, 'mem': 'GDDR6', 'vram': 12, 'bus': 192, 'mem_clock': 2250, 'core_clock': 2544, 'cores': 3456, 'power': 245, 'perf': 295, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 5060 Ti (8GB)', 'arch': 'Blackwell', 'year': 2025, 'mem': 'GDDR7', 'vram': 8, 'bus': 128, 'mem_clock': 1750, 'core_clock': 2572, 'cores': 4608, 'power': 180, 'perf': 295, 'tier': 'checked', 'legacy': False, 'pcie_gen': 5, 'pcie_lanes': 8},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 5060 Ti (16GB)', 'arch': 'Blackwell', 'year': 2025, 'mem': 'GDDR7', 'vram': 16, 'bus': 128, 'mem_clock': 1750, 'core_clock': 2572, 'cores': 4608, 'power': 180, 'perf': 297, 'tier': 'checked', 'legacy': False, 'pcie_gen': 5, 'pcie_lanes': 8},
    {'vendor': 'AMD', 'name': 'AMD Radeon Pro W6800', 'arch': 'RDNA 1/2/3', 'year': 2021, 'mem': 'GDDR6', 'vram': 32, 'bus': 256, 'mem_clock': 2000, 'core_clock': 2000, 'cores': 3840, 'power': 250, 'perf': 300, 'tier': 'unverified', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 9060 XT (8GB)', 'arch': 'RDNA 4', 'year': 2025, 'mem': 'GDDR6', 'vram': 8, 'bus': 128, 'mem_clock': 2500, 'core_clock': 3130, 'cores': 2048, 'power': 150, 'perf': 300, 'tier': 'checked', 'legacy': False, 'pcie_gen': 5, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 9060 XT (16GB)', 'arch': 'RDNA 4', 'year': 2025, 'mem': 'GDDR6', 'vram': 16, 'bus': 128, 'mem_clock': 2500, 'core_clock': 3130, 'cores': 2048, 'power': 160, 'perf': 302, 'tier': 'checked', 'legacy': False, 'pcie_gen': 5, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 6800', 'arch': 'RDNA 1/2/3', 'year': 2020, 'mem': 'GDDR6', 'vram': 16, 'bus': 256, 'mem_clock': 2000, 'core_clock': 2105, 'cores': 3840, 'power': 250, 'perf': 305, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 4070', 'arch': 'Ada Lovelace', 'year': 2023, 'mem': 'GDDR6X', 'vram': 12, 'bus': 192, 'mem_clock': 1312, 'core_clock': 2475, 'cores': 5888, 'power': 200, 'perf': 325, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 6800 XT', 'arch': 'RDNA 1/2/3', 'year': 2020, 'mem': 'GDDR6', 'vram': 16, 'bus': 256, 'mem_clock': 2000, 'core_clock': 2250, 'cores': 4608, 'power': 300, 'perf': 335, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 3080 (10GB)', 'arch': 'Ampere', 'year': 2020, 'mem': 'GDDR6X', 'vram': 10, 'bus': 320, 'mem_clock': 1188, 'core_clock': 1710, 'cores': 8704, 'power': 320, 'perf': 335, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 7800 XT', 'arch': 'RDNA 1/2/3', 'year': 2023, 'mem': 'GDDR6', 'vram': 16, 'bus': 256, 'mem_clock': 2438, 'core_clock': 2430, 'cores': 3840, 'power': 263, 'perf': 340, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 3080 (12GB)', 'arch': 'Ampere', 'year': 2022, 'mem': 'GDDR6X', 'vram': 12, 'bus': 384, 'mem_clock': 1188, 'core_clock': 1710, 'cores': 8960, 'power': 350, 'perf': 350, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 5070', 'arch': 'Blackwell', 'year': 2025, 'mem': 'GDDR7', 'vram': 12, 'bus': 192, 'mem_clock': 1750, 'core_clock': 2512, 'cores': 6144, 'power': 250, 'perf': 360, 'tier': 'checked', 'legacy': False, 'pcie_gen': 5, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 6900 XT', 'arch': 'RDNA 1/2/3', 'year': 2020, 'mem': 'GDDR6', 'vram': 16, 'bus': 256, 'mem_clock': 2000, 'core_clock': 2250, 'cores': 5120, 'power': 300, 'perf': 375, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 3080 Ti', 'arch': 'Ampere', 'year': 2021, 'mem': 'GDDR6X', 'vram': 12, 'bus': 384, 'mem_clock': 1188, 'core_clock': 1665, 'cores': 10240, 'power': 350, 'perf': 375, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 4070 Super', 'arch': 'Ada Lovelace', 'year': 2024, 'mem': 'GDDR6X', 'vram': 12, 'bus': 192, 'mem_clock': 1312, 'core_clock': 2475, 'cores': 7168, 'power': 220, 'perf': 375, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 7900 GRE', 'arch': 'RDNA 1/2/3', 'year': 2024, 'mem': 'GDDR6', 'vram': 16, 'bus': 256, 'mem_clock': 2250, 'core_clock': 2245, 'cores': 5120, 'power': 260, 'perf': 380, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 3090', 'arch': 'Ampere', 'year': 2020, 'mem': 'GDDR6X', 'vram': 24, 'bus': 384, 'mem_clock': 1219, 'core_clock': 1695, 'cores': 10496, 'power': 350, 'perf': 385, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 4070 Ti', 'arch': 'Ada Lovelace', 'year': 2023, 'mem': 'GDDR6X', 'vram': 12, 'bus': 192, 'mem_clock': 1312, 'core_clock': 2610, 'cores': 7680, 'power': 285, 'perf': 395, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 6950 XT', 'arch': 'RDNA 1/2/3', 'year': 2022, 'mem': 'GDDR6', 'vram': 16, 'bus': 256, 'mem_clock': 2250, 'core_clock': 2310, 'cores': 5120, 'power': 335, 'perf': 400, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 3090 Ti', 'arch': 'Ampere', 'year': 2022, 'mem': 'GDDR6X', 'vram': 24, 'bus': 384, 'mem_clock': 1312, 'core_clock': 1860, 'cores': 10752, 'power': 450, 'perf': 415, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 7900 XT', 'arch': 'RDNA 1/2/3', 'year': 2022, 'mem': 'GDDR6', 'vram': 20, 'bus': 320, 'mem_clock': 2500, 'core_clock': 2400, 'cores': 5376, 'power': 315, 'perf': 430, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 9070', 'arch': 'RDNA 4', 'year': 2025, 'mem': 'GDDR6', 'vram': 16, 'bus': 256, 'mem_clock': 2500, 'core_clock': 2520, 'cores': 3584, 'power': 220, 'perf': 430, 'tier': 'checked', 'legacy': False, 'pcie_gen': 5, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 4070 Ti Super', 'arch': 'Ada Lovelace', 'year': 2024, 'mem': 'GDDR6X', 'vram': 16, 'bus': 256, 'mem_clock': 1312, 'core_clock': 2610, 'cores': 8448, 'power': 285, 'perf': 440, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 5070 Ti', 'arch': 'Blackwell', 'year': 2025, 'mem': 'GDDR7', 'vram': 16, 'bus': 256, 'mem_clock': 1750, 'core_clock': 2452, 'cores': 8960, 'power': 300, 'perf': 455, 'tier': 'checked', 'legacy': False, 'pcie_gen': 5, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 9070 XT', 'arch': 'RDNA 4', 'year': 2025, 'mem': 'GDDR6', 'vram': 16, 'bus': 256, 'mem_clock': 2500, 'core_clock': 2970, 'cores': 4096, 'power': 304, 'perf': 465, 'tier': 'checked', 'legacy': False, 'pcie_gen': 5, 'pcie_lanes': 16},
    {'vendor': 'AMD', 'name': 'AMD Radeon RX 7900 XTX', 'arch': 'RDNA 1/2/3', 'year': 2022, 'mem': 'GDDR6', 'vram': 24, 'bus': 384, 'mem_clock': 2500, 'core_clock': 2500, 'cores': 6144, 'power': 355, 'perf': 490, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 4080', 'arch': 'Ada Lovelace', 'year': 2022, 'mem': 'GDDR6X', 'vram': 16, 'bus': 256, 'mem_clock': 1400, 'core_clock': 2505, 'cores': 9728, 'power': 320, 'perf': 500, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 4080 Super', 'arch': 'Ada Lovelace', 'year': 2024, 'mem': 'GDDR6X', 'vram': 16, 'bus': 256, 'mem_clock': 1438, 'core_clock': 2550, 'cores': 10240, 'power': 320, 'perf': 510, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 5080', 'arch': 'Blackwell', 'year': 2025, 'mem': 'GDDR7', 'vram': 16, 'bus': 256, 'mem_clock': 1875, 'core_clock': 2617, 'cores': 10752, 'power': 360, 'perf': 570, 'tier': 'checked', 'legacy': False, 'pcie_gen': 5, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 4090', 'arch': 'Ada Lovelace', 'year': 2022, 'mem': 'GDDR6X', 'vram': 24, 'bus': 384, 'mem_clock': 1312, 'core_clock': 2520, 'cores': 16384, 'power': 450, 'perf': 650, 'tier': 'checked', 'legacy': False, 'pcie_gen': 4, 'pcie_lanes': 16},
    {'vendor': 'NVIDIA', 'name': 'NVIDIA GeForce RTX 5090', 'arch': 'Blackwell', 'year': 2025, 'mem': 'GDDR7', 'vram': 32, 'bus': 512, 'mem_clock': 1750, 'core_clock': 2407, 'cores': 21760, 'power': 575, 'perf': 840, 'tier': 'checked', 'legacy': False, 'pcie_gen': 5, 'pcie_lanes': 16},
]

# ---- built-in list (cpu_db.py, generated) ----
CPUS = [
    {'vendor': 'Intel', 'name': 'Intel Core 2 Duo E4300', 'year': 2007, 'cores': 2, 'threads': 2, 'boost': 1.8, 'pcie_gen': 1, 'pcie_lanes': 16, 'tdp': 65, 'perf': 24.3},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Duo E6300', 'year': 2006, 'cores': 2, 'threads': 2, 'boost': 1.86, 'pcie_gen': 1, 'pcie_lanes': 16, 'tdp': 65, 'perf': 25.1},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Duo E4400', 'year': 2007, 'cores': 2, 'threads': 2, 'boost': 2.0, 'pcie_gen': 1, 'pcie_lanes': 16, 'tdp': 65, 'perf': 27.0},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Duo E6320', 'year': 2007, 'cores': 2, 'threads': 2, 'boost': 1.86, 'pcie_gen': 1, 'pcie_lanes': 16, 'tdp': 65, 'perf': 27.7},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Duo E6400', 'year': 2006, 'cores': 2, 'threads': 2, 'boost': 2.13, 'pcie_gen': 1, 'pcie_lanes': 16, 'tdp': 65, 'perf': 28.8},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Duo E4500', 'year': 2007, 'cores': 2, 'threads': 2, 'boost': 2.2, 'pcie_gen': 1, 'pcie_lanes': 16, 'tdp': 65, 'perf': 29.7},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Duo E6420', 'year': 2007, 'cores': 2, 'threads': 2, 'boost': 2.13, 'pcie_gen': 1, 'pcie_lanes': 16, 'tdp': 65, 'perf': 31.7},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Duo E4600', 'year': 2008, 'cores': 2, 'threads': 2, 'boost': 2.4, 'pcie_gen': 1, 'pcie_lanes': 16, 'tdp': 65, 'perf': 32.4},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Duo E6540', 'year': 2007, 'cores': 2, 'threads': 2, 'boost': 2.33, 'pcie_gen': 1, 'pcie_lanes': 16, 'tdp': 65, 'perf': 34.7},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Duo E6550', 'year': 2007, 'cores': 2, 'threads': 2, 'boost': 2.33, 'pcie_gen': 1, 'pcie_lanes': 16, 'tdp': 65, 'perf': 34.7},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Duo E4700', 'year': 2008, 'cores': 2, 'threads': 2, 'boost': 2.6, 'pcie_gen': 1, 'pcie_lanes': 16, 'tdp': 65, 'perf': 35.2},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Duo E6600', 'year': 2006, 'cores': 2, 'threads': 2, 'boost': 2.4, 'pcie_gen': 1, 'pcie_lanes': 16, 'tdp': 65, 'perf': 35.8},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Duo E6700', 'year': 2006, 'cores': 2, 'threads': 2, 'boost': 2.66, 'pcie_gen': 1, 'pcie_lanes': 16, 'tdp': 65, 'perf': 39.6},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Duo E6750', 'year': 2007, 'cores': 2, 'threads': 2, 'boost': 2.66, 'pcie_gen': 1, 'pcie_lanes': 16, 'tdp': 65, 'perf': 39.6},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Duo E7200', 'year': 2008, 'cores': 2, 'threads': 2, 'boost': 2.53, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 65, 'perf': 39.7},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Duo E7300', 'year': 2008, 'cores': 2, 'threads': 2, 'boost': 2.66, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 65, 'perf': 41.8},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Extreme X6800', 'year': 2006, 'cores': 2, 'threads': 2, 'boost': 2.93, 'pcie_gen': 1, 'pcie_lanes': 16, 'tdp': 75, 'perf': 43.7},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Duo E7400', 'year': 2008, 'cores': 2, 'threads': 2, 'boost': 2.8, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 65, 'perf': 44.0},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Quad Q8200', 'year': 2008, 'cores': 4, 'threads': 4, 'boost': 2.33, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 95, 'perf': 44.1},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Quad Q8200S', 'year': 2008, 'cores': 4, 'threads': 4, 'boost': 2.33, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 65, 'perf': 44.1},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Duo E8190', 'year': 2008, 'cores': 2, 'threads': 2, 'boost': 2.66, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 65, 'perf': 44.4},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Duo E8200', 'year': 2008, 'cores': 2, 'threads': 2, 'boost': 2.66, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 65, 'perf': 44.4},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Duo E6850', 'year': 2007, 'cores': 2, 'threads': 2, 'boost': 3.0, 'pcie_gen': 1, 'pcie_lanes': 16, 'tdp': 65, 'perf': 44.7},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Quad Q6600', 'year': 2007, 'cores': 4, 'threads': 4, 'boost': 2.4, 'pcie_gen': 1, 'pcie_lanes': 16, 'tdp': 105, 'perf': 45},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Duo E7500', 'year': 2009, 'cores': 2, 'threads': 2, 'boost': 2.93, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 65, 'perf': 46.0},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Duo E8300', 'year': 2008, 'cores': 2, 'threads': 2, 'boost': 2.83, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 65, 'perf': 47.3},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Quad Q8300', 'year': 2009, 'cores': 4, 'threads': 4, 'boost': 2.5, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 95, 'perf': 47.3},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Duo E7600', 'year': 2009, 'cores': 2, 'threads': 2, 'boost': 3.06, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 65, 'perf': 48.0},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Duo E8400', 'year': 2008, 'cores': 2, 'threads': 2, 'boost': 3.0, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 65, 'perf': 50},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Quad Q6700', 'year': 2007, 'cores': 4, 'threads': 4, 'boost': 2.66, 'pcie_gen': 1, 'pcie_lanes': 16, 'tdp': 105, 'perf': 50.3},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Extreme QX6700', 'year': 2006, 'cores': 4, 'threads': 4, 'boost': 2.66, 'pcie_gen': 1, 'pcie_lanes': 16, 'tdp': 130, 'perf': 50.3},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Quad Q8400S', 'year': 2009, 'cores': 4, 'threads': 4, 'boost': 2.66, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 65, 'perf': 50.3},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Quad Q9300', 'year': 2008, 'cores': 4, 'threads': 4, 'boost': 2.5, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 95, 'perf': 51.1},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Quad Q8400', 'year': 2009, 'cores': 4, 'threads': 4, 'boost': 2.66, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 95, 'perf': 52},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Duo E8500', 'year': 2008, 'cores': 2, 'threads': 2, 'boost': 3.16, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 65, 'perf': 52.8},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Quad Q9400S', 'year': 2009, 'cores': 4, 'threads': 4, 'boost': 2.66, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 65, 'perf': 54.3},
    {'vendor': 'AMD', 'name': 'AMD Athlon II X4 640', 'year': 2010, 'cores': 4, 'threads': 4, 'boost': 3.0, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 95, 'perf': 55},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Quad Q9400', 'year': 2008, 'cores': 4, 'threads': 4, 'boost': 2.66, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 95, 'perf': 55},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Extreme QX6800', 'year': 2007, 'cores': 4, 'threads': 4, 'boost': 2.93, 'pcie_gen': 1, 'pcie_lanes': 16, 'tdp': 130, 'perf': 55.4},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Duo E8600', 'year': 2008, 'cores': 2, 'threads': 2, 'boost': 3.33, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 65, 'perf': 55.6},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Extreme QX6850', 'year': 2007, 'cores': 4, 'threads': 4, 'boost': 3.0, 'pcie_gen': 1, 'pcie_lanes': 16, 'tdp': 130, 'perf': 56.8},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Quad Q9450', 'year': 2008, 'cores': 4, 'threads': 4, 'boost': 2.66, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 95, 'perf': 57.2},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Quad Q9500', 'year': 2009, 'cores': 4, 'threads': 4, 'boost': 2.83, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 95, 'perf': 57.8},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Quad Q9505', 'year': 2009, 'cores': 4, 'threads': 4, 'boost': 2.83, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 95, 'perf': 57.8},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Quad Q9505S', 'year': 2009, 'cores': 4, 'threads': 4, 'boost': 2.83, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 65, 'perf': 57.8},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Quad Q9550', 'year': 2008, 'cores': 4, 'threads': 4, 'boost': 2.83, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 95, 'perf': 60},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Quad Q9550S', 'year': 2008, 'cores': 4, 'threads': 4, 'boost': 2.83, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 65, 'perf': 60.8},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Quad Q9650', 'year': 2008, 'cores': 4, 'threads': 4, 'boost': 3.0, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 95, 'perf': 64.5},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Extreme QX9650', 'year': 2007, 'cores': 4, 'threads': 4, 'boost': 3.0, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 130, 'perf': 64.5},
    {'vendor': 'Intel', 'name': 'Intel Core i3-2100', 'year': 2011, 'cores': 2, 'threads': 4, 'boost': 3.1, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 65, 'perf': 65},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Extreme QX9770', 'year': 2008, 'cores': 4, 'threads': 4, 'boost': 3.2, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 136, 'perf': 68.8},
    {'vendor': 'Intel', 'name': 'Intel Core 2 Extreme QX9775', 'year': 2008, 'cores': 4, 'threads': 4, 'boost': 3.2, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 150, 'perf': 68.8},
    {'vendor': 'AMD', 'name': 'AMD FX-4300', 'year': 2012, 'cores': 4, 'threads': 4, 'boost': 4.0, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 95, 'perf': 70},
    {'vendor': 'AMD', 'name': 'AMD Phenom II X4 955', 'year': 2009, 'cores': 4, 'threads': 4, 'boost': 3.2, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 125, 'perf': 70},
    {'vendor': 'AMD', 'name': 'AMD Phenom II X4 965', 'year': 2009, 'cores': 4, 'threads': 4, 'boost': 3.4, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 125, 'perf': 75},
    {'vendor': 'Intel', 'name': 'Intel Core i5-750', 'year': 2009, 'cores': 4, 'threads': 4, 'boost': 3.2, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 95, 'perf': 80},
    {'vendor': 'AMD', 'name': 'AMD FX-6300', 'year': 2012, 'cores': 6, 'threads': 6, 'boost': 4.1, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 95, 'perf': 85},
    {'vendor': 'AMD', 'name': 'AMD Phenom II X6 1090T', 'year': 2010, 'cores': 6, 'threads': 6, 'boost': 3.6, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 125, 'perf': 85},
    {'vendor': 'Intel', 'name': 'Intel Core i7-920', 'year': 2008, 'cores': 4, 'threads': 8, 'boost': 2.93, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 130, 'perf': 85},
    {'vendor': 'Intel', 'name': 'Intel Core i7-860', 'year': 2009, 'cores': 4, 'threads': 8, 'boost': 3.46, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 95, 'perf': 90},
    {'vendor': 'Intel', 'name': 'Intel Core i7-930', 'year': 2009, 'cores': 4, 'threads': 8, 'boost': 3.06, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 130, 'perf': 90},
    {'vendor': 'AMD', 'name': 'AMD FX-6350', 'year': 2012, 'cores': 6, 'threads': 6, 'boost': 4.2, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 125, 'perf': 95},
    {'vendor': 'AMD', 'name': 'AMD FX-8320', 'year': 2012, 'cores': 8, 'threads': 8, 'boost': 4.0, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 125, 'perf': 100},
    {'vendor': 'Intel', 'name': 'Intel Core i3-3220', 'year': 2012, 'cores': 2, 'threads': 4, 'boost': 3.3, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 55, 'perf': 100},
    {'vendor': 'Intel', 'name': 'Intel Core i5-2400', 'year': 2011, 'cores': 4, 'threads': 4, 'boost': 3.4, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 95, 'perf': 100},
    {'vendor': 'AMD', 'name': 'AMD FX-8350', 'year': 2012, 'cores': 8, 'threads': 8, 'boost': 4.2, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 125, 'perf': 105},
    {'vendor': 'Intel', 'name': 'Intel Core i5-2500K', 'year': 2011, 'cores': 4, 'threads': 4, 'boost': 3.7, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 95, 'perf': 105},
    {'vendor': 'AMD', 'name': 'AMD FX-8370', 'year': 2014, 'cores': 8, 'threads': 8, 'boost': 4.3, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 125, 'perf': 110},
    {'vendor': 'Intel', 'name': 'Intel Pentium G3258', 'year': 2014, 'cores': 2, 'threads': 2, 'boost': 3.2, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 53, 'perf': 110},
    {'vendor': 'Intel', 'name': 'Intel Core i7-2600K', 'year': 2011, 'cores': 4, 'threads': 8, 'boost': 3.8, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 95, 'perf': 115},
    {'vendor': 'AMD', 'name': 'AMD FX-9590', 'year': 2013, 'cores': 8, 'threads': 8, 'boost': 4.7, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 220, 'perf': 120},
    {'vendor': 'Intel', 'name': 'Intel Core i3-4130', 'year': 2013, 'cores': 2, 'threads': 4, 'boost': 3.4, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 54, 'perf': 120},
    {'vendor': 'Intel', 'name': 'Intel Core i5-3470', 'year': 2012, 'cores': 4, 'threads': 4, 'boost': 3.6, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 77, 'perf': 120},
    {'vendor': 'Intel', 'name': 'Intel Core i7-2700K', 'year': 2011, 'cores': 4, 'threads': 8, 'boost': 3.9, 'pcie_gen': 2, 'pcie_lanes': 16, 'tdp': 95, 'perf': 120},
    {'vendor': 'Intel', 'name': 'Intel Core i5-3570K', 'year': 2012, 'cores': 4, 'threads': 4, 'boost': 3.8, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 77, 'perf': 125},
    {'vendor': 'Intel', 'name': 'Intel Pentium G4560', 'year': 2017, 'cores': 2, 'threads': 4, 'boost': 3.5, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 54, 'perf': 130},
    {'vendor': 'Intel', 'name': 'Intel Core i7-3770K', 'year': 2012, 'cores': 4, 'threads': 8, 'boost': 3.9, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 77, 'perf': 135},
    {'vendor': 'Intel', 'name': 'Intel Core i5-4460', 'year': 2014, 'cores': 4, 'threads': 4, 'boost': 3.4, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 84, 'perf': 140},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 3 2200GE', 'year': 2018, 'cores': 4, 'threads': 4, 'boost': 3.6, 'pcie_gen': 3, 'pcie_lanes': 8, 'tdp': 35, 'perf': 143},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 3 PRO 2200GE', 'year': 2018, 'cores': 4, 'threads': 4, 'boost': 3.6, 'pcie_gen': 3, 'pcie_lanes': 8, 'tdp': 35, 'perf': 143},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 3 1200', 'year': 2017, 'cores': 4, 'threads': 4, 'boost': 3.4, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 145},
    {'vendor': 'Intel', 'name': 'Intel Core i5-4570', 'year': 2013, 'cores': 4, 'threads': 4, 'boost': 3.6, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 84, 'perf': 145},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 3 3200GE', 'year': 2019, 'cores': 4, 'threads': 4, 'boost': 3.8, 'pcie_gen': 3, 'pcie_lanes': 8, 'tdp': 35, 'perf': 149},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 3 PRO 3200GE', 'year': 2019, 'cores': 4, 'threads': 4, 'boost': 3.8, 'pcie_gen': 3, 'pcie_lanes': 8, 'tdp': 35, 'perf': 149},
    {'vendor': 'Intel', 'name': 'Intel Celeron G5905', 'year': 2020, 'cores': 2, 'threads': 2, 'boost': 3.5, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 58, 'perf': 150},
    {'vendor': 'Intel', 'name': 'Intel Core i3-6100', 'year': 2015, 'cores': 2, 'threads': 4, 'boost': 3.7, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 51, 'perf': 150},
    {'vendor': 'Intel', 'name': 'Intel Core i5-4690K', 'year': 2014, 'cores': 4, 'threads': 4, 'boost': 3.9, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 88, 'perf': 155},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 2400GE', 'year': 2018, 'cores': 4, 'threads': 8, 'boost': 3.8, 'pcie_gen': 3, 'pcie_lanes': 8, 'tdp': 35, 'perf': 157},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 PRO 2400GE', 'year': 2018, 'cores': 4, 'threads': 8, 'boost': 3.8, 'pcie_gen': 3, 'pcie_lanes': 8, 'tdp': 35, 'perf': 157},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 3 1300X', 'year': 2017, 'cores': 4, 'threads': 4, 'boost': 3.7, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 160},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 3 2200G', 'year': 2018, 'cores': 4, 'threads': 4, 'boost': 3.7, 'pcie_gen': 3, 'pcie_lanes': 8, 'tdp': 65, 'perf': 160},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 3 PRO 2200G', 'year': 2018, 'cores': 4, 'threads': 4, 'boost': 3.7, 'pcie_gen': 3, 'pcie_lanes': 8, 'tdp': 65, 'perf': 160},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 3400GE', 'year': 2019, 'cores': 4, 'threads': 8, 'boost': 4.0, 'pcie_gen': 3, 'pcie_lanes': 8, 'tdp': 35, 'perf': 162},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 PRO 3400GE', 'year': 2019, 'cores': 4, 'threads': 8, 'boost': 4.0, 'pcie_gen': 3, 'pcie_lanes': 8, 'tdp': 35, 'perf': 162},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 1400', 'year': 2017, 'cores': 4, 'threads': 8, 'boost': 3.4, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 165},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 3 3200G', 'year': 2019, 'cores': 4, 'threads': 4, 'boost': 4.0, 'pcie_gen': 3, 'pcie_lanes': 8, 'tdp': 65, 'perf': 170},
    {'vendor': 'Intel', 'name': 'Intel Core i3-7100', 'year': 2017, 'cores': 2, 'threads': 4, 'boost': 3.9, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 51, 'perf': 170},
    {'vendor': 'Intel', 'name': 'Intel Pentium Gold G5400', 'year': 2018, 'cores': 2, 'threads': 4, 'boost': 3.7, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 54, 'perf': 170},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 3 PRO 3200G', 'year': 2019, 'cores': 4, 'threads': 4, 'boost': 4.0, 'pcie_gen': 3, 'pcie_lanes': 8, 'tdp': 65, 'perf': 170},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 1500X', 'year': 2017, 'cores': 4, 'threads': 8, 'boost': 3.7, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 175},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 2400G', 'year': 2018, 'cores': 4, 'threads': 8, 'boost': 3.9, 'pcie_gen': 3, 'pcie_lanes': 8, 'tdp': 65, 'perf': 175},
    {'vendor': 'Intel', 'name': 'Intel Core i5-7400', 'year': 2017, 'cores': 4, 'threads': 4, 'boost': 3.5, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 175},
    {'vendor': 'Intel', 'name': 'Intel Core i7-4770K', 'year': 2013, 'cores': 4, 'threads': 8, 'boost': 3.9, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 84, 'perf': 175},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 PRO 2400G', 'year': 2018, 'cores': 4, 'threads': 8, 'boost': 3.9, 'pcie_gen': 3, 'pcie_lanes': 8, 'tdp': 65, 'perf': 175},
    {'vendor': 'Intel', 'name': 'Intel Celeron G6900', 'year': 2022, 'cores': 2, 'threads': 2, 'boost': 3.4, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 46, 'perf': 180},
    {'vendor': 'Intel', 'name': 'Intel Core i5-6500', 'year': 2015, 'cores': 4, 'threads': 4, 'boost': 3.6, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 180},
    {'vendor': 'Intel', 'name': 'Intel Core i5-7500', 'year': 2017, 'cores': 4, 'threads': 4, 'boost': 3.8, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 180},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 3 3400G', 'year': 2019, 'cores': 4, 'threads': 8, 'boost': 4.2, 'pcie_gen': 3, 'pcie_lanes': 8, 'tdp': 65, 'perf': 185},
    {'vendor': 'Intel', 'name': 'Intel Core i5-7600K', 'year': 2017, 'cores': 4, 'threads': 4, 'boost': 4.2, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 91, 'perf': 185},
    {'vendor': 'Intel', 'name': 'Intel Core i7-4790K', 'year': 2014, 'cores': 4, 'threads': 8, 'boost': 4.4, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 88, 'perf': 185},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 PRO 3400G', 'year': 2019, 'cores': 4, 'threads': 8, 'boost': 4.2, 'pcie_gen': 3, 'pcie_lanes': 8, 'tdp': 65, 'perf': 185},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 1600', 'year': 2017, 'cores': 6, 'threads': 12, 'boost': 3.6, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 190},
    {'vendor': 'Intel', 'name': 'Intel Pentium Gold G6400', 'year': 2020, 'cores': 2, 'threads': 4, 'boost': 4.0, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 58, 'perf': 190},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 3 4300GE', 'year': 2020, 'cores': 4, 'threads': 8, 'boost': 4.0, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 35, 'perf': 190},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 3 PRO 4350GE', 'year': 2020, 'cores': 4, 'threads': 8, 'boost': 4.0, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 35, 'perf': 190},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 1700', 'year': 2017, 'cores': 8, 'threads': 16, 'boost': 3.7, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 195},
    {'vendor': 'Intel', 'name': 'Intel Core i3-8100', 'year': 2017, 'cores': 4, 'threads': 4, 'boost': 3.6, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 195},
    {'vendor': 'Intel', 'name': 'Intel Core i5-6600K', 'year': 2015, 'cores': 4, 'threads': 4, 'boost': 3.9, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 91, 'perf': 195},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 1600X', 'year': 2017, 'cores': 6, 'threads': 12, 'boost': 4.0, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 95, 'perf': 200},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 1700X', 'year': 2017, 'cores': 8, 'threads': 16, 'boost': 3.8, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 95, 'perf': 200},
    {'vendor': 'Intel', 'name': 'Intel Core i3-8350K', 'year': 2017, 'cores': 4, 'threads': 4, 'boost': 4.0, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 91, 'perf': 200},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 3 4300G', 'year': 2020, 'cores': 4, 'threads': 8, 'boost': 4.0, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 200},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 3 PRO 4350G', 'year': 2020, 'cores': 4, 'threads': 8, 'boost': 4.0, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 200},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 1800X', 'year': 2017, 'cores': 8, 'threads': 16, 'boost': 4.0, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 95, 'perf': 205},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 3 4100', 'year': 2022, 'cores': 4, 'threads': 8, 'boost': 4.0, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 215},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 2600', 'year': 2018, 'cores': 6, 'threads': 12, 'boost': 3.9, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 215},
    {'vendor': 'Intel', 'name': 'Intel Core i3-9100F', 'year': 2019, 'cores': 4, 'threads': 4, 'boost': 4.2, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 215},
    {'vendor': 'Intel', 'name': 'Intel Core i7-6700', 'year': 2015, 'cores': 4, 'threads': 8, 'boost': 4.0, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 215},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 2600X', 'year': 2018, 'cores': 6, 'threads': 12, 'boost': 4.25, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 95, 'perf': 225},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 2700', 'year': 2018, 'cores': 8, 'threads': 16, 'boost': 4.1, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 225},
    {'vendor': 'Intel', 'name': 'Intel Core i7-6700K', 'year': 2015, 'cores': 4, 'threads': 8, 'boost': 4.2, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 91, 'perf': 225},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 3 PRO 5350GE', 'year': 2021, 'cores': 4, 'threads': 8, 'boost': 4.0, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 35, 'perf': 228},
    {'vendor': 'Intel', 'name': 'Intel Core i7-7700', 'year': 2017, 'cores': 4, 'threads': 8, 'boost': 4.2, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 230},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 3 3100', 'year': 2020, 'cores': 4, 'threads': 8, 'boost': 3.9, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 65, 'perf': 235},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 2700X', 'year': 2018, 'cores': 8, 'threads': 16, 'boost': 4.3, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 105, 'perf': 235},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 3 5300GE', 'year': 2021, 'cores': 4, 'threads': 8, 'boost': 4.2, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 35, 'perf': 238},
    {'vendor': 'Intel', 'name': 'Intel Core i7-7700K', 'year': 2017, 'cores': 4, 'threads': 8, 'boost': 4.5, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 91, 'perf': 240},
    {'vendor': 'Intel', 'name': 'Intel Pentium Gold G7400', 'year': 2022, 'cores': 2, 'threads': 4, 'boost': 3.7, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 46, 'perf': 240},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 3 PRO 5350G', 'year': 2021, 'cores': 4, 'threads': 8, 'boost': 4.0, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 240},
    {'vendor': 'Intel', 'name': 'Intel Core i3-10100F', 'year': 2020, 'cores': 4, 'threads': 8, 'boost': 4.3, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 245},
    {'vendor': 'Intel', 'name': 'Intel Core i5-8400', 'year': 2017, 'cores': 6, 'threads': 6, 'boost': 4.0, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 245},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 3 5300G', 'year': 2021, 'cores': 4, 'threads': 8, 'boost': 4.2, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 250},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 4600GE', 'year': 2020, 'cores': 6, 'threads': 12, 'boost': 4.2, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 35, 'perf': 252},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 PRO 4650GE', 'year': 2020, 'cores': 6, 'threads': 12, 'boost': 4.2, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 35, 'perf': 252},
    {'vendor': 'Intel', 'name': 'Intel Core i3-10300', 'year': 2020, 'cores': 4, 'threads': 8, 'boost': 4.4, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 255},
    {'vendor': 'Intel', 'name': 'Intel Core i5-9400F', 'year': 2019, 'cores': 6, 'threads': 6, 'boost': 4.1, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 255},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 4700GE', 'year': 2020, 'cores': 8, 'threads': 16, 'boost': 4.3, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 35, 'perf': 255},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 PRO 4750GE', 'year': 2020, 'cores': 8, 'threads': 16, 'boost': 4.3, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 35, 'perf': 255},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 3 8300GE', 'year': 2024, 'cores': 4, 'threads': 8, 'boost': 4.9, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 35, 'perf': 255},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 3 PRO 8300GE', 'year': 2024, 'cores': 4, 'threads': 8, 'boost': 4.9, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 35, 'perf': 255},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 3 3300X', 'year': 2020, 'cores': 4, 'threads': 8, 'boost': 4.3, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 65, 'perf': 265},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 4600G', 'year': 2021, 'cores': 6, 'threads': 12, 'boost': 4.2, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 265},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 PRO 4650G', 'year': 2020, 'cores': 6, 'threads': 12, 'boost': 4.2, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 265},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 3500X', 'year': 2019, 'cores': 6, 'threads': 6, 'boost': 4.1, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 65, 'perf': 270},
    {'vendor': 'Intel', 'name': 'Intel Core i5-8600K', 'year': 2017, 'cores': 6, 'threads': 6, 'boost': 4.3, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 95, 'perf': 270},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 3 8300G', 'year': 2024, 'cores': 4, 'threads': 8, 'boost': 4.9, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 65, 'perf': 270},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 3 PRO 8300G', 'year': 2024, 'cores': 4, 'threads': 8, 'boost': 4.9, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 65, 'perf': 270},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 4500', 'year': 2022, 'cores': 6, 'threads': 12, 'boost': 4.1, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 275},
    {'vendor': 'Intel', 'name': 'Intel Core i7-8700', 'year': 2017, 'cores': 6, 'threads': 12, 'boost': 4.6, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 275},
    {'vendor': 'Intel', 'name': 'Intel Core i3-12100', 'year': 2022, 'cores': 4, 'threads': 8, 'boost': 4.3, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 60, 'perf': 285},
    {'vendor': 'Intel', 'name': 'Intel Core i3-12100F', 'year': 2022, 'cores': 4, 'threads': 8, 'boost': 4.3, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 58, 'perf': 285},
    {'vendor': 'Intel', 'name': 'Intel Core i5-10400', 'year': 2020, 'cores': 6, 'threads': 12, 'boost': 4.3, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 285},
    {'vendor': 'Intel', 'name': 'Intel Core i5-10400F', 'year': 2020, 'cores': 6, 'threads': 12, 'boost': 4.3, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 285},
    {'vendor': 'Intel', 'name': 'Intel Core i5-9600K', 'year': 2018, 'cores': 6, 'threads': 6, 'boost': 4.6, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 95, 'perf': 285},
    {'vendor': 'Intel', 'name': 'Intel Core i5-9600KF', 'year': 2019, 'cores': 6, 'threads': 6, 'boost': 4.6, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 95, 'perf': 285},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 3600', 'year': 2019, 'cores': 6, 'threads': 12, 'boost': 4.2, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 65, 'perf': 290},
    {'vendor': 'Intel', 'name': 'Intel Core i7-8700K', 'year': 2017, 'cores': 6, 'threads': 12, 'boost': 4.7, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 95, 'perf': 290},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 4700G', 'year': 2020, 'cores': 8, 'threads': 16, 'boost': 4.4, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 290},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 PRO 4750G', 'year': 2020, 'cores': 8, 'threads': 16, 'boost': 4.4, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 290},
    {'vendor': 'Intel', 'name': 'Intel Core i3-12300', 'year': 2022, 'cores': 4, 'threads': 8, 'boost': 4.4, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 60, 'perf': 295},
    {'vendor': 'Intel', 'name': 'Intel Core i5-10500', 'year': 2020, 'cores': 6, 'threads': 12, 'boost': 4.5, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 295},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 5600GE', 'year': 2021, 'cores': 6, 'threads': 12, 'boost': 4.4, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 35, 'perf': 295},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 PRO 5650GE', 'year': 2021, 'cores': 6, 'threads': 12, 'boost': 4.4, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 35, 'perf': 295},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 3600X', 'year': 2019, 'cores': 6, 'threads': 12, 'boost': 4.4, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 95, 'perf': 300},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 5500', 'year': 2022, 'cores': 6, 'threads': 12, 'boost': 4.2, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 300},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 5700GE', 'year': 2021, 'cores': 8, 'threads': 16, 'boost': 4.6, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 35, 'perf': 300},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 PRO 5750GE', 'year': 2021, 'cores': 8, 'threads': 16, 'boost': 4.6, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 35, 'perf': 300},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 3600XT', 'year': 2020, 'cores': 6, 'threads': 12, 'boost': 4.5, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 95, 'perf': 305},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 5500GT', 'year': 2024, 'cores': 6, 'threads': 12, 'boost': 4.4, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 305},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 3700X', 'year': 2019, 'cores': 8, 'threads': 16, 'boost': 4.4, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 65, 'perf': 305},
    {'vendor': 'Intel', 'name': 'Intel Core i3-13100F', 'year': 2023, 'cores': 4, 'threads': 8, 'boost': 4.5, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 58, 'perf': 305},
    {'vendor': 'Intel', 'name': 'Intel Core i7-9700F', 'year': 2019, 'cores': 8, 'threads': 8, 'boost': 4.7, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 305},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 5600G', 'year': 2021, 'cores': 6, 'threads': 12, 'boost': 4.4, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 310},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 3800X', 'year': 2019, 'cores': 8, 'threads': 16, 'boost': 4.5, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 105, 'perf': 310},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 PRO 5650G', 'year': 2021, 'cores': 6, 'threads': 12, 'boost': 4.4, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 310},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 5600GT', 'year': 2024, 'cores': 6, 'threads': 12, 'boost': 4.6, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 315},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 3800XT', 'year': 2020, 'cores': 8, 'threads': 16, 'boost': 4.7, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 105, 'perf': 315},
    {'vendor': 'Intel', 'name': 'Intel Core i5-10600K', 'year': 2020, 'cores': 6, 'threads': 12, 'boost': 4.8, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 125, 'perf': 315},
    {'vendor': 'Intel', 'name': 'Intel Core i5-10600KF', 'year': 2020, 'cores': 6, 'threads': 12, 'boost': 4.8, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 125, 'perf': 315},
    {'vendor': 'Intel', 'name': 'Intel Core i5-11400F', 'year': 2021, 'cores': 6, 'threads': 12, 'boost': 4.4, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 65, 'perf': 315},
    {'vendor': 'Intel', 'name': 'Intel Core i7-9700K', 'year': 2018, 'cores': 8, 'threads': 8, 'boost': 4.9, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 95, 'perf': 315},
    {'vendor': 'Intel', 'name': 'Intel Core i7-9700KF', 'year': 2019, 'cores': 8, 'threads': 8, 'boost': 4.9, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 95, 'perf': 315},
    {'vendor': 'Intel', 'name': 'Intel Core i3-14100F', 'year': 2024, 'cores': 4, 'threads': 8, 'boost': 4.7, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 58, 'perf': 320},
    {'vendor': 'Intel', 'name': 'Intel Core i7-10700', 'year': 2020, 'cores': 8, 'threads': 16, 'boost': 4.8, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 320},
    {'vendor': 'Intel', 'name': 'Intel Core i7-10700F', 'year': 2020, 'cores': 8, 'threads': 16, 'boost': 4.8, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 320},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 5700G', 'year': 2021, 'cores': 8, 'threads': 16, 'boost': 4.6, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 325},
    {'vendor': 'Intel', 'name': 'Intel Core i5-11500', 'year': 2021, 'cores': 6, 'threads': 12, 'boost': 4.6, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 65, 'perf': 325},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 PRO 5750G', 'year': 2021, 'cores': 8, 'threads': 16, 'boost': 4.6, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 325},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 8500GE', 'year': 2024, 'cores': 6, 'threads': 12, 'boost': 5.0, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 35, 'perf': 325},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 PRO 8500GE', 'year': 2024, 'cores': 6, 'threads': 12, 'boost': 5.0, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 35, 'perf': 325},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 9 3900X', 'year': 2019, 'cores': 12, 'threads': 24, 'boost': 4.6, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 105, 'perf': 330},
    {'vendor': 'Intel', 'name': 'Intel Core i5-12400', 'year': 2022, 'cores': 6, 'threads': 12, 'boost': 4.4, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 330},
    {'vendor': 'Intel', 'name': 'Intel Core i5-12400F', 'year': 2022, 'cores': 6, 'threads': 12, 'boost': 4.4, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 330},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 9 3900XT', 'year': 2020, 'cores': 12, 'threads': 24, 'boost': 4.7, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 105, 'perf': 335},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 9 3950X', 'year': 2019, 'cores': 16, 'threads': 32, 'boost': 4.7, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 105, 'perf': 335},
    {'vendor': 'Intel', 'name': 'Intel Core i9-9900K', 'year': 2018, 'cores': 8, 'threads': 16, 'boost': 5.0, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 95, 'perf': 335},
    {'vendor': 'Intel', 'name': 'Intel Core i9-9900KF', 'year': 2019, 'cores': 8, 'threads': 16, 'boost': 5.0, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 95, 'perf': 335},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 5600', 'year': 2022, 'cores': 6, 'threads': 12, 'boost': 4.4, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 65, 'perf': 340},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 8500G', 'year': 2024, 'cores': 6, 'threads': 12, 'boost': 5.0, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 65, 'perf': 340},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 5700', 'year': 2024, 'cores': 8, 'threads': 16, 'boost': 4.6, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 340},
    {'vendor': 'Intel', 'name': 'Intel Core i7-10700K', 'year': 2020, 'cores': 8, 'threads': 16, 'boost': 5.1, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 125, 'perf': 340},
    {'vendor': 'Intel', 'name': 'Intel Core i7-10700KF', 'year': 2020, 'cores': 8, 'threads': 16, 'boost': 5.1, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 125, 'perf': 340},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 PRO 8500G', 'year': 2024, 'cores': 6, 'threads': 12, 'boost': 5.0, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 65, 'perf': 340},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 5600T', 'year': 2022, 'cores': 6, 'threads': 12, 'boost': 4.6, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 65, 'perf': 345},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 5600X', 'year': 2020, 'cores': 6, 'threads': 12, 'boost': 4.6, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 65, 'perf': 345},
    {'vendor': 'Intel', 'name': 'Intel Core i5-11600K', 'year': 2021, 'cores': 6, 'threads': 12, 'boost': 4.9, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 125, 'perf': 345},
    {'vendor': 'Intel', 'name': 'Intel Core i5-11600KF', 'year': 2021, 'cores': 6, 'threads': 12, 'boost': 4.9, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 125, 'perf': 345},
    {'vendor': 'Intel', 'name': 'Intel Core i5-12500', 'year': 2022, 'cores': 6, 'threads': 12, 'boost': 4.6, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 345},
    {'vendor': 'Intel', 'name': 'Intel Core i9-10900', 'year': 2020, 'cores': 10, 'threads': 20, 'boost': 5.2, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 65, 'perf': 350},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 5700X', 'year': 2022, 'cores': 8, 'threads': 16, 'boost': 4.6, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 65, 'perf': 355},
    {'vendor': 'Intel', 'name': 'Intel Core i7-11700', 'year': 2021, 'cores': 8, 'threads': 16, 'boost': 4.9, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 65, 'perf': 355},
    {'vendor': 'Intel', 'name': 'Intel Core i9-10850K', 'year': 2020, 'cores': 10, 'threads': 20, 'boost': 5.2, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 125, 'perf': 360},
    {'vendor': 'Intel', 'name': 'Intel Core i7-11700K', 'year': 2021, 'cores': 8, 'threads': 16, 'boost': 5.0, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 125, 'perf': 365},
    {'vendor': 'Intel', 'name': 'Intel Core i7-11700KF', 'year': 2021, 'cores': 8, 'threads': 16, 'boost': 5.0, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 125, 'perf': 365},
    {'vendor': 'Intel', 'name': 'Intel Core i9-10900K', 'year': 2020, 'cores': 10, 'threads': 20, 'boost': 5.3, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 125, 'perf': 365},
    {'vendor': 'Intel', 'name': 'Intel Core i9-10900KF', 'year': 2020, 'cores': 10, 'threads': 20, 'boost': 5.3, 'pcie_gen': 3, 'pcie_lanes': 16, 'tdp': 125, 'perf': 365},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 5800X', 'year': 2020, 'cores': 8, 'threads': 16, 'boost': 4.7, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 105, 'perf': 370},
    {'vendor': 'Intel', 'name': 'Intel Core i5-13400', 'year': 2023, 'cores': 10, 'threads': 16, 'boost': 4.6, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 370},
    {'vendor': 'Intel', 'name': 'Intel Core i5-13400F', 'year': 2023, 'cores': 10, 'threads': 16, 'boost': 4.6, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 370},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 5800XT', 'year': 2024, 'cores': 8, 'threads': 16, 'boost': 4.8, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 105, 'perf': 375},
    {'vendor': 'Intel', 'name': 'Intel Core i5-14400', 'year': 2024, 'cores': 10, 'threads': 16, 'boost': 4.7, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 375},
    {'vendor': 'Intel', 'name': 'Intel Core i5-14400F', 'year': 2024, 'cores': 10, 'threads': 16, 'boost': 4.7, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 375},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 9 5900X', 'year': 2020, 'cores': 12, 'threads': 24, 'boost': 4.8, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 105, 'perf': 380},
    {'vendor': 'Intel', 'name': 'Intel Core i9-11900K', 'year': 2021, 'cores': 8, 'threads': 16, 'boost': 5.3, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 125, 'perf': 380},
    {'vendor': 'Intel', 'name': 'Intel Core i9-11900KF', 'year': 2021, 'cores': 8, 'threads': 16, 'boost': 5.3, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 125, 'perf': 380},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 PRO 8600GE', 'year': 2024, 'cores': 6, 'threads': 12, 'boost': 5.0, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 35, 'perf': 380},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 9 5900XT', 'year': 2024, 'cores': 16, 'threads': 32, 'boost': 4.8, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 105, 'perf': 385},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 9 5950X', 'year': 2020, 'cores': 16, 'threads': 32, 'boost': 4.9, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 105, 'perf': 385},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 8400F', 'year': 2024, 'cores': 6, 'threads': 12, 'boost': 4.7, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 65, 'perf': 390},
    {'vendor': 'Intel', 'name': 'Intel Core i5-12600', 'year': 2022, 'cores': 6, 'threads': 12, 'boost': 4.8, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 395},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 PRO 8700GE', 'year': 2024, 'cores': 8, 'threads': 16, 'boost': 5.1, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 35, 'perf': 395},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 8600G', 'year': 2024, 'cores': 6, 'threads': 12, 'boost': 5.0, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 65, 'perf': 400},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 PRO 8600G', 'year': 2024, 'cores': 6, 'threads': 12, 'boost': 5.0, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 65, 'perf': 400},
    {'vendor': 'Intel', 'name': 'Intel Core i5-12600K', 'year': 2021, 'cores': 10, 'threads': 16, 'boost': 4.9, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 125, 'perf': 405},
    {'vendor': 'Intel', 'name': 'Intel Core i5-12600KF', 'year': 2021, 'cores': 10, 'threads': 16, 'boost': 4.9, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 125, 'perf': 405},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 8700F', 'year': 2024, 'cores': 8, 'threads': 16, 'boost': 5.0, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 65, 'perf': 415},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 8700G', 'year': 2024, 'cores': 8, 'threads': 16, 'boost': 5.1, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 65, 'perf': 420},
    {'vendor': 'Intel', 'name': 'Intel Core i5-13500', 'year': 2023, 'cores': 14, 'threads': 20, 'boost': 4.8, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 420},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 PRO 8700G', 'year': 2024, 'cores': 8, 'threads': 16, 'boost': 5.1, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 65, 'perf': 420},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 7500F', 'year': 2023, 'cores': 6, 'threads': 12, 'boost': 5.0, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 430},
    {'vendor': 'Intel', 'name': 'Intel Core i7-12700', 'year': 2022, 'cores': 12, 'threads': 20, 'boost': 4.9, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 430},
    {'vendor': 'Intel', 'name': 'Intel Core i7-12700F', 'year': 2022, 'cores': 12, 'threads': 20, 'boost': 4.9, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 430},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 5600X3D', 'year': 2023, 'cores': 6, 'threads': 12, 'boost': 4.4, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 105, 'perf': 440},
    {'vendor': 'Intel', 'name': 'Intel Core i5-14500', 'year': 2024, 'cores': 14, 'threads': 20, 'boost': 5.0, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 440},
    {'vendor': 'Intel', 'name': 'Intel Core i7-12700K', 'year': 2021, 'cores': 12, 'threads': 20, 'boost': 5.0, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 125, 'perf': 440},
    {'vendor': 'Intel', 'name': 'Intel Core i7-12700KF', 'year': 2021, 'cores': 12, 'threads': 20, 'boost': 5.0, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 125, 'perf': 440},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 7600', 'year': 2023, 'cores': 6, 'threads': 12, 'boost': 5.1, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 445},
    {'vendor': 'Intel', 'name': 'Intel Core Ultra 5 225', 'year': 2025, 'cores': 10, 'threads': 10, 'boost': 4.9, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 450},
    {'vendor': 'Intel', 'name': 'Intel Core Ultra 5 225F', 'year': 2025, 'cores': 10, 'threads': 10, 'boost': 4.9, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 450},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 7600X', 'year': 2022, 'cores': 6, 'threads': 12, 'boost': 5.3, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 105, 'perf': 460},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 5700X3D', 'year': 2024, 'cores': 8, 'threads': 16, 'boost': 4.1, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 105, 'perf': 460},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 7700', 'year': 2023, 'cores': 8, 'threads': 16, 'boost': 5.3, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 460},
    {'vendor': 'Intel', 'name': 'Intel Core i9-12900', 'year': 2022, 'cores': 16, 'threads': 24, 'boost': 5.1, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 460},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 9 7900', 'year': 2023, 'cores': 12, 'threads': 24, 'boost': 5.4, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 470},
    {'vendor': 'Intel', 'name': 'Intel Core i9-12900K', 'year': 2021, 'cores': 16, 'threads': 24, 'boost': 5.2, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 125, 'perf': 470},
    {'vendor': 'Intel', 'name': 'Intel Core i9-12900KF', 'year': 2021, 'cores': 16, 'threads': 24, 'boost': 5.2, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 125, 'perf': 470},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 7700X', 'year': 2022, 'cores': 8, 'threads': 16, 'boost': 5.4, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 105, 'perf': 475},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 5800X3D', 'year': 2022, 'cores': 8, 'threads': 16, 'boost': 4.5, 'pcie_gen': 4, 'pcie_lanes': 16, 'tdp': 105, 'perf': 480},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 9 7900X', 'year': 2022, 'cores': 12, 'threads': 24, 'boost': 5.6, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 170, 'perf': 480},
    {'vendor': 'Intel', 'name': 'Intel Core i9-12900KS', 'year': 2022, 'cores': 16, 'threads': 24, 'boost': 5.5, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 150, 'perf': 480},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 9 7950X', 'year': 2022, 'cores': 16, 'threads': 32, 'boost': 5.7, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 170, 'perf': 495},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 9600', 'year': 2025, 'cores': 6, 'threads': 12, 'boost': 5.2, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 510},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 9600X', 'year': 2024, 'cores': 6, 'threads': 12, 'boost': 5.4, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 520},
    {'vendor': 'Intel', 'name': 'Intel Core Ultra 5 245', 'year': 2024, 'cores': 14, 'threads': 14, 'boost': 5.1, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 520},
    {'vendor': 'Intel', 'name': 'Intel Core i5-13600K', 'year': 2022, 'cores': 14, 'threads': 20, 'boost': 5.1, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 125, 'perf': 520},
    {'vendor': 'Intel', 'name': 'Intel Core i5-13600KF', 'year': 2022, 'cores': 14, 'threads': 20, 'boost': 5.1, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 125, 'perf': 520},
    {'vendor': 'Intel', 'name': 'Intel Core Ultra 5 245K', 'year': 2024, 'cores': 14, 'threads': 14, 'boost': 5.2, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 125, 'perf': 535},
    {'vendor': 'Intel', 'name': 'Intel Core Ultra 5 245KF', 'year': 2024, 'cores': 14, 'threads': 14, 'boost': 5.2, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 125, 'perf': 535},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 9700X', 'year': 2024, 'cores': 8, 'threads': 16, 'boost': 5.5, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 540},
    {'vendor': 'Intel', 'name': 'Intel Core i7-13700', 'year': 2023, 'cores': 16, 'threads': 24, 'boost': 5.2, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 540},
    {'vendor': 'Intel', 'name': 'Intel Core i7-13700F', 'year': 2023, 'cores': 16, 'threads': 24, 'boost': 5.2, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 540},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 9 9900X', 'year': 2024, 'cores': 12, 'threads': 24, 'boost': 5.6, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 120, 'perf': 545},
    {'vendor': 'Intel', 'name': 'Intel Core i5-14600K', 'year': 2023, 'cores': 14, 'threads': 20, 'boost': 5.3, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 125, 'perf': 545},
    {'vendor': 'Intel', 'name': 'Intel Core i5-14600KF', 'year': 2023, 'cores': 14, 'threads': 20, 'boost': 5.3, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 125, 'perf': 545},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 9 9950X', 'year': 2024, 'cores': 16, 'threads': 32, 'boost': 5.7, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 170, 'perf': 555},
    {'vendor': 'Intel', 'name': 'Intel Core i7-14700', 'year': 2024, 'cores': 20, 'threads': 28, 'boost': 5.4, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 560},
    {'vendor': 'Intel', 'name': 'Intel Core i7-14700F', 'year': 2024, 'cores': 20, 'threads': 28, 'boost': 5.4, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 560},
    {'vendor': 'Intel', 'name': 'Intel Core i7-13700K', 'year': 2022, 'cores': 16, 'threads': 24, 'boost': 5.4, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 125, 'perf': 570},
    {'vendor': 'Intel', 'name': 'Intel Core i7-13700KF', 'year': 2022, 'cores': 16, 'threads': 24, 'boost': 5.4, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 125, 'perf': 570},
    {'vendor': 'Intel', 'name': 'Intel Core Ultra 7 265', 'year': 2024, 'cores': 20, 'threads': 20, 'boost': 5.3, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 580},
    {'vendor': 'Intel', 'name': 'Intel Core Ultra 7 265F', 'year': 2024, 'cores': 20, 'threads': 20, 'boost': 5.3, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 580},
    {'vendor': 'Intel', 'name': 'Intel Core i9-13900', 'year': 2023, 'cores': 24, 'threads': 32, 'boost': 5.6, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 590},
    {'vendor': 'Intel', 'name': 'Intel Core Ultra 7 265K', 'year': 2024, 'cores': 20, 'threads': 20, 'boost': 5.5, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 125, 'perf': 595},
    {'vendor': 'Intel', 'name': 'Intel Core Ultra 7 265KF', 'year': 2024, 'cores': 20, 'threads': 20, 'boost': 5.5, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 125, 'perf': 595},
    {'vendor': 'Intel', 'name': 'Intel Core i7-14700K', 'year': 2023, 'cores': 20, 'threads': 28, 'boost': 5.6, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 125, 'perf': 600},
    {'vendor': 'Intel', 'name': 'Intel Core i7-14700KF', 'year': 2023, 'cores': 20, 'threads': 28, 'boost': 5.6, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 125, 'perf': 600},
    {'vendor': 'Intel', 'name': 'Intel Core i9-14900', 'year': 2024, 'cores': 24, 'threads': 32, 'boost': 5.8, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 600},
    {'vendor': 'Intel', 'name': 'Intel Core Ultra 9 285', 'year': 2024, 'cores': 24, 'threads': 24, 'boost': 5.6, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 610},
    {'vendor': 'Intel', 'name': 'Intel Core Ultra 9 285K', 'year': 2024, 'cores': 24, 'threads': 24, 'boost': 5.7, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 125, 'perf': 625},
    {'vendor': 'Intel', 'name': 'Intel Core i9-13900K', 'year': 2022, 'cores': 24, 'threads': 32, 'boost': 5.8, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 125, 'perf': 625},
    {'vendor': 'Intel', 'name': 'Intel Core i9-13900KF', 'year': 2022, 'cores': 24, 'threads': 32, 'boost': 5.8, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 125, 'perf': 625},
    {'vendor': 'Intel', 'name': 'Intel Core i9-13900KS', 'year': 2023, 'cores': 24, 'threads': 32, 'boost': 6.0, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 150, 'perf': 635},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 9 7900X3D', 'year': 2023, 'cores': 12, 'threads': 24, 'boost': 5.6, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 120, 'perf': 640},
    {'vendor': 'Intel', 'name': 'Intel Core i9-14900K', 'year': 2023, 'cores': 24, 'threads': 32, 'boost': 6.0, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 125, 'perf': 640},
    {'vendor': 'Intel', 'name': 'Intel Core i9-14900KF', 'year': 2023, 'cores': 24, 'threads': 32, 'boost': 6.0, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 125, 'perf': 640},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 5 7600X3D', 'year': 2024, 'cores': 6, 'threads': 12, 'boost': 4.7, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 65, 'perf': 650},
    {'vendor': 'Intel', 'name': 'Intel Core i9-14900KS', 'year': 2024, 'cores': 24, 'threads': 32, 'boost': 6.2, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 150, 'perf': 650},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 7800X3D', 'year': 2023, 'cores': 8, 'threads': 16, 'boost': 5.0, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 120, 'perf': 690},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 9 7950X3D', 'year': 2023, 'cores': 16, 'threads': 32, 'boost': 5.7, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 120, 'perf': 700},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 9 9900X3D', 'year': 2025, 'cores': 12, 'threads': 24, 'boost': 5.5, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 120, 'perf': 745},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 7 9800X3D', 'year': 2024, 'cores': 8, 'threads': 16, 'boost': 5.2, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 120, 'perf': 760},
    {'vendor': 'AMD', 'name': 'AMD Ryzen 9 9950X3D', 'year': 2025, 'cores': 16, 'threads': 32, 'boost': 5.7, 'pcie_gen': 5, 'pcie_lanes': 16, 'tdp': 170, 'perf': 765},
]


# ---------- Colors ----------
BLACK = (0, 0, 0, 1)
PANEL = (0.05, 0.015, 0.10, 1)
PURPLE = (0.24, 0.04, 0.47, 1)
PURPLE_LIGHT = (0.55, 0.30, 0.85, 1)
DIM = (0.16, 0.09, 0.26, 1)
STOCK_BAR = (0.50, 0.45, 0.70, 1)
FIELD = (0.02, 0.02, 0.04, 1)
WHITE = (1, 1, 1, 1)
GREY = (0.70, 0.66, 0.80, 1)
AMBER = (1, 0.78, 0.10, 1)
RED = (0.96, 0.27, 0.32, 1)
GREEN = (0.38, 0.86, 0.52, 1)

NVIDIA_GREEN = (0.46, 0.72, 0.0, 1)
NVIDIA_PANEL_BG = (0.02, 0.12, 0.02, 1)

AMD_RED = (0.90, 0.15, 0.15, 1)
AMD_PANEL_BG = (0.15, 0.02, 0.02, 1)

INTEL_BLUE = (0.329, 0.004, 0.773, 1)
INTEL_PANEL_BG = (0.05, 0.0, 0.18, 1)

MONO = resource_find("data/fonts/RobotoMono-Regular.ttf") or "Roboto"

Window.clearcolor = BLACK
Window.softinput_mode = "below_target"
if platform.system().lower() in ("windows", "linux", "darwin"):
    Window.size = (1000, 920)

# ---------- Data ----------
MEM_TYPES = {
    "SDR": 1, "DDR1": 2, "DDR2": 2, "DDR3": 2, "DDR4": 2, "GDDR2": 2, "GDDR3": 2, "GDDR4": 2, "GDDR5": 4, "GDDR5X": 8,
    "GDDR6": 8, "GDDR6X": 16, "GDDR7": 16, "HBM": 2, "HBM2": 2, "HBM3": 2, "LPDDR5": 2,
}

NVIDIA_ARCHS = {
    "Celsius": "Celsius (GeForce 256 / 2): Fixed-function era. Compute (TFLOPS) is not meaningful.",
    "Kelvin": "Kelvin (GeForce 3 / 4): DX8 era. Compute (TFLOPS) is not meaningful.",
    "Rankine": "Rankine (GeForce FX): DX9 era. Compute (TFLOPS) is not meaningful.",
    "Curie": "Curie (GeForce 6 / 7): Pre-unified shaders. Compute (TFLOPS) is not meaningful.",
    "Tesla": "Tesla (GeForce 8 / 9 / 200): Shaders use their own clock, so TFLOPS from the core clock is not meaningful.",
    "Fermi": "Fermi Architecture: DX11 Legacy.",
    "Kepler": "Kepler (GTX 600/700): Good headroom, power limits apply.",
    "Maxwell": "Maxwell (GTX 900): High OC scaling, unlocked BIOS potential.",
    "Pascal": "Pascal (GTX 1000): Efficient architecture, voltage scales automatically.",
    "Turing": "Turing (RTX 2000 / GTX 16): Ray Tracing era, power limit sensitive.",
    "Ampere": "Ampere (RTX 3000): High power draw, undervolting highly recommended.",
    "Ada Lovelace": "Ada Lovelace (RTX 4000): Extremely power efficient.",
    "Volta": "Volta (Titan V): HBM2 compute card, sensitive to power limits.",
    "Blackwell": "Blackwell Architecture.",
}

AMD_ARCHS = {
    "Rage / R100": "ATI Rage / Radeon R100: Fixed-function era. Compute (TFLOPS) is not meaningful.",
    "R300 / R400": "Radeon 8500 to X850: Pre-unified shaders. Compute (TFLOPS) is not meaningful.",
    "R500 / TeraScale": "Radeon X1000 / HD 2000-4000: Older design that runs hot, very limited headroom.",
    "GCN / TeraScale": "AMD Legacy GCN: High power draw, benefits from undervolting.",
    "RDNA 1/2/3": "AMD RDNA Architecture: Scales well with memory tuning and undervolting.",
    "RDNA 4": "AMD RDNA 4 (RX 9000): Efficient, responds well to undervolting and memory tuning.",
}

INTEL_ARCHS = {
    "Intel GMA": "Intel GMA integrated graphics (shared memory): practically no overclocking headroom.",
    "Intel Graphics": "Intel Integrated / Arc Graphics Architecture.",
}

ALL_ARCHS = {
    "Auto/Generic": "Generic GPU architecture profile.",
    **NVIDIA_ARCHS,
    **AMD_ARCHS,
    **INTEL_ARCHS,
}

PSU_RATINGS = {
    "80 Plus White":    [(0.20, 0.80), (0.50, 0.80), (1.00, 0.80)],
    "80 Plus Bronze":   [(0.20, 0.82), (0.50, 0.85), (1.00, 0.82)],
    "80 Plus Silver":   [(0.20, 0.85), (0.50, 0.88), (1.00, 0.85)],
    "80 Plus Gold":     [(0.20, 0.87), (0.50, 0.90), (1.00, 0.87)],
    "80 Plus Platinum": [(0.20, 0.90), (0.50, 0.92), (1.00, 0.89)],
    "80 Plus Titanium": [(0.20, 0.92), (0.50, 0.94), (1.00, 0.90)],
    "Not certified":    [(0.20, 0.75), (0.50, 0.75), (1.00, 0.75)],
}
OTHER_POWER = 75
NUM_FIELDS = [
    "bus", "mem_clock", "core_clock", "cores", "power", "voltage",
    "new_mem_clock", "new_core_clock", "new_voltage", "cpu_power", "psu_watts", "vram_gb"
]


class DarkSpinnerOption(SpinnerOption):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_color = OPTION_BG
        self.color = WHITE
        self.font_name = MONO
        self.font_size = sp(12)


def fmt_vram(gb):
    """0.032 -> '32MB', 8 -> '8GB'."""
    gb = float(gb)
    return f"{gb * 1000:.0f}MB" if gb < 1 else f"{gb:g}GB"


def is_locked_card(name):
    """Cards the app treats as non-overclockable (same rule as the rest of the app)."""
    up = name.upper()
    return "NVS" in up or "QUADRO NVS" in up or "VEGA 64" in up


VENDOR_ROW_BG = {
    "NVIDIA": (0.03, 0.10, 0.03, 1),
    "AMD": (0.12, 0.03, 0.03, 1),
    "Intel": (0.05, 0.03, 0.16, 1),
}
VENDOR_TAG = {"NVIDIA": "76b900", "AMD": "ff4d4d", "Intel": "8a7dff"}


# ---------- THEMES ----------
# Every value below is a theme key. apply_theme() copies them into module globals, so the whole app
# (which reads those globals when widgets are built) picks the theme up when the UI is rebuilt.
# Text colors: WHITE = normal text on panels (dark on light themes), ON_ACCENT = text on headers/buttons,
# GREY = secondary text. FONT = list of (regular, bold) font files; the first one found on this device is used
# (looked up in a "fonts" folder next to this program first, then in the system font folders). If none is
# found the theme falls back to the original Roboto Mono.
POPUP_IMG_DEFAULT = "atlas://data/images/defaulttheme/modalview-background"
HB_AMBER, HB_RED, HB_GREEN = (1, 0.82, 0.25, 1), (1, 0.45, 0.45, 1), (0.45, 0.95, 0.55, 1)
_HDR_LIGHT = dict(AMBER=HB_AMBER, RED=HB_RED, GREEN=HB_GREEN)   # status colors that stay readable on a dark header

_LIGHT_ROWS = {"NVIDIA": (0.84, 0.91, 0.80, 1), "AMD": (0.93, 0.83, 0.83, 1), "Intel": (0.85, 0.84, 0.94, 1)}
_LIGHT_TAGS = {"NVIDIA": "3f7d00", "AMD": "c01818", "Intel": "4b3fd0"}
_DARK_ROWS = {"NVIDIA": (0.05, 0.11, 0.05, 1), "AMD": (0.13, 0.05, 0.05, 1), "Intel": (0.07, 0.06, 0.15, 1)}
MONO_DEFAULT = MONO

DEFAULT_THEME = "Default (Purple)"
THEMES = {
    DEFAULT_THEME: dict(
        VENDOR_TINT=True, FONT=None, HDR={},
        BG=BLACK, BLACK=BLACK, PANEL=PANEL, PURPLE=PURPLE, PURPLE_LIGHT=PURPLE_LIGHT, DIM=DIM,
        BTN_OFF=DIM, STOCK_BAR=STOCK_BAR, FIELD=FIELD, FIELD2=(0.09, 0.05, 0.16, 1),
        WHITE=WHITE, GREY=GREY, ON_ACCENT=WHITE, ON_SOFT=GREY, IDLE=PURPLE_LIGHT,
        AMBER=AMBER, RED=RED, GREEN=GREEN,
        POPUP_BG=(0.04, 0.02, 0.08, 1), POPUP_IMG=POPUP_IMG_DEFAULT, OPTION_BG=(0.08, 0.04, 0.12, 1),
        HINT=(0.42, 0.38, 0.52, 1), HINT2=(0.60, 0.54, 0.74, 1),
        SUB_HEX="b7aacc", WARN_HEX="ffb347",
        VENDOR_ROW_BG=dict(VENDOR_ROW_BG), VENDOR_TAG=dict(VENDOR_TAG),
    ),
    "Retro Silver": dict(      # brushed-silver hardware look, Lucida Console
        VENDOR_TINT=False, HDR=_HDR_LIGHT,
        FONT=[("lucon.ttf", "lucon.ttf"), ("cour.ttf", "courbd.ttf")],
        BG=(0.60, 0.61, 0.64, 1), BLACK=(0.92, 0.92, 0.94, 1), PANEL=(0.80, 0.81, 0.83, 1),
        PURPLE=(0.33, 0.35, 0.40, 1), PURPLE_LIGHT=(0.40, 0.44, 0.52, 1), DIM=(0.68, 0.69, 0.72, 1),
        BTN_OFF=(0.45, 0.46, 0.50, 1), STOCK_BAR=(0.42, 0.43, 0.47, 1),
        FIELD=(0.98, 0.98, 1, 1), FIELD2=(0.98, 0.98, 1, 1),
        WHITE=(0.05, 0.05, 0.08, 1), GREY=(0.25, 0.26, 0.31, 1),
        ON_ACCENT=(1, 1, 1, 1), ON_SOFT=(0.85, 0.87, 0.92, 1), IDLE=(0.85, 0.87, 0.92, 1),
        AMBER=(0.70, 0.42, 0.0, 1), RED=(0.75, 0.08, 0.10, 1), GREEN=(0.05, 0.48, 0.15, 1),
        POPUP_BG=(0.72, 0.73, 0.76, 1), POPUP_IMG="", OPTION_BG=(0.90, 0.90, 0.93, 1),
        HINT=(0.45, 0.46, 0.52, 1), HINT2=(0.45, 0.46, 0.52, 1),
        SUB_HEX="3a3f4a", WARN_HEX="a05a00",
        VENDOR_ROW_BG=dict(_LIGHT_ROWS), VENDOR_TAG=dict(_LIGHT_TAGS),
    ),
    "Windows XP": dict(        # Luna blue + green, Tahoma
        VENDOR_TINT=False, HDR=_HDR_LIGHT,
        FONT=[("tahoma.ttf", "tahomabd.ttf"), ("verdana.ttf", "verdanab.ttf")],
        BG=(0.23, 0.43, 0.83, 1), BLACK=(0.98, 0.97, 0.92, 1), PANEL=(0.93, 0.91, 0.84, 1),
        PURPLE=(0.0, 0.33, 0.87, 1), PURPLE_LIGHT=(0.22, 0.58, 0.20, 1), DIM=(0.82, 0.80, 0.72, 1),
        BTN_OFF=(0.20, 0.38, 0.78, 1), STOCK_BAR=(0.50, 0.52, 0.60, 1),
        FIELD=(1, 1, 1, 1), FIELD2=(1, 1, 1, 1),
        WHITE=(0.04, 0.07, 0.20, 1), GREY=(0.25, 0.28, 0.40, 1),
        ON_ACCENT=(1, 1, 1, 1), ON_SOFT=(0.80, 0.88, 1, 1), IDLE=(0.75, 0.92, 0.75, 1),
        AMBER=(0.75, 0.45, 0.0, 1), RED=(0.75, 0.08, 0.08, 1), GREEN=(0.05, 0.50, 0.10, 1),
        POPUP_BG=(0.93, 0.91, 0.84, 1), POPUP_IMG="", OPTION_BG=(1, 1, 0.97, 1),
        HINT=(0.50, 0.50, 0.55, 1), HINT2=(0.50, 0.50, 0.55, 1),
        SUB_HEX="3a4a70", WARN_HEX="b25f00",
        VENDOR_ROW_BG=dict(_LIGHT_ROWS), VENDOR_TAG=dict(_LIGHT_TAGS),
    ),
    "Windows 98": dict(        # teal desktop, grey 3D panels, navy title bars, MS Sans Serif
        VENDOR_TINT=False, HDR=_HDR_LIGHT,
        FONT=[("micross.ttf", "arialbd.ttf"), ("arial.ttf", "arialbd.ttf")],
        BG=(0.0, 0.50, 0.50, 1), BLACK=(0.85, 0.85, 0.85, 1), PANEL=(0.75, 0.75, 0.75, 1),
        PURPLE=(0.0, 0.0, 0.50, 1), PURPLE_LIGHT=(0.45, 0.45, 0.45, 1), DIM=(0.60, 0.60, 0.60, 1),
        BTN_OFF=(0.32, 0.32, 0.32, 1), STOCK_BAR=(0.35, 0.35, 0.35, 1),
        FIELD=(1, 1, 1, 1), FIELD2=(1, 1, 1, 1),
        WHITE=(0, 0, 0, 1), GREY=(0.25, 0.25, 0.25, 1),
        ON_ACCENT=(1, 1, 1, 1), ON_SOFT=(0.80, 0.80, 1, 1), IDLE=(0.75, 1, 1, 1),
        AMBER=(0.60, 0.38, 0.0, 1), RED=(0.70, 0.0, 0.0, 1), GREEN=(0.0, 0.45, 0.0, 1),
        POPUP_BG=(0.75, 0.75, 0.75, 1), POPUP_IMG="", OPTION_BG=(0.92, 0.92, 0.92, 1),
        HINT=(0.45, 0.45, 0.45, 1), HINT2=(0.45, 0.45, 0.45, 1),
        SUB_HEX="404040", WARN_HEX="a05a00",
        VENDOR_ROW_BG=dict(_LIGHT_ROWS), VENDOR_TAG=dict(_LIGHT_TAGS),
    ),
    "MSI": dict(               # black + dragon red, Bahnschrift
        VENDOR_TINT=False, HDR={},
        FONT=[("bahnschrift.ttf", "bahnschrift.ttf"), ("arial.ttf", "arialbd.ttf")],
        BG=(0.02, 0.02, 0.02, 1), BLACK=(0, 0, 0, 1), PANEL=(0.07, 0.07, 0.08, 1),
        PURPLE=(0.50, 0.0, 0.03, 1), PURPLE_LIGHT=(0.86, 0.06, 0.10, 1), DIM=(0.17, 0.17, 0.18, 1),
        BTN_OFF=(0.22, 0.22, 0.24, 1), STOCK_BAR=(0.55, 0.55, 0.58, 1),
        FIELD=(0.02, 0.02, 0.02, 1), FIELD2=(0.10, 0.10, 0.11, 1),
        WHITE=(1, 1, 1, 1), GREY=(0.72, 0.72, 0.74, 1),
        ON_ACCENT=(1, 1, 1, 1), ON_SOFT=(0.95, 0.75, 0.75, 1), IDLE=(1.0, 0.45, 0.45, 1),
        AMBER=(1, 0.78, 0.10, 1), RED=(1.0, 0.30, 0.30, 1), GREEN=(0.38, 0.86, 0.52, 1),
        POPUP_BG=(0.05, 0.05, 0.05, 1), POPUP_IMG=POPUP_IMG_DEFAULT, OPTION_BG=(0.10, 0.10, 0.11, 1),
        HINT=(0.45, 0.45, 0.48, 1), HINT2=(0.60, 0.60, 0.62, 1),
        SUB_HEX="b5b5bb", WARN_HEX="ffb347",
        VENDOR_ROW_BG=dict(_DARK_ROWS), VENDOR_TAG=dict(VENDOR_TAG),
    ),
    "ASUS": dict(              # TUF-style black + amber (dark text on the amber), Agency FB / Bahnschrift
        VENDOR_TINT=False,
        HDR=dict(AMBER=(0.35, 0.18, 0.0, 1), RED=(0.65, 0.0, 0.0, 1), GREEN=(0.0, 0.35, 0.05, 1)),
        FONT=[("arial.ttf", "arialbd.ttf"), ("bahnschrift.ttf", "bahnschrift.ttf")],
        BG=(0.04, 0.04, 0.04, 1), BLACK=(0, 0, 0, 1), PANEL=(0.10, 0.10, 0.09, 1),
        PURPLE=(0.95, 0.60, 0.0, 1), PURPLE_LIGHT=(1.0, 0.72, 0.10, 1), DIM=(0.20, 0.19, 0.16, 1),
        BTN_OFF=(0.62, 0.50, 0.22, 1), STOCK_BAR=(0.55, 0.53, 0.48, 1),
        FIELD=(0.03, 0.03, 0.03, 1), FIELD2=(0.12, 0.12, 0.11, 1),
        WHITE=(1, 1, 1, 1), GREY=(0.75, 0.73, 0.68, 1),
        ON_ACCENT=(0.05, 0.03, 0.0, 1), ON_SOFT=(0.30, 0.18, 0.0, 1), IDLE=(0.10, 0.07, 0.0, 1),
        AMBER=(1, 0.78, 0.10, 1), RED=(1.0, 0.35, 0.30, 1), GREEN=(0.45, 0.88, 0.40, 1),
        POPUP_BG=(0.06, 0.06, 0.05, 1), POPUP_IMG=POPUP_IMG_DEFAULT, OPTION_BG=(0.14, 0.13, 0.10, 1),
        HINT=(0.45, 0.43, 0.38, 1), HINT2=(0.60, 0.58, 0.50, 1),
        SUB_HEX="bdb7a6", WARN_HEX="ffb347",
        VENDOR_ROW_BG=dict(_DARK_ROWS), VENDOR_TAG=dict(VENDOR_TAG),
    ),
    "Aero": dict(              # Vista/7 sky blue, Segoe UI
        VENDOR_TINT=False, HDR=_HDR_LIGHT,
        FONT=[("segoeui.ttf", "segoeuib.ttf"), ("tahoma.ttf", "tahomabd.ttf")],
        BG=(0.40, 0.62, 0.85, 1), BLACK=(0.93, 0.97, 1, 1), PANEL=(0.85, 0.92, 0.98, 1),
        PURPLE=(0.24, 0.50, 0.78, 1), PURPLE_LIGHT=(0.10, 0.58, 0.82, 1), DIM=(0.74, 0.84, 0.92, 1),
        BTN_OFF=(0.35, 0.55, 0.75, 1), STOCK_BAR=(0.45, 0.55, 0.65, 1),
        FIELD=(1, 1, 1, 1), FIELD2=(1, 1, 1, 1),
        WHITE=(0.05, 0.12, 0.22, 1), GREY=(0.22, 0.33, 0.45, 1),
        ON_ACCENT=(1, 1, 1, 1), ON_SOFT=(0.85, 0.93, 1, 1), IDLE=(0.80, 0.95, 1, 1),
        AMBER=(0.78, 0.47, 0.0, 1), RED=(0.78, 0.10, 0.10, 1), GREEN=(0.05, 0.52, 0.20, 1),
        POPUP_BG=(0.78, 0.88, 0.96, 1), POPUP_IMG="", OPTION_BG=(0.94, 0.97, 1, 1),
        HINT=(0.45, 0.52, 0.60, 1), HINT2=(0.45, 0.52, 0.60, 1),
        SUB_HEX="2f4a66", WARN_HEX="b25f00",
        VENDOR_ROW_BG=dict(_LIGHT_ROWS), VENDOR_TAG=dict(_LIGHT_TAGS),
    ),
    "Glass": dict(             # clearer ice-blue / cyan glass; translucent surfaces and high-contrast text
        VENDOR_TINT=False, HDR={},
        FONT=[("segoeui.ttf", "segoeuib.ttf"), ("arial.ttf", "arialbd.ttf")],
        # Keep the window backdrop dark; translucent panels, cards and fields layer over it.
        BG=(0.012, 0.035, 0.070, 1), BLACK=(0.018, 0.075, 0.125, 0.48), PANEL=(0.10, 0.34, 0.48, 0.42),
        PURPLE=(0.035, 0.22, 0.34, 0.86), PURPLE_LIGHT=(0.12, 0.68, 0.86, 0.96), DIM=(0.46, 0.78, 0.88, 0.24),
        BTN_OFF=(0.08, 0.34, 0.48, 0.76), STOCK_BAR=(0.38, 0.76, 0.88, 0.66),
        FIELD=(0.012, 0.065, 0.112, 0.54), FIELD2=(0.035, 0.16, 0.23, 0.62),
        WHITE=(0.97, 0.995, 1.0, 1), GREY=(0.76, 0.90, 0.96, 1),
        ON_ACCENT=(0.985, 1.0, 1.0, 1), ON_SOFT=(0.82, 0.94, 0.99, 1), IDLE=(0.42, 0.88, 1.0, 1),
        AMBER=(1.0, 0.80, 0.30, 1), RED=(1.0, 0.48, 0.52, 1), GREEN=(0.34, 0.96, 0.72, 1),
        POPUP_BG=(0.018, 0.085, 0.135, 0.94), POPUP_IMG="", OPTION_BG=(0.045, 0.19, 0.27, 0.92),
        HINT=(0.66, 0.84, 0.91, 1), HINT2=(0.77, 0.91, 0.96, 1),
        SUB_HEX="d2f2fb", WARN_HEX="ffe08a",
        VENDOR_ROW_BG={"NVIDIA": (0.28, 0.84, 0.55, 0.20), "AMD": (1.0, 0.40, 0.46, 0.20), "Intel": (0.48, 0.62, 1.0, 0.22)},
        VENDOR_TAG={"NVIDIA": "8ff0a4", "AMD": "ff9299", "Intel": "b7c5ff"},
    ),
    "White": dict(             # clean light mode with dark slate text and blue accents
        VENDOR_TINT=False, HDR=_HDR_LIGHT,
        FONT=[("segoeui.ttf", "segoeuib.ttf"), ("arial.ttf", "arialbd.ttf")],
        BG=(0.94, 0.96, 0.98, 1), BLACK=(0.985, 0.99, 1, 1), PANEL=(0.89, 0.925, 0.96, 1),
        PURPLE=(0.16, 0.30, 0.47, 1), PURPLE_LIGHT=(0.18, 0.43, 0.70, 1), DIM=(0.78, 0.83, 0.88, 1),
        BTN_OFF=(0.35, 0.45, 0.57, 1), STOCK_BAR=(0.64, 0.68, 0.73, 1),
        FIELD=(1, 1, 1, 1), FIELD2=(0.96, 0.98, 1, 1),
        WHITE=(0.08, 0.13, 0.20, 1), GREY=(0.30, 0.38, 0.48, 1),
        ON_ACCENT=(1, 1, 1, 1), ON_SOFT=(0.88, 0.93, 0.98, 1), IDLE=(0.16, 0.43, 0.70, 1),
        AMBER=(0.72, 0.43, 0.02, 1), RED=(0.72, 0.10, 0.12, 1), GREEN=(0.06, 0.48, 0.20, 1),
        POPUP_BG=(0.95, 0.97, 0.99, 1), POPUP_IMG="", OPTION_BG=(0.98, 0.99, 1, 1),
        HINT=(0.43, 0.50, 0.58, 1), HINT2=(0.43, 0.50, 0.58, 1),
        SUB_HEX="30465f", WARN_HEX="9a5900",
        VENDOR_ROW_BG=dict(_LIGHT_ROWS), VENDOR_TAG=dict(_LIGHT_TAGS),
    ),
    "Core Extreme (Classic Intel)": dict(  # charcoal, brushed steel and small multicolor package accents
        VENDOR_TINT=False,
        HDR=dict(AMBER=(0.95, 0.70, 0.22, 1), RED=(0.88, 0.29, 0.26, 1), GREEN=(0.30, 0.76, 0.48, 1)),
        FONT=[("segoeui.ttf", "segoeuib.ttf"), ("arial.ttf", "arialbd.ttf")],
        # The reference packaging is graphite/black with a silver sweep; color is restricted to a tiny pixel accent.
        BG=(0.022, 0.025, 0.031, 1), BLACK=(0.038, 0.043, 0.052, 1), PANEL=(0.095, 0.105, 0.122, 1),
        PURPLE=(0.165, 0.182, 0.205, 1), PURPLE_LIGHT=(0.315, 0.345, 0.385, 1), DIM=(0.145, 0.158, 0.180, 1),
        BTN_OFF=(0.225, 0.247, 0.275, 1), STOCK_BAR=(0.455, 0.485, 0.525, 1),
        FIELD=(0.030, 0.035, 0.043, 1), FIELD2=(0.075, 0.086, 0.102, 1),
        WHITE=(0.955, 0.965, 0.980, 1), GREY=(0.675, 0.705, 0.745, 1),
        ON_ACCENT=(0.975, 0.980, 0.990, 1), ON_SOFT=(0.805, 0.830, 0.865, 1), IDLE=(0.790, 0.850, 0.920, 1),
        AMBER=(0.96, 0.70, 0.24, 1), RED=(0.95, 0.35, 0.32, 1), GREEN=(0.35, 0.82, 0.50, 1),
        POPUP_BG=(0.045, 0.051, 0.062, 1), POPUP_IMG="", OPTION_BG=(0.115, 0.130, 0.150, 1),
        HINT=(0.500, 0.535, 0.585, 1), HINT2=(0.635, 0.675, 0.730, 1),
        SUB_HEX="d5dbe4", WARN_HEX="f0c66f",
        VENDOR_ROW_BG={"NVIDIA": (0.045, 0.105, 0.070, 1), "AMD": (0.135, 0.055, 0.055, 1), "Intel": (0.045, 0.075, 0.125, 1)},
        VENDOR_TAG={"NVIDIA": "9bd36a", "AMD": "ff8c82", "Intel": "82bdf5"},
    ),
}
CURRENT_THEME = DEFAULT_THEME
HDR_STATUS = {}
THEME_FILE = "oc_theme.json"

_FONT_INDEX = None


def _font_index():
    """lower-case file name -> path, for the local fonts folder and the usual system font folders."""
    global _FONT_INDEX
    if _FONT_INDEX is not None:
        return _FONT_INDEX
    idx = {}
    here = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
    dirs = [os.path.join(here, "fonts"), os.path.join(os.getcwd(), "fonts"),
            os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts"),
            "/system/fonts", "/Library/Fonts", "/System/Library/Fonts", "/System/Library/Fonts/Supplemental",
            "/usr/share/fonts", os.path.expanduser("~/.fonts"), os.path.expanduser("~/.local/share/fonts"),
            os.path.expanduser("~/Library/Fonts")]
    for d in dirs:
        try:
            if not os.path.isdir(d):
                continue
            for root, _dirs, files in os.walk(d):
                for fn in files:
                    idx.setdefault(fn.lower(), os.path.join(root, fn))
        except Exception:
            pass
    _FONT_INDEX = idx
    return idx


def _resolve_font(key, pairs):
    if not pairs:
        return MONO_DEFAULT
    idx = _font_index()
    for reg, bold in pairs:
        rp = idx.get(reg.lower())
        if rp:
            bp = idx.get(bold.lower(), rp)
            name = "ocfont_" + re.sub(r"\W", "_", key)
            try:
                LabelBase.register(name=name, fn_regular=rp, fn_bold=bp)
                return name
            except Exception:
                return MONO_DEFAULT
    return MONO_DEFAULT


def apply_theme(name):
    """Copy a theme into the module-level color/font globals (widgets read them when they are built)."""
    global CURRENT_THEME, HDR_STATUS, MONO
    if name not in THEMES:
        name = DEFAULT_THEME
    t = THEMES[name]
    for k, v in t.items():
        if k not in ("FONT", "HDR"):
            globals()[k] = v
    MONO = _resolve_font(name, t.get("FONT"))
    CURRENT_THEME = name
    # status text sits on the header: map the normal status colors to ones that are readable there
    HDR_STATUS = {tuple(t[k]): v for k, v in t.get("HDR", {}).items()}
    Window.clearcolor = t["BG"]


def load_theme_pref():
    try:
        if os.path.exists(THEME_FILE):
            with open(THEME_FILE, "r") as f:
                name = json.load(f).get("theme", DEFAULT_THEME)
            # Migrate the previous label so existing users keep their selected theme.
            name = {"Core Extreme (Classic Intel)": "Core Extreme (Classic Intel)"}.get(name, name)
            return name if name in THEMES else DEFAULT_THEME
    except Exception:
        pass
    return DEFAULT_THEME


def save_theme_pref(name):
    try:
        with open(THEME_FILE, "w") as f:
            json.dump({"theme": name}, f)
    except Exception:
        pass


apply_theme(DEFAULT_THEME)


class GpuRow(RecycleDataViewBehavior, Button):
    """One line of the GPU CATEGORY list (two lines of text: name + key specs)."""
    gpu_id = NumericProperty(0)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.markup = True
        self.halign = "left"
        self.valign = "middle"
        self.font_name = MONO
        self.font_size = sp(12)
        self.color = WHITE
        self.background_normal = ""
        self.background_down = ""
        self.bind(size=lambda i, s: setattr(i, "text_size", (s[0] - dp(20), s[1])))
        self.bind(on_release=self._picked)

    def _picked(self, *_):
        app = App.get_running_app()
        if app is not None:
            app.pick_gpu(self.gpu_id)


# ---------- Calculation & Rich Alerts Engine ----------
def efficiency_at(load, points):
    if load <= points[0][0]:
        return points[0][1]
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        if load <= x2:
            return y1 + (y2 - y1) * (load - x1) / (x2 - x1)
    return points[-1][1]


def calculate(v, gpu_name=""):
    r = {}
    mult = MEM_TYPES.get(v["mem_name"], 8)
    pts = PSU_RATINGS.get(v["rating_name"], PSU_RATINGS["80 Plus Bronze"])

    r["speed_old"] = v["mem_clock"] * mult / 1000
    r["speed_new"] = v["new_mem_clock"] * mult / 1000
    r["bw_old"] = r["speed_old"] * v["bus"] / 8
    r["bw_new"] = r["speed_new"] * v["bus"] / 8
    r["mem_gain"] = (r["bw_new"] / r["bw_old"] - 1) * 100 if r["bw_old"] > 0 else 0

    r["tf_old"] = v["cores"] * 2 * v["core_clock"] / 1_000_000
    r["tf_new"] = v["cores"] * 2 * v["new_core_clock"] / 1_000_000
    r["core_gain"] = (v["new_core_clock"] / v["core_clock"] - 1) * 100 if v["core_clock"] > 0 else 0

    r["p_new"] = v["power"] * (v["new_core_clock"] / v["core_clock"]) * (v["new_voltage"] / v["voltage"]) ** 2 if v["core_clock"] > 0 and v["voltage"] > 0 else v["power"]
    r["p_gain"] = (r["p_new"] / v["power"] - 1) * 100 if v["power"] > 0 else 0

    r["tot_old"] = v["cpu_power"] + v["power"] + OTHER_POWER
    r["tot_new"] = v["cpu_power"] + r["p_new"] + OTHER_POWER
    r["load_old"] = r["tot_old"] / v["psu_watts"] * 100 if v["psu_watts"] > 0 else 0
    r["load_new"] = r["tot_new"] / v["psu_watts"] * 100 if v["psu_watts"] > 0 else 0
    r["rec_psu"] = math.ceil(r["tot_new"] / 0.8 / 50) * 50

    r["eff_old"] = efficiency_at(r["tot_old"] / v["psu_watts"], pts) if v["psu_watts"] > 0 else 0.8
    r["eff_new"] = efficiency_at(r["tot_new"] / v["psu_watts"], pts) if v["psu_watts"] > 0 else 0.8
    r["wall_old"] = r["tot_old"] / r["eff_old"] if r["eff_old"] > 0 else r["tot_old"]
    r["wall_new"] = r["tot_new"] / r["eff_new"] if r["eff_new"] > 0 else r["tot_new"]
    r["heat_old"] = r["wall_old"] - r["tot_old"]
    r["heat_new"] = r["wall_new"] - r["tot_new"]

    w = []
    gpu_upper = gpu_name.upper()
    arch_name = v.get("arch_name", "Auto/Generic")

    if "NVS" in gpu_upper or "QUADRO NVS" in gpu_upper or "VEGA 64" in gpu_upper:
        r["verdict"], r["vcolor"] = "RESTRICTED", RED
        w.append((RED, "Overclocking Locked: Architecture does not support OC."))
    else:
        if r["load_new"] > 100:
            r["verdict"], r["vcolor"] = "CHANGE PSU", RED
            w.append((RED, f"PSU Overload Warning: System power ({r['tot_new']:.0f}W) exceeds PSU rated capacity ({v['psu_watts']:.0f}W)! Upgrade immediately."))
        elif r["load_new"] > 90:
            r["verdict"], r["vcolor"] = "CHANGE PSU", RED
            w.append((RED, f"PSU Critical Load: Load is at {r['load_new']:.0f}%. High risk of system shutdown under heavy load."))
        elif r["load_new"] > 80:
            r["verdict"], r["vcolor"] = "BORDERLINE", AMBER
            w.append((AMBER, f"PSU High Load: Load is at {r['load_new']:.0f}%. Consider a higher wattage PSU for stability."))
        else:
            r["verdict"], r["vcolor"] = "OK", GREEN

    if "VEGA 56" in gpu_upper:
        w.append((AMBER, "RX Vega 56: Unlocked via Vega 64 BIOS flash (Requires Samsung VRAM)."))

    if "QUADRO" in gpu_upper or "QUADRO K" in gpu_upper:
        w.append((AMBER, "Quadro Card: Requires Nvidia Inspector / Maxwell BIOS Tweaker for custom VBIOS flashing."))

    if re.search(r"MOBILE|LAPTOP|MAX-Q|\b\d{3,4}M\b", gpu_upper):
        w.append((AMBER, "Laptop GPU Warning: Thermal dissipation is limited. Watch temperatures carefully."))

    if arch_name in ALL_ARCHS and arch_name != "Auto/Generic":
        w.append((AMBER, f"Arch Note: {ALL_ARCHS[arch_name]}"))

    if not ("NVS" in gpu_upper or "QUADRO NVS" in gpu_upper or "VEGA 64" in gpu_upper):
        w.append((AMBER, "OC Advice: Raise clock speeds in safe steps of +10 MHz to +15 MHz and run stress tests."))

    return r, w


# ---------- Deep PnP & Hardware Inspector ----------
def is_integrated_gpu(name):
    upper = name.upper()
    igpu_keywords = [
        "INTEL(R) HD GRAPHICS", "INTEL(R) UHD GRAPHICS", "INTEL HD GRAPHICS",
        "INTEL IRIS", "RADEON(TM) GRAPHICS", "VEGA 3", "VEGA 6", "VEGA 8", "VEGA 11",
        "MICROSOFT BASIC DISPLAY ADAPTER", "STANDARD VGA"
    ]
    return any(k in upper for k in igpu_keywords) and not ("NVIDIA" in upper or "GEFORCE" in upper or "QUADRO" in upper or "NVS" in upper or "RADEON RX" in upper or "ARC" in upper)


def detect_hardware_specs():
    specs = {
        "gpu_name": "", "vram_gb": "", "driver_version": "N/A",
        "core_clock": "", "mem_clock": "", "bus": "", "power": "", "cores": "", "arch": "Auto/Generic", "mem_type": "GDDR6", "voltage": ""
    }
    
    if platform.system() == "Windows":
        try:
            ps_cmd = "Get-CimInstance Win32_PnPEntity | Where-Object {$_.PNPClass -eq 'Display'} | Select-Object Name, DeviceID | ConvertTo-Json"
            cmd = ["powershell", "-Command", ps_cmd]
            out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, timeout=5).decode('utf-8', errors='ignore')
            data = json.loads(out)
            items = data if isinstance(data, list) else [data] if isinstance(data, dict) else []
            
            selected_name = ""
            for item in items:
                name = item.get("Name", "")
                if name and not is_integrated_gpu(name):
                    selected_name = name
                    break
            
            if not selected_name and items:
                selected_name = items[0].get("Name", "")

            specs["gpu_name"] = selected_name

            try:
                ps_vram = "Get-CimInstance Win32_VideoController | Select-Object AdapterRAM, DriverVersion | ConvertTo-Json"
                out_vram = subprocess.check_output(["powershell", "-Command", ps_vram], stderr=subprocess.DEVNULL, timeout=3).decode('utf-8', errors='ignore')
                vram_data = json.loads(out_vram)
                v_items = vram_data if isinstance(vram_data, list) else [vram_data] if isinstance(vram_data, dict) else []
                for vi in v_items:
                    ram_bytes = vi.get("AdapterRAM", 0)
                    if ram_bytes and isinstance(ram_bytes, int) and ram_bytes > 0:
                        specs["vram_gb"] = str(round(ram_bytes / (1024**3)))
                        specs["driver_version"] = vi.get("DriverVersion", "N/A")
                        break
            except Exception:
                pass

            name_up = specs["gpu_name"].upper()
            if "NVIDIA" in name_up or "GEFORCE" in name_up or "QUADRO" in name_up or "NVS" in name_up:
                if "RTX 5" in name_up: specs["arch"] = "Blackwell"
                elif "RTX 4" in name_up: specs["arch"] = "Ada Lovelace"
                elif "RTX 3" in name_up: specs["arch"] = "Ampere"
                elif "RTX 2" in name_up or "GTX 16" in name_up: specs["arch"] = "Turing"
                elif "GTX 10" in name_up: specs["arch"] = "Pascal"
                elif "GTX 9" in name_up or "QUADRO K" in name_up: specs["arch"] = "Maxwell"
                elif "GTX 6" in name_up or "GTX 7" in name_up: specs["arch"] = "Kepler"
                else: specs["arch"] = "Fermi"
            elif "RADEON" in name_up or "AMD" in name_up:
                mm = re.search(r"\bRX\s*(\d{3,4})\b", name_up)
                if mm and int(mm.group(1)) >= 9000: specs["arch"] = "RDNA 4"
                elif mm and int(mm.group(1)) >= 5000: specs["arch"] = "RDNA 1/2/3"
                else: specs["arch"] = "GCN / TeraScale"
            elif "INTEL" in name_up or "ARC" in name_up:
                specs["arch"] = "Intel Graphics"

        except Exception:
            pass

    return specs


# ---------- UI Helpers ----------
def paint(widget, fill, border=None):
    """Paint a themed surface with restrained package-inspired steel highlights."""
    with widget.canvas.before:
        Color(*fill)
        rect = Rectangle(pos=widget.pos, size=widget.size)

    glass_top = glass_side = None
    core_sheen = core_edge = core_sweep = None
    if CURRENT_THEME == "Glass":
        # Glass theme: two translucent overlays create a soft reflection without hiding text.
        with widget.canvas.before:
            Color(0.72, 0.94, 1.0, 0.105)
            glass_top = Rectangle(pos=(widget.x, widget.y + widget.height * 0.72),
                                  size=(widget.width, widget.height * 0.28))
            Color(0.42, 0.84, 1.0, 0.055)
            glass_side = Rectangle(pos=(widget.x, widget.y),
                                   size=(max(dp(2), widget.width * 0.012), widget.height))
    elif CURRENT_THEME == "Core Extreme (Classic Intel)":
        # Matte graphite base with a very low-opacity brushed-steel sheen. No blanket gold overlay.
        with widget.canvas.before:
            Color(0.88, 0.91, 0.96, 0.045)
            core_sheen = Rectangle(pos=(widget.x, widget.y + widget.height * 0.86),
                                   size=(widget.width, max(dp(1), widget.height * 0.14)))
            Color(0.72, 0.77, 0.84, 0.10)
            core_edge = Rectangle(pos=(widget.x, widget.y),
                                  size=(max(dp(1), widget.width * 0.004), widget.height))
        if getattr(widget, "_core_brand_sweep", False):
            with widget.canvas.before:
                Color(0.62, 0.67, 0.74, 0.065)
                core_sweep = Line(bezier=[
                    widget.x + widget.width * 0.18, widget.y + widget.height * 0.92,
                    widget.x + widget.width * 0.38, widget.y + widget.height * 0.78,
                    widget.x + widget.width * 0.58, widget.y + widget.height * 0.60,
                    widget.x + widget.width * 0.82, widget.y + widget.height * 0.72,
                    widget.x + widget.width * 0.98, widget.y + widget.height * 0.82,
                ], width=dp(22))

    line = None
    core_tiles = []
    if border:
        with widget.canvas.after:
            if CURRENT_THEME == "Glass":
                Color(0.55, 0.88, 1.0, 0.82)
                line = Line(rectangle=(*widget.pos, *widget.size), width=dp(1.15))
            elif CURRENT_THEME == "Core Extreme (Classic Intel)":
                Color(0.66, 0.71, 0.78, 0.78)
                line = Line(rectangle=(*widget.pos, *widget.size), width=dp(1.0))
            else:
                Color(*border)
                line = Line(rectangle=(*widget.pos, *widget.size), width=dp(1))

            # A small four-colour pixel ribbon appears only in the app's main title bar.
            # It echoes the package corner detail without turning the UI gold or multicoloured.
            if CURRENT_THEME == "Core Extreme (Classic Intel)" and getattr(widget, "_core_brand_strip", False):
                palette = ((0.83, 0.20, 0.45, 1), (0.99, 0.56, 0.16, 1),
                           (0.48, 0.31, 0.76, 1), (0.16, 0.58, 0.80, 1),
                           (0.94, 0.76, 0.22, 1))
                for i, color in enumerate(palette):
                    Color(*color)
                    tile = Rectangle(pos=(widget.right - dp(56) + i * dp(11), widget.top - dp(4)),
                                     size=(dp(10), dp(4)))
                    core_tiles.append(tile)

    def sync(*_):
        rect.pos, rect.size = widget.pos, widget.size
        if glass_top is not None:
            glass_top.pos = (widget.x, widget.y + widget.height * 0.72)
            glass_top.size = (widget.width, widget.height * 0.28)
            glass_side.pos = widget.pos
            glass_side.size = (max(dp(2), widget.width * 0.012), widget.height)
        if core_sheen is not None:
            core_sheen.pos = (widget.x, widget.y + widget.height * 0.86)
            core_sheen.size = (widget.width, max(dp(1), widget.height * 0.14))
            core_edge.pos = widget.pos
            core_edge.size = (max(dp(1), widget.width * 0.004), widget.height)
        if core_sweep is not None:
            core_sweep.bezier = [
                widget.x + widget.width * 0.18, widget.y + widget.height * 0.92,
                widget.x + widget.width * 0.38, widget.y + widget.height * 0.78,
                widget.x + widget.width * 0.58, widget.y + widget.height * 0.60,
                widget.x + widget.width * 0.82, widget.y + widget.height * 0.72,
                widget.x + widget.width * 0.98, widget.y + widget.height * 0.82,
            ]
        for i, tile in enumerate(core_tiles):
            tile.pos = (widget.right - dp(56) + i * dp(11), widget.top - dp(4))
        if line:
            line.rectangle = (*widget.pos, *widget.size)
    widget.bind(pos=sync, size=sync)


def mono(text, color=WHITE, size=13, halign="left", bold=False, **kw):
    lbl = Label(text=text, color=color, font_size=sp(size), font_name=MONO,
                bold=bold, halign=halign, valign="middle", **kw)
    lbl.bind(size=lambda i, s: setattr(i, "text_size", s))
    return lbl


def wrap(text, color=WHITE, size=12):
    lbl = Label(text=text, color=color, font_size=sp(size), font_name=MONO,
                halign="left", valign="middle", size_hint_y=None)
    lbl.bind(width=lambda i, w: setattr(i, "text_size", (w, None)))
    lbl.bind(texture_size=lambda i, ts: setattr(i, "height", ts[1] + dp(6)))
    return lbl


def panel(title, tag=""):
    p = BoxLayout(orientation="vertical", size_hint_y=None, opacity=0)
    p.bind(minimum_height=p.setter("height"))
    head = BoxLayout(size_hint_y=None, height=dp(28), padding=[dp(10), 0])
    p.head_box = head
    paint(head, PURPLE)
    head.add_widget(mono(title, ON_ACCENT, 13, bold=True))
    if tag:
        head.add_widget(mono(tag, ON_SOFT, 11, "right"))
    body = BoxLayout(orientation="vertical", size_hint_y=None, padding=dp(10), spacing=dp(8))
    body.bind(minimum_height=body.setter("height"))
    p.add_widget(head)
    p.add_widget(body)
    p.body = body
    paint(p, PANEL, PURPLE_LIGHT)
    
    anim = Animation(opacity=1, duration=0.25)
    anim.start(p)
    return p


class WarnIcon(Widget):
    def __init__(self, color=None, **kw):
        super().__init__(size_hint=(None, None), size=(dp(26), dp(26)), **kw)
        self.color = color or AMBER
        self.bind(pos=self.draw, size=self.draw)

    def draw(self, *_):
        self.canvas.clear()
        x, y = self.pos
        w, h = self.size
        with self.canvas:
            Color(*self.color)
            Triangle(points=[x, y + dp(2), x + w, y + dp(2), x + w / 2, y + h])
            Color(0, 0, 0, 1)
            Rectangle(pos=(x + w / 2 - dp(1.5), y + h * 0.36), size=(dp(3), h * 0.28))
            Rectangle(pos=(x + w / 2 - dp(1.5), y + h * 0.17), size=(dp(3), dp(3)))


class Led(Widget):
    def __init__(self, **kw):
        super().__init__(size_hint=(None, None), size=(dp(14), dp(14)), **kw)
        self.color = IDLE
        self.bind(pos=self.draw, size=self.draw)

    def set(self, color):
        self.color = color
        self.draw()

    def draw(self, *_):
        self.canvas.clear()
        with self.canvas:
            Color(*self.color[:3], 0.3)
            Ellipse(pos=(self.x - dp(3), self.y - dp(3)), size=(self.width + dp(6), self.height + dp(6)))
            Color(*self.color)
            Ellipse(pos=self.pos, size=self.size)


class SegBar(Widget):
    def __init__(self, value=0, color=None, marks=(), **kw):
        super().__init__(size_hint_y=None, height=dp(12), **kw)
        self.value, self.color, self.marks = value, (color or PURPLE_LIGHT), marks
        self.bind(pos=self.draw, size=self.draw)

    def draw(self, *_):
        self.canvas.clear()
        n, gap = 28, dp(2)
        x, y = self.pos
        w, h = self.size
        sw = max((w - gap * (n - 1)) / n, 1)
        with self.canvas:
            for i in range(n):
                lit = (i + 0.5) / n <= min(max(self.value, 0), 1)
                Color(*(self.color if lit else DIM))
                Rectangle(pos=(x + i * (sw + gap), y), size=(sw, h))
            Color(*WHITE)
            for m in self.marks:
                Rectangle(pos=(x + m * w - dp(1), y - dp(3)), size=(dp(2), h + dp(6)))


def warn_row(color, text):
    row = BoxLayout(size_hint_y=None, height=dp(30), spacing=dp(10))
    holder = AnchorLayout(anchor_y="top", size_hint_x=None, width=dp(30))
    holder.add_widget(WarnIcon(color))
    lbl = wrap(text, WHITE, 12)
    lbl.bind(height=lambda i, h: setattr(row, "height", max(h, dp(30))))
    row.add_widget(holder)
    row.add_widget(lbl)
    return row


def kv_row(name, value, color=WHITE):
    row = BoxLayout(size_hint_y=None, height=dp(22))
    row.add_widget(mono(name, GREY, 12))
    row.add_widget(mono(value, color, 12, "right", True))
    return row


def tile(caption, value, delta, dcolor):
    t = BoxLayout(orientation="vertical", padding=dp(8), spacing=dp(2))
    paint(t, BLACK, PURPLE_LIGHT)
    t.add_widget(mono(caption, GREY, 10))
    t.add_widget(mono(value, WHITE, 21, bold=True))
    t.add_widget(mono(delta, dcolor, 12))
    return t


def compare(body, label, old, new, unit, fmt, color):
    body.add_widget(mono(f"{label}   {old:{fmt}} > {new:{fmt}} {unit}", WHITE, 12, size_hint_y=None, height=dp(18)))
    top = max(old, new) if max(old, new) > 0 else 1.0
    body.add_widget(SegBar(old / top, STOCK_BAR))
    body.add_widget(SegBar(new / top, color))



# ---------- COMPATIBILITY engine (CPU + GPU): PCIe link + CPU bottleneck. All numbers are estimates. ----------
PCIE_LANE_GBPS = {1: 0.25, 2: 0.5, 3: 0.985, 4: 1.969, 5: 3.938}     # GB/s per lane, per direction
RES_LOAD = {"720p": 1.35, "1080p": 1.0, "1440p": 0.72, "4K": 0.50}  # relative GPU throughput per frame
RES_CHOICES = list(RES_LOAD.keys())
SLOT_CHOICES = ["Auto (CPU limit)", "PCIe 2.0", "PCIe 3.0", "PCIe 4.0", "PCIe 5.0"]
SLOT_LANE_CHOICES = ["Auto (CPU limit)", "x1", "x4", "x8", "x16"]
LEVEL_NAME = ["GOOD MATCH", "MINOR LIMITS", "NOTICEABLE LOSS", "BAD MATCH"]


def _norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def find_matches(db, text, limit=6):
    """Offline name search. 'rtx 4070', '4070', 'i5 12400f', '5600x' all work. Best match first."""
    typed = _norm(text)
    if len(typed) < 2:
        return []
    tokens = [_norm(t) for t in text.split() if _norm(t)]
    hits = []
    for item in db:
        nn = _norm(item["name"])
        if typed in nn or all(t in nn for t in tokens):
            rank = 0 if nn == typed else (1 if nn.endswith(typed) else 2)
            hits.append((rank, len(nn), item))
    hits.sort(key=lambda h: (h[0], h[1]))
    return [h[2] for h in hits[:limit]]


def pcie_bw(gen, lanes):
    return PCIE_LANE_GBPS[gen] * lanes


def _pcie_penalty(link_bw, gpu):
    """Rough % of frame rate lost because the link is narrower than the card is built for."""
    if link_bw >= 31:
        base = 0.0
    elif link_bw >= 15:
        base = 1.0
    elif link_bw >= 7.5:
        base = 4.0
    elif link_bw >= 3.5:
        base = 10.0
    elif link_bw >= 1.9:
        base = 20.0
    elif link_bw >= 0.9:
        base = 35.0
    else:
        base = 50.0
    scale = min(1.6, max(0.35, 0.35 + gpu["perf"] / 450.0))
    pen = base * scale
    if gpu["vram"] <= 4 and link_bw < 15:      # small VRAM = more traffic over the bus (RX 6500 XT case)
        pen *= 2.2
    return min(pen, 60.0)


def pcie_loss_pct(run_bw, native_bw, gpu):
    return max(0.0, _pcie_penalty(run_bw, gpu) - _pcie_penalty(native_bw, gpu))


def _level_from_loss(loss):
    return 0 if loss < 3 else (1 if loss < 10 else (2 if loss < 25 else 3))


def compat_report(cpu, gpu, res="1080p", slot_gen=None, gpu_core=None, gpu_mem=None, cpu_ghz=None,
                  stock_core=None, stock_mem=None, slot_lanes=None):
    """Compare a CPU/GPU pair using the built-in relative performance indexes.

    slot_gen and slot_lanes describe the motherboard's physical graphics slot.
    None means that the motherboard detail is unknown / auto-estimated.
    OC arguments are optional; omitted values mean stock clocks.
    """
    if res not in RES_LOAD:
        res = "1080p"
    notes = []

    def note(level, text):
        notes.append((level, text))

    out = {"cpu": cpu, "gpu": gpu, "res": res, "notes": notes, "pcie": None, "fits": True, "fit_text": ""}

    # ----- PCIe generation + lane-width negotiation -----
    pcie_loss = 0.0
    if gpu.get("pcie_gen") is None or gpu.get("pcie_lanes") is None:
        if gpu.get("legacy"):
            # every card in the list without PCIe data is AGP / PCI / onboard graphics from before PCI Express
            out["pcie_level"] = 3
            out["fits"] = False
            if gpu.get("arch") == "Intel GMA" or "Extreme Graphics" in gpu.get("name", ""):
                out["fit_text"] = "ONBOARD GRAPHICS - NOT A CARD"
                note(3, "This is onboard graphics built into an old motherboard chipset. It is not a card, so it "
                        "cannot be plugged into any slot or paired with this CPU.")
            else:
                out["fit_text"] = "DOES NOT FIT - NO PCIe CONNECTOR"
                note(3, "This card is AGP / PCI, not PCI Express. It does NOT fit and cannot be plugged into a PCIe "
                        "slot, even if the CPU and the motherboard are modern and support PCIe. It only works on an "
                        "old motherboard that has an AGP or PCI slot.")
        else:
            out["pcie_level"] = 0
            note(0, "PCIe details are not present for this GPU in the offline database. Check the card's interface "
                    "and your motherboard manual; physical compatibility cannot be confirmed from this entry.")
    else:
        gpu_gen = int(gpu["pcie_gen"])
        gpu_lanes = int(gpu["pcie_lanes"])
        cpu_gen = int(cpu.get("pcie_gen") or gpu_gen)
        cpu_lanes = int(cpu.get("pcie_lanes") or gpu_lanes)
        effective_gen_limit = min(cpu_gen, int(slot_gen)) if slot_gen else cpu_gen
        run_gen = min(gpu_gen, effective_gen_limit)
        slot_lane_limit = int(slot_lanes) if slot_lanes else gpu_lanes
        run_lanes = min(gpu_lanes, cpu_lanes, slot_lane_limit)
        run_bw = pcie_bw(run_gen, run_lanes)
        native_bw = pcie_bw(gpu_gen, gpu_lanes)
        pcie_loss = pcie_loss_pct(run_bw, native_bw, gpu) if run_bw < native_bw else 0.0

        # Separate theoretical bandwidth shortfall into independent lane and generation effects.
        lane_only_bw = pcie_bw(gpu_gen, run_lanes)
        generation_only_bw = pcie_bw(run_gen, gpu_lanes)
        bandwidth_loss = max(0.0, (1.0 - run_bw / native_bw) * 100.0) if native_bw else 0.0
        lane_loss = max(0.0, (1.0 - run_lanes / gpu_lanes) * 100.0) if gpu_lanes else 0.0
        generation_loss = max(0.0, (1.0 - generation_only_bw / native_bw) * 100.0) if native_bw else 0.0
        lane_matched = run_lanes >= gpu_lanes
        generation_matched = run_gen >= gpu_gen
        out["pcie"] = {
            "gpu_gen": gpu_gen, "gpu_lanes": gpu_lanes,
            "cpu_gen": cpu_gen, "cpu_lanes": cpu_lanes,
            "slot_gen": slot_gen, "slot_lanes": slot_lanes,
            "run_gen": run_gen, "run_lanes": run_lanes,
            "run_bw": run_bw, "native_bw": native_bw,
            "lane_only_bw": lane_only_bw, "generation_only_bw": generation_only_bw,
            "bandwidth_loss": bandwidth_loss, "lane_loss": lane_loss,
            "generation_loss": generation_loss, "lane_matched": lane_matched,
            "generation_matched": generation_matched, "link_matched": lane_matched and generation_matched,
            "loss": pcie_loss,
        }
        out["pcie_level"] = _level_from_loss(pcie_loss)

        if not generation_matched:
            who = "the motherboard slot" if slot_gen and slot_gen < cpu_gen else "this CPU"
            note(_level_from_loss(pcie_loss),
                 f"The GPU supports PCIe {gpu_gen}.0, but {who} limits the link to PCIe {run_gen}.0. "
                 "PCIe is backward compatible; the card should negotiate the lower generation.")
        elif slot_gen and slot_gen > cpu_gen:
            note(0, f"The selected slot is PCIe {slot_gen}.0, while this CPU supports up to PCIe {cpu_gen}.0 "
                    "for this graphics link.")

        if not lane_matched:
            cause = "the motherboard slot" if slot_lanes and slot_lanes < min(gpu_lanes, cpu_lanes) else "the CPU / platform"
            note(_level_from_loss(pcie_loss),
                 f"Lane width is reduced: the GPU is designed for x{gpu_lanes}, but {cause} allows only x{run_lanes}. "
                 f"That is {lane_loss:.0f}% fewer lanes than the card's full interface.")
        if gpu_lanes <= 8 and not generation_matched:
            note(_level_from_loss(pcie_loss),
                 f"This GPU is an x{gpu_lanes} design. A lower PCIe generation cuts its already narrower link bandwidth.")
        if gpu.get("vram", 0) <= 4 and pcie_loss >= 3:
            note(2 if pcie_loss >= 10 else 1,
                 f"The card has {fmt_vram(gpu['vram'])} of VRAM. When a workload exceeds VRAM, assets may spill over "
                 "PCIe, making a restricted link more noticeable; reducing texture settings can help.")
        if cpu.get("year", 9999) < 2011:
            note(0, "On some older platforms, graphics lanes and generation are provided by the motherboard chipset. "
                    "The board manual or a live PCIe link readout is needed to confirm the actual connection.")

    # ----- Resizable BAR hint for Intel Arc -----
    if gpu.get("vendor") == "Intel" and gpu.get("arch") == "Intel Graphics":
        old = (cpu["vendor"] == "Intel" and cpu["year"] < 2020) or (cpu["vendor"] == "AMD" and cpu["year"] < 2019)
        if old:
            note(2, "Intel Arc cards benefit strongly from Resizable BAR. This CPU generation may not support it; "
                    "confirm motherboard BIOS support before buying or testing the card.")
        else:
            note(0, "Intel Arc: enable Resizable BAR / Above 4G Decoding in the BIOS when the platform supports it.")

    # ----- OC scaling -----
    gs = 1.0
    sc = stock_core or gpu["core_clock"]
    sm = stock_mem or gpu["mem_clock"]
    if gpu_core:
        r = gpu_core / sc
        gs += 0.65 * (r - 1)
        if abs(r - 1) > 0.35:
            note(1, f"GPU core {gpu_core:g} MHz is very far from the stock {sc:g} MHz. Check the value.")
    if gpu_mem:
        r = gpu_mem / sm
        gs += 0.25 * (r - 1)
        if abs(r - 1) > 0.35:
            note(1, f"GPU memory {gpu_mem:g} MHz is very far from the stock {sm:g} MHz. Check the value and unit.")
    gs = min(1.6, max(0.4, gs))

    cs = 1.0
    if cpu_ghz:
        r = cpu_ghz / cpu["boost"]
        cs += 0.6 * (r - 1)
        if abs(r - 1) > 0.35:
            note(1, f"CPU {cpu_ghz:g} GHz differs greatly from the listed boost of {cpu['boost']:g} GHz. Check the value.")
    cs = min(1.4, max(0.5, cs))

    # ----- CPU/GPU balance by resolution -----
    # GPU performance index represents estimated frame throughput. Lower pixels per frame at
    # 720p raise the CPU-feed requirement; heavier resolutions reduce it.
    load = gpu["perf"] * gs * RES_LOAD[res]
    cap = cpu["perf"] * cs
    ratio = cap / load if load > 0 else float("inf")
    cpu_loss = max(0.0, (1.0 - ratio) * 100.0) if math.isfinite(ratio) else 0.0
    # When the GPU is slower, this is the share of CPU capacity left waiting for the GPU,
    # not a claim that this percentage of GPU FPS is being lost.
    gpu_headroom = max(0.0, (1.0 - (load / cap)) * 100.0) if cap > 0 else 0.0
    out["bn"] = {
        "load": load, "cap": cap, "ratio": ratio, "loss": cpu_loss,
        "gpu_headroom": gpu_headroom, "skew": max(cpu_loss, gpu_headroom),
        "gpu_scale": gs, "cpu_scale": cs,
    }
    out["bn_level"] = _level_from_loss(cpu_loss)

    rec = None
    if cpu_loss >= 10:
        for c in sorted(CPUS, key=lambda c: c["perf"]):
            if c["perf"] >= load * 0.95:
                rec = c
                break
    out["rec_cpu"] = rec
    out["gpu_limited"] = ratio >= 3.5
    if ratio >= 3.5 and out["fits"]:
        note(1, f"GPU-limited pairing: CPU capacity is about {ratio:.1f}x the estimated GPU throughput. "
                "The GPU is the main performance limit; a stronger graphics card would make a larger difference.")
    elif ratio >= 2.2 and load > 60 and out["fits"]:
        note(0, "The CPU has plenty of headroom for this GPU. In a gaming workload, the GPU is expected to be the limit.")
    if ratio < 1 and gpu.get("legacy"):
        note(0, "This is an older GPU architecture; its performance index is a broad ordering aid, not a modern game benchmark.")

    # ----- Combined estimate -----
    retained = (1.0 - cpu_loss / 100.0) * (1.0 - pcie_loss / 100.0) * 100.0
    if not out["fits"]:
        retained = 0.0
    out["retained"] = retained
    level = max([out["pcie_level"], out["bn_level"]] + [n[0] for n in notes])
    out["level"] = level

    # ----- Power hint -----
    total = gpu["power"] + cpu["tdp"] + OTHER_POWER
    out["psu"] = {"total": total, "rec": int(math.ceil(total / 0.8 / 50.0) * 50)}

    # ----- Deep analysis: every resolution, PCIe generation, and lane width -----
    rows = []
    for rs in RES_CHOICES:
        ld = gpu["perf"] * gs * RES_LOAD[rs]
        lo = max(0.0, (1.0 - cap / ld) * 100.0) if ld > 0 else 0.0
        headroom = max(0.0, (1.0 - ld / cap) * 100.0) if cap > 0 else 0.0
        rows.append({
            "res": rs, "load": ld, "loss": lo, "gpu_headroom": headroom,
            "retained": (1.0 - lo / 100.0) * (1.0 - pcie_loss / 100.0) * 100.0,
            "level": _level_from_loss(lo), "current": rs == res,
        })

    prow, lane_rows = [], []
    if out["pcie"] is not None:
        pc = out["pcie"]
        top_gen = min(pc["gpu_gen"], pc["cpu_gen"])
        for g in range(1, top_gen + 1):
            lanes = pc["run_lanes"]
            bw = pcie_bw(g, lanes)
            ls = pcie_loss_pct(bw, pc["native_bw"], gpu) if bw < pc["native_bw"] else 0.0
            prow.append({"gen": g, "lanes": lanes, "bw": bw, "loss": ls, "current": g == pc["run_gen"]})
        for lanes in (1, 4, 8, 16):
            if lanes <= pc["gpu_lanes"]:
                bw = pcie_bw(pc["run_gen"], lanes)
                ls = pcie_loss_pct(bw, pc["native_bw"], gpu) if bw < pc["native_bw"] else 0.0
                lane_rows.append({"lanes": lanes, "bw": bw, "loss": ls, "current": lanes == pc["run_lanes"]})

    oc = None
    if gpu_core or gpu_mem:
        stock_load = gpu["perf"] * RES_LOAD[res]
        oc_load = load
        real = min(oc_load, cap) / min(stock_load, cap) - 1 if min(stock_load, cap) > 0 else 0.0
        oc = {"wanted": (gs - 1.0) * 100.0, "real": real * 100.0, "cpu_limited": oc_load > cap}
    out["deep"] = {"res_rows": rows, "pcie_rows": prow, "lane_rows": lane_rows, "oc": oc}
    return out

# ---------- App ----------
class OCApp(App):
    title = "OC//CALC v2.0.2-beta4 - Extreme Overclock & Experiment Suite"

    def _make_ui(self):
        self.fields = {}
        self._last_result = None
        self.panels = []
        self.spinners_list = []
        self.buttons_list = []

        self.root_layout = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(8))

        # Header
        self.head_box = BoxLayout(size_hint_y=None, height=dp(58), padding=[dp(12), dp(6)])
        self.head_box._core_brand_strip = True
        paint(self.head_box, PURPLE, PURPLE_LIGHT)
        left = BoxLayout(orientation="vertical")
        left.add_widget(mono("OC//CALC v2.0.2-beta4", ON_ACCENT, 20, bold=True))
        left.add_widget(mono("EXTREME OVERCLOCK & EXPERIMENT BENCH", ON_SOFT, 10))
        right = BoxLayout(orientation="vertical", size_hint_x=None, width=dp(120))
        led_row = BoxLayout(spacing=dp(6))
        tb_holder = AnchorLayout(anchor_x="right", anchor_y="center", size_hint_x=None, width=dp(58))
        self.theme_btn = Button(text="THEMES", size_hint=(None, None), size=(dp(58), dp(20)), bold=True,
                                font_name=MONO, font_size=sp(9), color=ON_ACCENT, background_normal="",
                                background_color=(1, 1, 1, 0.20))
        self.theme_btn.bind(on_release=self.open_theme_menu)
        tb_holder.add_widget(self.theme_btn)
        led_holder = AnchorLayout(anchor_x="center", anchor_y="center", size_hint_x=None, width=dp(16))
        self.led = Led()
        led_holder.add_widget(self.led)
        led_row.add_widget(Widget())            # spacer: lamp + THEMES button stay on the right
        led_row.add_widget(led_holder)
        led_row.add_widget(tb_holder)
        self.status = mono("READY", IDLE, 11, "right", True)
        right.add_widget(led_row)
        right.add_widget(self.status)
        self.head_box.add_widget(left)
        self.head_box.add_widget(right)
        self.root_layout.add_widget(self.head_box)

        self.content_container = BoxLayout(orientation="horizontal", spacing=dp(10))
        self.root_layout.add_widget(self.content_container)

        self.inputs_scroll = ScrollView(do_scroll_x=False, bar_color=PURPLE_LIGHT, size_hint_x=0.48)
        self.inputs_main = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(10), padding=[0, 0, dp(4), dp(20)])
        self.inputs_main.bind(minimum_height=self.inputs_main.setter("height"))
        self.inputs_scroll.add_widget(self.inputs_main)

        self.results_scroll = ScrollView(do_scroll_x=False, bar_color=PURPLE_LIGHT, size_hint_x=0.52)
        if CURRENT_THEME == "Core Extreme (Classic Intel)":
            self.results_scroll._core_brand_sweep = True
            paint(self.results_scroll, BG)
        self.results = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(10), padding=[0, 0, 0, dp(20)])
        self.results.bind(minimum_height=self.results.setter("height"))
        self.results_scroll.add_widget(self.results)

        # 1. GPU-Z Inspector Panel
        p_gpuz = panel("GPU-Z BUILT-IN", "DEEP SCANNER")
        self.panels.append(p_gpuz)
        self.gpuz_btn = Button(text="DETECT REAL HARDWARE (BENCHMARK)", size_hint_y=None, height=dp(34), bold=True,
                               font_name=MONO, font_size=sp(11), color=ON_ACCENT,
                               background_normal="", background_color=PURPLE_LIGHT)
        self.gpuz_btn.bind(on_release=self.run_gpuz_detection)
        self.buttons_list.append(self.gpuz_btn)
        p_gpuz.body.add_widget(self.gpuz_btn)
        self.inputs_main.add_widget(p_gpuz)

        # 2. GPU Specs Panel
        p1 = panel("GPU CONFIGURATION", "CARD")
        self.panels.append(p1)
        
        self.gpu_cat_btn = Button(text=f"GPU CATEGORY  |  {len(GPUS)} CARDS  |  OFFLINE", size_hint_y=None,
                                  height=dp(38), bold=True, font_name=MONO, font_size=sp(12), color=ON_ACCENT,
                                  background_normal="", background_color=PURPLE_LIGHT)
        self.gpu_cat_btn.bind(on_release=self.open_gpu_category)
        p1.body.add_widget(self.gpu_cat_btn)

        self.compat_btn = Button(text="COMPATIBILITY  |  CPU + GPU  |  PCIe & BOTTLENECK", size_hint_y=None,
                                 height=dp(38), bold=True, font_name=MONO, font_size=sp(12), color=ON_ACCENT,
                                 background_normal="", background_color=PURPLE_LIGHT)
        self.compat_btn.bind(on_release=self.open_compat)
        p1.body.add_widget(self.compat_btn)

        gpu_name_row = BoxLayout(size_hint_y=None, height=dp(36), spacing=dp(8))
        gpu_name_row.add_widget(mono("NAME", GREY, 12))
        ti_gpu = self.input_box("gpu", "", text=True)
        ti_gpu.bind(text=self.on_gpu_name_change)
        gpu_name_row.add_widget(ti_gpu)
        p1.body.add_widget(gpu_name_row)

        p1.body.add_widget(self.labeled("ARCH", self.spinner(ALL_ARCHS.keys(), "Auto/Generic", "arch_spin")))
        p1.body.add_widget(self.labeled("MEMORY", self.spinner(MEM_TYPES.keys(), "GDDR6", "mem_spin")))
        self.row(p1.body, "VRAM  GB", [("vram_gb", "")])
        self.row(p1.body, "BUS  bit", [("bus", "")])
        self.row(p1.body, "CORES", [("cores", "")])
        self.row(p1.body, "POWER  W", [("power", "")])
        self.inputs_main.add_widget(p1)

        # 3. Clocks & Voltage Panel
        p2 = panel("CLOCKS & VOLTAGE", "STOCK / OC")
        self.panels.append(p2)
        hdr = BoxLayout(size_hint_y=None, height=dp(18), spacing=dp(8))
        for t in ("", "STOCK", "OVERCLOCK"):
            hdr.add_widget(mono(t, PURPLE_LIGHT, 11, "center", True))
        p2.body.add_widget(hdr)
        self.row(p2.body, "VRAM  MHz", [("mem_clock", ""), ("new_mem_clock", "")])
        self.row(p2.body, "CORE  MHz", [("core_clock", ""), ("new_core_clock", "")])
        self.row(p2.body, "VOLT  V", [("voltage", ""), ("new_voltage", "")])
        self.inputs_main.add_widget(p2)

        # 4. System & PSU Panel
        p3 = panel("SYSTEM POWER", "PSU")
        self.panels.append(p3)
        self.row(p3.body, "CPU  W", [("cpu_power", "")])
        self.row(p3.body, "PSU  W", [("psu_watts", "")])
        p3.body.add_widget(self.labeled("80 PLUS", self.spinner(PSU_RATINGS.keys(), "80 Plus Bronze", "psu_spin")))
        self.inputs_main.add_widget(p3)

        # 5. Action Buttons Panel
        btn_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(170), spacing=dp(8))
        
        self.apply_btn = Button(text="APPLY OC", size_hint_y=None, height=dp(44), bold=True,
                           font_name=MONO, font_size=sp(16), color=ON_ACCENT, background_normal="",
                           background_down="", background_color=PURPLE_LIGHT)
        self.apply_btn.bind(on_release=self.apply_oc)
        self.buttons_list.append(self.apply_btn)
        btn_layout.add_widget(self.apply_btn)

        row_btns_1 = BoxLayout(size_hint_y=None, height=dp(34), spacing=dp(6))
        for name, callback in [("EXPORT PRESET", self.export_preset_dialog), ("IMPORT PRESET", self.import_preset_dialog)]:
            b = Button(text=name, bold=True, font_name=MONO, font_size=sp(11), color=ON_ACCENT, background_normal="", background_color=PURPLE)
            b.bind(on_release=callback)
            self.buttons_list.append(b)
            row_btns_1.add_widget(b)
        btn_layout.add_widget(row_btns_1)

        row_btns_2 = BoxLayout(size_hint_y=None, height=dp(34), spacing=dp(6))
        for name, callback in [("SAVE CONFIG", self.save_config_file), ("CLEAR ALL", self.on_clear_pressed), ("LAPTOP PROFILE", self.load_laptop_profile)]:
            b = Button(text=name, bold=True, font_name=MONO, font_size=sp(10), color=ON_ACCENT, background_color=PURPLE)
            b.bind(on_release=callback)
            self.buttons_list.append(b)
            row_btns_2.add_widget(b)
        btn_layout.add_widget(row_btns_2)
        
        self.inputs_main.add_widget(btn_layout)

        self.content_container.add_widget(self.inputs_scroll)
        self.content_container.add_widget(self.results_scroll)

        return self.root_layout

    def build(self):
        apply_theme(load_theme_pref())
        root = self._make_ui()
        Clock.schedule_once(self.load_startup_config, 0.4)
        return root

    # ---------- THEMES ----------
    def open_theme_menu(self, *_):
        body = BoxLayout(orientation="vertical", spacing=dp(6), padding=dp(8))
        for name, t in THEMES.items():
            b = Button(text=("> " if name == CURRENT_THEME else "") + name.upper(), size_hint_y=None,
                       height=dp(38), bold=True, font_name=MONO, font_size=sp(12), color=t["ON_ACCENT"],
                       background_normal="", background_color=t["PURPLE_LIGHT"])
            b.bind(on_release=lambda _b, n=name: self.set_theme(n))
            body.add_widget(b)
        self._theme_popup = Popup(title="THEMES", content=body, size_hint=(None, None),
                                  size=(dp(270), dp(84) + len(THEMES) * dp(44)), title_font=MONO,
                                  title_color=WHITE, title_size=sp(13), separator_color=PURPLE_LIGHT,
                                  background=POPUP_IMG, background_color=POPUP_BG, auto_dismiss=True)
        self._theme_popup.open()

    def set_theme(self, name):
        pop = getattr(self, "_theme_popup", None)
        if pop is not None:
            pop.dismiss()
        if name == CURRENT_THEME or name not in THEMES:
            return
        # remember what is on screen, rebuild the whole UI in the new colors, then put everything back
        snap = {k: ti.text for k, ti in self.fields.items()}
        spin = {a: getattr(self, a).text for a in ("arch_spin", "mem_spin", "psu_spin")}
        last = self._last_result
        status = (self.status.text, list(self.status.color))
        apply_theme(name)
        save_theme_pref(name)
        self._gpu_popup = None            # cached popups were built in the old colors
        self._cmp_popup = None
        old = self.root_layout
        new = self._make_ui()
        Window.remove_widget(old)
        Window.add_widget(new)
        self.root = new
        f = self.fields
        if snap.get("gpu"):
            f["gpu"].text = snap["gpu"]
        for a, t in spin.items():
            sp_ = getattr(self, a)
            if t in sp_.values:
                sp_.text = t
        for k, t in snap.items():
            if k != "gpu" and t and not f[k].disabled:
                f[k].text = t
        if last and last[0] == "apply":
            self.apply_oc()
        else:
            if last and last[0] == "gpu":
                self._show_gpu_loaded(last[1])
            self.set_status(*status)

    def input_box(self, key, hint, text=False):
        ti = TextInput(hint_text=hint, multiline=False, input_filter=None if text else "float",
                       font_size=sp(14), font_name=MONO, halign="left" if text else "right",
                       background_normal="", background_active="", background_color=FIELD,
                       foreground_color=WHITE, hint_text_color=HINT,
                       cursor_color=PURPLE_LIGHT, padding=[dp(8), dp(9), dp(8), dp(4)])
        ti.bind(on_text_validate=self.apply_oc)
        self.fields[key] = ti
        return ti

    def row(self, body, label, keys, text=False):
        r = BoxLayout(size_hint_y=None, height=dp(36), spacing=dp(8))
        r.add_widget(mono(label, GREY, 12))
        for key, hint in keys:
            r.add_widget(self.input_box(key, hint, text))
        body.add_widget(r)

    def spinner(self, values, default, attr):
        s = Spinner(text=default, values=list(values), font_name=MONO, font_size=sp(12),
                    color=ON_ACCENT, background_normal="", background_color=PURPLE,
                    option_cls=DarkSpinnerOption)
        setattr(self, attr, s)
        self.spinners_list.append(s)
        return s

    def labeled(self, label, widget):
        r = BoxLayout(size_hint_y=None, height=dp(36), spacing=dp(8))
        r.add_widget(mono(label, GREY, 12))
        r.add_widget(widget)
        return r

    # ---------- GPU CATEGORY (offline list) ----------
    def open_gpu_category(self, *_):
        if getattr(self, "_gpu_popup", None) is None:
            self._build_gpu_popup()
        self._refresh_gpu_list()
        self._gpu_popup.open()

    def _build_gpu_popup(self):
        self._gpu_vendor = "ALL"
        self._gpu_desc = False
        self._gpu_checked = False

        body = BoxLayout(orientation="vertical", spacing=dp(6), padding=dp(6))

        self._gpu_search = TextInput(hint_text="SEARCH  (e.g. 4070, rx 6600, arc)", multiline=False,
                                     size_hint_y=None, height=dp(38), font_size=sp(14), font_name=MONO,
                                     background_normal="", background_active="", background_color=FIELD,
                                     foreground_color=WHITE, hint_text_color=HINT,
                                     cursor_color=PURPLE_LIGHT, padding=[dp(8), dp(9), dp(8), dp(4)])
        self._gpu_search.bind(text=lambda *_: self._refresh_gpu_list())
        body.add_widget(self._gpu_search)

        bar = BoxLayout(size_hint_y=None, height=dp(34), spacing=dp(4))
        self._vendor_btns = {}
        for v in ("ALL", "NVIDIA", "AMD", "Intel"):
            b = Button(text=v.upper(), bold=True, font_name=MONO, font_size=sp(11), color=ON_ACCENT,
                       background_normal="", background_color=BTN_OFF)
            b.bind(on_release=lambda _b, v=v: self._set_gpu_vendor(v))
            self._vendor_btns[v] = b
            bar.add_widget(b)
        self._chk_btn = Button(text="CHECKED ONLY", bold=True, font_name=MONO, font_size=sp(10), color=ON_ACCENT,
                               background_normal="", background_color=BTN_OFF, size_hint_x=1.3)
        self._chk_btn.bind(on_release=self._toggle_gpu_checked)
        bar.add_widget(self._chk_btn)
        self._sort_btn = Button(text="WEAK > STRONG", bold=True, font_name=MONO, font_size=sp(10), color=ON_ACCENT,
                                background_normal="", background_color=PURPLE, size_hint_x=1.3)
        self._sort_btn.bind(on_release=self._toggle_gpu_sort)
        bar.add_widget(self._sort_btn)
        body.add_widget(bar)

        self._gpu_count = mono("", GREY, 11, size_hint_y=None, height=dp(18))
        body.add_widget(self._gpu_count)

        rv = RecycleView(scroll_type=["bars", "content"], bar_width=dp(8), bar_color=PURPLE_LIGHT,
                         do_scroll_x=False)
        layout = RecycleBoxLayout(default_size=(None, dp(50)), default_size_hint=(1, None),
                                  size_hint_y=None, orientation="vertical", spacing=dp(2))
        layout.bind(minimum_height=layout.setter("height"))
        rv.add_widget(layout)
        rv.viewclass = GpuRow
        self._gpu_rv = rv
        body.add_widget(rv)

        close = Button(text="CLOSE", size_hint_y=None, height=dp(36), bold=True, font_name=MONO,
                       font_size=sp(12), color=ON_ACCENT, background_normal="", background_color=PURPLE)
        body.add_widget(close)

        self._gpu_popup = Popup(title="GPU CATEGORY  -  weakest to strongest (approximate)", content=body,
                                size_hint=(0.92, 0.94), title_font=MONO, title_color=WHITE, title_size=sp(13),
                                separator_color=PURPLE_LIGHT, background=POPUP_IMG, background_color=POPUP_BG,
                                auto_dismiss=True)
        close.bind(on_release=self._gpu_popup.dismiss)

    def _set_gpu_vendor(self, vendor):
        self._gpu_vendor = vendor
        self._refresh_gpu_list()

    def _toggle_gpu_checked(self, *_):
        self._gpu_checked = not self._gpu_checked
        self._refresh_gpu_list()

    def _toggle_gpu_sort(self, *_):
        self._gpu_desc = not self._gpu_desc
        self._refresh_gpu_list()

    def _refresh_gpu_list(self):
        for v, b in self._vendor_btns.items():
            b.background_color = PURPLE_LIGHT if v == self._gpu_vendor else BTN_OFF
        self._sort_btn.text = "STRONG > WEAK" if self._gpu_desc else "WEAK > STRONG"
        self._chk_btn.background_color = PURPLE_LIGHT if self._gpu_checked else BTN_OFF
        tokens = self._gpu_search.text.strip().lower().split()
        items = []
        for i, g in enumerate(GPUS):
            if self._gpu_vendor != "ALL" and g["vendor"] != self._gpu_vendor:
                continue
            if self._gpu_checked and g["tier"] != "checked":
                continue
            hay = g["name"].lower()
            if all(t in hay for t in tokens):
                items.append((i, g))
        if self._gpu_desc:
            items.reverse()
        data = []
        for i, g in items:
            tag = VENDOR_TAG.get(g["vendor"], "ffffff")
            sub = (f"{fmt_vram(g['vram'])} {g['mem']} | {g['bus']}-bit | {g['cores']} cores | "
                   f"{g['core_clock']} MHz | {g['power']} W | {g['year']}")
            if g["legacy"]:
                sub += " | TFLOPS n/a"
            if g["tier"] != "checked":
                sub += f" | [color={WARN_HEX}]UNVERIFIED[/color]"
            data.append({
                "text": f"[b][color={tag}]#{i + 1}[/color]  {g['name']}[/b]\n[color={SUB_HEX}]{sub}[/color]",
                "gpu_id": i,
                "background_color": VENDOR_ROW_BG.get(g["vendor"], PANEL),
            })
        self._gpu_rv.data = data
        self._gpu_rv.scroll_y = 1
        self._gpu_count.text = f"{len(items)} of {len(GPUS)} cards   (#1 = weakest, #{len(GPUS)} = strongest)"

    def pick_gpu(self, gid):
        g = GPUS[gid]
        if getattr(self, "_gpu_popup", None) is not None:
            self._gpu_popup.dismiss()
        f = self.fields
        f["gpu"].text = g["name"]            # also applies vendor theme / architecture list
        if is_locked_card(g["name"]):        # same lock rule as typing the name by hand
            return
        if g["arch"] in ALL_ARCHS:
            self.arch_spin.text = g["arch"]
        if g["mem"] in MEM_TYPES:
            self.mem_spin.text = g["mem"]
        f["vram_gb"].text = str(g["vram"])
        f["bus"].text = str(g["bus"])
        f["cores"].text = "0" if g["legacy"] else str(g["cores"])
        f["power"].text = str(g["power"])
        f["mem_clock"].text = str(g["mem_clock"])
        f["core_clock"].text = str(g["core_clock"])
        for k in ("voltage", "new_mem_clock", "new_core_clock", "new_voltage"):
            f[k].text = ""
        self.set_status("SPECS LOADED", GREEN)
        self._show_gpu_loaded(gid)

    def _show_gpu_loaded(self, gid):
        g = GPUS[gid]
        self._last_result = ("gpu", gid)
        mult = MEM_TYPES[g["mem"]]
        bw = g["mem_clock"] * mult * g["bus"] / 8 / 1000
        tf = g["cores"] * 2 * g["core_clock"] / 1_000_000
        self.results.clear_widgets()
        p = panel("GPU LOADED", f"#{gid + 1} OF {len(GPUS)}")
        p.body.add_widget(kv_row("CARD", g["name"], GREEN))
        p.body.add_widget(kv_row("ARCHITECTURE / YEAR", f"{g['arch']}  {g['year']}"))
        p.body.add_widget(kv_row("STOCK BANDWIDTH", f"{bw:.1f} GB/s"))
        if g["legacy"]:
            p.body.add_widget(kv_row("STOCK COMPUTE", "n/a (older architecture)"))
        else:
            p.body.add_widget(kv_row("STOCK COMPUTE", f"{tf:.2f} TFLOPS"))
        p.body.add_widget(wrap("Reference specs (usually boost clock, TDP). Your card may differ: factory-OC and "
                               "partner models use other clocks and power limits. Now type your overclock "
                               "values (stock/new voltage optional: leave both empty if unchanged) and press "
                               "APPLY OC.", AMBER, 11))
        if g["tier"] != "checked":
            p.body.add_widget(wrap("UNVERIFIED entry: values come from a community-built list and were not "
                                   "cross-checked. Compare with GPU-Z before trusting the numbers.", RED, 11))
        if g["legacy"]:
            p.body.add_widget(wrap("Cores are set to 0 because TFLOPS from the core clock is not meaningful "
                                   "for this architecture. Bandwidth and power are still calculated.", GREY, 11))
        self.results.add_widget(p)

    # ---------- COMPATIBILITY window ----------
    def open_compat(self, *_):
        if getattr(self, "_cmp_popup", None) is None:
            self._build_compat_popup()
        f = self.fields
        gname = f["gpu"].text.strip()
        if gname and not self._cmp_gpu.text.strip():       # prefill from the main screen
            self._cmp_gpu.text = gname
        self._cmp_stock = None
        try:
            if f["new_core_clock"].text.strip():
                self._cmp_core.text = f["new_core_clock"].text.strip()
            if f["new_mem_clock"].text.strip():
                self._cmp_mem.text = f["new_mem_clock"].text.strip()
            if f["core_clock"].text.strip() and f["mem_clock"].text.strip():
                self._cmp_stock = (gname, float(f["core_clock"].text), float(f["mem_clock"].text))
        except ValueError:
            self._cmp_stock = None
        self._cmp_popup.open()

    def _cmp_text_input(self, hint, text=True):
        ti = self._cmp_text_input_raw(hint, text)
        with ti.canvas.after:                                 # border only (a fill would cover the text)
            Color(*PURPLE_LIGHT)
            frame = Line(rectangle=(*ti.pos, *ti.size), width=dp(1.2))
        ti.bind(pos=lambda i, v: setattr(frame, "rectangle", (*i.pos, *i.size)),
                size=lambda i, v: setattr(frame, "rectangle", (*i.pos, *i.size)))
        return ti

    def _cmp_text_input_raw(self, hint, text=True):
        return TextInput(hint_text=hint, multiline=False, input_filter=None if text else "float",
                         size_hint_y=None, height=dp(38), font_size=sp(14), font_name=MONO,
                         halign="left" if text else "right",
                         background_normal="", background_active="", background_color=FIELD2,
                         foreground_color=WHITE, hint_text_color=HINT2,
                         cursor_color=PURPLE_LIGHT, padding=[dp(8), dp(9), dp(8), dp(4)])

    def _build_compat_popup(self):
        self._cmp_stock = None
        scroll = ScrollView(do_scroll_x=False, bar_color=PURPLE_LIGHT, bar_width=dp(8))
        inner = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(6), padding=[dp(6), dp(6), dp(10), dp(16)])
        inner.bind(minimum_height=inner.setter("height"))
        scroll.add_widget(inner)

        def label(t):
            inner.add_widget(mono(t, GREY, 11, size_hint_y=None, height=dp(18)))

        label("CPU  (type the name, e.g. i5-12400F, ryzen 5 5600x)")
        self._cmp_cpu = self._cmp_text_input("CPU name")
        inner.add_widget(self._cmp_cpu)
        self._cmp_cpu_sug = BoxLayout(orientation="vertical", size_hint_y=None, height=0, spacing=dp(2))
        inner.add_widget(self._cmp_cpu_sug)

        label("GPU  (type the name, e.g. rx 6500 xt, rtx 4060)")
        self._cmp_gpu = self._cmp_text_input("GPU name")
        inner.add_widget(self._cmp_gpu)
        self._cmp_gpu_sug = BoxLayout(orientation="vertical", size_hint_y=None, height=0, spacing=dp(2))
        inner.add_widget(self._cmp_gpu_sug)

        self._cmp_cpu.bind(text=lambda i, v: self._cmp_suggest(CPUS, v, self._cmp_cpu, self._cmp_cpu_sug))
        self._cmp_gpu.bind(text=lambda i, v: self._cmp_suggest(GPUS, v, self._cmp_gpu, self._cmp_gpu_sug))

        self._cmp_res = Spinner(text="1080p", values=RES_CHOICES, font_name=MONO, font_size=sp(12), color=ON_ACCENT,
                                background_normal="", background_color=PURPLE, option_cls=DarkSpinnerOption)
        self._cmp_slot = Spinner(text=SLOT_CHOICES[0], values=SLOT_CHOICES, font_name=MONO, font_size=sp(12),
                                 color=ON_ACCENT, background_normal="", background_color=PURPLE,
                                 option_cls=DarkSpinnerOption)
        self._cmp_slot_lanes = Spinner(text=SLOT_LANE_CHOICES[0], values=SLOT_LANE_CHOICES,
                                       font_name=MONO, font_size=sp(12), color=ON_ACCENT,
                                       background_normal="", background_color=PURPLE,
                                       option_cls=DarkSpinnerOption)
        inner.add_widget(self.labeled("RESOLUTION", self._cmp_res))
        inner.add_widget(self.labeled("BOARD PCIe GEN", self._cmp_slot))
        inner.add_widget(self.labeled("BOARD SLOT WIDTH", self._cmp_slot_lanes))

        label("OPTIONAL: OVERCLOCK  (leave empty = stock)")
        self._cmp_core = self._cmp_text_input("GPU core MHz (OC)", text=False)
        self._cmp_mem = self._cmp_text_input("GPU memory MHz (OC, GPU-Z value)", text=False)
        self._cmp_cpuoc = self._cmp_text_input("CPU all-core GHz (OC)", text=False)
        for w in (self._cmp_core, self._cmp_mem, self._cmp_cpuoc):
            inner.add_widget(w)

        go = Button(text="CHECK COMPATIBILITY", size_hint_y=None, height=dp(44), bold=True, font_name=MONO,
                    font_size=sp(15), color=ON_ACCENT, background_normal="", background_color=PURPLE_LIGHT)
        go.bind(on_release=self._cmp_check)
        self._cmp_go = go
        inner.add_widget(go)

        self._cmp_out = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(8))
        self._cmp_out.bind(minimum_height=self._cmp_out.setter("height"))
        inner.add_widget(self._cmp_out)

        body = BoxLayout(orientation="vertical", spacing=dp(6), padding=dp(6))
        body.add_widget(scroll)
        close = Button(text="CLOSE", size_hint_y=None, height=dp(36), bold=True, font_name=MONO,
                       font_size=sp(12), color=ON_ACCENT, background_normal="", background_color=PURPLE)
        body.add_widget(close)
        self._cmp_popup = Popup(title="COMPATIBILITY  -  PCIe link & CPU bottleneck (estimates)", content=body,
                                size_hint=(0.94, 0.95), title_font=MONO, title_color=WHITE, title_size=sp(13),
                                separator_color=PURPLE_LIGHT, background=POPUP_IMG, background_color=POPUP_BG,
                                auto_dismiss=True)
        close.bind(on_release=self._cmp_close)

    def _cmp_reset(self):
        """Empty every field of the COMPATIBILITY window and its results."""
        if getattr(self, "_cmp_popup", None) is None:
            return
        for w in (self._cmp_cpu, self._cmp_gpu, self._cmp_core, self._cmp_mem, self._cmp_cpuoc):
            w.text = ""
        self._cmp_res.text = "1080p"
        self._cmp_slot.text = SLOT_CHOICES[0]
        self._cmp_slot_lanes.text = SLOT_LANE_CHOICES[0]
        self._cmp_out.clear_widgets()
        self._cmp_cpu_sug.clear_widgets(); self._cmp_cpu_sug.height = 0
        self._cmp_gpu_sug.clear_widgets(); self._cmp_gpu_sug.height = 0
        self._cmp_stock = None

    def _cmp_close(self, *_):
        """CLOSE = clear everything and close."""
        self._cmp_reset()
        self._cmp_popup.dismiss()

    def _cmp_suggest(self, db, text, box, holder):
        holder.clear_widgets()
        matches = find_matches(db, text, 4)
        if len(matches) == 1 and _norm(matches[0]["name"]) == _norm(text):
            matches = []
        for m in matches:
            b = Button(text=m["name"], size_hint_y=None, height=dp(30), font_name=MONO, font_size=sp(11),
                       color=ON_ACCENT, background_normal="", background_color=BTN_OFF, halign="left", valign="middle")
            b.bind(size=lambda i, s: setattr(i, "text_size", (s[0] - dp(14), s[1])))
            b.bind(on_release=lambda _b, n=m["name"]: setattr(box, "text", n))
            holder.add_widget(b)
        holder.height = len(matches) * dp(32)

    def _cmp_pick(self, db, text):
        hits = find_matches(db, text, 1)
        return hits[0] if hits else None

    def _cmp_check(self, *_):
        out = self._cmp_out
        out.clear_widgets()
        cpu = self._cmp_pick(CPUS, self._cmp_cpu.text)
        gpu = self._cmp_pick(GPUS, self._cmp_gpu.text)
        if cpu is None or gpu is None:
            p = panel("CHECK", "INPUT")
            if cpu is None:
                p.body.add_widget(warn_row(AMBER, "CPU not found in the built-in list. Type part of the model "
                                                  "(e.g. 5600x) and pick one of the suggestions, or use a similar desktop CPU."))
            if gpu is None:
                p.body.add_widget(warn_row(AMBER, "GPU not found in the built-in list. Type part of the name "
                                                  "(e.g. 6600) and pick one of the suggestions."))
            out.add_widget(p)
            return

        def num(w):
            t = w.text.strip()
            if not t:
                return None, True
            try:
                v = float(t)
                return (v, True) if v > 0 else (None, False)
            except ValueError:
                return None, False

        core, ok1 = num(self._cmp_core)
        mem, ok2 = num(self._cmp_mem)
        ghz, ok3 = num(self._cmp_cpuoc)
        if not (ok1 and ok2 and ok3):
            p = panel("CHECK", "INPUT")
            p.body.add_widget(warn_row(AMBER, "Overclock fields must be positive numbers, or empty for stock."))
            out.add_widget(p)
            return
        slot = self._cmp_slot.text
        slot_gen = None if slot.startswith("Auto") else int(slot.split()[1][0])
        slot_lane_text = self._cmp_slot_lanes.text
        slot_lanes = None if slot_lane_text.startswith("Auto") else int(slot_lane_text[1:])
        stock_core = stock_mem = None
        if self._cmp_stock and self._cmp_stock[0].lower() == gpu["name"].lower():
            stock_core, stock_mem = self._cmp_stock[1], self._cmp_stock[2]
        r = compat_report(cpu, gpu, self._cmp_res.text, slot_gen, core, mem, ghz, stock_core, stock_mem, slot_lanes)
        self._render_compat(r, core, mem, ghz)

    def _render_compat(self, r, core, mem, ghz):
        out, cpu, gpu, bn, pc = self._cmp_out, r["cpu"], r["gpu"], r["bn"], r["pcie"]
        colors = [GREEN, AMBER, AMBER, RED]

        v = panel("VERDICT", "ESTIMATE")
        if not r["fits"]:
            v.body.add_widget(mono(r["fit_text"], RED, 17, bold=True, size_hint_y=None, height=dp(30)))
        elif r["gpu_limited"] and r["level"] <= 1:
            v.body.add_widget(mono("UNBALANCED: GPU IS THE WEAK LINK", AMBER, 17, bold=True, size_hint_y=None, height=dp(30)))
        else:
            v.body.add_widget(mono(LEVEL_NAME[r["level"]], colors[r["level"]], 20, bold=True, size_hint_y=None, height=dp(30)))
        v.body.add_widget(kv_row("CPU", cpu["name"]))
        v.body.add_widget(kv_row("GPU", gpu["name"]))
        if pc is not None:
            v.body.add_widget(kv_row("EST. PERFORMANCE RETAINED", f"~{r['retained']:.0f}% of GPU potential",
                                     colors[r["level"]]))
        if not r["fits"]:
            v.body.add_widget(kv_row("CAN IT BE INSTALLED?", "NO - cannot be plugged in", RED))
        else:
            v.body.add_widget(kv_row("EST. CPU BOTTLENECK", f"{bn['loss']:.1f}%", colors[r["bn_level"]]))
        if r["fits"] and bn["gpu_headroom"] >= 3:
            v.body.add_widget(kv_row("GPU-LIMITED CPU HEADROOM", f"{bn['gpu_headroom']:.1f}%", AMBER))
        out.add_widget(v)

        pl = panel("PCIe LINK MATCH", "GENERATION + LANES")
        if pc is None:
            if gpu.get("legacy"):
                pl.body.add_widget(kv_row("CARD LINK", "no PCIe (AGP / PCI / onboard)", RED))
            else:
                pl.body.add_widget(kv_row("CARD LINK", "not listed - verify GPU interface", AMBER))
        else:
            pl.body.add_widget(kv_row("GPU MAX LINK", f"PCIe {pc['gpu_gen']}.0 x{pc['gpu_lanes']}  |  {pc['native_bw']:.2f} GB/s"))
            pl.body.add_widget(kv_row("CPU / PLATFORM LIMIT", f"PCIe {pc['cpu_gen']}.0 x{pc['cpu_lanes']}"))
            slot_gen_text = f"PCIe {pc['slot_gen']}.0" if pc["slot_gen"] else "Auto / CPU limit"
            slot_lanes_text = f"x{pc['slot_lanes']}" if pc["slot_lanes"] else "Auto / platform limit"
            pl.body.add_widget(kv_row("MOTHERBOARD SLOT", f"{slot_gen_text}  |  {slot_lanes_text}"))
            pl.body.add_widget(kv_row("NEGOTIATED LINK", f"PCIe {pc['run_gen']}.0 x{pc['run_lanes']}  |  {pc['run_bw']:.2f} GB/s",
                                      colors[r["pcie_level"]]))
            lane_label = (f"MATCHED  (x{pc['run_lanes']} / x{pc['gpu_lanes']})" if pc["lane_matched"] else
                          f"REDUCED  ({pc['lane_loss']:.0f}% lane loss; x{pc['run_lanes']} / x{pc['gpu_lanes']})")
            pl.body.add_widget(kv_row("LANE WIDTH", lane_label, GREEN if pc["lane_matched"] else AMBER))
            gen_label = (f"MATCHED  (PCIe {pc['run_gen']}.0)" if pc["generation_matched"] else
                         f"DOWNGRADED  ({pc['generation_loss']:.0f}% raw gen bandwidth loss)")
            pl.body.add_widget(kv_row("GENERATION", gen_label, GREEN if pc["generation_matched"] else AMBER))
            pl.body.add_widget(kv_row("RAW LINK BANDWIDTH LOSS", f"{pc['bandwidth_loss']:.1f}%  vs GPU maximum",
                                      AMBER if pc["bandwidth_loss"] >= 10 else GREEN))
            pl.body.add_widget(kv_row("EST. GAMING FPS IMPACT", f"~{pc['loss']:.1f}%  (heuristic)",
                                      colors[r["pcie_level"]]))
            pl.body.add_widget(SegBar(min(1.0, pc["run_bw"] / pc["native_bw"]), colors[r["pcie_level"]]))
            pl.body.add_widget(wrap("Raw bandwidth loss is link throughput, not the same as FPS loss. The FPS figure is a broad estimate.", GREY, 10))
        out.add_widget(pl)

        if not r["fits"]:                      # no point estimating a bottleneck for a card that cannot be installed
            n = panel("NOTES", f"{len(r['notes'])}")
            for lvl, text in r["notes"]:
                n.body.add_widget(warn_row(RED if lvl >= 3 else (AMBER if lvl else GREY), text))
            out.add_widget(n)
            return

        b = panel(f"BOTTLENECK @ {r['res']}", "CPU vs GPU ESTIMATE")
        b.body.add_widget(kv_row("CPU BOTTLENECK (EST. FPS LOSS)", f"{bn['loss']:.1f}%", colors[r["bn_level"]]))
        b.body.add_widget(kv_row("GPU-LIMITED CPU HEADROOM", f"{bn['gpu_headroom']:.1f}%",
                                 AMBER if bn["gpu_headroom"] >= 3 else GREEN))
        b.body.add_widget(kv_row("CPU / GPU INDEX RATIO", f"{bn['ratio']:.2f} : 1"))
        b.body.add_widget(mono(f"GPU DEMAND   {bn['load']:.0f}", WHITE, 12, size_hint_y=None, height=dp(18)))
        top = max(bn["load"], bn["cap"]) or 1.0
        b.body.add_widget(SegBar(bn["load"] / top, PURPLE_LIGHT))
        b.body.add_widget(mono(f"CPU CAPACITY {bn['cap']:.0f}", WHITE, 12, size_hint_y=None, height=dp(18)))
        b.body.add_widget(SegBar(bn["cap"] / top, colors[r["bn_level"]]))
        if bn["loss"] < 3:
            if r["gpu_limited"]:
                msg, col = (f"GPU BOTTLENECK: the card is far weaker than the CPU (CPU capacity is about "
                            f"{bn['ratio']:.0f}x what the GPU needs). The CPU does not hold anything back, "
                            f"but the GPU limits the whole system."), AMBER
            else:
                msg, col = ("No CPU bottleneck: the GPU is the limiting part." if bn["ratio"] < 1.6 else
                            "No CPU bottleneck: the CPU has plenty of headroom."), GREEN
        else:
            msg, col = (f"CPU BOTTLENECK: about {bn['loss']:.0f}% of the GPU's frame rate is lost because the CPU "
                        f"cannot feed it fast enough at {r['res']}."), colors[r["bn_level"]]
        b.body.add_widget(wrap(msg, col, 12))
        if r["rec_cpu"] is not None:
            b.body.add_widget(wrap(f"A CPU like the {r['rec_cpu']['name']} would feed this GPU at {r['res']}.", GREY, 11))
        if r["res"] in ("720p", "1080p") and bn["loss"] >= 3:
            b.body.add_widget(wrap("Higher resolution or heavier graphics settings usually shift more work to the GPU "
                                   "and can reduce the CPU-side limit.", GREY, 11))
        if core or mem:
            b.body.add_widget(kv_row("GPU OC EFFECT (est.)", f"{(bn['gpu_scale'] - 1) * 100:+.1f}%"))
        if ghz:
            b.body.add_widget(kv_row("CPU OC EFFECT (est.)", f"{(bn['cpu_scale'] - 1) * 100:+.1f}%"))
        out.add_widget(b)

        if r["notes"]:
            n = panel("NOTES", f"{len(r['notes'])}")
            for lvl, text in r["notes"]:
                n.body.add_widget(warn_row([GREEN, AMBER, AMBER, RED][lvl] if lvl else GREY, text))
            out.add_widget(n)

        d = r["deep"]
        dp_ = panel("DEEP ANALYSIS", "ALL RESOLUTIONS")
        dp_.body.add_widget(mono("CPU FPS LOSS + GPU-LIMITED HEADROOM BY RESOLUTION", GREY, 10, size_hint_y=None, height=dp(16)))
        for row in d["res_rows"]:
            lv = row["level"]
            mark = "  <" if row["current"] else ""
            dp_.body.add_widget(kv_row(f"{row['res']}{mark}",
                                       f"CPU loss {row['loss']:.1f}%  |  GPU headroom {row['gpu_headroom']:.1f}%", colors[lv]))
            dp_.body.add_widget(kv_row("  EST. PERFORMANCE RETAINED", f"~{row['retained']:.1f}%", colors[lv]))
        if d["pcie_rows"]:
            dp_.body.add_widget(mono("IF THE LINK RAN AT (same lanes)", GREY, 10, size_hint_y=None, height=dp(16)))
            for pr in d["pcie_rows"]:
                lv = _level_from_loss(pr["loss"])
                mark = "  <" if pr["current"] else ""
                dp_.body.add_widget(kv_row(f"PCIe {pr['gen']}.0 x{pr['lanes']}{mark}",
                                           f"{pr['bw']:.1f} GB/s   loss {pr['loss']:.0f}%", colors[lv]))
            if d["lane_rows"]:
                dp_.body.add_widget(mono("LANE WIDTH WHAT-IF (IF THE SLOT / CPU SUPPORTS IT)", GREY, 10, size_hint_y=None, height=dp(16)))
                for lr in d["lane_rows"]:
                    lv = _level_from_loss(lr["loss"])
                    mark = "  <" if lr["current"] else ""
                    dp_.body.add_widget(kv_row(f"PCIe x{lr['lanes']}{mark}",
                                               f"{lr['bw']:.2f} GB/s  |  est. FPS impact {lr['loss']:.1f}%", colors[lv]))
        if d["oc"]:
            oc = d["oc"]
            dp_.body.add_widget(mono("GPU OVERCLOCK", GREY, 10, size_hint_y=None, height=dp(16)))
            dp_.body.add_widget(kv_row("GAIN ON PAPER", f"{oc['wanted']:+.1f}%"))
            dp_.body.add_widget(kv_row("GAIN YOU WILL SEE", f"{oc['real']:+.1f}%", RED if oc["real"] < oc["wanted"] - 0.5 else GREEN))
            if oc["cpu_limited"]:
                dp_.body.add_widget(wrap("The CPU limits this setup, so part (or all) of the overclock gain is lost "
                                         "at this resolution.", AMBER, 11))
        out.add_widget(dp_)

        pw = panel("POWER HINT", "STOCK")
        pw.body.add_widget(kv_row("GPU + CPU + 75 W", f"{r['psu']['total']} W"))
        pw.body.add_widget(kv_row("PSU AT LEAST", f"{r['psu']['rec']} W"))
        pw.body.add_widget(wrap("Quality 80 Plus unit, about 80% load at peak. Use APPLY OC on the main screen "
                                "for an overclocked estimate.", GREY, 11))
        out.add_widget(pw)

        out.add_widget(wrap("Estimates use the offline CPU/GPU performance indexes, selected PCIe limits and a simplified "
                            "gaming-load model. CPU bottleneck % estimates potential GPU FPS lost to CPU throughput; "
                            "GPU headroom % describes unused CPU capacity while waiting on the GPU, not FPS lost. "
                            "Real results depend on the game, RAM, board wiring, BIOS, drivers and cooling. "
                            "Use a live PCIe link readout or benchmark for confirmation.", GREY, 10))

    def run_gpuz_detection(self, *_):
        self.set_status("SCANNING...", AMBER)
        threading.Thread(target=self._read_hardware, daemon=True).start()

    def _read_hardware(self):
        specs = detect_hardware_specs()
        Clock.schedule_once(lambda dt: self._apply_gpuz_specs(specs))

    def _apply_gpuz_specs(self, specs):
        if specs.get("gpu_name"):
            self.fields["gpu"].text = specs["gpu_name"]
            if specs.get("vram_gb"): self.fields["vram_gb"].text = specs["vram_gb"]
            self.fields["core_clock"].text = specs.get("core_clock", "")
            self.fields["mem_clock"].text = specs.get("mem_clock", "")
            self.fields["bus"].text = specs.get("bus", "")
            self.fields["cores"].text = specs.get("cores", "")
            self.fields["power"].text = specs.get("power", "")
            self.fields["voltage"].text = specs.get("voltage", "")
            
            if specs.get("arch") and specs["arch"] in ALL_ARCHS: self.arch_spin.text = specs["arch"]
            
            self.fields["new_mem_clock"].text = ""
            self.fields["new_core_clock"].text = ""
            self.fields["new_voltage"].text = ""

            self.set_status("GPU DETECTED", GREEN)
            
            self.results.clear_widgets()
            p = panel("GPU TELEMETRY", "BENCHMARK SCAN")
            p.body.add_widget(kv_row("DETECTED CARD", specs["gpu_name"], GREEN))
            p.body.add_widget(kv_row("DRIVER VERSION", specs.get("driver_version", "N/A")))
            if specs.get("vram_gb"): p.body.add_widget(kv_row("VRAM CAPACITY", f"{specs['vram_gb']} GB"))
            p.body.add_widget(wrap("Hardware scan complete. Enter overclock parameters.", AMBER, 11))
            self.results.add_widget(p)
        else:
            self.clear_all_fields()
            self.set_status("NO GPU FOUND", RED)

    def export_preset_dialog(self, *_):
        try:
            filename = f"oc_preset_{(self.fields['gpu'].text or 'gpu').replace(' ', '_').lower()}.json"
            data = {k: self.fields[k].text for k in self.fields}
            data["mem_type"] = self.mem_spin.text
            data["architecture"] = self.arch_spin.text
            data["psu_rating"] = self.psu_spin.text
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
            self.set_status(f"EXPORTED: {filename}", GREEN)
        except Exception:
            self.set_status("EXPORT ERROR", RED)

    def import_preset_dialog(self, *_):
        try:
            files = [f for f in os.listdir('.') if f.endswith('.json')]
            if files:
                target_file = files[0]
                with open(target_file, "r") as f:
                    data = json.load(f)
                for k in self.fields:
                    if k in data: self.fields[k].text = str(data[k])
                if "mem_type" in data: self.mem_spin.text = data["mem_type"]
                if "architecture" in data: self.arch_spin.text = data["architecture"]
                if "psu_rating" in data: self.psu_spin.text = data["psu_rating"]
                self.set_status(f"IMPORTED: {target_file}", GREEN)
                self.apply_oc()
            else:
                self.set_status("NO PRESETS FOUND", AMBER)
        except Exception:
            self.set_status("IMPORT ERROR", RED)

    def on_gpu_name_change(self, instance, value):
        self._last_result = None
        val_upper = value.strip().upper()
        
        is_restricted = "NVS" in val_upper or "QUADRO NVS" in val_upper or "VEGA 64" in val_upper
        is_vega56 = "VEGA 56" in val_upper

        # Disable/Enable all fields and apply button when restricted
        for k, ti in self.fields.items():
            if k != "gpu":
                ti.disabled = is_restricted
                if is_restricted:
                    ti.text = ""
        
        self.apply_btn.disabled = is_restricted

        self.results.clear_widgets()
        if is_restricted:
            self.set_status("RESTRICTED", RED)
            p = panel("ALERTS", "LOCKED CARD")
            p.body.add_widget(warn_row(RED, "Overclocking Locked: Architecture does not support OC."))
            self.results.add_widget(p)
        elif is_vega56:
            self.set_status("CAUTION", AMBER)
            p = panel("ALERTS", "VEGA 56 RULE")
            p.body.add_widget(warn_row(AMBER, "RX Vega 56: Unlocked via Vega 64 BIOS flash (Requires Samsung VRAM)."))
            self.results.add_widget(p)

        is_intel = any(x in val_upper for x in ["INTEL", "ARC", "IRIS", "HD GRAPHICS"])
        is_nvidia = any(x in val_upper for x in ["NVIDIA", "GTX", "RTX", "QUADRO", "NVS", "TITAN", "GEFORCE"])
        is_amd = any(x in val_upper for x in ["AMD", "RADEON", "VEGA", "RX", "R9", "R7", "NAVI", "ATI", "RAGE"])

        if is_nvidia:
            self.arch_spin.values = list(NVIDIA_ARCHS.keys())
            if self.arch_spin.text not in NVIDIA_ARCHS: self.arch_spin.text = list(NVIDIA_ARCHS.keys())[0]
        elif is_amd:
            self.arch_spin.values = list(AMD_ARCHS.keys())
            if self.arch_spin.text not in AMD_ARCHS: self.arch_spin.text = list(AMD_ARCHS.keys())[0]
        elif is_intel:
            self.arch_spin.values = list(INTEL_ARCHS.keys())
            if self.arch_spin.text not in INTEL_ARCHS: self.arch_spin.text = list(INTEL_ARCHS.keys())[0]
        else:
            self.arch_spin.values = list(ALL_ARCHS.keys())

        if not VENDOR_TINT:
            header_col, border_col, panel_bg = PURPLE, PURPLE_LIGHT, PANEL
        elif is_intel:
            header_col, border_col, panel_bg = (0.15, 0.0, 0.45, 1), INTEL_BLUE, INTEL_PANEL_BG
        elif is_nvidia:
            header_col, border_col, panel_bg = (0.05, 0.20, 0.02, 1), NVIDIA_GREEN, NVIDIA_PANEL_BG
        elif is_amd:
            header_col, border_col, panel_bg = (0.22, 0.02, 0.02, 1), AMD_RED, AMD_PANEL_BG
        else:
            header_col, border_col, panel_bg = PURPLE, PURPLE_LIGHT, PANEL

        if VENDOR_TINT:
            # Only vendor-tinted themes need a second paint pass. Repainting every surface in
            # non-tinted themes duplicated translucent canvas layers and made theme changes muddy.
            paint(self.head_box, header_col, border_col)
            for p in self.panels:
                paint(p.head_box, header_col)
                paint(p, panel_bg, border_col)
            for s in self.spinners_list:
                s.background_color = header_col
            self.apply_btn.background_color = border_col
            self.gpu_cat_btn.background_color = border_col
            self.compat_btn.background_color = border_col
            for b in self.buttons_list:
                if b not in (self.apply_btn, self.gpuz_btn, self.gpu_cat_btn, self.compat_btn):
                    b.background_color = header_col

    def save_config_file(self, *_):
        try:
            data = {k: self.fields[k].text for k in self.fields}
            data["mem_type"] = self.mem_spin.text
            data["architecture"] = self.arch_spin.text
            data["psu_rating"] = self.psu_spin.text
            with open("oc_profile.json", "w") as f:
                json.dump(data, f, indent=4)
            self.set_status("CONFIG SAVED", GREEN)
        except Exception:
            self.set_status("SAVE ERROR", RED)

    def on_clear_pressed(self, *_):
        try:
            if os.path.exists("oc_profile.json"):
                os.remove("oc_profile.json")      # otherwise the cleared values would come back on next start
        except Exception:
            pass
        self.clear_all_fields()

    def load_startup_config(self, *_):
        """Restore the values saved with SAVE CONFIG (oc_profile.json next to the program)."""
        try:
            if not os.path.exists("oc_profile.json"):
                return
            with open("oc_profile.json", "r") as f:
                data = json.load(f)
            if data.get("gpu"):
                self.fields["gpu"].text = str(data["gpu"])     # applies theme + architecture list first
            for k, ti in self.fields.items():
                if k != "gpu" and k in data and not ti.disabled:
                    ti.text = str(data[k])
            if data.get("mem_type") in MEM_TYPES:
                self.mem_spin.text = data["mem_type"]
            if data.get("architecture") in ALL_ARCHS and data["architecture"] in self.arch_spin.values:
                self.arch_spin.text = data["architecture"]
            if data.get("psu_rating") in PSU_RATINGS:
                self.psu_spin.text = data["psu_rating"]
            self.set_status("CONFIG LOADED", IDLE)
        except Exception:
            self.set_status("CONFIG ERROR", RED)

    def clear_all_fields(self, *_):
        self._last_result = None
        for ti in self.fields.values():
            ti.disabled = False
            ti.text = ""
        self.apply_btn.disabled = False
        self.arch_spin.disabled = False
        self.mem_spin.disabled = False
        self.results.clear_widgets()
        self._cmp_reset()                      # the COMPATIBILITY window starts empty too
        self.on_gpu_name_change(self.fields["gpu"], "")
        self.set_status("CLEARED", IDLE)

    def load_laptop_profile(self, *_):
        try:
            if "core_clock" in self.fields and self.fields["core_clock"].text:
                self.fields["new_core_clock"].text = str(float(self.fields["core_clock"].text) + 15)
            if "mem_clock" in self.fields and self.fields["mem_clock"].text:
                self.fields["new_mem_clock"].text = str(float(self.fields["mem_clock"].text) + 35)
            if "voltage" in self.fields and self.fields["voltage"].text:
                self.fields["new_voltage"].text = self.fields["voltage"].text
            self.set_status("LAPTOP PROFILE", AMBER)
        except Exception:
            self.set_status("PROFILE ERROR", RED)

    def set_status(self, text, color):
        color = HDR_STATUS.get(tuple(color), color)
        self.status.text, self.status.color = text, color
        self.led.set(color)

    def fail(self, text):
        self.set_status("INPUT ERROR", RED)
        p = panel("ALERTS", "ERROR")
        p.body.add_widget(warn_row(RED, text))
        self.results.add_widget(p)

    def apply_oc(self, *_):
        self.results.clear_widgets()
        self._last_result = ("apply",)
        gpu_name = self.fields["gpu"].text.strip().upper()
        
        if "NVS" in gpu_name or "QUADRO NVS" in gpu_name or "VEGA 64" in gpu_name:
            self.set_status("RESTRICTED", RED)
            p = panel("ALERTS", "LOCKED CARD")
            p.body.add_widget(warn_row(RED, "Overclocking Locked: Architecture does not support OC."))
            self.results.add_widget(p)
            return

        vs = self.fields["voltage"].text.strip()
        nvs = self.fields["new_voltage"].text.strip()
        if not vs and not nvs:
            vs = nvs = "1.0"          # voltage unchanged: only the ratio new/stock matters
        elif bool(vs) != bool(nvs):
            return self.fail("Fill both voltage fields, or leave both empty if you do not change the voltage.")
        try:
            vals = {k: self.fields[k].text for k in NUM_FIELDS}
            vals["voltage"], vals["new_voltage"] = vs, nvs
            v = {k: float(t) for k, t in vals.items()}
        except ValueError:
            return self.fail("Fill every numeric field before applying.")
        if any(not math.isfinite(x) for x in v.values()):
            return self.fail("Values must be ordinary numbers.")
        if any(x < 0 for x in v.values()):
            return self.fail("Values cannot be negative.")
        v["mem_name"], v["rating_name"] = self.mem_spin.text, self.psu_spin.text
        v["arch_name"] = self.arch_spin.text
        v["gpu_name"] = self.fields["gpu"].text.strip()
        name = (v["gpu_name"] or "MY GPU").upper()
        
        r, warns = calculate(v, v["gpu_name"])

        if any(c == RED for c, _ in warns):
            self.set_status("DANGER", RED)
        elif warns:
            self.set_status("CAUTION", AMBER)
        else:
            self.set_status("NO ALERTS", GREEN)

        p = panel("READOUT", name)
        row = BoxLayout(size_hint_y=None, height=dp(84), spacing=dp(8))
        row.add_widget(tile("BANDWIDTH GB/s", f"{r['bw_new']:.1f}", f"{r['mem_gain']:+.2f}%", GREEN))
        row.add_widget(tile("COMPUTE TFLOPS", f"{r['tf_new']:.2f}", f"{r['core_gain']:+.2f}%", GREEN))
        row.add_widget(tile("GPU POWER W", f"{r['p_new']:.0f}", f"{r['p_gain']:+.1f}%", RED if r["p_gain"] > 25 else AMBER))
        p.body.add_widget(row)
        p.body.add_widget(mono(f"{v['mem_name']} ({fmt_vram(v['vram_gb'])} {v['arch_name']})  {r['speed_old']:.2f} > {r['speed_new']:.2f} Gbps", GREY, 11, size_hint_y=None, height=dp(16)))
        self.results.add_widget(p)

        p = panel("STOCK vs OC", "GREY = STOCK")
        compare(p.body, "BANDWIDTH", r["bw_old"], r["bw_new"], "GB/s", ".1f", PURPLE_LIGHT)
        compare(p.body, "COMPUTE  ", r["tf_old"], r["tf_new"], "TFLOPS", ".2f", PURPLE_LIGHT)
        compare(p.body, "GPU POWER", v["power"], r["p_new"], "W", ".0f", AMBER)
        self.results.add_widget(p)

        p = panel("PSU LOAD", v["rating_name"].upper())
        p.body.add_widget(mono(f"{r['load_old']:.0f}% > {r['load_new']:.0f}%      ticks: 80% / 90%", WHITE, 12, size_hint_y=None, height=dp(18)))
        p.body.add_widget(SegBar(r["load_new"] / 100, r["vcolor"], marks=(0.8, 0.9)))
        p.body.add_widget(kv_row("SYSTEM POWER", f"{r['tot_old']:.0f} > {r['tot_new']:.0f} W"))
        p.body.add_widget(kv_row("RECOMMENDED PSU", f"{r['rec_psu']} W"))
        p.body.add_widget(kv_row("VERDICT", r["verdict"], r["vcolor"]))
        p.body.add_widget(kv_row("EFFICIENCY", f"{r['eff_old'] * 100:.1f}% > {r['eff_new'] * 100:.1f}%"))
        p.body.add_widget(kv_row("FROM WALL (AC)", f"{r['wall_old']:.0f} > {r['wall_new']:.0f} W"))
        p.body.add_widget(kv_row("LOST AS HEAT", f"{r['heat_old']:.0f} > {r['heat_new']:.0f} W"))
        p.body.add_widget(kv_row("EXTRA WALL POWER", f"{r['wall_new'] - r['wall_old']:.1f} W", AMBER))
        self.results.add_widget(p)

        p = panel("ALERTS", f"{len(warns)} ACTIVE")
        if warns:
            for color, text in warns:
                p.body.add_widget(warn_row(color, text))
        else:
            p.body.add_widget(wrap("NO ALERTS. The values look reasonable.", GREEN, 12))
        p.body.add_widget(wrap("Theoretical estimates. Real FPS gains are usually lower.", GREY, 10))
        self.results.add_widget(p)


if __name__ == "__main__":
    OCApp().run()