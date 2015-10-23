def req_date(ldate):
    d, m, y = ldate.split('.')
    return '{0}-{1}-{2}'.format(y, m, d)
