# main.py
# Отправляет ИК-сигнал Power (PlayStation 2) при старте Pico
# Имитация удержания кнопки ~2 секунды

from machine import Pin, PWM
import time

# --- Настройки ---
IR_PIN = 15          # GPIO для ИК светодиода
START_DELAY = 0.1    # задержка перед отправкой (сек)
HOLD_TIME = 2.5      # длительность "удержания" кнопки (сек)
INTER_REPEAT_MS = 40 # пауза между повторами пакета
LOWER_POWER = False  # False = ярче (если резистор >= 220 Ом)
CARRIER_DUTY = 52768 if not LOWER_POWER else 20000  # заполнение несущей

# --- PRONTO_HEX код кнопки Power (PS2) ---
PRONTO_HEX = "0000 0067 0000 0015 0060 0018 0030 0018 0018 0018 0030 0018 0018 0018 0030 0018 0018 0018 0018 0018 0018 0018 0030 0018 0018 0018 0030 0018 0030 0018 0018 0018 0030 0018 0018 0018 0030 0018 0030 0018 0018 0018 0030 0018 0030 01E0"

# --- Инициализация PWM на пине ---
pwm = PWM(Pin(IR_PIN))
pwm.duty_u16(0)

# --- Функции ---
def parse_pronto(pronto_str):
    """Разбирает Pronto HEX и возвращает (freq_hz, list_of_durations)."""
    parts = pronto_str.strip().split()
    words = [int(x, 16) for x in parts if x.strip() != ""]
    if words[0] != 0x0000:
        raise ValueError("Требуется формат 0000 (RAW pronto).")
    freq_word = words[1]
    freq_hz = 1.0 / (freq_word * 0.241246e-6)  # формула из спецификации Pronto
    durations = words[4:]  # пропускаем заголовок
    return freq_hz, durations

def pronto_to_us(freq_hz, durations):
    """Конвертирует слова pronto в микросекунды."""
    unit_us = 1e6 / freq_hz
    return [max(1, int(round(d * unit_us))) for d in durations]

def send_hold(pronto_str, hold_time_s=2.0, inter_repeat_ms=40, duty=CARRIER_DUTY):
    """Имитация зажатия кнопки — повторяем пакет в течение hold_time_s."""
    freq_hz, durations_words = parse_pronto(pronto_str)
    pwm.freq(int(round(freq_hz)))
    durations_us = pronto_to_us(freq_hz, durations_words)
    
    print(f"Частота: {int(freq_hz)} Гц, удержание: {hold_time_s} сек")
    start_ms = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start_ms) < hold_time_s * 1000:
        for i, dur in enumerate(durations_us):
            pwm.duty_u16(duty if i % 2 == 0 else 0)
            time.sleep_us(dur)
        pwm.duty_u16(0)
        time.sleep_ms(inter_repeat_ms)
    pwm.duty_u16(0)

# --- Основная логика ---
time.sleep(START_DELAY)
print("Отправка PS2 Power (удержание 2 секунды)...")
send_hold(PRONTO_HEX, hold_time_s=HOLD_TIME, inter_repeat_ms=INTER_REPEAT_MS)
print("Готово.")
pwm.deinit()


