import requests, urllib
from django.utils.encoding import smart_str
key = 'AIzaSyDlFVWD7CVtS_Sy6LeKkeKhaabRX6AfJV0'

def get_lat(location):

    location = smart_str(location)
    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    r = requests.get(url, params={'address': location, 'key': key})
    data = r.json()
    if r.status_code == requests.codes.ok:
        lat = str(data['results'][0]['geometry']['location']['lat'])
        return '%s' % (lat)
    else:
        return ''

def get_lng(location):

    location = smart_str(location)
    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    r = requests.get(url, params={'address': location, 'key': key})
    data = r.json()
    if r.status_code == requests.codes.ok:
        lng = str(data['results'][0]['geometry']['location']['lng'])
        return '%s' % (lng)
    else:
        return ''
