import serial
import serial.tools.list_ports

def btn_record():
    ports_list = list(serial.tools.list_ports.comports())
    com = ''
    ser = None
    if len(ports_list) < 0:
        print('no serial')
    else:
        for comport in ports_list:
            if 'USB-SERIAL CH340'in list(comport)[1]:
                print(list(comport)[0],':', list(comport)[1])
                com = list(comport)[0]
        ser = serial.Serial(com, 115200)
        if ser.isOpen():
            print('ok')      
            ser.write(bytearray([0xf0]))
            ser.close()
            
# btn_record()