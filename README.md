# CORS Demos

A simple demo to explore CORS behaviors

## Description

This project spins up a "client" server and an "API" server. These sites operate
on different ports so they will be different origins according to 
[CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS). This
sample shows what types of calls are allowed and which calls end in error.

## Getting Started

### Dependencies

* Python (flask, flask_socketid)
* openssl (for setup)

### Installing

* These examples involve using cookies across different origins. In order to
make Chrome happy, we need to operate over SSL. Follow these steps
to generate a local certificate authority and site certificate.
  ```
  cd certs/
  ./certs.sh
  # you will be promted for a passkey. Make one up
  # and enter it each time you are asked
  ```
* After you create your certificate authority, you will need to trust that
certificate. If you are on a Mac, you can drag the `certificate_authority.pem`
file into your System keychain in the "Keychain Access" app. This will stop
Chrome from warning you about the untructed certificate. After you 
drag it in (it shoud be named `cors.local`), you need to double click on it
and expand the "Trust" section and choose "Always Trust"
* Since the cite uses SSL, it needs a domain name. The site uses `cors.local`
as a host name. You will need to tell your computer to resolve that 
host name to the local host. Typically you can add a line like `cors.local 127.0.0.1`
to your `/etc/hosts` file on a Mac.

### Executing program

Once setup is complete, you will need to launch the two servers
* `python server.py`
* `python client.py`

You should then go to `https://cors.local:8000` to experiment with the demo.


## Version History

* 0.1
    * Initial Release
