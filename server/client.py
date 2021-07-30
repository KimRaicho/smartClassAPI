from __future__ import print_function
import requests


address = 'http://127.0.0.1:5000/test/connection'
my_img = {'image': open('sheep.jpg', 'rb')}

r = requests.post(address, files=my_img)

print(r.json())
