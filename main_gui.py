import PySimpleGUI as sg
import serial
import time
from binascii import unhexlify


def execute(uart, command, verbose=True):
    uart.write(command.encode())
    if verbose:
        print('>: ' + command)
    ret = uart.read_until(b'#OK>>:')
    if verbose:
        print('<: ' + ret.decode())
    return ret


def read_reg(uart, address, verbose=True):
    cmd = "rdreg" + hex(address)
    uart.write(cmd.encode())
    if verbose:
        print('>: ' + cmd)
    ret = uart.read_until(b'#OK>>:')
    if verbose:
        print('<: ' + ret.decode())
    return ret


# Initialize UART
def connect(port, baudrate):
    uart = serial.Serial(port, 9600, timeout=5)
    while True:
        print('Sending the "UXTDWU" command...')
        buffer = bytearray();
        uart.write('UXTDWU'.encode())
        time.sleep(0.0566)
        # This response from the MCU should be b'\x00cmd>>:'
        while uart.in_waiting:
            msg = uart.read(1)
            buffer.append(msg[0])
            if buffer.endswith(b'cmd>>:'):
                print('Response is:', buffer)
                break
        if buffer.endswith(b'cmd>>:'):
            break
    time.sleep(0.1)
    # Changing the baudrate
    uart.baudrate = 115200
    time.sleep(0.1)

    # Change baudrate if necessary
    if baudrate != 115200:
        None

    return uart


EXECUTE = 'Execute'
QUIT = 'Quit'
CONNECT = 'Connect'
SWITCH_BAUD = 'Switch Baud'
READ_ADDR = 'Read Address'

PORT = 'port'
BAUD_RATE = 'baud_rate'
COMMAND = 'command'
RESULT = 'result'
ADDRESS = 'address'
REG_VALUE = 'reg_value'

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Text('ST17H66 Utils:')],
          [sg.Text('Porte:'), sg.InputText(key=PORT, default_text='COM3')],
          [sg.Text('Baud rate:'), sg.InputText(key=BAUD_RATE, default_text='115200')],
          [sg.Button(CONNECT), sg.Button(SWITCH_BAUD)],
          [sg.HorizontalSeparator()],
          [sg.Button('#rdrev'), sg.Button('#er512'), sg.Button('#er64k'), sg.Button('#era4k'), sg.Button('#erall'), sg.Button('#crc16')],
          [sg.Text('Command:'), sg.InputText(key=COMMAND)],
          [sg.Text('Result:'), sg.Multiline(size=32, key=RESULT, no_scrollbar=True, disabled=True, background_color='black', text_color='green')],
          [sg.Button(EXECUTE)],
          [sg.HorizontalSeparator()],
          [sg.Text('Addr:'), sg.InputText(key=ADDRESS, default_text='0x00000000')],
          [sg.Text('Value:'), sg.Multiline(size=32, key=REG_VALUE, no_scrollbar=True, disabled=True, background_color='black', text_color='green')],
          [sg.Button(READ_ADDR)],
          [sg.HorizontalSeparator()],
          [sg.Button(QUIT)]
]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
my_uart = None
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == QUIT: # if user closes window or clicks cancel
        break
    if event == CONNECT:
        my_uart = connect(values[PORT], values[BAUD_RATE])
    if event == EXECUTE:
        print('You entered ', values[COMMAND])
        command = values[COMMAND]
        if command.startswith('er'):
            y_n = sg.popup_yes_no('This is an Erase command. Are you sure?')
            if y_n == 'No':
                continue
        res = execute(my_uart, command)
        window[RESULT].update(value=res)
    if event == READ_ADDR:
        print('You entered ', values[ADDRESS])
        address = int(values[ADDRESS], 0) #we'll do base guessing!
        res = read_reg(my_uart, address)
        window[REG_VALUE].update(value=res)
    if event.startswith('#'):
        command = event[1:]
        window[COMMAND].update(value=command)

window.close()