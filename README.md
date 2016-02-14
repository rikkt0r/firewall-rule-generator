# FwGen
* [backend] Grzegorz Wójcicki, grzegorz-wojcicki@outlook.com
* [frontend] Kamil Kopczyk,  snajqer@gmail.com


## TODO:

* everything

### Run:

* apt-get install mongodb // brew install mongodb
* @mongo CLI:
```mongo
use iptables
db.addUser({'user': 'iptables', 'pwd': 'iptables_pass', roles: ['readWrite', 'dbAdmin']})
```
* python virtualenv:
```sh
virtualenv env
. env/bin/activate
pip install -r requirements.txt
python server/manage.py runserver 5000
```


# API

## >>> Hosts <<<

#### GET /api/hosts/
Request
```json
{}
```

Response
```json
{
  "hosts": [
    {
      "id": "d4b96f81-23b5-48db-9892-4e5db63ca1c5",
      "htype": 3
      "name": "Some host 1",
      "interfaces_count": 2,
      "template_name": "template name"
    },
    {
      "id": "e508011e-3484-401d-a3c8-5aa797075f2c",
      "htype": 1
      "name": "Some host 2",
      "interfaces_count": 1,
      "template_name": "template name"
    }
  ]
}
```


#### POST /api/hosts/
Request
```json
{
  "name": "Host name",
  "htype": 3,
  "template_id": 1,
  "interfaces": [
    {"sys": "eth0", "desc": "gigabitowy realtek", "ip": "12.11.10.1", "netmask": 24},
    {"sys": "wlan0", "desc": "bezprzewodowe cudo", "ip": "12.11.9.1", "netmask": 24},
  ]
}
```

Response
```json
{}
```

## >>> Rules <<<
#### GET /api/hosts/[host_id_w_uuid4]/rules
