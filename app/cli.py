import serial.tools.list_ports
import serial
import time

ports = serial.tools.list_ports.comports()
hardware_id = '10C4:EA60'
for port, desc, hwid in sorted(ports):
	if hardware_id in hwid:
		ser = serial.Serial(port)  # open serial port
		ser.close() 
		ser = serial.Serial(port)  # open serial port
		ser.baudrate = 500000
		print(ser.name)         # check which port was really used

		ser.write(b'0')     # write a string
		ans = ser.read_until(b'\nEND')
		print(ans)

		n = 5
		for i in range(n):
			print(f'{i}/{n}',end='\r',flush=True)
			time.sleep(1)

		ser.write(b'1')     # write a string
		ans = ser.read_until(b'\nEND')
		print(ans)

		ser.write(b'2')     # write a string
		ans = ser.read_until(b'\nEND')
		print(ans)
		data = ser.read_until(b'END').decode('UTF-8')
		print(data)
		with open('data.txt', 'w') as f:
			f.write(data.split('END')[0])
		print(ans)
		ser.close()             # close port
		break




