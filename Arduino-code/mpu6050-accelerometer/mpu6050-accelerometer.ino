/*
===Contact & Support===
Website: http://eeenthusiast.com/
Youtube: https://www.youtube.com/EEEnthusiast
Facebook: https://www.facebook.com/EEEnthusiast/
Patreon: https://www.patreon.com/EE_Enthusiast
Revision: 1.0 (July 13th, 2016)
===Hardware===
- Arduino Uno R3
- MPU-6050 (Available from: http://eeenthusiast.com/product/6dof-mpu-6050-accelerometer-gyroscope-temperature/)
===Software===
- Latest Software: https://github.com/VRomanov89/EEEnthusiast/tree/master/MPU-6050%20Implementation/MPU6050_Implementation
- Arduino IDE v1.6.9
- Arduino Wire library
===Terms of use===
The software is provided by EEEnthusiast without warranty of any kind. In no event shall the authors or 
copyright holders be liable for any claim, damages or other liability, whether in an action of contract, 
tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in 
the software.
*/

/*
===Contact & Support===
Website: http://eeenthusiast.com/
Youtube: https://www.youtube.com/EEEnthusiast
Facebook: https://www.facebook.com/EEEnthusiast/
Patreon: https://www.patreon.com/EE_Enthusiast
Revision: 1.0 (July 13th, 2016)
===Hardware===
- Arduino Uno R3
- MPU-6050 (Available from: http://eeenthusiast.com/product/6dof-mpu-6050-accelerometer-gyroscope-temperature/)
===Software===
- Latest Software: https://github.com/VRomanov89/EEEnthusiast/tree/master/MPU-6050%20Implementation/MPU6050_Implementation
- Arduino IDE v1.6.9
- Arduino Wire library
===Terms of use===
The software is provided by EEEnthusiast without warranty of any kind. In no event shall the authors or 
copyright holders be liable for any claim, damages or other liability, whether in an action of contract, 
tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in 
the software.
*/

#include <Wire.h>


long accelX, accelY, accelZ;
float gForceX, gForceY, gForceZ;

long gyroX, gyroY, gyroZ;
float rotX, rotY, rotZ;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  setupMPU();
}


void loop() {
  recordAccelRegisters();
  recordGyroRegisters();
  printData();
}

void setupMPU(){
  Wire.beginTransmission(0b1101000); //This is the I2C address of the MPU (b1101000/b1101001 for AC0 low/high datasheet sec. 9.2)
  Wire.write(0x6B); //Accessing the register 6B - Power Management (Sec. 4.28)
  Wire.write(0b00000000); //Setting SLEEP register to 0. (Required; see Note on p. 9)
  Wire.endTransmission();  
  Wire.beginTransmission(0b1101000); //I2C address of the MPU
  Wire.write(0x1B); //Accessing the register 1B - Gyroscope Configuration (Sec. 4.4) 
  Wire.write(0x00000000); //Setting the gyro to full scale +/- 250deg./s // Mudar para 0b00010000 para pegar +/- 1000 °/s
  Wire.endTransmission(); 
  Wire.beginTransmission(0b1101000); //I2C address of the MPU
  Wire.write(0x1C); //Accessing the register 1C - Acccelerometer Configuration (Sec. 4.5) 
  Wire.write(0b000000000); //Setting the accel to +/- 2g // chage to 0b00010000 to get range +/- 8g // change to 0b00011000 to gget range +/- 16g
  Wire.endTransmission(); 
}

void recordAccelRegisters() {
  Wire.beginTransmission(0b1101000); //I2C address of the MPU
  Wire.write(0x3B); //Starting register for Accel Readings
  Wire.endTransmission();
  Wire.requestFrom(0b1101000,6); //Request Accel Registers (3B - 40)
  while(Wire.available() < 6);
  accelX = Wire.read()<<8|Wire.read(); //Store first two bytes into accelX
  accelY = Wire.read()<<8|Wire.read(); //Store middle two bytes into accelY
  accelZ = Wire.read()<<8|Wire.read(); //Store last two bytes into accelZ
  processAccelData();
}

void processAccelData(){            //change to 16384 if in range of +/- 2g // change to 4096 if in range of +/- 8g // change to 2048 if in range of +/- 16g
  gForceX = (accelX / 4096.0);
  gForceY = (accelY / 4096.0); 
  gForceZ = (accelZ / 4096.0);
}

void recordGyroRegisters() {
  Wire.beginTransmission(0b1101000); //I2C address of the MPU
  Wire.write(0x43); //Starting register for Gyro Readings
  Wire.endTransmission();
  Wire.requestFrom(0b1101000,6); //Request Gyro Registers (43 - 48)
  while(Wire.available() < 6);
  gyroX = Wire.read()<<8|Wire.read(); //Store first two bytes into accelX
  gyroY = Wire.read()<<8|Wire.read(); //Store middle two bytes into accelY
  gyroZ = Wire.read()<<8|Wire.read(); //Store last two bytes into accelZ
  processGyroData();
}

void processGyroData() {      
  rotX = (gyroX / 131.0);     
  rotY = (gyroY / 131.0); 
  rotZ = (gyroZ / 131.0);
}

void printData() {

  /*Serial.print(gForceX);
  Serial.print(",");
  Serial.print("\t");
  Serial.print(gForceY);
  Serial.print(",");
  Serial.print("\t");*/
  //Serial.print(gForceZ);
  Serial.print(accelZ);           //accelZ
  Serial.println(",");
  /*Serial.print("\t");
  Serial.print(rotX);
  Serial.print(",");
  Serial.print("\t");
  Serial.print(rotY);
  Serial.print(",");
  Serial.print("\t");
  Serial.print(rotZ);
  Serial.print(",");
  Serial.println("\t");*/
  delayMicroseconds(500);         // T = 0.0005
//Serial.print("\t");
//Serial.println(Tmp/(340.00 + 36.53));
}


