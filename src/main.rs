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

    let pwm_timer = Timer0Pwm::new(dp.TC0, Prescale64);

    let mut noise = pins.d6.into_output().into_pwm(&pwm_timer);
    noise.set_duty(127);
    noise.enable();

    let mut serial = arduino_hal::default_serial!(dp, pins, 57600);

    let timer = dp.TC1;
    timer.tccr1b.write(|w| w.cs1().prescale_64());

    loop {
        let mut t1: u16 = 0;
        let mut t2: u16 = 0;
        let mut t3: u16 = 0;

        while s1.is_high() { //&& s2.is_high() && s3.is_high() {

        }

        timer.tcnt1.write(|w| w.bits(0));

        let mut t: u16;

        while ({t = timer.tcnt1.read().bits(); t} < 25000) && (t1 == 0 || t2 == 0 || t3 == 0) {
            // ufmt::uwriteln!(&mut serial, "t {}, {}, {} {} {}", t, s1.is_low(), t1, t2, t3);
            if (t1 == 0) && s1.is_low() {
                t1 = t;
            }
            if (t2 == 0) && s3.is_low() {
                t2 = t;
            }
            if (t3 == 0) && s3.is_low() {
                t3 = t;
            }
        }

        if t >= 25000 {
            ufmt::uwriteln!(&mut serial, "misfire {}, {}, {}, {}", t1, t2, t3, t);
        }
        else {
            ufmt::uwriteln!(&mut serial, "{},{},{}", t1, t2, t3);
        }

        arduino_hal::delay_ms(500);
    }
}
