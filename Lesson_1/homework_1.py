# Сценарий Foursquare
# Напишите сценарий на языке Python, который предложит пользователю ввести
# интересующую его категорию (например, кофейни, музеи, парки и т.д.).
# Используйте API Foursquare для поиска заведений в указанной категории.
# Получите название заведения, его адрес и рейтинг для каждого из них.
# Скрипт должен вывести название и адрес и рейтинг каждого заведения в консоль.

import requests

KEY = "fsq3Dzlf4mzZ5Qea/T8VxcLPOD+avdOPHw7ub28s6NT4q6Q="
URL = "https://api.foursquare.com/v3/places/search"

print(
    "Это сценарий, который предложит пользователю ввести интересующую\n\
его категорию (например, кофейни, музеи, парки и т.д.).\n"
)

temp = input("Введите категорию: ")

headers = {
    "Accept": "application/json",
    "Authorization": KEY
}

params = {
    "query": f"{temp}",
    "fields": "name,location,rating"
}

response = requests.get(URL, params=params, headers=headers)
print(response.status_code)

if response.status_code == 200:
    jdata = response.json()
    for place in jdata['results']:
        print('------------------------------------------------')
        name = place['name']
        print('НАЗВАНИЕ: ', name)
        location = place['location']
        address = location['formatted_address']
        print('АДРЕС: ', address)
        rating = place['rating']
        print('РЕЙТИНГ: ', rating)
