def get_angle_from_minor(minor: str) -> int:
    """
    As Marek told us, the minors contain the angles.

    Although, they contain angles in base-16 notation,
    that is supposed to be read as base-10

    Example:
    0x30 in hex is 48 in dec, but its meant to represent the angle od 30 in dec

    But the scanner reads the minor value in the decimal system, so it would read 
    a value '48' from the beacon. We need to convert it into a hex value,
    then interpret it as a dec value
    """
    return int(hex(int(minor))[2:])


if __name__ == '__main__':
    # The value for a given angle can be obtained using `int('360', 16)` where 360 is the angle
    # (remember about the quotation, it has to be string-type)
    print(get_angle_from_minor('48'))  # 30
    print(get_angle_from_minor('864'))  # 360
