from datetime import timedelta


def req_date(local_date):
    d, m, y = local_date.split('.')
    return '{0}-{1}-{2}'.format(y, m, d)


def req_timedelta(arg):
    if isinstance(arg, timedelta):
        return arg
    else:
        if isinstance(arg, str):
            parts = arg.split(':')
            return timedelta(hours=int(parts[0]), minutes=int(parts[1]))
        else:
            return timedelta(0)
