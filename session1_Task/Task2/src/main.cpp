#include <Arduino.h>
#include <avr/io.h>
#include <util/delay.h>

void setup(){    
    DDRB |= (1 << PB3);

    TCCR0 = (1 << WGM01) |(1 << WGM00) |(1 << COM01) |  (1 << CS01);

    //25% start 
    OCR0 = 64;
}

void loop(){

    for (uint16_t duty = 64; duty <= 255; duty++){
        OCR0 = (uint8_t)duty;
        _delay_ms(10);}
    

    
    for (int16_t duty = 255; duty >= 64; duty--){
        OCR0 = (uint8_t)duty;
        _delay_ms(10);}
  

    // 25% end
    OCR0 = 64;




}