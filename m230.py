import serial
import struct
import time

sn = 50

def crc16(data):
    crc = 0xFFFF 
    l = len(data)
    i = 0
    while i < l:
        j = 0
        crc = crc ^ data[i]
        while j < 8:
            if (crc & 0x1):
                mask = 0xA001
            else:
                mask = 0x00
            crc = ((crc >> 1) & 0x7FFF) ^ mask
            j += 1
        i += 1
    if crc < 0:
        crc -= 256
    result = data + chr(crc % 256).encode() + chr(crc // 256).encode('latin-1')
    return result

# Открываем соединение
#ser = serial.Serial('/dev/ttyUSB0', 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
ser = serial.serial_for_url("socket://172.30.100.115:4001")
print ('Connected:', ser.isOpen())

#print (crc16("321234453432"))

# \x2f - Команда для получения серийного номера
chunk = struct.pack('>L', int(sn))
chunk += b'\x2f'
chunk = crc16(chunk)

print ('chunk:', chunk)

# Отправим данные на счетчик и получим информацию с него
ser.write(chunk)
time.sleep(1)
out = ser.read_all()
ser.close()

print ('Check CRC:', out[-2:] == crc16(out[:-2])[-2:])
print ('Result string:', ':'.join('{:02x}'.format(c) for c in out))
