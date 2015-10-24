def req_date(local_date):
    d, m, y = local_date.split('.')
    return '{0}-{1}-{2}'.format(y, m, d)
