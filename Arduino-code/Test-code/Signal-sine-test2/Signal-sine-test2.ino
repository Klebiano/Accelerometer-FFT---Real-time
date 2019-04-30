#include <math.h>

void setup() {

  Serial.begin(115200);

}

void loop() {
  for(float d = 0; d < 1; d+=0.001){
    float resultado = 7*sin(15 * 2 * PI * d) + 3*sin(13 * 2 * PI * d);
    Serial.println(resultado, 3);
    delayMicroseconds(500);                       // Sampling rate is 1/T -> 2000Hz
  }
}
