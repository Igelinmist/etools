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
            try:
                res = timedelta(hours=int(parts[0]), minutes=int(parts[1]))
            except ValueError:
                res = timedelta(0)
            return res
        else:
            return timedelta(0)


def yesterday_local():
    return (date.today() - timedelta(days=1)).strftime("%d.%m.%Y")


def stat_timedelta_for_report(time_delta, round_to_hour=True):
    if time_delta:
        sec = time_delta.total_seconds()
        hours, remainder = divmod(sec, 3600)
        if round_to_hour:
            if remainder >= 1800:
                hours += 1
            return str(int(hours))
        minutes, remainder = divmod(remainder, 60)
        return "{0:,d}:{1:02}".format(int(hours), int(minutes)).replace(',',' ')
    else:
        return '-'


def custom_redirect(url_name, *args, **kwargs):
    from django.core.urlresolvers import reverse
    from django.http import HttpResponseRedirect
    from django.utils.http import urlencode
    url = reverse(url_name, args=args)
    params = urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)
