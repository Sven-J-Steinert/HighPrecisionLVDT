#include <Arduino.h>
#include <ADS1220_WE.h>
#include <SPI.h>

// 24-bit ADC
#define ADS1220_CS_PIN    10 // chip select pin
#define ADS1220_DRDY_PIN  8 // data ready pin 

ADS1220_WE ads = ADS1220_WE(ADS1220_CS_PIN, ADS1220_DRDY_PIN); // using Default SPI Pins

// RAM Storage
#define RAM_STORAGE_SIZE 12000 // with 100 [Hz] results in 120 [s] max
long *time_RAM; // 4 Bytes per entry
double *value_RAM; // 4 Bytes per entry

int index_RAM = 0;
double val_buffer;
double time_buffer;
char val_buffer_str[50];

byte incomingByte = 0; // for incoming serial data
String header = "time [ms],value [mm]\n" ; // table head
String databuffer = "" ; // buffer for recording data

bool record = false;
bool stream = false;
unsigned long ref_time = 0;
double value = 0.0;
ulong last_measure = 0;

void setup() {
  // MCU bootinfo during startup is passed in 115200 baudrate
  Serial.begin(921600); // very high speed, no bitloss observed however
  // dynamically Allocate 48kB of RAM for time_RAM
  time_RAM = new long[RAM_STORAGE_SIZE];
  // dynamically Allocate 48kB of RAM for value_RAM
  value_RAM = new double[RAM_STORAGE_SIZE];
  // initialize ADC
  if(!ads.init()){
    Serial.println("ERROR | ADS1220 not found!"); // should hopefully never occur
    while(1);
  }
  ads.bypassPGA(true);
  ads.setRefp0Refn0AsVefAndCalibrate();
  ads.setCompareChannels(ADS1220_MUX_0_AVSS); // measure IN0 to AVSS (AVDD as max value)
  ads.setDataRate(ADS1220_DR_LVL_6);
}

void loop() {
  

  if (record){
    if(index_RAM < RAM_STORAGE_SIZE && millis()>=last_measure+10){
      last_measure = millis();
      // read ADC
      value = ads.getVoltage_mV();
      // prepare value and time to write
      time_buffer = (millis()-ref_time);
      val_buffer = value;

      time_RAM[index_RAM] = time_buffer;
      value_RAM[index_RAM] = val_buffer;
      ++index_RAM;

      //delay(10); // could've been also done via interrupts for more accurate timing performance
      // interrupts not implemented due to missing necessity
      }
    }
  else if (stream){
    // read ADC
    val_buffer = ads.getVoltage_mV();
    dtostrf(val_buffer, 10, 8, val_buffer_str);
    Serial.println(val_buffer_str);
    delay(10);
  }

  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();

    switch(incomingByte) {
      case 48:
        // Start Recording = '0' = 48 [ASCII]
        index_RAM = 0; // reset buffer
        Serial.print("RECORDING");
        Serial.print("\nEND");
        record = true;
        stream = false;
        ref_time = millis()+1;
        break;
      case 49:
        // Stop Recording = '1' = 49 [ASCII]
        Serial.print("STOPPED");
        Serial.print("\nEND");
        record = false;
        stream = false;
        break;
      case 50:
        // Start Download = '2' = 50 [ASCII]
        Serial.print("DOWNLOAD");
        Serial.print("\nEND");
        
        Serial.print(header);
        for (int i = 0; i < index_RAM; ++i)
          {
            Serial.print(time_RAM[i]);
            Serial.print(',');
            dtostrf(value_RAM[i], 10, 8, val_buffer_str);
            Serial.print(val_buffer_str);
            Serial.print('\n');
          }
        
        Serial.print("END-OF-FILE-SEQUENCE\n");
        break;
      case 51:
        // Enable Stream Data = '3' = 51 [ASCII]
        stream = true;
        Serial.println("Stream Data Enabled");
        break;
      case 52:
        // Disable Stream Data = '4' = 52 [ASCII]
        stream = false;
        Serial.println("Stream Data Disabled");
      default:
        break;
    }
  }
}