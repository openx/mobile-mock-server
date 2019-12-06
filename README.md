# Installation

In order to use and install this server you need to have a **Python 3**

Additional libraries are required:

```
pip3 install Django Pillow django-extensions Werkzeug pyOpenSSL
```

or you can use **install.sh** script

After this navigate to your clone project folder and run:
`python3 manage.py runserver_plus --cert-file example.crt`

where example.crt is your generated certificate for your IP address or host. 

There is included certificate for android emulator which points to 10.0.2.2 IP.

Good one-liner:

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
    
# HTTP API

## Get ad response

`POST ma/1.0/acj`

### Params
`auid` - unit id (required)

### Type
`application/x-www-form-urlencoded`

### Returns
Returns `application/json` with an ad response


## Get video ad response

`POST v/1.0/av`

### Params
`auid` - unit id (required)

### Type
`application/x-www-form-urlencoded`

### Returns
Returns `text/xml` with video ad response

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
POST /api/add_mock HTTP/1.1
Host: 192.168.1.3:8000
Content-Type: application/x-www-form-urlencoded
User-Agent: PostmanRuntime/7.20.1
Accept: */*
Cache-Control: no-cache
Postman-Token: 23379e21-1a4c-4591-9b69-03fb3bdd08af,1b5286ee-088d-4f8d-9ec8-7dca98076779
Host: 192.168.1.3:8000
Accept-Encoding: gzip, deflate
Content-Length: 2395
Connection: keep-alive
cache-control: no-cache

mock=%7B%0A%09%22ads%22%3A+%7B%0A%09%09%22medium%22%3A+%22ma%22%2C%0A%09%09%22record_tmpl%22%3A+%22https%3A%2F%2F10.0.2.2%3A8000%2Fevents%2F%7Bmedium%7D%2F1.0%2F%7Brtype%7D%3Fai%3Daae57568-450a-4d45-895f-1f4289bf4331%26ph%3Da51065ab-17ee-4394-b5a7-32debc04780a%26ts%3D%7Btxn_state%7D%22%2C%0A%09%09%22oxt%22%3A+23.753%2C%0A%09%09%22adunits%22%3A+%5B%7B%0A%09%09%09%22auid%22%3A+%22537454411%22%2C%0A%09%09%09%22idx%22%3A+%220%22%2C%0A%09%09%09%22refresh_delay%22%3A+%2210%22%2C%0A%09%09%09%22refresh_max%22%3A+%225%22%2C%0A%09%09%09%22chain_revenue%22%3A+%22%22%2C%0A%09%09%09%22chain%22%3A+%5B%7B%0A%09%09%09%09%22is_fallback%22%3A+0%2C%0A%09%09%09%09%22ad_id%22%3A+%22540857694%22%2C%0A%09%09%09%09%22adv_acct_id%22%3A+%22537137359%22%2C%0A%09%09%09%09%22is_ng%22%3A+1%2C%0A%09%09%09%09%22adv_id%22%3A+%22%3A537137359%22%2C%0A%09%09%09%09%22brand_id%22%3A+%22%22%2C%0A%09%09%09%09%22cpipc%22%3A+0%2C%0A%09%09%09%09%22auct_win_is_deal%22%3A+0%2C%0A%09%09%09%09%22pub_rev%22%3A+%220%22%2C%0A%09%09%09%09%22width%22%3A+%22320%22%2C%0A%09%09%09%09%22height%22%3A+%2250%22%2C%0A%09%09%09%09%22html%22%3A+%22%3Cscript+src%3D%5C%22https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fomsdk-files%2Fcompliance-js%2Fomid-validation-verification-script-v1.js%5C%22%3E%3C%2Fscript%3E%5Cn%3Ca+href%3D%5C%22https%3A%2F%2Fwww.openx.com%2F%5C%22%3E%3Cimg+width%3D%5C%22320%5C%22+height%3D%5C%2250%5C%22+src%3D%5C%22https%3A%2F%2F10.0.2.2%3A8000%2Fimage%3FunitId%3D537454411%5C%22%3E%3C%2Fimg%3E%3C%2Fa%3E%22%2C%0A%09%09%09%09%22target%22%3A+%22_blank%22%2C%0A%09%09%09%09%22ts%22%3A+%222DAABBgABAAECAAIBAAsAAgAAAJkcGApIVzVuVUVsekg5HBbiqpLYkPvW2Z0BFtvWjIDX8NX_qQEAHBaN9u2L9pqN1qEBFq2P0Pjzl5yIhQEAFt7z69oLFQIRACwcFQIAHBUCAAAcJpadx4AEFQ4VBCaQuaaABBaggJyABNYAABwmnsOggAQWotXmgwQWvNXmgwQWutXmgwQVFBwUZBSABQAVBBUKFgAmAEUKAAAA%22%2C%0A%09%09%09%09%22type%22%3A+%22html%22%2C%0A%09%09%09%09%22ad_url%22%3A+%22%3Cscript+src%3D%5C%22https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fomsdk-files%2Fcompliance-js%2Fomid-validation-verification-script-v1.js%5C%22%3E%3C%2Fscript%3E%5Cn%3Ca+href%3D%5C%22https%3A%2F%2Fwww.openx.com%2F%5C%22%3E%3Cimg+width%3D%5C%22320%5C%22+height%3D%5C%2250%5C%22+src%3D%5C%22https%3A%2F%2F10.0.2.2%3A8000%2Fimage%3FunitId%3D537454411%5C%22%3E%3C%2Fimg%3E%3C%2Fa%3E%22%0A%09%09%09%7D%5D%0A%09%09%7D%5D%0A%09%7D%0A%7D&auid=540881524
```

## Get logs

`GET api/logs`

### Params
No params
### Type
`application/x-www-form-urlencoded`

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

## Log any request (events)

Every request sent to this URL will be logged with all the data comes int

`GET/POST events`

### Params
Any number of params
### Type
Any type
### Returns
200 OK HTTP code on success
