// /dev/ttyACM0

/*
 * 224724  brand 1
910155 brand 2

RC522 MODULE     MEGA
SDA             D45
SCK             D52
MOSI            D51
MISO            D50
IRQ             N/A
GND             GND
RST             D43
3.3V             3.3V


 */

const unsigned int MAX_MESSAGE_LENGTH = 6;  //color message not more that this length

#include <SPI.h>
#include <MFRC522.h>
#include <FastLED.h>  // Include the FastLED Library


String TAG1  = "0241020";   // ------------------------------------- TAG1 ----------------------------------
String TAG2 = "19171020";    // ------------------------------------- TAG2 ------------------------------------


#define RST_1_PIN         43                            // Configurable, see typical pin layout above
#define SS_1_PIN          45                            // Configurable, see typical pin layout above

#define RPI_1_PIN         7   // to pin number 40 on jetson nano board
#define RPI_2_PIN         8   // to pin number 38 on jetson nano board
#define RPI_3_PIN         9

#define LED               13
#define NUM_LEDS 255  // Set the total number of LEDs from 1

CRGB leds[NUM_LEDS];  // Add these LEDs to an array
#define DATA_PIN 6    // Set the Data Pin that the LED data is transferred across

String Brand = String("");
MFRC522 mfrc522_1(SS_1_PIN, RST_1_PIN);  // Create MFRC522 instance
//MFRC522 mfrc522_2(SS_2_PIN, RST_2_PIN);  // Create MFRC522 instance
//MFRC522 mfrc522_3(SS_3_PIN, RST_3_PIN);  // Create MFRC522 instanc
// "do" function once LEDs have been configured
void showStrip() {
  FastLED.show();
}
// Set an individual pixel
void setPixel(int Pixel, byte red, byte green, byte blue) {
  leds[Pixel].r = red;
  leds[Pixel].g = green;
  leds[Pixel].b = blue;
}

// Sets all LEDs in the array to a specific colour / state
// uses bytes, not integers
void setAll(byte red, byte green, byte blue) {
  for (int i = 0; i < NUM_LEDS; i++ ) {
    setPixel(i, red, green, blue);
  }
  showStrip();
}


void setup() {
  Serial.begin(115200);   // Initialize serial communications with the PC
  SPI.begin();      // Init SPI bus

  mfrc522_1.PCD_Reset();
  mfrc522_1.PCD_Init();   // Init MFRC522
  mfrc522_1.PCD_SetAntennaGain(mfrc522_1.RxGain_max);
  mfrc522_1.PCD_AntennaOn();
  mfrc522_1.PCD_SoftPowerUp();
//  mfrc522_2.PCD_Reset();
//  mfrc522_2.PCD_Init();   // Init MFRC522
//  mfrc522_2.PCD_SetAntennaGain(mfrc522_1.RxGain_max);
//  mfrc522_2.PCD_AntennaOn();
//  mfrc522_2.PCD_SoftPowerUp();
//  digitalWrite(SS_1_PIN, HIGH);
//  digitalWrite(SS_2_PIN, HIGH);
//  mfrc522_3.PCD_Reset();
//  mfrc522_3.PCD_Init();   // Init MFRC522
//  mfrc522_3.PCD_SetAntennaGain(mfrc522_1.RxGain_max);
//  mfrc522_3.PCD_AntennaOn();
//  mfrc522_3.PCD_SoftPowerUp();
  delay(4);       // Optional delay. Some board do need more time after init to be ready, see Readme

  pinMode(LED, OUTPUT);
  pinMode(RPI_1_PIN, OUTPUT);
  pinMode(RPI_2_PIN, OUTPUT);
  pinMode(RPI_3_PIN, OUTPUT);
  digitalWrite(RPI_1_PIN, LOW);
  digitalWrite(RPI_2_PIN, LOW);
  digitalWrite(RPI_3_PIN, LOW);

    mfrc522_1.PCD_Reset();
    mfrc522_1.PCD_Init();   // Init MFRC522
    mfrc522_1.PCD_SetAntennaGain(mfrc522_1.RxGain_max);
    mfrc522_1.PCD_AntennaOn();
    mfrc522_1.PCD_SoftPowerUp();
    // initialize FastLED
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
  FastLED.setBrightness(50);
 showStrip();
 Green();
}
// Helper function that blends one uint8_t toward another by a given amount
void nblendU8TowardU8( uint8_t& cur, const uint8_t target, uint8_t amount)
{
  if( cur == target) return;

  if( cur < target ) {
    uint8_t delta = target - cur;
    delta = scale8_video( delta, amount);
    cur += delta;
  } else {
    uint8_t delta = cur - target;
    delta = scale8_video( delta, amount);
    cur -= delta;
  }
}

// Blend one CRGB color toward another CRGB color by a given amount.
// Blending is linear, and done in the RGB color space.
// This function modifies 'cur' in place.
CRGB fadeTowardColor( CRGB& cur, const CRGB& target, uint8_t amount)
{
  nblendU8TowardU8( cur.red,   target.red,   amount);
  nblendU8TowardU8( cur.green, target.green, amount);
  nblendU8TowardU8( cur.blue,  target.blue,  amount);
  return cur;
}

byte * Wheel(byte WheelPos) {
  static byte c[3];

  if(WheelPos < 85) {
   c[0]=WheelPos * 3;
   c[1]=255 - WheelPos * 3;
   c[2]=0;
  } else if(WheelPos < 170) {
   WheelPos -= 85;
   c[0]=255 - WheelPos * 3;
   c[1]=0;
   c[2]=WheelPos * 3;
  } else {
   WheelPos -= 170;
   c[0]=0;
   c[1]=WheelPos * 3;
   c[2]=255 - WheelPos * 3;
  }

  return c;
}

//////////////////////////////////NEW CODE BEGINS//////////////////////////////

void Blue() {

    for (int i = 0; i <= NUM_LEDS; i++) {

        leds[i] = CRGB(0,0,255);
    }
      showStrip();
  }


//////////////////////////////Change LED colour to white///////////////////////

void  White() {

    for (int i = 0; i <= NUM_LEDS; i++) {

        leds[i] = CRGB(255,255,255);
    }
      showStrip();
  }



void Green() {

    for (int i = 0; i <= NUM_LEDS; i++) {
        leds[i] = CRGB(0,255,0);
    }
      showStrip();
  }

void loop() {

  delay(10);
  String j = RFID_1_Check();


  if(j != "NULL" )
  {
    delay(1000);
    Serial.println(j);


                 char inByte = (char)Serial.read();
                     if (inByte == 'B')
                     {Blue();}
                      if (inByte == 'G')
                      {Green();}
                      if (inByte == 'W')
                      {White();}

  }

}


String RFID_1_Check(){
  int productNumber = 0;
  mfrc522_1.PCD_Reset();
  mfrc522_1.PCD_Init();   // Init MFRC522
  mfrc522_1.PCD_SetAntennaGain(mfrc522_1.RxGain_max);
  mfrc522_1.PCD_AntennaOn();
  mfrc522_1.PCD_SoftPowerUp();
  delay(15);
    // Look for new cards
  if ( ! mfrc522_1.PICC_IsNewCardPresent())
  {
//    Serial.print("\nNo Card1");
    return "NULL";
  }
  if ( ! mfrc522_1.PICC_ReadCardSerial())
  {
//    Serial.print("\nNo Comms");
    return "NULL";
  }
  String content= "";
  byte letter;
  int j;
  for (byte i = 0; i < mfrc522_1.uid.size; i++)
  {
     content.concat(String(mfrc522_1.uid.uidByte[i]/10,DEC));
  }

  //Serial.println(content);
  return content;
}