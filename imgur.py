import urllib
import base64
import simplejson

API_KEY = '1c5bc30783866fee7a0bda498abfd281'
BASE_URL = 'http://api.imgur.com/2/%s.json'

def upload(image):
    if type(image) in [str, unicode]:
        data_dict = {'key': API_KEY, 'image': image}
    else:
        data_dict = {'key': API_KEY, 'image': base64.b64encode(image.read())}
    server_data = urllib.urlencode(data_dict)
    response = urllib.urlopen(BASE_URL % 'upload', data = server_data)
    return simplejson.loads(response.read())