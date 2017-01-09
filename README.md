# ccurl

        __     __  __ __  ____   _
       /  ]   /  ]|  |  ||    \ | |
      /  /   /  / |  |  ||  D  )| |
     /  /   /  /  |  |  ||    / | |___
    /   \_ /   \_ |  :  ||    \ |     |
    \     |\     ||     ||  .  \|     |
     \____| \____| \__,_||__|\_||_____|

			*-Configurable Curl-*

Ccurl is a simple application that can be used to cURL APIs using a configuration file.
The configuration file can be used to maintain a set of commonly uses data such as
the base url, different set of headers etc. Along with this there are a few niche features
of CcURL that would help in testing a REST API.

Underneath, it a wrapper for python requests, that takes in a config file to
simplify `curling` REST URLs If you are thinking of using this tool, be warned this
is an alpha stage code, that uses things like eval to execute injected python code,
which can be a security issue in some situations. Only use this tool if you really
know what you are doing and to test an API you have prior permission to test.

## Configuration

Below is a sample configuration that can be used to intitiate ccurling.

    [Defaults]
    accept_type = application/json
    content_type = application/json
    content_length=0
    auth_token=your_token #  if needed
    base_url = https://localhost:80/

A sample configuration file `ccurl.conf` has been provided with the repo.

## Usage

### Basic usage

If you want to ccurl `https://localhost:80/cgi-bin/items.php` you just need:

```
./ccurl.py -r /cgi-bin/items.php
```
ccurl.py will read the `base_url` and other header information provided
in the config file ccurl.conf (by default) in the same directory as you
are running ccurl.py. If you want to provide a seperate directory you coulr
do so using:

#### Example

```
./ccurl.py -c config_file.conf -r /cgi-bin/items.php

```

You can also provide the HTTP verb (by default ccurl intiates a GET request)
using:

#### Example
```
./ccurl.py -r /cgi-bin/items.php -X HEAD
```

Available verbs are HEAD, GET, PUT, POST and DELETE.

### Advanced usage

Beyond these straight forward usage, there are some some special features
of ccurl that would fit certain usecases very well.

Consider you are testing and application, or that you need to upload a specially
crafted file to a particular API. Traditionally you would create a file using
some bash script / python code or someway simlar and then upload the file.
With ccurl you can use the option `--payload` to give a piece of code, that
would be evaluated on the fly by the app and send the URL.

#### Example
```
./ccurl.py -r /cgi-bin/upload.php --payload "eval: '\x0' * 100 * 2 ** 20"
```

For a single use, it might not seem that helpful, but if you would need to fuzz the
application with a set of crafted values, this can be very helpful in  quickly
testing out tiny one liners. This feature is experimetnal and should be used
only if you are permitted by the application owner to test the API in such a way.

For a more complete use case of this feature, refer to the repo on [attack_payloads](https://github.com/rahulunair/attack_payloads
"attack_payloads") which was used to test few OpenStack swift APIs.

You could provided additional headers as well using the -H option of ccurl,

#### Example
```
./ccurl.py -r /cgi-bin/upload.php -H {'meta-name': 'meta-value'}
```

### Debugging

To debug ccurl, you can use the `-d` switch and it will printout the raw curl
command with all the supplied parameters and a few other details.


As of now, this tool does some cool things, that is specially tailored to test APIs.
