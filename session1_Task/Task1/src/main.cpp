#include <Arduino.h>
#include <avr/io.h>

// Counter for the 1 ms Timer0 events
uint16_t count = 0;

void setup()
{
    DDRB |= (1 << PB0);

    PORTB &= ~(1 << PB0);

    TIMSK &= ~((1 << OCIE0) | (1 << TOIE0));

    TCNT0 = 0;

    OCR0 = 124;

  
    TCCR0 = (1 << WGM01) | (1 << CS01) | (1 << CS00);

    TIFR = (1 << OCF0);}


void loop(){
    if (TIFR & (1 << OCF0)){
    
        TIFR = (1 << OCF0);
        count++;
        if (count >= 500){
            count = 0;
            PORTB ^= (1 << PB0);
        }
    }
}