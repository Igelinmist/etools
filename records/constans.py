
STATE_CHOICES = (
    ('rsv', 'Резерв'),
    ('trm', 'Тек. ремонт'),
    ('arm', 'Ав. ремонт'),
    ('krm', 'Кап. ремонт'),
    ('srm', 'Сред. ремонт'),
    ('rcd', 'Реконструкция'),
)

EVENT_CHOICES = (
    ('vvd', 'Ввод'),
    ('vkr', 'Ввод из капремонта'),
    ('vsr', 'Ввод из ср. ремонта'),
    ('vrc', 'Ввод из реконструкции'),
    ('zmn', 'Ввод после замены'),
    ('sps', 'Списание'),
)
EVENT_CHOICES_DICT = dict(EVENT_CHOICES)

STANDARD_STATE_DATA = ('date', 'work', 'ostanov_cnt', 'pusk_cnt')

EXT_STATE_DATA = ('rsv', 'arm', 'trm', 'krm', 'srm', 'rcd')
