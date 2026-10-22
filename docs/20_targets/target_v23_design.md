# Target with nRF52 and MSP430

## Implemented Changes

- new Target-Port
- wider PCB allowed, BB-Heigth is 54.1 mm ⇾ half is max 27 mm
- TargetPCB: are there constraints or feedback for the MSP430 + NRF - Combination
  - Which IC would you prefer?
  - example-schematic for the combination available?
  - IC interconnect: SPI (4 Lines), 2+ handshake-lines (Project Squeece)
  - Target-Connector-Gpio access for both uCs?
  - TODO: use nRF TRCDAT0 / P1.00 / on Target header
  - Github / squeece
- target ⇾ add target powered LED to burn away energy (or use second LED for that purpose)
- nice to keep similarity to DK, but not a must
- Squeece Pin-usage
  - C2C CLK,  P0.13,  P1-6_UCA0CLK
  - C2C MOSI, P0.12,  P1-4_UCA0TXD
  - C2C MISO, P0.16,  P1-5_UCA0RXD
  - C2C CS,   P0.15,  P1-7_UCA0STE
  - C2C GPIO, P0.14,  P2-7_CAP3
  - nrf-gp0   p0.17
  - nrf-gp1   p0.19
  - nrf-gp2   p0.28
  - nrf-led   p0.29
  - msp-gp0           P2-1_XIN
  - msp-gp1           P1-1_UCB0CLK
- MSP430 Variants
  - MSP430FR2433IYQWR ⇾ BGA-Version, 16 kB FRAM
  - **MSP430FR5964** with 87 Pins, 256 kB FRAM ⇾ there is an 48 PinVersion FR5994, even 59941 is ok
  - MSP430FR5992IRGZR, 48 Pins, 128 kB FRAM
  - or MSP430FR2155 with 32 kB and 48Pins and 32 MHz ⇾ PinCompatible?
  - SPI to Target, seconds SPI to nRF
  - prepare to equip both crystals (HF, LF)
  - eine der eUSCI Schnittstellen (sind beim MSP hart verdrahtet) soll richtung BB gehen. Und der eine pin davon (z.B. UCA0RXD/UCA0SOMI) muss auf BB richtungsschaltbar sein.
- msp430
- shared pins are working fine on squeece, ~ 10nA draw on high impedance
- add star-resistors

## Open Issues

- programmer - compensate lines with passive network
