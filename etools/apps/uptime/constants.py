
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

RECORD_SET = {'rdate', 'down_cnt', 'up_cnt'}

INTERVAL_SET = {'wrk', 'hrs', 'rsv', 'arm', 'trm', 'krm', 'srm', 'rcd'}

EXT_INTERVAL_SET = {'rsv', 'arm', 'trm', 'krm', 'srm', 'rcd'}
