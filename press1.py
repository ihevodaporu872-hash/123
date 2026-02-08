"""
Каждые 3 минуты нажимает клавишу '1'.
Закрытие окна консоли (Ctrl+C или крестик) — всё останавливается.
Без зависимостей — только стандартная библиотека + Windows API.
"""

import ctypes
import ctypes.wintypes
import time
import sys

# Windows SendInput API
PUL = ctypes.POINTER(ctypes.c_ulong)

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.wintypes.WORD),
        ("wScan", ctypes.wintypes.WORD),
        ("dwFlags", ctypes.wintypes.DWORD),
        ("time", ctypes.wintypes.DWORD),
        ("dwExtraInfo", PUL),
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.wintypes.DWORD),
        ("ki", KEYBDINPUT),
        ("padding", ctypes.c_ubyte * 8),
    ]

KEYEVENTF_KEYUP = 0x0002
INPUT_KEYBOARD = 1
VK_1 = 0x31  # Virtual key code for '1'

def press_key(vk_code):
    # Key down
    inp = INPUT()
    inp.type = INPUT_KEYBOARD
    inp.ki.wVk = vk_code
    inp.ki.dwFlags = 0
    ctypes.windll.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))
    time.sleep(0.05)
    # Key up
    inp.ki.dwFlags = KEYEVENTF_KEYUP
    ctypes.windll.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

INTERVAL = 3 * 60  # 3 минуты в секундах

print("=== Автонажатие клавиши '1' каждые 3 минуты ===")
print("Закройте окно или нажмите Ctrl+C для остановки.")
print()

try:
    while True:
        now = time.strftime("%H:%M:%S")
        print(f"[{now}] Нажимаю '1'...")
        press_key(VK_1)
        print(f"[{now}] Жду 3 минуты...")
        time.sleep(INTERVAL)
except KeyboardInterrupt:
    print("\nОстановлено.")
    sys.exit(0)
