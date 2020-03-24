import datetime

# 将时间的字符格式转换为时间格式
def trans_str_date(strdate):
    if not isinstance(strdate, str):
        return strdate
    if len(strdate) > 12:
        date = datetime.datetime.strptime(strdate, '%Y-%m-%d %H:%M:%S')
    else:
        date = datetime.datetime.strptime(strdate, '%Y-%m-%d')
    return date


# 将时间的时间格式转换为字符格式：
def trans_date_str(date):
    if isinstance(date, str):
        return date
    try:
        strdate = datetime.datetime.strftime(date, '%Y-%m-%d %H:%M:%S')
    except:
        strdate = datetime.datetime.strftime(date, '%Y-%m-%d')
    return strdate