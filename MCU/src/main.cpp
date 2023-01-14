#include <Arduino.h>
#include <EEPROM.h>

byte incomingByte = 0; // for incoming serial data
String databuffer = "time, value [mm]\n" ; // buffer for recording data
bool record = false;
unsigned long ref_time = 0;
double value = 1.50040301;
char val_buffer[50];
char time_buffer[50];
u_long addr = 0;
int EEPROM_cache = 0;

// define the number of bytes you want to access
#define EEPROM_SIZE 400

void setup() {
  // put your setup code here, to run once:
  Serial.begin(500000);
  EEPROM.begin(EEPROM_SIZE);
}

void loop() {
  // put your main code here, to run repeatedly:

  if (record){
    dtostrf(value, 10, 8, val_buffer);
    dtostrf(double(millis()-ref_time), 5, 0, time_buffer);
    databuffer = time_buffer + String(",") + val_buffer + String("\n");
    for (int i = 0; i < databuffer.length(); ++i)
    {
      EEPROM.write(addr, int(databuffer[i]));
      ++addr;
    }
    EEPROM.commit();

    delay(10);
  }

  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();

    switch(incomingByte) {
      case 48:
        // Start Recording = '0' = 48 [ASCII]
        databuffer = "time, value [um]\n" ; // reset buffer
        addr = 0;
        Serial.print("RECORDING");
        Serial.print("\nEND");
        record = true;
        ref_time = millis();
        break;
      case 49:
        // Stop Recording = '1' = 49 [ASCII]
        Serial.print("STOPPED");
        Serial.print("\nEND");
        record = false;
        break;
      case 50:
        // Start Download = '2' = 50 [ASCII]
        Serial.print("DOWNLOADING");
        Serial.print("\nEND");

        //EEPROM_SIZE
        for (int i = 0; i < EEPROM_SIZE; ++i)
        {
          EEPROM_cache = EEPROM.read(i);
          Serial.print(char(EEPROM_cache));
          //if (EEPROM_cache == 0x00)
          //{
          //  break;
          //}
        }
        Serial.print("END");
        break;
      default:
        break;
    }


    // say what you got:
    //Serial.print("I received: ");
    //Serial.println(incomingByte);
  }
}