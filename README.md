# Installation

In order to use and install this server you need to have a **Python 3**

Additional libraries are required:

```
pip3 install Django Pillow django-extensions Werkzeug pyOpenSSL
```

or you can use **install.sh** script

After this navigate to your clone project folder and perform migrations:
```
python3 manage.py makemigrations
python3 manage.py migrate
```

After this you can run the mock-server with predefined self-signed sertificates:

**Android**: `manage.py runserver_plus 0.0.0.0:8000 --cert-file emulator.crt`
**iOS**: `python3 manage.py runserver_plus 10.0.2.2:8000 --cert-file emulator.crt`

## Generating of certificate
If you want to generate own certificate here is a good one-liner:

```
openssl req -x509 -newkey rsa:4096 -sha256 -days 3650 -nodes \
  -keyout example.key -out example.crt -extensions san -config \
  <(echo "[req]"; 
    echo distinguished_name=req; 
    echo "[san]"; 
    echo subjectAltName=DNS:example.com,DNS:example.net,IP:10.0.0.1
    ) \
  -subj /CN=example.com
```

where example.com is your domain, and 10.0.0.1 is your IP. You remove not needed. After this you can use example.crt with your server.

## iOS: Setup loclalhost alias

You may need to add the alias `10.0.0.2` to `localhost` in this case:

`sudo ifconfig lo0 alias 10.0.2.2`

See this [article](https://medium.com/@david.limkys/permanently-create-an-ifconfig-loopback-alias-macos-b7c93a8b0db) if
you want to add the alias permanently.

    
# HTTP API

## Get ad response

`POST ma/1.0/acj`

### Params
`auid` - unit id (required)

### Type
`application/x-www-form-urlencoded`

### Returns
Returns `application/json` with an ad response


### Request example

```
curl -X POST \
  https://localhost:8000/ma/1.0/acj \
  -H 'Accept: */*' \
  -H 'Accept-Encoding: gzip, deflate' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Length: 14' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Cookie: i=0563f8b6-1cf2-0748-1940-670f86558a55|1575290845; pd=v2|1575375930|gu' \
  -H 'Host: mobile-d.openx.net' \
  -H 'Postman-Token: 49e4ac05-ef66-432e-8a52-65d80b3b93b2,3f6af8f2-60bc-4e82-ad75-4f9df620fb5d' \
  -H 'User-Agent: PostmanRuntime/7.20.1' \
  -H 'cache-control: no-cache' \
  -d auid=540854022
```

#### Note:
If you get the error message:
```
curl: (60) SSL certificate problem: self signed certificate
...
```
add the **-k** key to the request:
```
curl -k -X POST 
...
```

## Get video ad response

`POST v/1.0/av`

### Params
`auid` - unit id (required)

### Type
`application/x-www-form-urlencoded`

### Returns
Returns `text/xml` with video ad response

### Request Example

```
curl -X POST \
  https://localhost:8000/v/1.0/av \
  -H 'Accept: */*' \
  -H 'Accept-Encoding: gzip, deflate' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Length: 14' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Cookie: i=0563f8b6-1cf2-0748-1940-670f86558a55|1575290845; pd=v2|1575375930|gu' \
  -H 'Host: mobile-d.openx.net' \
  -H 'Postman-Token: 3c3329d5-adc5-421d-bb84-b8ff381914c3,6113d21f-0d7a-4111-b7d3-720a64436120' \
  -H 'User-Agent: PostmanRuntime/7.20.1' \
  -H 'cache-control: no-cache' \
  -d auid=540854022
```

## Add mock

`POST api/add_mock`

### Params
`auid` - unit id (required)

`mock` - needed mock response (required)

`type` - needed mock type. Currently supported: `regular` and `video` (optional, default is regular)

### Type
`application/x-www-form-urlencoded`

### Returns
Returns `application/json` with a result.
Success: 
```
{
  "result": true
}
```

When failed:
```
{
  "result": false,
  "message": "reason"
}
```

### Request example
```
curl -X POST \
  https://localhost:8000/api/add_mock \
  -H 'Accept: */*' \
  -H 'Accept-Encoding: gzip, deflate' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Length: 2395' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Host: 192.168.1.3:8000' \
  -H 'Postman-Token: e3b87ac3-fab7-478d-83c4-00f8334287ee,55ddbf5b-9488-44ed-95ba-c46e95dec6e1' \
  -H 'User-Agent: PostmanRuntime/7.20.1' \
  -H 'cache-control: no-cache' \
  -d 'mock=%7B%0A%09%22ads%22%3A%20%7B%0A%09%09%22medium%22%3A%20%22ma%22%2C%0A%09%09%22record_tmpl%22%3A%20%22https%3A%2F%2F10.0.2.2%3A8000%2Fevents%2F%7Bmedium%7D%2F1.0%2F%7Brtype%7D%3Fai%3Daae57568-450a-4d45-895f-1f4289bf4331%26ph%3Da51065ab-17ee-4394-b5a7-32debc04780a%26ts%3D%7Btxn_state%7D%22%2C%0A%09%09%22oxt%22%3A%2023.753%2C%0A%09%09%22adunits%22%3A%20%5B%7B%0A%09%09%09%22auid%22%3A%20%22537454411%22%2C%0A%09%09%09%22idx%22%3A%20%220%22%2C%0A%09%09%09%22refresh_delay%22%3A%20%2210%22%2C%0A%09%09%09%22refresh_max%22%3A%20%225%22%2C%0A%09%09%09%22chain_revenue%22%3A%20%22%22%2C%0A%09%09%09%22chain%22%3A%20%5B%7B%0A%09%09%09%09%22is_fallback%22%3A%200%2C%0A%09%09%09%09%22ad_id%22%3A%20%22540857694%22%2C%0A%09%09%09%09%22adv_acct_id%22%3A%20%22537137359%22%2C%0A%09%09%09%09%22is_ng%22%3A%201%2C%0A%09%09%09%09%22adv_id%22%3A%20%22%3A537137359%22%2C%0A%09%09%09%09%22brand_id%22%3A%20%22%22%2C%0A%09%09%09%09%22cpipc%22%3A%200%2C%0A%09%09%09%09%22auct_win_is_deal%22%3A%200%2C%0A%09%09%09%09%22pub_rev%22%3A%20%220%22%2C%0A%09%09%09%09%22width%22%3A%20%22320%22%2C%0A%09%09%09%09%22height%22%3A%20%2250%22%2C%0A%09%09%09%09%22html%22%3A%20%22%3Cscript%20src%3D%5C%22https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fomsdk-files%2Fcompliance-js%2Fomid-validation-verification-script-v1.js%5C%22%3E%3C%2Fscript%3E%5Cn%3Ca%20href%3D%5C%22https%3A%2F%2Fwww.openx.com%2F%5C%22%3E%3Cimg%20width%3D%5C%22320%5C%22%20height%3D%5C%2250%5C%22%20src%3D%5C%22https%3A%2F%2F10.0.2.2%3A8000%2Fimage%3FunitId%3D537454411%5C%22%3E%3C%2Fimg%3E%3C%2Fa%3E%22%2C%0A%09%09%09%09%22target%22%3A%20%22_blank%22%2C%0A%09%09%09%09%22ts%22%3A%20%222DAABBgABAAECAAIBAAsAAgAAAJkcGApIVzVuVUVsekg5HBbiqpLYkPvW2Z0BFtvWjIDX8NX_qQEAHBaN9u2L9pqN1qEBFq2P0Pjzl5yIhQEAFt7z69oLFQIRACwcFQIAHBUCAAAcJpadx4AEFQ4VBCaQuaaABBaggJyABNYAABwmnsOggAQWotXmgwQWvNXmgwQWutXmgwQVFBwUZBSABQAVBBUKFgAmAEUKAAAA%22%2C%0A%09%09%09%09%22type%22%3A%20%22html%22%2C%0A%09%09%09%09%22ad_url%22%3A%20%22%3Cscript%20src%3D%5C%22https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fomsdk-files%2Fcompliance-js%2Fomid-validation-verification-script-v1.js%5C%22%3E%3C%2Fscript%3E%5Cn%3Ca%20href%3D%5C%22https%3A%2F%2Fwww.openx.com%2F%5C%22%3E%3Cimg%20width%3D%5C%22320%5C%22%20height%3D%5C%2250%5C%22%20src%3D%5C%22https%3A%2F%2F10.0.2.2%3A8000%2Fimage%3FunitId%3D537454411%5C%22%3E%3C%2Fimg%3E%3C%2Fa%3E%22%0A%09%09%09%7D%5D%0A%09%09%7D%5D%0A%09%7D%0A%7D&auid=540881524'
```

## Get logs

`GET api/logs`

### Params
No params
### Type
`application/x-www-form-urlencoded`

### Request example
```
curl -X GET \
  https://localhost:8000/api/logs \
  -H 'Accept: */*' \
  -H 'Accept-Encoding: gzip, deflate' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Host: 192.168.1.3:8000' \
  -H 'Postman-Token: a9cfa9be-46d6-474d-80cf-3a41f142f999,30c75011-2953-477a-a275-0a5107e377bf' \
  -H 'User-Agent: PostmanRuntime/7.20.1' \
  -H 'cache-control: no-cache'
```

### Returns
Returns `application/json` with a list of requests which has been logged.
Success: 
```
{
  "requests": [
    {
      "path": "/ma/1.0/acj",
      "host": "10.0.2.2:8000",
      "method": "POST",
      "body": "sv=4.11.0&openrtb=%7B%22tmax%22%3A3000%2C%22imp%22%3A%5B%7B%22displaymanager%22%3A%22openx%22%2C%22displaymanagerver%22%3A%224.11.0%22%2C%22instl%22%3A0%2C%22clickBrowser%22%3A0%2C%22secure%22%3A1%2C%22banner%22%3A%7B%22api%22%3A%5B5%2C3%2C7%5D%7D%7D%5D%2C%22app%22%3A%7B%22name%22%3A%22OpenX%20Internal%20Test%22%2C%22bundle%22%3A%22com.openx.internal_test_app%22%7D%2C%22device%22%3A%7B%22lmt%22%3A0%2C%22make%22%3A%22Google%22%2C%22model%22%3A%22Android%20SDK%20built%20for%20x86%22%2C%22os%22%3A%22Android%22%2C%22osv%22%3A%227.1.1%22%2C%22language%22%3A%22en%22%2C%22carrier%22%3A%22Android%22%2C%22mccmnc%22%3A%22310-260%22%2C%22ifa%22%3A%22fcdae928-c694-4222-a7c7-7d9a28f117ab%22%2C%22h%22%3A1920%2C%22w%22%3A1080%2C%22connectiontype%22%3A2%2C%22geo%22%3A%7B%7D%7D%2C%22user%22%3A%7B%7D%7D&aus=320x50%2C%20300x250&sp=Android&auid=537454411",
      "queryString": {
        
      }
    },
    {
      "path": "/events/sendmessage?version=1.0.2-dev",
      "host": "10.0.2.2:8000",
      "method": "GET",
      "body": "",
      "queryString": {
        "version": "1.0.2-dev"
      }
    },
    {
      "path": "/events/sendmessage?adSessionId=e234bc1e-c9bd-4735-aa33-8862cc4ac075&timestamp=1574436343010&type=sessionStart&data%5Bcontext%5D%5BapiVersion%5D=1.0&data%5Bcontext%5D%5BaccessMode%5D=limited&data%5Bcontext%5D%5BomidJsInfo%5D%5BomidImplementer%5D=omsdk&data%5Bcontext%5D%5BomidJsInfo%5D%5BserviceVersion%5D=1.2.13-iab735&data%5Bcontext%5D%5Benvironment%5D=app&data%5Bcontext%5D%5BadSessionType%5D=html&data%5Bcontext%5D%5BdeviceInfo%5D%5BdeviceType%5D=Google%3B%20Android%20SDK%20built%20for%20x86&data%5Bcontext%5D%5BdeviceInfo%5D%5BosVersion%5D=25&data%5Bcontext%5D%5BdeviceInfo%5D%5Bos%5D=Android&data%5Bcontext%5D%5Bsupports%5D%5B0%5D=clid&data%5Bcontext%5D%5Bsupports%5D%5B1%5D=vlid&data%5Bcontext%5D%5BomidNativeInfo%5D%5BpartnerName%5D=Openx&data%5Bcontext%5D%5BomidNativeInfo%5D%5BpartnerVersion%5D=4.11.0&data%5Bcontext%5D%5Bapp%5D%5BlibraryVersion%5D=1.2.13-Openx&data%5Bcontext%5D%5Bapp%5D%5BappId%5D=com.openx.internal_test_app&data%5Bcontext%5D%5BcustomReferenceData%5D=&data%5BverificationParameters%5D=undefined",
      "host": "10.0.2.2:8000",
      "method": "GET",
      "body": "",
      "queryString": {
        "adSessionId": "e234bc1e-c9bd-4735-aa33-8862cc4ac075",
        "timestamp": "1574436343010",
        "type": "sessionStart",
        "data[context][apiVersion]": "1.0",
        "data[context][accessMode]": "limited",
        "data[context][omidJsInfo][omidImplementer]": "omsdk",
        "data[context][omidJsInfo][serviceVersion]": "1.2.13-iab735",
        "data[context][environment]": "app",
        "data[context][adSessionType]": "html",
        "data[context][deviceInfo][deviceType]": "Google; Android SDK built for x86",
        "data[context][deviceInfo][osVersion]": "25",
        "data[context][deviceInfo][os]": "Android",
        "data[context][supports][0]": "clid",
        "data[context][supports][1]": "vlid",
        "data[context][omidNativeInfo][partnerName]": "Openx",
        "data[context][omidNativeInfo][partnerVersion]": "4.11.0",
        "data[context][app][libraryVersion]": "1.2.13-Openx",
        "data[context][app][appId]": "com.openx.internal_test_app",
        "data[context][customReferenceData]": "",
        "data[verificationParameters]": "undefined"
      }
    }
  ]
```

## Clear logs

`GET api/clear_logs`

### Params
No params
### Type
`application/x-www-form-urlencoded`
### Returns
200 HTTP code on success

### Request example
```
curl -X GET \
  https://localhost:8000/api/clear_logs \
  -H 'Accept: */*' \
  -H 'Accept-Encoding: gzip, deflate' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Host: 192.168.1.3:8000' \
  -H 'Postman-Token: 198213f5-8176-49d1-8c6a-7d0e8fd5141b,009c7bb2-8689-40c9-b487-c22d50aa4c8e' \
  -H 'User-Agent: PostmanRuntime/7.20.1' \
  -H 'cache-control: no-cache'
```

## Generate banner image

`GET image`

### Params
```auid``` - unit id which will be used as a text on a banner. (required)

```width``` - width in pixels (default 640)

```height``` - width in pixels (default 100)

### Type
`application/x-www-form-urlencoded`
### Returns
PNG Image

### Request example
```
curl -X GET \
  'https://localhost:8000/image?auid=12321526' \
  -H 'Accept: */*' \
  -H 'Accept-Encoding: gzip, deflate' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Host: 192.168.1.3:8000' \
  -H 'Postman-Token: 0cdd8ec3-e403-4fd7-869a-5803aeb7410e,2f88c921-324d-4737-8d1a-dbc150c21e19' \
  -H 'User-Agent: PostmanRuntime/7.20.1' \
  -H 'cache-control: no-cache'
```

## Log any request (events)

Every request sent to this URL will be logged with all the data comes in

`GET/POST events`

### Params
Any number of params
### Type
Any type
### Returns
200 OK HTTP code on success

## Set response with error

`GET set_error`

After this request all acj/vast requests will get response with error.

### Params
No params

### Type
`application/x-www-form-urlencoded`

### Returns
200 HTTP code on success

### Request example

```
curl -L -X GET 'https://localhost:8000/api/set_error' \
-H 'Accept-Encoding: gzip, deflate' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-H 'User-Agent: PostmanRuntime/7.21.0' \
-H 'Accept: */*' \
-H 'Cache-Control: no-cache' \
-H 'Postman-Token: c579e7d6-294b-47e2-8e81-4a53b21bd975' \
-H 'Host: localhost:8000' \
-H 'Content-Length: ' \
-H 'Connection: keep-alive'
```

## Cancel response with error

`GET cancel_error`

Resets response with error flag

### Params
No params

### Type
`application/x-www-form-urlencoded`

### Returns
200 HTTP code on success

### Request example
```
curl -L -X GET 'https://localhost:8000/api/cancel_error' \
-H 'Accept-Encoding: gzip, deflate' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-H 'User-Agent: PostmanRuntime/7.21.0' \
-H 'Accept: */*' \
-H 'Cache-Control: no-cache' \
-H 'Postman-Token: c579e7d6-294b-47e2-8e81-4a53b21bd975' \
-H 'Host: localhost:8000' \
-H 'Content-Length: ' \
-H 'Connection: keep-alive'
```

## Set response latency

`POST set_latency`

Sets the time in milliseconds, after which server will return response

### Params
No params

### Body
`latency` - time units in milliseconds (required)

### Type
`application/x-www-form-urlencoded`

### Returns
200 HTTP code on success

### Request example
```
curl -L -X POST 'https://localhost:8000/api/set_latency' \
-H 'Accept-Encoding: gzip, deflate' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-H 'User-Agent: PostmanRuntime/7.21.0' \
-H 'Accept: */*' \
-H 'Cache-Control: no-cache' \
-H 'Postman-Token: c579e7d6-294b-47e2-8e81-4a53b21bd975' \
-H 'Host: localhost:8000' \
-H 'Content-Length: ' \
-H 'Connection: keep-alive' \
--data-urlencode 'latency=1000'
```

## Cancel latency

`GET cancel_latency`

Disable response latency

### Params
No params

### Type
`application/x-www-form-urlencoded`

### Returns
200 HTTP code on success

### Request example
```
curl -L -X GET 'https://localhost:8000/api/cancel_latency' \
-H 'Accept-Encoding: gzip, deflate' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-H 'User-Agent: PostmanRuntime/7.21.0' \
-H 'Accept: */*' \
-H 'Cache-Control: no-cache' \
-H 'Postman-Token: c579e7d6-294b-47e2-8e81-4a53b21bd975' \
-H 'Host: localhost:8000' \
-H 'Content-Length: ' \
-H 'Connection: keep-alive'
```
