# Este es el programa que va en el microcontrolador ESP32
# se agrega acá como referecia, pero debe ser cargado en el
# microcontrolador con algun IDE que lo permita la interacción
# con los microcontroladores. En este caso hice uso de Thonny 3.2.7

import socket, network, time, json
import sys
from machine import Pin
from machine import ADC

adc_temp = ADC(Pin(39))
adc_temp.atten(ADC.ATTN_11DB)
adc_temp.width(ADC.WIDTH_12BIT)

adc_fot = ADC(Pin(36))
adc_fot.atten(ADC.ATTN_11DB)
adc_fot.width(ADC.WIDTH_10BIT)


def read_sensors():
    sensor1 = adc_temp.read()
    time.sleep_ms(10)
    sensor2 = adc_fot.read()
    return sensor1, sensor2


def do_connect():
    # import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('home', 'default02')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


def my_socket():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('192.168.0.101', 10000)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

    try:
        # Send data
        my_data = json.dumps(read_sensors())
        print(my_data)
        sock.send(my_data)

    finally:
        print('closing socket')
        sock.close()

do_connect()
my_socket()