import datetime

def date_format_ics(date, time):
    '''Converts date to date in ICS format'''
    def add_zeros(s, year=False):
        '''Adds the right number of zeros before the string s so that len(s) = 2 (4 if it is a year)'''
        if year:
            return (4 -len(s))*'0' + s

        return (2-len(s))*'0' + s

    if time == None:
        time = datetime.time.min

    s1 = str(date.year)
    s2 = str(date.month)
    s3 = str(date.day)
    s4 = str(time.hour)
    s5 = str(time.minute)
    s6 = str(time.second)
    return add_zeros(s1) + add_zeros(s2) + add_zeros(s3) + "T" + add_zeros(s4) + add_zeros(s5) + add_zeros(s6) + "Z"
