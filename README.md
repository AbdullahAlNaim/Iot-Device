# IoT Device API

A Django REST Framework application for ingesting and processing payloads from IoT devices. This project was created as part of a coding challenge for Hexmodal.

## Features

- Two main models: `Device` and `Payload`
- Receives payloads via POST request and:
  - Associates them with a device (via `devEUI`)
  - Parses base64-encoded `data` into hexadecimal
  - Determines pass/fail status based on data
  - Stores and updates the latest device status
- Token-based authentication (DRF TokenAuth)
- Handles duplicate messages using `fCnt` per device
- Supports camelCase payload fields from external IoT systems

---

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


