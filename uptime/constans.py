
STATE_CHOICES = (
    ('wrk', 'Работа'),
    ('hrs', 'Горячий резерв'),
    ('rsv', 'Резерв'),
    ('trm', 'Тек. ремонт'),
    ('arm', 'Ав. ремонт'),
    ('krm', 'Кап. ремонт'),
    ('srm', 'Сред. ремонт'),
    ('rcd', 'Реконструкция'),
)

EVENT_CHOICES = (
    ('vkr', 'Ввод из капремонта'),
    ('zmn', 'Ввод после замены'),
    ('vsr', 'Ввод из ср. ремонта'),
    ('vrc', 'Ввод из реконструкции'),
    ('vvd', 'Ввод'),
    ('sps', 'Списание'),
)
EVENT_CHOICES_DICT = dict(EVENT_CHOICES)

STANDARD_STATE_DATA = ('date', 'work', 'ostanov_cnt', 'pusk_cnt')

EXT_STATE_DATA = ('rsv', 'arm', 'trm', 'krm', 'srm', 'rcd')
