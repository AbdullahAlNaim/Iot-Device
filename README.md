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

#### Install dependencies
```bash
pip install -r requirements.txt
```

#### Create .env file
```bash
DJANGO_SECRET_KEY=your_very_secret_key
```
You can generate one secret key using Python
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

#### Apply migrations and create superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```


#### Run the server
```bash
python manage.py runserver
```

## API Authentication
Authorization: Token your_token_here


with body
```bash
{
  "username": "your-username",
  "password": "your-password"
}
```

#### Include the token
```bash
Authorization: Token your_token_here
```


## Example Payload

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