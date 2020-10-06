from datetime import datetime


def strftime(date_format, date):
    def suffix(day):
        return 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')

    return date.strftime(date_format).replace('{S}', str(date.day) + suffix(date.day))


def roam_date(date: datetime):
    return strftime("%B {S}, %Y", date)
