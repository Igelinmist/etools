from django import template

from ..constans import EVENT_CHOICES_DICT

register = template.Library()


@register.filter()
def interval(time_delta):
    sec = time_delta.total_seconds()
    hours, remainder = divmod(sec, 3600)
    minutes, sec = divmod(remainder, 60)
    return '%4d:%02d' % (int(hours), int(minutes))


@register.filter()
def make_ident(ident):
    return '--' * ident + ' '


@register.filter()
def sum_stat(journal, key):
    stat_pair_list = journal.last_stat.split(',')
    stat_dict = dict([par.split('=') for par in stat_pair_list])
    return stat_dict[key]


@register.filter()
def human_event(event_code):
    return EVENT_CHOICES_DICT[event_code]


@register.filter()
def key(d, key_name):
    return d[key_name]
