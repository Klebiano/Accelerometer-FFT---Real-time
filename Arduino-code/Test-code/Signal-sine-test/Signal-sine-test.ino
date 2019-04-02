#include <math.h>

void setup() {

  Serial.begin(115200);

}

// you use a newline as the delimiter; no need to use a comma too
void loop() {
  for(int d = 0; d < 360; d++){
    float resultado = 2.0*sin(DEG_TO_RAD * d*2*PI) + 3.0*sin(DEG_TO_RAD * d*2*PI*100.0);
    Serial.println(resultado, 6);
    //Serial.println(DEG_TO_RAD * d);
    delayMicroseconds(500);                       // Sampling rate is 1/T -> 2000Hz
  }
}
