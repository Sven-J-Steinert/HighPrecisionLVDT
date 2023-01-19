#include <Arduino.h>

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

void setup() {
  pinMode(A0,INPUT);
  // put your setup code here, to run once:
  Serial.begin(921600);
  // dynamically Allocate 48kB of RAM for time_RAM
  time_RAM = new long[RAM_STORAGE_SIZE];
  // dynamically Allocate 48kB of RAM for value_RAM
  value_RAM = new double[RAM_STORAGE_SIZE];
}

void loop() {
  // put your main code here, to run repeatedly:

  if (record){
    if(index_RAM < RAM_STORAGE_SIZE){
      // read ADC
      value = analogRead(A0);
      // prepare value and time to write
      time_buffer = (millis()-ref_time);
      val_buffer = value;

      time_RAM[index_RAM] = time_buffer;
      value_RAM[index_RAM] = val_buffer;
      ++index_RAM;

      delay(10);
      }
    }
  else if (stream){
    // read ADC
    val_buffer = analogRead(A0);
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
        ref_time = millis();
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