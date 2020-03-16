import math

__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'

# TODO: Hold library for making flag bus into one wire protocol


def bit_set(
    byte: int,
    bit_pos: int
):
    """
    Sets bit b of byte with value a

    :param byte: int
    :param bit_pos: int

    :return new_val: int
    """
    mask = (1 << bit_pos)
    new_val = byte | mask
    return new_val


def bit_clear(
    byte: int,
    bit_pos: int
):
    """
    Clears bit b of byte with value a

    :param byte: int
    :param bit_pos: int

    :return new_val: int
    """
    mask = ~(1 << bit_pos)
    new_val = byte & mask
    return new_val


def bit_flip(
    byte: int,
    bit_pos: int
):
    """
    Flips bit b of byte with value a

    :param byte: int
    :param bit_pos: int

    :return new_val: int
    """
    mask = (1 << bit_pos)
    new_val = byte ^ mask
    return new_val


def bit_check(
    byte: int,
    bit_pos: int
):
    """
    Checks bit b of byte with value a

    :param byte: int
    :param bit_pos: int

    :return new_val: int
    """
    mask = (1 << bit_pos)
    new_val = byte & mask
    return new_val


def bitmask_set(
    byte: int,
    bit_pos: int
):
    """
    Sets bits y in byte with value x

    :param byte: int
    :param bit_pos: int

    :return new_val: int
    """
    new_val = byte | bit_pos
    return new_val


def bitmask_clear(
    byte: int,
    bit_pos: int
):
    """
    Clears bits y in byte with value x

    :param byte: int
    :param bit_pos: int

    :return new_val: int
    """
    new_val = byte & (~bit_pos)
    return new_val


def bitmask_flip(
    byte: int,
    bit_pos: int
):
    """
    Flips bits y in byte with value x

    :param byte: int
    :param bit_pos: int

    :return new_val: int
    """
    new_val = byte ^ bit_pos
    return new_val


def bitmask_check(
    byte: int,
    bit_pos: int
):
    """
    Checks bits y in byte with value x

    :param byte: int
    :param bit_pos: int

    :return new_val: int
    """
    new_val = byte & bit_pos
    return new_val


def twos_comp_neg(
    byte: int,
    bit_pos: int
):
    """
    Converts twos complement value to negative value

    :param byte: int
    :param bit_pos: int

    :return new_val: int
    """
    new_val = -1 * ((byte - 1) ^ bit_pos)
    return new_val


def frac_to_bin(byte: int):
    """
    Converts floating fraction to binary fraction

    :param byte: int

    :return new_val: int
    """
    new_val = 0
    bit_pos = 7
    while bit_pos > 0:
        prod = byte * 2
        bit = int(math.floor(prod))
        new_val |= bit << bit_pos
        if prod >= 1:
            byte = prod - 1
        else:
            byte = prod
        bit_pos -= 1
    return new_val


def number_segment(
    float_num: float,
    num_bytes: int
):
    """
    Segments float into whole/fraction of n bytes

    :param float_num: float
    :param num_bytes: int

    :return seg_num: list
    """

    def mask(nbr_bytes: int):
        """
        :param nbr_bytes: int

        :return mask_a: int
        :return mask_b: int
        """
        if nbr_bytes == 1:
            mask_a = 0xFF
            mask_b = 0xFF
        elif nbr_bytes == 2:
            mask_a = 0xFFFF
            mask_b = 0xFF00
        elif nbr_bytes == 3:
            mask_a = 0xFFFFFF
            mask_b = 0xFF0000
        elif nbr_bytes == 4:
            mask_a = 0xFFFFFFFF
            mask_b = 0xFF000000
        elif nbr_bytes == 5:
            mask_a = 0xFFFFFFFFFF
            mask_b = 0xFF00000000
        else:
            mask_a = None
            mask_b = None
        return int(mask_a), int(mask_b)

    mask1, mask2 = mask(num_bytes)

    if float_num < 0:
        whole = int(-1 * math.ceil(float_num))
        decimal = int(-1 * (float_num % -1))
        decimal = frac_to_bin(decimal)
        whole = bitmask_flip(whole, mask1)
        decimal = bitmask_flip(decimal, int(0xFF))
        decimal += 1
        if decimal > 255:
            whole += 1
            decimal = bit_clear(decimal, 8)
    else:
        whole = int(math.floor(float_num))
        decimal = int(float_num % 1)
        decimal = frac_to_bin(decimal)

    whole = whole << 8
    number = whole + decimal

    seg_num = []
    for i in range(0, num_bytes):
        seg_num.append(0)
        seg_num[i] = int((number & mask2) >> (8 * (num_bytes - 1)))
        number <<= 8

    return seg_num


def number_concatenate(
    seg_num: list,
    num_bytes: int
):
    """
    Converts segmented float number to single float

    :param seg_num: list
    :param num_bytes: int

    :return float_num: float
    """

    def mask(nbr_bytes: int):
        """
        :param nbr_bytes: int

        :return mask_a: int
        :return mask_b: int
        :return mask_b: int
        """
        if nbr_bytes == 1:
            mask_a = 0x80
            mask_b = 0xFF
            mask_c = 0x00
        elif nbr_bytes == 2:
            mask_a = 0x8000
            mask_b = 0xFFFF
            mask_c = 0x00FF
        elif nbr_bytes == 3:
            mask_a = 0x800000
            mask_b = 0xFFFFFF
            mask_c = 0x0000FF
        elif nbr_bytes == 4:
            mask_a = 0x80000000
            mask_b = 0xFFFFFFFF
            mask_c = 0x000000FF
        elif nbr_bytes == 5:
            mask_a = 0x8000000000
            mask_b = 0xFFFFFFFFFF
            mask_c = 0x00000000FF
        else:
            mask_a = None
            mask_b = None
            mask_c = None
        return int(mask_a), int(mask_b), int(mask_c)

    mask1, mask2, mask3 = mask(num_bytes)

    float_num = 0
    for i in range(0, num_bytes):
        float_num += seg_num[i] << (8 * ((num_bytes - 1) - i))

    sign = float_num & mask1
    if sign > 0:
        float_num = bitmask_flip(float_num, mask2)
        float_num += 1

    dec = float_num & mask3
    decimal = float(0)
    if dec != 0:
        for i in range(0, 8):
            bit_val = bit_check(dec, i)
            if bit_val > 0:
                decimal += float(1) / (2 ** (-1 * (i - 8)))

    if num_bytes > 1:
        whole = float_num >> 8
    else:
        whole = float_num

    if sign > 0:
        whole = -1 * float(whole)
        float_num = float(whole) - float(decimal)
    else:
        float_num = float(whole) + float(decimal)

    return float_num
