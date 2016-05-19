from datetime import date, timedelta


def yesterday():
    return date.today() - timedelta(days=1)

SYS_MASK = 0xFF000000
CTRL_MASK = 0xFFFF00
CHAN_MASK = 0xFF


class AddrCoder:
    """ Description: Class for encode/decode flat address of systems """

    def decode_addr(flat_addr):
        sys_addr = (flat_addr & SYS_MASK) >> 24
        ctrl_addr = (flat_addr & CTRL_MASK) >> 8
        chan_addr = flat_addr & CHAN_MASK
        return sys_addr, ctrl_addr, chan_addr

    def encode_addr(sys_addr, ctrl_addr, chan_addr):
        return ((sys_addr << 24) | (ctrl_addr << 8) | chan_addr)
