#![no_std]
#![no_main]

use arduino_hal::simple_pwm::{IntoPwmPin, Timer0Pwm};
use arduino_hal::simple_pwm::Prescaler::Prescale64;
use panic_halt as _;

#[arduino_hal::entry]
fn main() -> ! {
    let dp = arduino_hal::Peripherals::take().unwrap();
    let pins = arduino_hal::pins!(dp);

    let s1 = pins.d11;
    let s2 = pins.d12;
    let s3 = pins.d13;

    let mut adc = arduino_hal::Adc::new(dp.ADC, Default::default());

    let a0 = pins.a0.into_analog_input(&mut adc);
    let a1 = pins.a1.into_analog_input(&mut adc);
    let a2 = pins.a2.into_analog_input(&mut adc);

    let pwm_timer = Timer0Pwm::new(dp.TC0, Prescale64);

    let mut serial = arduino_hal::default_serial!(dp, pins, 57600);

    let timer = dp.TC1;
    timer.tccr1b.write(|w| w.cs1().prescale_8());

    loop {
        let mut t1: u16 = 0;
        let mut t2: u16 = 0;
        let mut t3: u16 = 0;

        while s1.is_low() && s2.is_low() && s3.is_low() {
            //ufmt::uwriteln!(&mut serial, "{}", a0.analog_read(&mut adc));
        }



        timer.tcnt1.write(|w| w.bits(0));

        let mut t: u16 = 0;

        while (t < 25000) && (t1 == 0 || t2 == 0 || t3 == 0) {
            t = timer.tcnt1.read().bits();
            //ufmt::uwriteln!(&mut serial, "t {}, {}, {}, {}", t, t1, t2, t3);
            if (t1 == 0) && s1.is_high() {
                t1 = t.clone();
            }
            if (t2 == 0) && s2.is_high() {
                t2 = t.clone();
            }
            if (t3 == 0) && s3.is_high() {
                t3 = t.clone();
            }
        }

        if t >= 25000 {
            ufmt::uwriteln!(&mut serial, "misfire {}, {}, {}, {}", t1, t2, t3, t);
        }
        else {
            ufmt::uwriteln!(&mut serial, "{},{},{}", t1, t2, t3);
        }

        while s1.is_high() || s2.is_high() || s3.is_high() {
            ufmt::uwriteln!(&mut serial, "still high: {} {} {}", s1.is_high(), s2.is_high(), s3.is_high());
        }

        arduino_hal::delay_ms(500);
    }
}
