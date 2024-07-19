import requests
import openpyxl
import redis
import json
from config import TRUECALLER_API_KEY, NUMBERBOOK_API_KEY, NUMVERIFY_API_KEY, OPENCNAM_API_KEY, REDIS_HOST, REDIS_PORT, REDIS_DB

# اتصال به Redis
redis_client = None
try:
    redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    redis_client.ping()
    print("Connected to Redis")
except (redis.ConnectionError, redis.TimeoutError):
    redis_client = None
    print("Could not connect to Redis")

def check_truecaller(number):
    cache_key = f'truecaller:{number}'
    if redis_client:
        cached_result = redis_client.get(cache_key)
        if cached_result:
            return json.loads(cached_result.decode('utf-8'))
    headers = {
        'Authorization': f'Bearer {TRUECALLER_API_KEY}',
    }
    response = requests.get(f'https://api.truecaller.com/v1/search?number={number}', headers=headers)
    if response.status_code == 200:
        data = response.json()
        result = {
            'name': data['data'][0]['name'],
            'carrier': data['data'][0]['carrier']
        }
        if redis_client:
            redis_client.setex(cache_key, 3600, json.dumps(result))
        return result
    else:
        return None

def check_numberbook(number):
    cache_key = f'numberbook:{number}'
    if redis_client:
        cached_result = redis_client.get(cache_key)
        if cached_result:
            return json.loads(cached_result.decode('utf-8'))
    headers = {
        'Authorization': f'Bearer {NUMBERBOOK_API_KEY}',
    }
    response = requests.get(f'https://api.numberbook.com/v1/search?number={number}', headers=headers)
    if response.status_code == 200:
        data = response.json()
        result = {
            'name': data['data'][0]['name']
        }
        if redis_client:
            redis_client.setex(cache_key, 3600, json.dumps(result))
        return result
    else:
        return None

def check_numverify(number):
    cache_key = f'numverify:{number}'
    if redis_client:
        cached_result = redis_client.get(cache_key)
        if cached_result:
            return json.loads(cached_result.decode('utf-8'))
    response = requests.get(f'http://apilayer.net/api/validate?access_key={NUMVERIFY_API_KEY}&number={number}')
    if response.status_code == 200:
        data = response.json()
        result = {
            'country_name': data['country_name'],
            'carrier': data['carrier']
        }
        if redis_client:
            redis_client.setex(cache_key, 3600, json.dumps(result))
        return result
    else:
        return None

def check_opencnam(number):
    cache_key = f'opencnam:{number}'
    if redis_client:
        cached_result = redis_client.get(cache_key)
        if cached_result:
            return json.loads(cached_result.decode('utf-8'))
    response = requests.get(f'https://api.opencnam.com/v3/phone/{number}?account_sid={OPENCNAM_API_KEY}')
    if response.status_code == 200:
        data = response.json()
        result = {
            'name': data['name']
        }
        if redis_client:
            redis_client.setex(cache_key, 3600, json.dumps(result))
        return result
    else:
        return None

def check_local_database(number):
    workbook = openpyxl.load_workbook('data/local_database.xlsx')
    sheet = workbook.active
    for row in sheet.iter_rows(values_only=True):
        if row[0] == number:
            return row[1]
    return None
