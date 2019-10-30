## Installation

In order to use and install this server you need to have a **Python 3**

Additional libraries are required:

```
pip install Django Pillow django-extensions Werkzeug pyOpenSSL
```

After this navigate to your clone project folder and run:
`python3 manage.py runserver_plus --cert-file example.crt`

where example.crt is your generated certificate for your IP address or host. 

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

where example.com is your domain, and 10.0.0.1 is your IP. You remove not needed. After this you can use example.crt with your server
