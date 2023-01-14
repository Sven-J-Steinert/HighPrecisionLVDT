import time
import serial
import serial.tools.list_ports

baudrate = 921600
hardware_id = '10C4:EA60'
connected = False
con_dic = {True:'CONNECTED',False:'DISCONNECTED'}
state = 'STOPPED'
dev_port = ''
infostr = ''

def p_reline(str=''):
	global connected
	global dev_port
	global state
	infostr = f' {con_dic[connected]} │ {port} │ {state:9} │ '
	print(infostr + str,end='\r')

def start_connection(port):
	global state

	ser = serial.Serial(port=port,baudrate=baudrate)  # open serial port
	infostr = f' {con_dic[connected]} │ {port} │  {state}  │ '
	n = input(infostr + 'Enter seconds to record: ')
	try:
		n = int(n)
	except:
		print(' ERROR: you didnt enter a valid number')
		exit(0)
	ser.write(b'0')     # write 0 = RECORD to MCU
	ans = ser.read_until(b'\nEND')
	try:
		state = ans[:-4].decode('UTF-8')
	except:
		try:
			state = ans[24:-4].decode('UTF-8')
		except:
			print(f'{ans} not decodable')

	for i in range(n):
		p_reline(f'{i}/{n}')
		time.sleep(1)
	p_reline(f'{n}/{n}')

	ser.write(b'1')     # write 1 = STOPP to MCU
	ans = ser.read_until(b'\nEND')
	state = ans[:-4].decode('UTF-8')
	p_reline('       ')

	ser.write(b'2')     # write 1 = DOWNLOAD to MCU
	ans = ser.read_until(b'\nEND')
	state = ans[:-4].decode('UTF-8')
	p_reline()
	cache = ''
	while True:
		data = ser.read_until(b'\n').decode('UTF-8')
		if 'END-OF-FILE-SEQUENCE' in data:
			break
		p_reline(data.split(',')[0])
		cache += data

	with open('data.txt', 'w') as f:
		f.write(cache)
	print()
	ser.close()             # close port
	state = 'STOPPED'
	p_reline()


print("""
┌───────────────────────────────────────────────────────────────────────┐
│ ████ █████    High Precision LVDT Control                             │
│  █ █ █ █ █                                                            │
│  █ ███ █ █    https://github.com/Sven-J-Steinert/HighPrecisionLVDT	│
└───────────────────────────────────────────────────────────────────────┘""")

while True:
	connected = False
	while not connected:
		ports = serial.tools.list_ports.comports()
		for port, desc, hwid in sorted(ports):
			print(f'DISCONNECTED',end='\r')
			if hardware_id in hwid:
				dev_port = port
				connected = True
		time.sleep(0.1)
	start_connection(port)
		




