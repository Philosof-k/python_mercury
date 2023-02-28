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

# Open serial port
ser = serial.serial_for_url("socket://172.30.100.115:4001")
print ('Connected:', ser.isOpen())

#chunk = struct.pack('B', sn)
chunk = b'\x01'  # код запроса
chunk += b'\x01'  # код уровня доступа
chunk += b'\x01'  # 1 символ пароля
chunk += b'\x11'  # 2 символ пароля
#chunk += b'\x01'  # 3 символ пароля
#chunk += b'\x01'  # 4 символ пароля
#chunk += b'\x01'  # 5 символ пароля
#chunk += b'\x01'  # 6 символ пароля
print ('chunk:', chunk)
# There are commands for get different data:
# \x2f - serial number
# \x21 - self time
# \x63 - get U,I,P
# \x27 - expended electricity distributed according to tariffs
# More information you can get there: http://www.incotexcom.ru/doc/M20x.rev2015.02.15.pdf
#chunk += b'\x27'
chunk += b'\x27'  # 3 символ пароля
print ('chunk:', chunk)
chunk = crc16(chunk)
print ('chunk:', chunk)

# Send data
ser.write(chunk)
time.sleep(1)
out = ser.read_all()
ser.close()

print ('Result string:', ':'.join('{:02x}'.format(c) for c in out))
print ('Check CRC:', out[-2:] == crc16(out[:-2])[-2:])
t1 = ''.join('{:02x}'.format(c) for c in out[5:9])
t2 = ''.join('{:02x}'.format(c) for c in out[9:13])
print ('T1 =', float(t1)*0.01, '(кВт*ч)', 'T2 =', float(t2)*0.01, '(кВт*ч)')
