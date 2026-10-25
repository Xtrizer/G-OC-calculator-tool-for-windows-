"""OC//CALC v2.0.1 - Extreme Overclock & Experiment Suite (Clean Alerts & Instant Lock)."""
import math
import json
import threading
import os
import subprocess
import platform

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Line, Rectangle, Triangle
from kivy.metrics import dp, sp
from kivy.resources import resource_find
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.clock import Clock

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
    "DDR2": 2, "DDR3": 2, "GDDR3": 2, "GDDR5": 4, "GDDR5X": 8,
    "GDDR6": 8, "GDDR6X": 16, "GDDR7": 32, "HBM": 2, "HBM2": 2, "HBM3": 2,
}

NVIDIA_ARCHS = {
    "Fermi": "Fermi Architecture: DX11 Legacy.",
    "Kepler": "Kepler (GTX 600/700): Good headroom, power limits apply.",
    "Maxwell": "Maxwell (GTX 900): High OC scaling, unlocked BIOS potential.",
    "Pascal": "Pascal (GTX 1000): Efficient architecture, voltage scales automatically.",
    "Turing": "Turing (RTX 2000 / GTX 16): Ray Tracing era, power limit sensitive.",
    "Ampere": "Ampere (RTX 3000): High power draw, undervolting highly recommended.",
    "Ada Lovelace": "Ada Lovelace (RTX 4000): Extremely power efficient.",
    "Blackwell": "Blackwell Architecture.",
}

AMD_ARCHS = {
    "GCN / TeraScale": "AMD Legacy GCN: High power draw, benefits from undervolting.",
    "RDNA 1/2/3": "AMD RDNA Architecture: Scales well with memory tuning and undervolting.",
}

INTEL_ARCHS = {
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
        self.background_color = (0.08, 0.04, 0.12, 1)
        self.color = WHITE
        self.font_name = MONO
        self.font_size = sp(12)


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

    if "M" in gpu_upper or "MOBILE" in gpu_upper:
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
                if "RTX 4" in name_up: specs["arch"] = "Ada Lovelace"
                elif "RTX 3" in name_up: specs["arch"] = "Ampere"
                elif "RTX 2" in name_up or "GTX 16" in name_up: specs["arch"] = "Turing"
                elif "GTX 10" in name_up: specs["arch"] = "Pascal"
                elif "GTX 9" in name_up or "QUADRO K" in name_up: specs["arch"] = "Maxwell"
                elif "GTX 6" in name_up or "GTX 7" in name_up: specs["arch"] = "Kepler"
                else: specs["arch"] = "Fermi"
            elif "RADEON" in name_up or "AMD" in name_up:
                if "RX" in name_up: specs["arch"] = "RDNA 1/2/3"
                else: specs["arch"] = "GCN / TeraScale"
            elif "INTEL" in name_up or "ARC" in name_up:
                specs["arch"] = "Intel Graphics"

        except Exception:
            pass

    return specs


# ---------- UI Helpers ----------
def paint(widget, fill, border=None):
    with widget.canvas.before:
        Color(*fill)
        rect = Rectangle(pos=widget.pos, size=widget.size)
    line = None
    if border:
        with widget.canvas.after:
            Color(*border)
            line = Line(rectangle=(*widget.pos, *widget.size), width=dp(1))

    def sync(*_):
        rect.pos, rect.size = widget.pos, widget.size
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
    head.add_widget(mono(title, WHITE, 13, bold=True))
    if tag:
        head.add_widget(mono(tag, GREY, 11, "right"))
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
    def __init__(self, color=AMBER, **kw):
        super().__init__(size_hint=(None, None), size=(dp(26), dp(26)), **kw)
        self.color = color
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
        self.color = PURPLE_LIGHT
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
    def __init__(self, value=0, color=PURPLE_LIGHT, marks=(), **kw):
        super().__init__(size_hint_y=None, height=dp(12), **kw)
        self.value, self.color, self.marks = value, color, marks
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


# ---------- App ----------
class OCApp(App):
    title = "OC//CALC v2.0.1 - Extreme Overclock & Experiment Suite"

    def build(self):
        self.fields = {}
        self.panels = []
        self.spinners_list = []
        self.buttons_list = []

        self.root_layout = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(8))

        # Header
        self.head_box = BoxLayout(size_hint_y=None, height=dp(58), padding=[dp(12), dp(6)])
        paint(self.head_box, PURPLE, PURPLE_LIGHT)
        left = BoxLayout(orientation="vertical")
        left.add_widget(mono("OC//CALC v2.0.1", WHITE, 20, bold=True))
        left.add_widget(mono("EXTREME OVERCLOCK & EXPERIMENT BENCH", GREY, 10))
        right = BoxLayout(orientation="vertical", size_hint_x=None, width=dp(120))
        led_row = AnchorLayout(anchor_x="right", anchor_y="center")
        self.led = Led()
        led_row.add_widget(self.led)
        self.status = mono("READY", PURPLE_LIGHT, 11, "right", True)
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
        self.results = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(10), padding=[0, 0, 0, dp(20)])
        self.results.bind(minimum_height=self.results.setter("height"))
        self.results_scroll.add_widget(self.results)

        # 1. GPU-Z Inspector Panel
        p_gpuz = panel("GPU-Z BUILT-IN", "DEEP SCANNER")
        self.panels.append(p_gpuz)
        self.gpuz_btn = Button(text="DETECT REAL HARDWARE (BENCHMARK)", size_hint_y=None, height=dp(34), bold=True,
                               font_name=MONO, font_size=sp(11), color=WHITE,
                               background_normal="", background_color=PURPLE_LIGHT)
        self.gpuz_btn.bind(on_release=self.run_gpuz_detection)
        self.buttons_list.append(self.gpuz_btn)
        p_gpuz.body.add_widget(self.gpuz_btn)
        self.inputs_main.add_widget(p_gpuz)

        # 2. GPU Specs Panel
        p1 = panel("GPU CONFIGURATION", "CARD")
        self.panels.append(p1)
        
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
                           font_name=MONO, font_size=sp(16), color=WHITE, background_normal="",
                           background_down="", background_color=PURPLE_LIGHT)
        self.apply_btn.bind(on_release=self.apply_oc)
        self.buttons_list.append(self.apply_btn)
        btn_layout.add_widget(self.apply_btn)

        row_btns_1 = BoxLayout(size_hint_y=None, height=dp(34), spacing=dp(6))
        for name, callback in [("EXPORT PRESET", self.export_preset_dialog), ("IMPORT PRESET", self.import_preset_dialog)]:
            b = Button(text=name, bold=True, font_name=MONO, font_size=sp(11), color=WHITE, background_normal="", background_color=PURPLE)
            b.bind(on_release=callback)
            self.buttons_list.append(b)
            row_btns_1.add_widget(b)
        btn_layout.add_widget(row_btns_1)

        row_btns_2 = BoxLayout(size_hint_y=None, height=dp(34), spacing=dp(6))
        for name, callback in [("SAVE CONFIG", self.save_config_file), ("CLEAR ALL", self.clear_all_fields), ("LAPTOP PROFILE", self.load_laptop_profile)]:
            b = Button(text=name, bold=True, font_name=MONO, font_size=sp(10), color=WHITE, background_color=PURPLE)
            b.bind(on_release=callback)
            self.buttons_list.append(b)
            row_btns_2.add_widget(b)
        btn_layout.add_widget(row_btns_2)
        
        self.inputs_main.add_widget(btn_layout)

        self.content_container.add_widget(self.inputs_scroll)
        self.content_container.add_widget(self.results_scroll)

        return self.root_layout

    def input_box(self, key, hint, text=False):
        ti = TextInput(hint_text=hint, multiline=False, input_filter=None if text else "float",
                       font_size=sp(14), font_name=MONO, halign="left" if text else "right",
                       background_normal="", background_active="", background_color=FIELD,
                       foreground_color=WHITE, hint_text_color=(0.42, 0.38, 0.52, 1),
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
                    color=WHITE, background_normal="", background_color=PURPLE,
                    option_cls=DarkSpinnerOption)
        setattr(self, attr, s)
        self.spinners_list.append(s)
        return s

    def labeled(self, label, widget):
        r = BoxLayout(size_hint_y=None, height=dp(36), spacing=dp(8))
        r.add_widget(mono(label, GREY, 12))
        r.add_widget(widget)
        return r

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
        is_amd = any(x in val_upper for x in ["AMD", "RADEON", "VEGA", "RX", "R9", "R7", "NAVI"])

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

        if is_intel:
            header_col, border_col, panel_bg = (0.15, 0.0, 0.45, 1), INTEL_BLUE, INTEL_PANEL_BG
        elif is_nvidia:
            header_col, border_col, panel_bg = (0.05, 0.20, 0.02, 1), NVIDIA_GREEN, NVIDIA_PANEL_BG
        elif is_amd:
            header_col, border_col, panel_bg = (0.22, 0.02, 0.02, 1), AMD_RED, AMD_PANEL_BG
        else:
            header_col, border_col, panel_bg = PURPLE, PURPLE_LIGHT, PANEL

        paint(self.head_box, header_col, border_col)
        for p in self.panels:
            paint(p.head_box, header_col)
            paint(p, panel_bg, border_col)
        for s in self.spinners_list:
            s.background_color = header_col
        self.apply_btn.background_color = border_col
        for b in self.buttons_list:
            if b != self.apply_btn and b != self.gpuz_btn:
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

    def clear_all_fields(self, *_):
        for ti in self.fields.values():
            ti.disabled = False
            ti.text = ""
        self.apply_btn.disabled = False
        self.arch_spin.disabled = False
        self.mem_spin.disabled = False
        self.results.clear_widgets()
        self.on_gpu_name_change(self.fields["gpu"], "")
        self.set_status("CLEARED", PURPLE_LIGHT)

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
        self.status.text, self.status.color = text, color
        self.led.set(color)

    def fail(self, text):
        self.set_status("INPUT ERROR", RED)
        p = panel("ALERTS", "ERROR")
        p.body.add_widget(warn_row(RED, text))
        self.results.add_widget(p)

    def apply_oc(self, *_):
        self.results.clear_widgets()
        gpu_name = self.fields["gpu"].text.strip().upper()
        
        if "NVS" in gpu_name or "QUADRO NVS" in gpu_name or "VEGA 64" in gpu_name:
            self.set_status("RESTRICTED", RED)
            p = panel("ALERTS", "LOCKED CARD")
            p.body.add_widget(warn_row(RED, "Overclocking Locked: Architecture does not support OC."))
            self.results.add_widget(p)
            return

        try:
            v = {k: float(self.fields[k].text) for k in NUM_FIELDS}
        except ValueError:
            return self.fail("Fill every numeric field before applying.")
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
        p.body.add_widget(mono(f"{v['mem_name']} ({v['vram_gb']:.0f}GB {v['arch_name']})  {r['speed_old']:.2f} > {r['speed_new']:.2f} Gbps", GREY, 11, size_hint_y=None, height=dp(16)))
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