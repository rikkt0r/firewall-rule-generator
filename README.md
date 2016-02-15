# FwGen
* [backend] @rikkt0r, grzegorz-wojcicki@outlook.com
* [frontend] @castoridae,  snajqer@gmail.com


## TODO:

* everything

### Run:

* apt-get install mongodb // brew install mongodb
* mongo CLI:
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
      "interfaces": [
        {"sys": "eth0", "desc": "100mbps realtek", "ip": "1.2.3.1", "netmask": 28},
        {"sys": "eth1", "desc": "gigabitowy realtek", "ip": "1.2.4.133", "netmask": 24},
      ],
      "template_name": "template name"
    },
    {
      "id": "e508011e-3484-401d-a3c8-5aa797075f2c",
      "htype": 1
      "name": "Some host 2",
      "interfaces": [
        {"sys": "eth0", "desc": "gigabitowy realtek", "ip": "12.11.10.1", "netmask": 24},
        {"sys": "eth1", "desc": "gigabitowy realtek 2", "ip": "12.11.5.1", "netmask": 24},
      ],
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

## >>> Modules <<<
#### GET /api/modules/available/
Response
```json
{
  "modules": [
    {
      "sys": "limit",
      "desc": "Limit incoming packets",
      "params_available": [
        {"sys": "limit", "desc": "N/interval ex.  4/minute"},
        {"sys": "limit-burst", "desc": "N ex. 10, temporary enable more than limit"},
      ]
    },
    {
      "sys": "multiport",
      "desc": "Match multiple ports",
      "params_available": [
        {"sys": "sports", "desc": "source ports: port:post or port,port,port or port:port,port,port"},
        {"sys": "dports", "desc": "destination ports: port:post or port,port,port or port:port,port,port"},
        {"sys": "ports", "desc": "source or destination ports: port:post or port,port,port or port:port,port,port"},
      ]
    },
    {
      "sys": "state",
      "desc": "Matching connection state (aliased to conntrack)",
      "params_available": [
        {"sys": "state", "desc": "available: NEW,RELATED,ESTABLISHED,CLOSED"}
      ]
    },
    {
      "sys": "tcp",
      "desc": "TCP, enabled automatically when -p tcp",
      "params_available": [
        {"sys": "sport", "desc": "source port:  port or port:port"},
        {"sys": "dport", "desc": "destination port:  port or port:port"},
        {"sys": "tcp-flags", "desc": "flags for tcp. which flags to examined <space> which should be set (ALL=SYN,ACK,FIN,RST,URG,PSH)  example: SYN,ACK FIN"},
      ]
    },
    {
      "sys": "udp",
      "desc": "UDP, enabled automatically when -p udp",
      "params_available": [
        {"sys": "sport", "desc": "source port:  port or port:port"},
        {"sys": "dport", "desc": "destination port:  port or port:port"},
      ]
    },
    {
      "sys": "icmp",
      "desc": "ICMP, enabled automatically when -p icmp",
      "params_available": [
        {"sys": "icmp-type", "desc": "type of icmp, string or number, ex: echo-request or 8"},
      ]
    },
  ]
}
```

## >>> Rules <<<
#### GET /api/hosts/[host_id_w_uuid4]/rules
Response
```json
{
  "rules": [
    {
      "table": "filter",
      "chain": "INPUT",
      "protocol": "tcp",
      "protocol_reverse": 0,
      "source": null,
      "source_mask": null,
      "source_reverse": 0,
      "destination": null,
      "destination_mask": null,
      "destination_reverse": 0,
      "interface_in": "eth0",
      "interface_in_reverse": 0,
      "interface_out": null,
      "interface_out_reverse": 0,
      "fragment": null,
      "counter": "bytes",
      "modules": [
        {"sys": "state", "params_set": [
          {"sys": "state", "value": "RELATED,ESTABLISHED"},
        ]},
      ],
      "action": "DROP"
    }
  ]
}
```
