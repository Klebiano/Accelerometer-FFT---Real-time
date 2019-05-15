#include <math.h>

void setup() {

  Serial.begin(2000000);

}

void loop() {
  for(float d = 0; d <= 1; d+=0.0005){                              // d+=1/2000
    float resultado = 2.0*sin(d*2*PI) + 3.0*sin(d*2*PI*100.0);     
    Serial.println(resultado,2);
    //Serial.println(DEG_TO_RAD * d);
    delayMicroseconds(500);                                         // Sampling rate is 1/T -> 2000Hz
  }
}
