import time
import subprocess

while True:
	try:
		import serial
		import serial.tools.list_ports
		import pandas as pd
		import plotly.express as px
		break
	except:
		ans = input('Missing libraries. Do you want me to install them for you? (pyserial pandas plotly) [Y]/n: ')
		if ans in ['N','n','no','No']:
			exit(0)
		else:
			subprocess.run("pip install pyserial pandas plotly", shell=True)
			print('')
			print('reloading libraries')


baudrate = 921600
hardware_id = '10C4:EA60'
connected = False
con_dic = {True:'CONNECTED',False:'DISCONNECTED'}
state = 'STOPPED'
dev_port = ''
infostr = ''

def plot_csv():
	df = pd.read_csv('data.csv')
	fig = px.line(df, x = 'time [ms]', y = 'value [mm]', title='Recorded Data from LVDT')
	fig.show()

def p_reline(str=''):
	global connected
	global dev_port
	global state
	infostr = f' {con_dic[connected]} │ {port} │ {state:9} │ '
	print(infostr + str,end='\r')

def start_connection(port):
	global state

	try:
		ser = serial.Serial(port=port,baudrate=baudrate)  # open serial port
	except:
		print('ERROR: Can not open Port - is it in use?')
		input('press any button to exit')
		exit(0)
	infostr = f' {con_dic[connected]} │ {port} │  {state}  │ '
	n = input(infostr + 'Enter seconds to record: ')
	try:
		n = int(n)
		if n > 60: n = 60
	except:
		print(' ERROR: you didnt enter a valid integer')
		exit(0)
	ser.write(b'0')     # write 0 = RECORD to MCU
	ans = ser.read_until(b'\nEND')
	try:
		state = ans[:-4].decode('UTF-8')
	except:
		try:
			state = ans[24:-4].decode('UTF-8')
		except:
			#print(f'{ans} not decodable')
			pass

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
	cache = b''
	while True:
		if ser.in_waiting > 0:
			cache += ser.read(ser.in_waiting)
			time.sleep(0.1)
		else:
			break
	try:
		check = cache[-21:-1]
		if check == b'END-OF-FILE-SEQUENCE':
			p_reline('Transfer successful')
		else:
			p_reline(check.decode('UTF-8'))
	except:
		p_reline('unexpected Error')

	with open('data.csv', 'wb') as f:
		f.write(cache[:-21])
	print()
	ser.close()             # close port
	state = 'STOPPED'
	p_reline()
	try:
		plot_csv()
	except:
		print('Plotting Error')


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
		




