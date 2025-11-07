# main.py
# Sends Power IR signal (PlayStation 2) on Pico startup
# Simulates button hold for ~2 seconds

from machine import Pin, PWM
import time

# --- Settings ---
IR_PIN = 15          # GPIO for IR LED
START_DELAY = 0.1    # delay before sending (sec)
HOLD_TIME = 2.5      # button "hold" duration (sec)
INTER_REPEAT_MS = 40 # pause between packet repeats
LOWER_POWER = False  # False = brighter (if resistor >= 220 Ohm)
CARRIER_DUTY = 32768 if not LOWER_POWER else 20000  # Brightness,  MAX Value 65535 

# --- PRONTO_HEX code for Power button (PS2) ---
PRONTO_HEX = "0000 0067 0000 0015 0060 0018 0030 0018 0018 0018 0030 0018 0018 0018 0030 0018 0018 0018 0018 0018 0018 0018 0030 0018 0018 0018 0030 0018 0030 0018 0018 0018 0030 0018 0018 0018 0030 0018 0030 0018 0018 0018 0030 0018 0030 01E0"

# --- Initialize PWM on pin ---
pwm = PWM(Pin(IR_PIN))
pwm.duty_u16(0)

# --- Functions ---
def parse_pronto(pronto_str):
    """Parses Pronto HEX and returns (freq_hz, list_of_durations)."""
    parts = pronto_str.strip().split()
    words = [int(x, 16) for x in parts if x.strip() != ""]
    if words[0] != 0x0000:
        raise ValueError("0000 format required (RAW pronto).")
    freq_word = words[1]
    freq_hz = 1.0 / (freq_word * 0.241246e-6)  # formula from Pronto specification
    durations = words[4:]  # skip header
    return freq_hz, durations

def pronto_to_us(freq_hz, durations):
    """Converts pronto words to microseconds."""
    unit_us = 1e6 / freq_hz
    return [max(1, int(round(d * unit_us))) for d in durations]

def send_hold(pronto_str, hold_time_s=2.0, inter_repeat_ms=40, duty=CARRIER_DUTY):
    """Simulates button hold - repeats packet for hold_time_s."""
    freq_hz, durations_words = parse_pronto(pronto_str)
    pwm.freq(int(round(freq_hz)))
    durations_us = pronto_to_us(freq_hz, durations_words)
    
    print(f"Frequency: {int(freq_hz)} Hz, hold: {hold_time_s} sec")
    start_ms = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start_ms) < hold_time_s * 1000:
        for i, dur in enumerate(durations_us):
            pwm.duty_u16(duty if i % 2 == 0 else 0)
            time.sleep_us(dur)
        pwm.duty_u16(0)
        time.sleep_ms(inter_repeat_ms)
    pwm.duty_u16(0)

# --- Main logic ---
time.sleep(START_DELAY)
print("Sending PS2 Power (hold 2 seconds)...")
send_hold(PRONTO_HEX, hold_time_s=HOLD_TIME, inter_repeat_ms=INTER_REPEAT_MS)
print("Done.")
pwm.deinit()
