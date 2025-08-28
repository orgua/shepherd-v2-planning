# Hardware Casing for Nodes (2020)

**Deprecated / shelved!** Current lasercut case is in [main repo](https://github.com/nes-lab/shepherd/tree/dev/hardware/case_lasercut)

## Constraints

- nodes can vanish, wander
    - fixate
    - keep inconspicuous (under desk an option?), make it look official / blend in
- nodes can spook new people in the same office
    - must look professional, official
    - be transparent about the function (inform current people in office, but also use sticker to provide a FAQ-Website
- must support cooling (direct sunlight, proximity to radiator)
    - convectional cooling would be the easiest
- must contain
    - BBone with shepherd Cape (75 x 55 x 25 mm)
    - POE-Converter (81 x 55 x 25 mm)
    - Target nodes (20 x 30 x 4 mm) - orthogonal on capelet or in direction of longest edge of capelet)
    - < 20 cm Network cable
    - power-connection
    - USB-Stick (45 x 20 x 9 mm)
    - opening for one RJ-45-Socket
- must be transparent to RF
- input Marco:
    - open and transparent is fine and wanted (!)
    - boxy is ok
    - preferable hard mounted to the wall with just one cable attached

## Layout

- flat on one level
    - X: 75 + 45 + 30
    - Y: 55 + 55
    - Z: 25
    - 150 x 110 x 25 (412 cm²)
    - pro: clean,
    - contra: harder to cool, less optimal RF-performance (antenna near to ground)
- Stacked
    - X: 75 + 45
    - Y: 55
    - Z: 25 + 25 + 30
    - 120 x 55 x 80 (528 cm²)
    - pro: more boxy, would better fit on top of the cable canal
    - contra:

## Solutions

- 3d-Printing
    - flexible and custom case
    - way to expensive for 30 Nodes
- Casing in laser-acrylic or plywood
    - solid, custom
    - may look also unprofessional, like a building kit
    - design without screws ⇾ <https://hackaday.com/2013/02/27/acrylic-enclosures-use-integrated-clips-to-do-away-with-fasteners/>
- off-the-shelf case with custom front
    - can look professional
    - you have to take what the market offers
    - way around custom front is: just include an opening for the cable with a gasket (or right there where two halves meet)


## Off-the-shelf Cases

- flat (25-35 height, 150-183 length, 110-135 width)
    - https://www.mouser.de/Enclosures/_/N-5g3o?P=1yzti4fZ1yzxi2vZ1yzu1qgZ1yzxiszZ1yzu1na&Rl=5g3oZer8qZ1z0wu34Z1yzsnvlSGT5g3oZer7lZ1yzxi96Z1yzxi5vSGT
    - hammond 1599TABMBK / GY, 28 x 135 x 169 mm with custom cover, hardware can be mounted inside with laser-cut brackets
        - https://www.hammfg.com/electronics/small-case/plastic/1599tab
    - hammond 1557FGY, 160x160x45, no option for cover
        - https://www.hammfg.com/electronics/small-case/plastic/1557
    - hammond RM2055S
        - https://www.hammfg.com/electronics/small-case/plastic/rm2
- stacked (120-140 length, 55-75 width, 80-125 height)
    - https://www.mouser.de/Enclosures/_/N-5g3o?P=1yzu1tfZ1yzu1f6Z1yzu1ggZ1yzsn9pZ1yzoes7Z1yzxin2&Rl=5g3oZergvZ1yzu1ffZ1yzxigsSGT5g3oZer8qZ1y8pz55Z1z0wu4tSGT
    - Bud PTS-25312-C, 5.12x2.76x3.15"
    - Hammond 1554G2Gy, https://www.hammfg.com/part/1554G2GY
    - hammond 1555, https://www.hammfg.com/part/1555G2GY
    - hammond RP1150C, https://www.hammfg.com/part/RP1150C
    - hammond rp1155, https://www.hammfg.com/part/RP1155

## Favorite 1599TABMGY

![image](https://www.hammfg.com/files/products/1599tab/1599tab.jpg)
