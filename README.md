# FwGen
* [backend] @rikkt0r, grzegorz-wojcicki@outlook.com
* [frontend] @castoridae,  snajqer@gmail.com


## Before running our tool
check available modules
```bash
cat /proc/net/ip_tables_matches
```

check available actions
```bash
cat /proc/net/ip_tables_targets
```

also consider running the following for greater profit~~
```bash
echo 1 > /proc/sys/net/ipv4/tcp_syncookies
echo 1 > /proc/sys/net/ipv4/ip_forward
echo 1 > /proc/sys/net/ipv4/icmp_echo_ignore_broadcasts
# log packets from incorrect sources
echo 1 > /proc/sys/net/ipv4/conf/all/log_martians
echo 1 > /proc/sys/net/ipv4/icmp_ignore_bogus_error_responses
# source validation by reversed path (RFC1812)
echo 1 > /proc/sys/net/ipv4/conf/all/rp_filter 
echo 0 > /proc/sys/net/ipv4/conf/all/send_redirects
echo 0 > /proc/sys/net/ipv4/conf/all/accept_source_route
echo 1 > /proc/sys/net/ipv4/conf/all/secure_redirects
# dynamic address allocation
echo 1 > /proc/sys/net/ipv4/ip_dynaddr 
```

### Run:

* apt-get install mongodb // brew install mongodb
* $mongo:
```mongo
use iptables
db.addUser({'user': 'iptables', 'pwd': 'iptables_pass', roles: ['readWrite', 'dbAdmin']})
```
* $bash (import data):
```bash
mongoimport --db iptables --collection module_available --drop --file dataset_modules_available.json
mongoimport --db iptables --collection module --drop --file dataset_modules.json
mongoimport --db iptables --collection rule --drop --file dataset_rules.json
mongoimport --db iptables --collection template --drop --file dataset_templates.json
```
* python virtualenv:
```sh
virtualenv env
. env/bin/activate
pip install -r requirements.txt
python server/manage.py runserver 5000
```


# API

## W skrocie

* /api/hosts/ GET
* /api/hosts/[uuid4_host_id]/ POST
* /api/hosts/[uuid4_host_id]/ PUT
* /api/hosts/[uuid4_host_id]/ DELETE

* /api/hosts/[uuid4_host_id]/generate/iptables/ GET
* /api/hosts/[uuid4_host_id]/rules/ GET
* /api/hosts/[uuid4_host_id]/rules/ POST
* /api/hosts/[uuid4_host_id]/rules/[uuid4_rule_id]/ PUT
* /api/hosts/[uuid4_host_id]/rules/[uuid4_rule_id]/ DELETE
* /api/hosts/[uuid4_host_id]/rules/[uuid4_rule_id]/up/ POST (yup, we are implementing that..)
* /api/hosts/[uuid4_host_id]/rules/[uuid4_rule_id]/down/ POST

* /api/available/modules/ GET
* /api/available/chains/ GET
* /api/available/tables/ GET
* /api/available/actions/ GET
* /api/available/loglevels/ GET
* /api/available/templates/ GET
* /api/available/templates/[uuid4_template_id]/ GET

## >>> Hosts <<<

#### GET /api/hosts/
Request, no data

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
      "template_name": "template name",
      "rule_count": 14
    },
    {
      "id": "e508011e-3484-401d-a3c8-5aa797075f2c",
      "htype": 1
      "name": "Some host 2",
      "interfaces": [
        {"sys": "eth0", "desc": "gigabitowy realtek", "ip": "12.11.10.1", "netmask": 24},
        {"sys": "eth1", "desc": "gigabitowy realtek 2", "ip": "12.11.5.1", "netmask": 24},
      ],
      "template_name": "template name",
      "rule_count": 30
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
    {"sys": "eth0", "desc": "gigabit realtek", "ip": "12.11.10.1", "netmask": 24},
    {"sys": "wlan0", "desc": "wireless atheros 2k", "ip": "12.11.9.1", "netmask": 24},
  ]
}
```
Response
```json
{
  "id": "3fde83f0-3c57-42a0-bad6-7573e1313317"
}
```

#### PUT /api/hosts/[uuid4_host_id]/
Request, any field from POST, ex.
```json
{
  "name": "Another host name"
}
```
or
```json
{
  "interfaces": [{"sys": "brt0", "desc": "fastethernet intel", "ip": "12.11.10.1", "netmask": 24},]
}
```
Response, no data

#### DELETE /api/hosts/[uuid4_host_id]/
Request, no data

Response, no data

## >>> Available <<<
#### GET /api/available/modules/
Request, no data

Response
```json
{
  "modules": [
    {
      "sys": "limit",
      "desc": "Limit incoming packets",
      "params": [
        {"sys": "limit", "desc": "N/interval ex.  4/minute"},
        {"sys": "limit-burst", "desc": "N ex. 10, temporary enable more than limit"},
      ]
    },
    {
      "sys": "multiport",
      "desc": "Match multiple ports",
      "params": [
        {"sys": "sports", "desc": "source ports: port:post or port,port,port or port:port,port,port"},
        {"sys": "dports", "desc": "destination ports: port:post or port,port,port or port:port,port,port"},
        {"sys": "ports", "desc": "source or destination ports: port:post or port,port,port or port:port,port,port"},
      ]
    },
    {
      "sys": "state",
      "desc": "Matching connection state (aliased to conntrack)",
      "params": [
        {"sys": "state", "desc": "available: NEW,RELATED,ESTABLISHED,CLOSED"}
      ]
    },
    {
      "sys": "tcp",
      "desc": "TCP, enabled automatically when -p tcp",
      "params": [
        {"sys": "sport", "desc": "source port:  port or port:port"},
        {"sys": "dport", "desc": "destination port:  port or port:port"},
        {"sys": "tcp-flags", "desc": "flags for tcp. which flags to examined <space> which should be set (ALL=SYN,ACK,FIN,RST,URG,PSH)  example: SYN,ACK FIN"},
      ]
    },
    {
      "sys": "udp",
      "desc": "UDP, enabled automatically when -p udp",
      "params": [
        {"sys": "sport", "desc": "source port:  port or port:port"},
        {"sys": "dport", "desc": "destination port:  port or port:port"},
      ]
    },
    {
      "sys": "icmp",
      "desc": "ICMP, enabled automatically when -p icmp",
      "params": [
        {"sys": "icmp-type", "desc": "type of icmp, string or number, ex: echo-request or 8"},
      ]
    },
  ]
}
```

#### GET /api/available/chains/
Request, no data

Response (if advanced==true, only available in advanced mode),
no custom chains in this revision.
```json
{
  "chains": [
    {"sys": "INPUT", "advanced": false},
    {"sys": "OUTPUT", "advanced": false},
    {"sys": "FORWARDING", "advanced": true},
    {"sys": "PREROUTING", "advanced": true},
    {"sys": "POSTROUTING", "advanced": true},
  ]
}
```
#### GET /api/available/tables/
Request, no data

Response
```json
{
  "tables": [
    {"sys": "filter", "advanced": false},
    {"sys": "mangle", "advanced": true},
    {"sys": "nat", "advanced": true},
    {"sys": "raw", "advanced": true},
    {"sys": "security", "advanced": true},
  ]
}
```

#### GET /api/available/actions/
Request, no data

Response
```json
{
  "actions": [
    {"sys": "DROP", "advanced": false},
    {"sys": "ACCEPT", "advanced": false},
    {"sys": "REJECT", "advanced": false},
    {"sys": "MASQUERADE", "advanced": true},
  ]
}
```

#### GET /api/available/loglevels/
Request, no data
LOG_LEVELS = (
    (0, 'Emergency'),
    (1, 'Alert'),
    (2, 'Critical'),
    (3, 'Error'),
    (4, 'Warning'),
    (5, 'Notice'),
    (6, 'Informational'),
    (7, 'Debug'),
)

Response
```json
{
  "loglevels": [
    {"Emergency": 0},
    {"Alert": 1},
    {"Critical": 2},
    {"Error": 3},
    {"Warning": 4},
    {"Notice": 5},
    {"Informational": 6},
    {"Debug": 7},
  ]
}
```

#### GET /api/available/templates/
Request, no data

Response
```json
{
  "templates": [
    {"id": "bc06c2e6-ccb9-481b-9363-2e20b0a46258", "name": "All-negation", "desc": "All packets on input/output dropped by default"},
    {"id": "5837272e-80cc-4534-a10b-fb4ace090813", "name": "All-ok", "desc": "All packets on input/output accepted by default"},
  ]
}
```

## >>> Rules <<<
#### GET * /api/hosts/[uuid4_host_id]/generate/iptables/
Request, no data

Response, list of iptables commands.
```json
{
  "lines": [
     "iptables -A INPUT -i lo -j ACCEPT",
     "iptables -A INPUT -f -m limit --limit 5/m --limit-burst 7 -j LOG --log-level 4 --log-prefix \"Fragments Packets: \"",
     "iptables -A INPUT -f -j DROP"
  ]
}
```



#### GET /api/hosts/[uuid4_host_id]/rules/
Request, no data

Response
```json
{
  "rules": [
    {
      "id": "ca00049a-8348-4a53-b044-de0047a5de22",
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
        {"sys": "state", "params": [
          {"sys": "state", "value": "RELATED,ESTABLISHED"},
        ]},
      ],
      "action": "LOG",
      "log_level": 4,
      "log_prefix": "Log established"
    }
  ]
}
```

#### POST /api/hosts/[uuid4_host_id]/rules/
Request, any field from GET above(excluding id), table, chain and action are required
```json
{
  "table": "filter",
  "chain": "INPUT",
  "protocol": "tcp",
  "modules": [
    {"sys": "state", "params": [
      {"sys": "state", "value": "RELATED,ESTABLISHED"},
    ]},
  ],
  "action": "DROP"
}
```

Response
```json
{
    "id": "69a5d1d7-1d29-4b07-a6b0-af8034e7849d"
}
```

#### PUT /api/hosts/[uuid4_host_id]/rules/[uuid4_rule_id]/
Request, any field from GET above(excluding id)
```json
{
  "protocol_reverse": true,
}
```

Response, no data

#### DELETE /api/hosts/[uuid4_host_id]/rules/[uuid4_rule_id]/
Request, no data

Response, no data

#### POST /api/hosts/[uuid4_host_id]/rules/[uuid4_rule_id]/up/
Request, no data

Response, no data

#### POST /api/hosts/[uuid4_host_id]/rules/[uuid4_rule_id]/down/
Request, no data

Response, no data
