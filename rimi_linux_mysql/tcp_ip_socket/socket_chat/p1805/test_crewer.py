import requests

r = requests.get('http://blog.jobbole.com/114499/')

print(r.text)