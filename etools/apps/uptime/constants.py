EVENT_CHOICES = (
    ('vkr', 'Ввод из капремонта'),
    ('zmn', 'Ввод после замены'),
    ('vsr', 'Ввод из ср. ремонта'),
    ('vrc', 'Ввод из реконструкции'),
    ('vvd', 'Ввод'),
    ('sps', 'Списание'),
)
EVENT_CHOICES_DICT = dict(EVENT_CHOICES)

# Состояния описываются код, полное имя, короткое имя
STATE_FLAGS = (
    ('wrk', 'Работа', 'Работа'),
    ('hrs', 'Горячий резерв', 'ГР'),
    ('rsv', 'Резерв', 'РЗ'),
    ('arm', 'Аварийный ремонт', 'АР'),
    ('trm', 'Текущий ремонт', 'ТР'),
    ('krm', 'Капитальный ремонт', 'КР'),
    ('srm', 'Средний ремонт', 'СР'),
    ('rcd', 'Реконструкция', 'РК')
)

STATE_FNAME = {st[0]: st[1] for st in STATE_FLAGS}
STATE_SNAME = {st[0]: st[2] for st in STATE_FLAGS}
STATE_SET = {item[0] for item in STATE_FLAGS}
STATE_CHOICES = ((item[0], item[1]) for item in STATE_FLAGS)
