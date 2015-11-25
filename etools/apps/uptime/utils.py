from datetime import timedelta, date


def req_date(local_date):
    if isinstance(local_date, str):
        d, m, y = local_date.split('.')
        return '{0}-{1}-{2}'.format(y, m, d)
    elif isinstance(local_date, date):
        return local_date.strftime('%Y-%m-%d')
    else:
        return local_date


def req_timedelta(arg):
    if isinstance(arg, timedelta):
        return arg
    else:
        if isinstance(arg, str):
            parts = arg.split(':')
            return timedelta(hours=int(parts[0]), minutes=int(parts[1]))
        else:
            return timedelta(0)


def yesterday_local():
    return (date.today() - timedelta(days=1)).strftime("%d.%m.%Y")


def stat_timedelta_for_report(time_delta):
    if time_delta:
        sec = time_delta.total_seconds()
        hours, remainder = divmod(sec, 3600)
        if remainder >= 1800:
            hours += 1
        return str(int(hours))
    else:
        return '-'
