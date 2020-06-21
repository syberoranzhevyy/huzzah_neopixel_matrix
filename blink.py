def blink(num, pin=2):
    import machine
    import time
    led = machine.Pin(pin, machine.Pin.OUT)
    i = 0
    for i in range(num):
        time.sleep_ms(50)
        led.value(False) # LED an
        time.sleep_ms(50)
        led.value(True) # LED aus
    if num == 0:
        led.value(False) # LED an

