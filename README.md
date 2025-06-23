# IoT Device API

A Django REST Framework application for ingesting and processing payloads from IoT devices.

## Features

- Two models: `Device` and `Payload`
- Receives payloads via POST request and:
  - Associates them with a device (via `devEUI`)
  - Parses base64-encoded `data` into hexadecimal
  - Determines passing/failing status based on data
  - Stores and updates the latest device status
- Token-based authentication (DRF TokenAuth)
- Handles duplicate messages using `fCnt` per device
- Supports camelCase payload fields from external IoT systems

---

## Setup Instructions


#### Clone the Repo
```bash
git clone https://github.com/abdullahalnaim/iot-device-api.git
cd iot-device-api
```

#### Create the virtaul env
```bash
python -m venv venv
```

Run virtual env.

#### Install dependencies
```bash
pip install -r requirements.txt
```

#### Create .env file
```bash
DJANGO_SECRET_KEY=your_very_secret_key
```
You can generate one secret key using Python.
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

#### Apply migrations and create superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```
Check if the 2 models were created. Can check with:
```bash
python manage.py showmigrations
```

If it wasn't created, create the migration for the specific model.
```bash
python manage.py makemigrations devices
python manage.py migrate
```


#### Run the server
```bash
python manage.py runserver
```

## API Authentication Required
Authorization: Token your_token_here

Steps to acuire token:

POST url
```bash
http://localhost:8000/api-token-auth/
```

with body
```bash
{
  "username": "your-username",
  "password": "your-password"
}
```
copy the token and paste into request headers

#### Include the token
```bash
Authorization: Token your_token_here
```
## Running Tests

To ensure the app is working correctly, you can run:

```bash
python manage.py test devices/tests
```

## Example Payload
POST endpoint
```bash
http://localhost:8000/api/payloads/
```
Body

```json
{
  "fCnt": 100,
  "devEUI": "abcdabcdabcdabcd",
  "data": "AQ==",
  "rxInfo": [
    {
      "gatewayID": "1234123412341234",
      "name": "G1",
      "time": "2022-07-19T11:00:00",
      "rssi": -57,
      "loRaSNR": 10
    }
  ],
  "txInfo": {
    "frequency": 86810000,
    "dr": 5
  }
}
```