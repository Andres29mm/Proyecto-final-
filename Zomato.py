import requests
import pandas as pd
import boto3
import sys

zomato_api = '13790801be6b5c13a680ec73e5337562'

def get_cities(q):
    headers = {
        'Accept': 'application/json',
        'user-key': zomato_api,
    }
    params = (
        ('q', q),
    )

    response = requests.get('https://developers.zomato.com/api/v2.1/cities', headers=headers, params=params)
    data = response.json()
    return data

def get_cuisines(city_id):
    headers = {
        'Accept': 'application/json',
        'user-key': zomato_api,
    }
    params = (
        ('city_id', city_id),
    )

    response = requests.get('https://developers.zomato.com/api/v2.1/cuisines', headers=headers, params=params)
    data = response.json()
    return data

def get_establishment(city_id):
    headers = {
        'Accept': 'application/json',
        'user-key': zomato_api,
    }
    params = (
        ('city_id', city_id),
    )

    response = requests.get('https://developers.zomato.com/api/v2.1/establishments', headers=headers, params=params)
    data = response.json()
    return data

def get_location_details(query):

    headers = {
        'Accept': 'application/json',
        'user-key': zomato_api,
    }
    params = (
        ('query', query),
    )

    response = requests.get('https://developers.zomato.com/api/v2.1/locations', headers=headers, params=params)
    data = response.json()

    for loc in data['location_suggestions']:
        loc_id = loc['entity_id']
        loc_type = loc['entity_type']

    return loc_id, loc_type

def get_search(query):

    headers = {
        'Accept': 'application/json',
        'user-key': zomato_api,
    }
    params = (
        ('query', query),
    )

    response = requests.get('https://developers.zomato.com/api/v2.1/search', headers=headers, params=params)
    data = response.json()
    return data


def get_restaurants(ent_id, ent_type):

    headers = {
        'Accept': 'application/json',
        'user-key': zomato_api,
    }

    params = (
        ('entity_id', ent_id),
        ('entity_type', ent_type),
    )

    response = requests.get('https://developers.zomato.com/api/v2.1/search', headers=headers, params=params)

    return response.json()

def get_restaurants(ent_id, ent_type):

    headers = {
        'Accept': 'application/json',
        'user-key': zomato_api,
    }

    params = (
        ('entity_id', ent_id),
        ('entity_type', ent_type),
    )

    response = requests.get('https://developers.zomato.com/api/v2.1/search', headers=headers, params=params)

    return response.json()


if __name__ == '__main__':
               
# Se recupera la informaciopn de las ciudades 
    archivo_excel = pd.read_excel('C:/Users/ptapiero/Desktop/Ciudades.xlsx')
    print(archivo_excel.columns)
    nombres_ciudades = archivo_excel['Ciudades'].values
    city_ids=[]
    for c in nombres_ciudades:
        print(c)
        data_citys= get_cities(c)
        for city in data_citys['location_suggestions']:
            city_id=city['id']
            print(city['id'])
            print(city['name'].upper())
            print(city['country_id'])
            print(city['country_name'].upper())
            city_ids.append(city_id)
            
# Se accede a la configuracion del boot para cargar informacion al buscket
    s3 = boto3.resource('s3',region_name='us-east-2',aws_access_key_id='AKIA4EBNYS22ZWFWTBR6',aws_secret_access_key='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')
    s3.Bucket('testzomato').put_object(Key='citys.json', Body='data_citys')
    
# Se recupera informacion de los establecimientos registrados por ciudades
    for city_id in city_ids:
         establishment_data=get_establishment(city_id)
         print(establishment_data)
         for establishment in establishment_data['establishments']:
             e=establishment['establishment']
             print(e['id'])
             print(e['name'].upper())
    s3.Bucket('testzomato').put_object(Key='establishmen.json', Body='establishment_data')

# Se recupera informacion de los restaurantes con su especifica tipo de cocina por id de ciudad
    for city_id in city_ids:
         cuisines_data=get_cuisines(city_id)
         print(cuisines_data)
         for cuisine in cuisines_data['cuisines']:
             c=cuisine['cuisine']
             print(c['cuisine_id'])
             print(c['cuisine_name'].upper())
    s3.Bucket('testzomato').put_object(Key='cuisines.json', Body='cuisines_data')


