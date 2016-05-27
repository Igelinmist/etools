from datetime import date, timedelta, datetime


SYS_MASK = 0xFF000000
CTRL_MASK = 0xFFFF00
CHAN_MASK = 0xFF


def yesterday():
    return date.today() - timedelta(days=1)


def delta_e(p, t1, t2):
    """ Расчет приращения энергии """
    dt = t2 - t1
    return p * 1000 * dt.seconds / 3600


def round_tm_30_up(dttm):
    if dttm.minute < 30:
        return datetime(dttm.year, dttm.month, dttm.day, dttm.hour, 30)
    else:
        return datetime(dttm.year, dttm.month, dttm.day, dttm.hour) + timedelta(hours=1)


def round_hr(dttm):
    if dttm.minute < 30:
        return datetime(dttm.year, dttm.month, dttm.day, dttm.hour, 0, 0)
    else:
        return datetime(dttm.year, dttm.month, dttm.day, dttm.hour, 0, 0) + timedelta(hours=1)


class AddrCoder:
    """ Description: Class for encode/decode flat address of systems """

    def decode_addr(flat_addr):
        sys_addr = (flat_addr & SYS_MASK) >> 24
        ctrl_addr = (flat_addr & CTRL_MASK) >> 8
        chan_addr = flat_addr & CHAN_MASK
        return sys_addr, ctrl_addr, chan_addr

    def encode_addr(sys_addr, ctrl_addr, chan_addr):
        return ((sys_addr << 24) | (ctrl_addr << 8) | chan_addr)
