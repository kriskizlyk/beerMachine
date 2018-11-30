#include <HX711_ADC.h> 
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <EEPROM.h>
#include <EEPROMAnything.h>
#include <Bounce2.h>

HX711_ADC LoadCell(4, 5); // parameters: dt pin, sck pin
//LiquidCrystal_I2C lcd(0x27, 16, 2); // 0x27 is the i2c address of the LCM1602 IIC v1 module (might differ)
Bounce debouncer = Bounce(); 

#define SLAVE_ADDRESS 0x08
long i2c_buffer_send = 0;
int i2c_buffer_pointer = 0;
int i2c_buffer_process[10];
int i2c_buffer_command[10];
long i2c_buffer_read[10];

// EEPROM data to hold.
long eeprom_zero = 0;
long eeprom_span = 0;
int eeprom_cal_weight = 0;
int eeprom_dec_point = 0;

const int buttonClk = 3;
const int buttonDt = 2;
const int buttonSw = 11;
const int r = 7;
const int g = 9;
const int b = 8;

bool cal_in_progress = false;
int cal_state = 0;

int timer1_counter = 0;

int dt_prev = 0;
int clk_prev = 0;
int encoder_enable = 0;
int encoder_state = 0;
int encoder_prev_state = 0;

unsigned long filter_time = 0;
unsigned long lcd_time = 0;
int filter_update = 40;
int lcd_update = 100;

float scale_weight = 0;
long scaleFactor = 1;
float scale_weight_prev = 0;
float scale_weight_filtered = 0;
long scale_weight_filtered_for_i2c = 0;
int scaleFactorOld = 1;
int aLastState = 0;
int aState = 0;

bool flag = false;
bool on = LOW;
bool off = HIGH;

void setup() {
  noInterrupts();
  // Clear registers
  TCCR1A = 0;
  TCCR1B = 0;
  TCNT1 = 0;

  // 250 Hz (8000000/((124+1)*256))
  OCR1A = 124;
  // CTC
  TCCR1B |= (1 << WGM12);
  // Prescaler 256
  TCCR1B |= (1 << CS12);
  // Output Compare Match A Interrupt Enable
  TIMSK1 |= (1 << OCIE1A);
  interrupts();
    
  Serial.begin(9600);  
  pinMode(buttonDt, INPUT_PULLUP);
  pinMode(buttonClk, INPUT_PULLUP);
  pinMode(buttonSw, INPUT);
  pinMode(r, OUTPUT);
  pinMode(g, OUTPUT);
  pinMode(b, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);

  debouncer.attach(buttonDt);
  debouncer.interval(4);

  debouncer.attach(buttonClk);
  debouncer.interval(4);

  debouncer.attach(buttonSw);
  debouncer.interval(4);

//  lcd.init();  
//  lcd.backlight(); // turns on the backlight
  
  LoadCell.begin(); // start connection to HX711
  LoadCell.setCalFactor(1);

  // Ask the user to calibrate or not.
//  lcd.setCursor(0, 0);
  Serial.println("Calibrate");
//  lcd.setCursor(0, 1);
  Serial.println("Press to Start");
  bool activate = false;

  // Load data from the EEPROM
  EEPROM_readAnything(0, eeprom_zero);
  EEPROM_readAnything(4, eeprom_span);
  EEPROM_readAnything(8, eeprom_cal_weight);
  if (eeprom_cal_weight == 0){
    eeprom_cal_weight = 20000;
  }
  EEPROM_readAnything(10, eeprom_dec_point);      

  Serial.print("Zero: ");
  Serial.print(eeprom_zero);    
  Serial.print("  Span:  ");
  Serial.print(eeprom_span);    
  Serial.print("  WeightSize:  ");   
  Serial.print(eeprom_cal_weight);    
  Serial.print("  Decimal:  ");   
  Serial.println(eeprom_dec_point);             
  
  Serial.println("Calibrate?");             

  for(int x = 0; x < 500; x++) {
    if (digitalRead(buttonSw) == LOW) {
      activate = true;
//      lcd.setCursor(14, 0);      
      Serial.println(":)");
    } else {
//      lcd.setCursor(15, 1);      
      Serial.println(500-x);
    }
  }

  if (activate == true){
    calibration_procedure(); 
  }

 // Print the main screen
//  lcd.clear();
//  lcd.setCursor(0, 0); // set cursor to first row
//  lcd.print("Filtered: "); // print out to LCD
//  lcd.setCursor(0, 1);
//  lcd.print("Raw: ");

// Clear the I2C buffer  
  for(int x = 0; x <= 9 ; x++) {
  i2c_buffer_process[x] = 0;
  i2c_buffer_command[x] = 0;
  i2c_buffer_read[x] = 0;
  }
    Wire.begin(SLAVE_ADDRESS);
    Wire.setClock(25000);
    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);
}

ISR(TIMER1_COMPA_vect) {
  encoder();
}

void loop() {
  if (millis() > filter_time + filter_update){
    filter_time = millis();    
    LoadCell.update();
    scale_weight = get_live_weight() / pow(10, eeprom_dec_point);
    if (scale_weight < 0.0) {scale_weight = 0.0;}
    scale_weight_filtered = spf(scale_weight, scale_weight_prev);
    scale_weight_filtered_for_i2c = scale_weight_filtered * pow(10, eeprom_dec_point);
    scale_weight_prev = scale_weight_filtered;
    }
    
  if (millis() > lcd_time + lcd_update){
    lcd_time = millis();
      Serial.println("Weight: ");
      Serial.println(scale_weight_filtered_for_i2c);
//      sendData();

//    lcd_time = millis();
//    lcd.setCursor(10, 0);
//    lcd.print(scale_weight_filtered, eeprom_dec_point);
//    lcd.print("  ");      
//    lcd.setCursor(10, 1);
//    lcd.print(scale_weight, eeprom_dec_point);    
//    lcd.print("  ");  

//    if (scaleFactor != scaleFactorOld){
//      scaleFactorOld = Old;
//      LoadCell.setCalFactor();}
  
//    if (flag == false) {
//      digitalWrite(LED_BUILTIN, LOW);
//      flag = true;
//    } else {
//      digitalWrite(LED_BUILTIN, HIGH);   
//      flag = false;
//    }
  }
}

void receiveData(int byteCount){
  int offset = 3;
  int pointer = 0;
  int timeout = 10;
  int command = 0;
  long data = 0;

  while(Wire.available()){
    if (Wire.read() == 10){
     if (flag == false) {
        digitalWrite(LED_BUILTIN, LOW);
        flag = true;
      } else {
        digitalWrite(LED_BUILTIN, HIGH);   
        flag = false;
      }
      i2c_buffer_send = scale_weight_filtered_for_i2c;
    }
  }

//  while(Wire.available()) {
//    int byte_data = Wire.read();
//   
//    if (pointer == 0){
//      command = byte_data;
//    }
//    
//    else if (pointer > 0 && pointer <= 4) {
//      data = data | (long(byte_data) << (offset * 8));
//      offset--;      
//    }
//
////   values[pointer] = byte_data;
//   pointer++;   
//   
//   if(pointer >= timeout){
//    break;
//   }
//  }
//
//  i2c_buffer_process[i2c_buffer_pointer] = 1;
//  i2c_buffer_command[i2c_buffer_pointer] = command;
//  i2c_buffer_read[i2c_buffer_pointer] = data;  
//  i2c_buffer_pointer++;
}

void sendData(){
  long n = i2c_buffer_send;
  if (i2c_buffer_send < 0){
    i2c_buffer_send = 0.001;  
  }

  if (i2c_buffer_send > 100000){
    i2c_buffer_send = 50000.0;  
  }
  
  byte buf[5];
  buf[0] = (byte)((n >> 24) & 0x000000ff);
  buf[1] = (byte)((n >> 16) & 0x000000ff);
  buf[2] = (byte)((n >> 8) & 0x000000ff);
  buf[3] = (byte)(n & 0x000000ff);
  buf[4] = byte(0); // For some reason if I don't clear this it will mess up smbus2
  Wire.write(buf, 5);
}

float get_live_weight(){
  float live_weight_bottom = float(eeprom_span - eeprom_zero) / float(eeprom_cal_weight);
  float live_weight_top = LoadCell.getData() - float(eeprom_zero);
  float live_weight = live_weight_top / live_weight_bottom;
  return live_weight;
}


void calibration_procedure(){
  digitalWrite(b, off);  
  cal_in_progress = true;
  cal_state = 1;
  bool cal_break = false;
//  lcd.clear();
  int db_count = 0;

  while(cal_in_progress){
    if (cal_state == 1){
      lcd_print("Press to Zero", "");
      if (digitalRead(buttonSw) == LOW){
        db_count += 1;
        if (db_count >= 100){
          eeprom_zero = (long)LoadCell.getData();
          cal_break = true;}
      }
    }

    else if (cal_state == 2){
      lcd_print("Press to Span", "");
      if (digitalRead(buttonSw) == LOW){
        db_count += 1;
        if (db_count >= 100){        
          eeprom_span = long(LoadCell.getData());
          cal_break = true;}
      }
    }  

    else if (cal_state == 3){
      lcd_print("Set Max Weight", "");
      if (digitalRead(buttonSw) == LOW){
        db_count += 1;
        if (db_count >= 100){        
          cal_break = true;}
      }
    }

    else if (cal_state == 4){
      lcd_print("Set Decimal", "");
      if (digitalRead(buttonSw) == LOW){
        db_count += 1;
        if (db_count >= 100){        
          cal_break = true;}
      }
    }    

    else{
      cal_break = true;
      cal_in_progress = false;
      EEPROM_writeAnything(0, eeprom_zero);
      EEPROM_writeAnything(4, eeprom_span);
      EEPROM_writeAnything(8, eeprom_cal_weight);
      EEPROM_writeAnything(10, eeprom_dec_point);        
    }
    
    if (cal_break == true){
      db_count = 0;
      cal_break = false;
      cal_state++;
//      lcd.setCursor(14, 0);
      Serial.println(":)");   
      delay(1000);
//      lcd.clear();      
    }
    

  }
}

void lcd_print(String line1, String line2){
  if (millis() > lcd_time + lcd_update){
    LoadCell.update();
    lcd_time = millis();
//    lcd.setCursor(0, 0);
    Serial.println(line1);
//    lcd.setCursor(0, 1);

    if (cal_state == 0){
      Serial.println(line2);
    }
    
    if (cal_state == 1 || cal_state == 2) {
      Serial.println(long(LoadCell.getData()));
    }
    
    else if (cal_state == 3) {
      Serial.println(eeprom_cal_weight);
    }
    
    else if (cal_state ==4) {
      Serial.println(eeprom_dec_point);
    }
    
  } 
}

void encoder()
{
  int pulse_count = 0;
  int dt = digitalRead(buttonDt);
  int clk = digitalRead(buttonClk);

  if (dt == LOW and clk == LOW){
    encoder_enable = true;
  }

  else if (dt == LOW && clk == HIGH && encoder_enable == true){
      pulse_count++;
      digitalWrite(r, LOW);
      digitalWrite(g, HIGH);
      encoder_enable = false;
  }

  else if (dt == HIGH && clk == LOW && encoder_enable == true){
      pulse_count--;
      digitalWrite(r, HIGH);
      digitalWrite(g, LOW);
      encoder_enable = false;
  }

  if (cal_state == 3){
    eeprom_cal_weight += pulse_count;

    if (eeprom_cal_weight <= 0){
      eeprom_cal_weight = 0; }

    if (eeprom_cal_weight >= 50000){
      eeprom_cal_weight = 50000;
    }
  }

  else if (cal_state == 4){
    eeprom_dec_point += pulse_count;      

    if (eeprom_dec_point <= 0){
      eeprom_dec_point = 0; }

    if (eeprom_dec_point >= 3){
      eeprom_dec_point = 3; }      
    }
}

float spf(float NewInput, float OldOutput)
{
  float k = 1;
  float error = (NewInput - OldOutput);
  if (error < 0) {error = error * -1;}
  if (error > 0.5) {k = 1.0;}
  if (error > 0.4) {k = 0.5;}
  if (error > 0.3) {k = 0.4;}
  if (error > 0.2) {k = 0.3;}
  if (error > 0.1) {k = 0.2;}
  if (error > 0.05) {k = 0.1;}
  if (error < 0.05) {k = 0.01;} 

  float filtered = (OldOutput-(k*OldOutput)) + (k*NewInput);
  return filtered;
}
