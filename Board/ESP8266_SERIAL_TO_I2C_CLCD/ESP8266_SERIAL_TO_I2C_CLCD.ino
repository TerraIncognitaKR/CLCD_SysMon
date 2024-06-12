/**
  ******************************************************************************
  * @file           : ESP8266_SERIAL_TO_I2C_CLCD.ino
  * @brief          : Convert I2C interfaced CLCD to UART interfaced CLCD
  ******************************************************************************
  * @attention
  *
  *  2024 TeIn
  *  https://blog.naver.com/bieemiho92
  *
  *  (Tested) Target Device :
  *     ESP8266 NodeMCU
  *
  *  IDE :
  *     Arduino IDE 2.3.2
  *
  *  Dependancy    :
  *    ESP8266 board support package
  *       http://arduino.esp8266.com/stable/package_esp8266com_index.json
  *    LiquidCrystal_I2C-1.1.2 ~
  *
  * @note
  *   Ver.01 (2024/06) :
  *     - Initial Release
  *
  ******************************************************************************
  */

/* Includes ------------------------------------------------------------------*/
#include <Arduino.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>    // I2C CLCD

/* Defines -------------------------------------------------------------------*/
/**
 * @brief Feature ON/OFF Control
 * @note
 */
/*** enable cursor ***/
// #define FEATURE_CURSOR_EN             1
/*** enable cursor blink ***/
// #define FEATURE_CURSOR_BLINK_EN       1
/*** enable backlight --- some CLCD is MUST need backlight for visibility */
#define FEATURE_BACKLIGHT_EN          1

/**
 * @brief I2C Character LCD
 * @note  tested on 20x4 CLCD
 *        modify THIS section & some codes to fit your device.
 */
#define CLCD_I2C_ADDR                 0x27
#define CLCD_COL_NUM                  20
#define CLCD_ROW_NUM                  4

/**
 * @brief for System
 */
#define FW_VER                        1
#define CHAR_LF                       10  // Line Feed       '\n'
#define CHAR_CR                       13  // Carriage Return '\r'

/* Macros --------------------------------------------------------------------*/

/* Types ---------------------------------------------------------------------*/

/* Variables -----------------------------------------------------------------*/
uint32_t  g_dwCount = 0;
uint8_t   bCurX = 0;
uint8_t   bCurY = 0;
uint8_t   bCurrReadChar;

/* Function prototypes -------------------------------------------------------*/
void    handle_crlf(void);

/* Constructor ---------------------------------------------------------------*/
/**
 * @brief
 * Character LCD
 */
LiquidCrystal_I2C lcd(CLCD_I2C_ADDR, CLCD_ROW_NUM, CLCD_COL_NUM);


/* User code -----------------------------------------------------------------*/

/**
  * @brief      Handle line ending
  * @param      none
  * @return     none
  * @note       by default, only LF works
  */
void    handle_crlf(void)
{
  bCurY++;
  if(bCurY >= CLCD_ROW_NUM)
  {
    bCurY = 0;
    // lcd.clear(); // comment this line to prevent blanking
  }
  bCurX = 0;

  if(bCurY)         // increase line (1st->2nd->3rd->4th)
    lcd.setCursor(bCurX, bCurY);
  else              // reset    line (4th->1st)
    lcd.home();
}


/**
  * @brief      arduino setup()
  * @param      none
  * @return     none
  * @note       put your setup code here, to run once
  */
void setup() {

  // Initialize UART & LCD
  Serial.begin(115200);

  // Initialize I2C CLCD
  lcd.init();
  lcd.blink();  // blinks cursor during startup
#ifdef FEATURE_BACKLIGHT_EN
  lcd.backlight();
#endif /** FEATURE_BACKLIGHT_EN **/

  // Splash
  Serial.printf("\r\n\r\n");
  Serial.printf("********************************************************************************\r\n");
  Serial.printf("\t[ESP8266_SERIAL_TO_I2C_CLCD]\r\n");
  Serial.printf("\tFW Ver 0x%02X (Build @ %s %s)\r\n", FW_VER, __TIME__, __DATE__);
  Serial.printf("\tEnter = LF\r\n");

  lcd.home();
  lcd.print("Starting...");
  lcd.setCursor(0,1);
  lcd.print("FW Ver : ");
  lcd.print(FW_VER);
  lcd.setCursor(0,2);
  delay(5000);
  Serial.println(">> OK");

#ifdef FEATURE_CURSOR_EN
  lcd.cursor();
#endif /** FEATURE_CURSOR_EN **/

#ifndef FEATURE_CURSOR_BLINK_EN
    lcd.noBlink();
#endif /** FEATURE_CURSOR_BLINK_EN **/

  lcd.clear();
  lcd.home();
}


/**
  * @brief      arduino loop()
  * @param      none
  * @return     none
  * @note       put your main code here, to run repeatedly:
  */
void loop() {

  if(Serial.available())
  {
    // get current character
    bCurrReadChar = Serial.read();

    if(CHAR_LF == bCurrReadChar)
    {
      // accept NL
      handle_crlf();
    }
    else if (CHAR_CR == bCurrReadChar)
    {
      // ignore CR

    }
    else
    {
      // print characters to LCD
      lcd.write(bCurrReadChar);

      // update current position & handle line control
      bCurX++;
      if(bCurX >= CLCD_COL_NUM)
      {
        handle_crlf();
      }
    }

  }
}
