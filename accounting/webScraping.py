import bs4 as bs
import urllib.request
import datetime

def get_currency_equivalence(fromCurrency, toCurrency, amount):
    ''' Function that gets the omline exchange rate value '''

    url = "https://www.x-rates.com/calculator/"
    values = { 
      'from': fromCurrency,
      'to': toCurrency,
      'amount': str(amount)}

    data = urllib.parse.urlencode(values).encode('ascii')
    req = urllib.request.Request(url, data)

    sauce = urllib.request.urlopen(req).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')
    tag = soup.find_all('span',class_="ccOutputRslt")
    return float(tag[0].get_text()[0:8])
