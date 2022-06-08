/*********************************************************************
  Displays magnetic field measurements on OLED

  Magnetic field sensor: TLV493D
  OLED: 128x32 graphic display
  OLED Driver: SSD1306 (I2C)

  Trevor Bruns
  Dominick Ropella
  September 2018
*********************************************************************/

//#include <ros.h> //enable ROS communications
//#include <geometry_msgs/Vector3.h> //ROS msg type
#include <SPI.h> //SPI Communications
#include "TLV493D.h"  //Magnetic sensor header file
#include "Wire.h"  //for I2C comm
#include <Adafruit_GFX.h>  //Graphics header
#include <Adafruit_SSD1306.h> //OLED Screen header

// Set up ROS node and publisher
//geometry_msgs::Vector3 magfield_msg;
//ros::Publisher pub_field("Magnetic_Field", &magfield_msg);
//ros::NodeHandle nh;

TLV493D magSensor;
const int i2c_sda = 18;
double maxB = 20; // [mT] max expected B field value

//Setup Status LEDs
const int device_pwr_pin = 4;
const int device_data_pin = 7;
const int device_ros_pin = 10;

uint8_t debug = 0;

int xMag = 0;
int yMag = 0;
int zMag = 0;

#define OLED_RESET 14
Adafruit_SSD1306 display(OLED_RESET); //reset (wipe) display

const int pixPosUnitX = 66;
const int pixOffsetX = 23; //for equals sign
const int pixVert = 8; //vertical pixel spacing unit going from top to bottom
const int pixLoopTimeX = 100;
const int pixLoopTimeY = 24;
int16_t  X1, Y1;
int16_t  X2, Y2;
int16_t  X3, Y3;
int16_t  X4, Y4;
uint16_t w, h; //full width/height of drawing area for each bar
int16_t barX = pixPosUnitX + 14; //starting x position of each bar
int16_t barY = 3; //starting y position of first bar (pixel dead space padding between bars)
uint16_t barW = 128 - barX; //full/max bar width
uint16_t barH = 3; //bar height
uint16_t barFillX, barFillY, barFillZ; //Amount to fill bar for X,Y,Z field
const bool display_flag = true; //choose to display field data or not. With data displayed, ~15Hz sample rate. With display off, ~500 Hz sample rate.
const int history_size = 10;
double mag_field_history[3][history_size] = {{0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}};
int16_t history_index = 0;

void setup()   {
  // start serial
  delay(1000); // THIS DELAY INSERTED FOR SUCCESSFUL BOOTS ON USB POWER ALONE DO NOT REMOVE (relates to Teensy and Serial monitor load times)
  Serial.begin(115200);
  delay(1000);

  // Initialize OLED

  display.begin(SSD1306_SWITCHCAPVCC, 0X3C);  // initialize with the I2C addr 0X3D (for the 128x64)
  display.setRotation(4); //long side is horizontal with pins on right side of board
  display.clearDisplay();
  display.display(); //turns on display and clears

  display.setTextSize(2);
  display.setCursor(0, 0);
  display.setTextColor(WHITE);
  display.println("Starting");
  display.print("Sensor");
  display.display(); //displays starting sensor text at beginning


  // Initialize mag sensor

  pinMode(device_pwr_pin, OUTPUT);
  pinMode(device_data_pin, OUTPUT);
  pinMode(device_ros_pin, OUTPUT);

  // Initialize mag sensor
  pinMode(i2c_sda, OUTPUT);
  digitalWrite(i2c_sda, LOW); //0x1F
  delay(500);
  Wire.begin();
  //Serial.print("Initializing sensor 1: 0x");
  //Serial.println(magSensor.init(HIGH), HEX);
  magSensor.init(HIGH);

  // setup static text (so we don't waste time refreshing it over and over)

  display.clearDisplay();
  display.display(); //update the display to clear

  //text properties
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.setTextColor(WHITE);

  // Display Bx field text, equals sign, and units (first row)
  display.print("Bx");
  display.setCursor(16, 0);
  display.print("=");
  display.setCursor(pixPosUnitX, 0);
  display.print("mT");

  // Display By field text, equals sign, and units (second row)
  display.setCursor(0, pixVert);
  display.print("By");
  display.setCursor(16, pixVert);
  display.print("=");
  display.setCursor(pixPosUnitX, pixVert);
  display.println("mT");

  // Display Bz field text, equals sign, and units (third row)
  display.setCursor(0, pixVert * 2);
  display.print("Bz");
  display.setCursor(16, pixVert * 2);
  display.print("=");
  display.setCursor(pixPosUnitX, pixVert * 2);
  display.println("mT");

  //Display total field magnitude, equals sign, and units (fourth row)
  display.drawFastVLine(0, pixVert * 3, 8, WHITE);
  display.drawFastVLine(2, pixVert * 3, 8, WHITE);
  display.setCursor(4, pixVert * 3);
  display.print("B");
  display.drawFastVLine(10, pixVert * 3, 8, WHITE);
  display.drawFastVLine(12, pixVert * 3, 8, WHITE);
  display.setCursor(16, pixVert * 3);
  display.print("=");
  display.setCursor(pixPosUnitX, pixVert * 3);
  display.println("mT");
  display.display();

  char valString[] = "-123.45";
  display.getTextBounds(valString, pixOffsetX, 0, &X1, &Y1, &w, &h);
  display.getTextBounds(valString, pixOffsetX, pixVert, &X2, &Y2, &w, &h);
  display.getTextBounds(valString, pixOffsetX, pixVert * 2, &X3, &Y3, &w, &h);
  display.getTextBounds(valString, pixOffsetX, pixVert * 3, &X4, &Y4, &w, &h);

  //Initialize ROS Node
  //nh.initNode();
  //nh.advertise(pub_field);

  digitalWriteFast(device_pwr_pin, HIGH);
  digitalWriteFast(device_data_pin, LOW);
  digitalWriteFast(device_ros_pin, LOW);

}

//-----------------------------------------------------------------------------------//
//-----------------------------------------------------------------------------------//


void loop() {

  //digitalWriteFast(device_ros_pin, nh.connected());

  // update magnetic field sensor
  
  if (!magSensor.update()) {
    
    digitalWriteFast(device_data_pin, HIGH);

    double Bmag = sqrt(magSensor.m_dMag_2);

    //if (!nh.connected()) {
      display.fillRect(X1, Y1, w, h, BLACK); // clear text area for bx
      display.fillRect(X2, Y2, w, h, BLACK); // clear text area for by
      display.fillRect(X3, Y3, w, h, BLACK); // clear text area for bz
      display.fillRect(X4, Y4, w, h, BLACK); // clear text area for bmag
      display.fillRect(barX, barY, barW, barH, BLACK); // clear bx bar
      display.fillRect(barX, barY + pixVert, barW, barH, BLACK); // clear by bar
      display.fillRect(barX, barY + pixVert * 2, barW, barH, BLACK); // clear bz bar
      display.fillRect(barX, barY + pixVert * 3, barW, barH, BLACK); // clear bmag bar

      // display new values

      display.setTextColor(WHITE);

      //Draw objects in space with bars
      display.drawFastVLine(barX + 24, 0, 8, WHITE); //vertical line representing zero field
      display.drawFastVLine(barX + 24, pixVert, 8, WHITE); //vertical line representing zero field
      display.drawFastVLine(barX + 24, pixVert * 2, 8, WHITE); //vertical line representing zero field

      //Draw plus and minus sign in bar space area
      display.setCursor(barX + 5, pixVert); //place symbol in middle left section
      display.print("-"); //negative area marker for field bars
      display.setCursor(barX + 38, pixVert); //place symbol in middle right
      display.print("+"); //plus sign for positive field bars
      //NOTE: Middle field bar will overwrite the area in middle used by symbols

      barFillX = int(abs(barW * magSensor.m_dBx / maxB)); //calc pixel fill width of bx bar
      if (magSensor.m_dBx < 0) { //if there is a negative field, constrain limits and fill backwards
        display.setCursor(pixOffsetX, 0);
        if ( barFillX >= 24) { //limit max length to 24 pixels to prevent drawing on other stuff
          barFillX = 24;
        }
        else {
        }
        display.fillRect(barX + 24 - barFillX, barY,  barFillX, barH, WHITE); //fill backwards
      }
      else {
        display.setCursor(pixOffsetX + 6, 0); //offset number display to account for the negative sign
        display.fillRect(barX + 24, barY, barFillX, barH, WHITE); //fill bar forwards from zero line
      }

      display.print(magSensor.m_dBx, 2);

      barFillY = int(abs(barW * magSensor.m_dBy / maxB));
      if (magSensor.m_dBy < 0) {
        display.setCursor(pixOffsetX, pixVert);
        if (barFillY >= 24) {
          barFillY = 24; //Limit to 24 pixels. See barFillX for additional comments
        }
        else {
        }
        display.fillRect(barX + 24 - barFillY, barY + pixVert, barFillY, barH, WHITE); //draw backwards
      }
      else {
        display.setCursor(pixOffsetX + 6, pixVert); //offset for negative symbol
        display.fillRect(barX + 24, barY + pixVert, barFillY, barH, WHITE); //fill forwards
      }

      display.print(magSensor.m_dBy, 2);

      barFillZ = int(abs(barW * magSensor.m_dBz / maxB));
      //See barFillX code for more comments on this section
      if (magSensor.m_dBz < 0) {
        display.setCursor(pixOffsetX, pixVert * 2);
        if (barFillZ >= 24) {
          barFillZ = 24;
        }
        else {
        }
        display.fillRect(barX + 24 - barFillZ, barY + pixVert * 2, barFillZ, barH, WHITE);
      }
      else {
        display.setCursor(pixOffsetX + 6, pixVert * 2);
        display.fillRect(barX + 24, barY + pixVert * 2, barFillZ, barH, WHITE);
      }

      display.print(magSensor.m_dBz, 2);

      //Draw field magnitude bar (fourth row)
      display.setCursor(pixOffsetX + 6, pixVert * 3);
      display.print(Bmag, 2);
      display.fillRect(barX, barY + pixVert * 3, int(abs(barW * Bmag / maxB)), barH, WHITE);

      //Update display for all the changes created in the loop
      display.display();
    //}

    // store new field reading
    mag_field_history[0][history_index] = magSensor.m_dBx;
    mag_field_history[1][history_index] = magSensor.m_dBy;
    mag_field_history[2][history_index] = magSensor.m_dBz;

    // increment index
    history_index++;
    if (history_index >= history_size) {
      history_index = 0;
    }

    double mag_field_avg[3] = {0.0, 0.0, 0.0};

    // average readings
    for (int ii = 0; ii < history_size; ++ii) {
      for (int jj = 0; jj < 3; ++jj) {
        mag_field_avg[jj] += mag_field_history[jj][ii];
      }
    }

    //Publish Data to Serial Port
//    Serial.print(xMag++);
//    Serial.print(",");
//    Serial.print(yMag++);
//    Serial.print(",");
//    Serial.println(zMag++);
//    Serial.flush();
    
    Serial.print(mag_field_avg[0] / static_cast<double>(history_size));
    Serial.print(",");
    Serial.print(mag_field_avg[1] / static_cast<double>(history_size));
    Serial.print(",");
    Serial.println(mag_field_avg[2] / static_cast<double>(history_size));
    Serial.flush();
  }

  //nh.spinOnce();
}
