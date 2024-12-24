import requests

r = requests.get('https://placebear.com/g/200/300')

with open('bear.jpg', 'wb') as f:
    f.write(r.content)
