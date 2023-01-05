# HighPrecisionLVDT
This project is created during Praktikum Raumfahrtelektronik - Lehrstuhl für Raumfahrttechnik, Technische Universität München (TUM).
This board carries out submillimeter measurement of an actuator displacement. This is part of a testsetup for Regolith transport via hoppers.
As a sensing unit an LVDT is use, that is driven by a Signal Conditioner that is read by a 24-bit ADC to a MCU where the Experiment data is then delivered via WiFi.

Contributors: Beatriz Mas Sanz, Thilo Witzel and Sven Julius Steinert

# General Schematic
![schematic](doc/schematic.png)

# Partlist

|QTY|	DESCRIPTION	|PART NAME| PRICE | URL | 
| :---   | :---   | :---   | :---   | :---   |
|1|	LVDT Displacement Sensor |	Placeholder | 156€ |	[Mouser](https://www.mouser.de/ProductDetail/Measurement-Specialties/02560389-000?qs=%252BgKeJhng5iU0wv8eGISM%252BA%3D%3D) |
|1|	Microcontrollerboard |	ESP32-S3-DevKitC-1-N32R8V | 18€ | [Mouser](https://www.mouser.de/ProductDetail/Espressif-Systems/ESP32-S3-DevKitC-1-N32R8V?qs=Li%252BoUPsLEnvTvWIWLPCZ4g%3D%3D) [Doc](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/hw-reference/esp32s3/user-guide-devkitc-1.html)|
|1|	24-bit ADC | ADS1220  | 11€ |	x |
|1|	LVDT Signal Conditioner | AD698  | 54€  |	[Mouser](https://www.mouser.de/ProductDetail/Analog-Devices/AD698APZ?qs=NmRFExCfTkEHAhvFCYrQIg%3D%3D) |
|1|	PSU | 1W +15/-15V  | x  |	[Reichelt](https://www.reichelt.de/dc-dc-wandler-nma-1-w-15-v-33-ma-sil-dual-nma0515sc-p140635.html?&nbc=1) |
|4|	Capacitor | 16V  2200 µF  | x  |	[Reichelt](https://www.reichelt.de/elko-radial-2200-f-16-v-105-low-esr-12-5x25-mm-rm-5-rad-lxz-16-2k2-p166372.html?&nbc=1) |
