# HighPrecisionLVDT
This project is created during Praktikum Raumfahrtelektronik - Lehrstuhl für Raumfahrttechnik at the Technische Universität München (TUM).
This board carries out submillimeter measurement of an actuator displacement, which is part of a test-setup to transport Regolith via hoppers.
As a sensing unit an LVDT is used, that is driven by a Signal Conditioner which gets read by a 24-bit ADC to a MCU where the Experiment data is then delivered via USB.

Contributors: [Beatriz Mas Sanz](https://github.com/beatrizmassanz), [Thilo Witzel](https://github.com/TheWisator) and [Sven Julius Steinert](https://github.com/Sven-J-Steinert)

# Application

The [Python app](app/cli.py) gives easy access to the recording functionality. However the MCU can also be controlled directly via COM Terminal with the following commands

| CMD |	HEX | FUNCTION | ANSWER | 
| :---:   | :---   | :---   | :---   |
| '0' |	0x48 | start recording | RECORDING\nEND | 
| '1' |	0x49 | stop recording | STOPPED\nEND | 
| '2' |	0x50 | start download | <.csv file> | 
| '3' |	0x51 | Enable STREAM | < values > | 
| '4' |	0x52 | Disable STREAM |  | 

# Hardware Connections

The PCB has to be connected to the sensor and a computer to operate. The power and data transmission are

PCB designator | LVDT Cable | FUNCTION | 
| :---: | :--- | :--- |
| PYRD | yellow - red | Primary Coil | 
| PYBK | yellow- black | Primary Coil | 
| SBK | black | Secondary Coil | 
| SRD | red | Secondary Coil | 
| SBL | blue | Secondary Coil |
| SGN | green | Secondary Coil |

# Schematic
![pcb](doc/pcb.png)
![schematic](doc/schematic.png)

# Partlist

|Mfr. No|Manufacturer|Description|Qty.|Price|
|:----|:----|:----|----:|----:|
|02560389-000|TE Connectivity|Linear Displacement Sensors HR 050 LVDT .05in|1|166,31 €|
|AD698APZ|Analog Devices Inc.|Sensor Interface LVDT SIGNAL CONDITIONER|1|54,27 €|
|ADS1220IPWR|Olimex| BB-ADS1220 4 Channel Sigma Delta Precise 24-Bit ADC Breakboard | 1 | 13,00 €|
|ESP32-S3-DevKitC-1-N8|Espressif|WiFi Development Tools - 802.11 ESP32-S3 General-Purpose Development Board, ESP32-S3-WROOM-1-N8, with Pin Header|1|15,00 €|
|ERJ-8ENF1742V|Panasonic|Thick Film Resistors - SMD 1206 17.4Kohms 1% AEC-Q200|3|0,18 €|
|ERA-8AEB1692V|Panasonic|Thin Film Resistors - SMD 1206 16.9Kohm 25ppm 0.1% AEC-Q200|3|0,66 €|
|TNPW12066K26BEEN|Vishay|Thin Film Resistors - SMD 6.26Kohms .1% 25ppm|3|0,92 €|
|HV732BTTD1004D|KOA Speer|Thick Film Resistors - SMD 0.25W 1M 0.5% 500 VOLTS|3|0,563 €|
|C1206C104J1RACAUTO|KEMET|Multilayer Ceramic Capacitors MLCC - SMD/SMT 100V 0.1uF X7R 1206  5% AEC-Q200|13|0,199 €|
|12065A102GAT4A|KYOCERA AVX|Multilayer Ceramic Capacitors MLCC - SMD/SMT 50V 1000pF C0G 1206 2% Tol|3|0,65 €|
|12065C334JAT2A|KYOCERA AVX|Multilayer Ceramic Capacitors MLCC - SMD/SMT 50V 0.33uF X7R 1206 5%|7|0,491 €|
|12062A102GAT2A|KYOCERA AVX|Multilayer Ceramic Capacitors MLCC - SMD/SMT 200V 1000pF C0G 1206 2% Tol|3|0,87 €|
|PX-28LCC|Kycon|IC & Component Sockets LCC 28P PBT|2|1,75 €|
|CR1206-FX-47R0ELF|Bourns|Thick Film Resistors - SMD 47ohm 1%|11|0,045 €|
|CR0402-FX-4533GLF|Bourns|Thick Film Resistors - SMD CHIP RESISTOR|10|0,058 €|
|B41888C4228M000|EPCOS / TDK|Aluminium Electrolytic Capacitors - Radial Leaded 16VDC 2200uF 20% STD Leads|4|1,89 €|
|C1206C685K4PACTU|KEMET|Multilayer Ceramic Capacitors MLCC - SMD/SMT 16V 6.8uF X5R 1206 10%|5|0,87 €|
|NMA0515SC|Murata|Isolated DC/DC Converters - Through Hole 1W  5-15V SIP DUAL DC/DC|2|5,08 €|
|12063A103FAT2A|KYOCERA AVX|Multilayer Ceramic Capacitors MLCC - SMD/SMT 25V 0.01uF C0G 1206 1%|3|0,96 €|
