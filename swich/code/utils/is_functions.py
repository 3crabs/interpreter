def is_digit_16(s: str):
    return len(s) == 1 and s in '0123456789abcdefABCDEF'


def is_digit_16_not_zero(s: str):
    return len(s) == 1 and s in '0123456789abcdefABCDEF'


def is_digit(s: str):
    return len(s) == 1 and s in '0123456789'


def is_digit_not_zero(s: str):
    return len(s) == 1 and s in '123456789'


def is_not_digit(s: str):
    return len(s) == 1 and s in 'abcdefghijklmnopqrstuvwxyz_ABCDIFJHIJKLMNOPQRSTUVWXYZ'
