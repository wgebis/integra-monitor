## Overview

This is a simple app called as "Integra monitor" for receiving monitoring events from Satel Integra advanced alarm control panel. 
Application is written in Python and can be run as a Flask application. 

## Requirement
 
This software requires the Satel Integra board with ETHM module.
Python requires version >= 3.6. 
Currently the application supports ContactID payloads transferred via SIA packets.
It has been tested with Integra64 board (firmware v.1.17 PL) and ETHM-1 module (firmware v2.02).

Events can be handle in two ways:
* could be forwarded to ElasticSearch database (when `ES_URL` is present in config file),
* and also could be sent as an e-mail message (when `TO_EMAIL` is defined).   

## Running

Integra monitor can be run as regular Flask app:

```
$ export FLASK_APP=integra
$ export FLASK_ENV=development
$ flask run 
```

With the `development` environment, `instance` config should be placed into the `./instance/` directory. On the production, you should place the instance config under `/etc/integra/` directory. 
Content of `./misc` folder:
 * `config.py` - example of instance config
 * `integra-monitor.service` - ready to use systemd descriptor
 * `send.py` - example script which sends sample SIA package with CID payload.
 
## Packaging and installing

Here is `setup.py` configuration for packaging purposes, source distribution should be generated with the following manner:

```
$ python3 setup.py sdist bdist_wheel
```

And then, the source dist can be installed on the target host via `pip`:

```
$ pip3 install integra_monitor-0.0.1-py3-none-any.whl
```

## Links:

* [Satel website](https://www.satel.pl)
* [Integra64 board home](https://www.satel.pl/en/product/85/INTEGRA%2064,Plyta-glowna-centrali-alarmowej-od-16-do-64-wejsc)