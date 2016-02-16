<?php

header('content-type: application/json; charset=utf-8');

$hosts = array(
    array(
        'id' => "b21ae08f-2b93-412d-ab46-9da6c84e3495",
        'ip' => array(
            'address' => '192.168.0.1',
            'netmask' => '255.255.255.0',
            'network' => '192.168.0.1'
        ),
        'interfaces' => [
            [
                'desc' => 'eth0',
                'ip' => '192.168.0.1',
                'sys' => 'eth0',
                'netmask' => '255.255.255.0'
            ]
        ],
        'rules' => [],
        'netmask' => '24',
        'name' => 'host 1',
        'htype' => 1
    ),
    array(
        'id' => "e508011e-3484-401d-a3c8-5aa797075f2c",
        'ip' => array(
            'address' => '192.168.0.1',
            'netmask' => '255.255.255.0',
            'network' => '192.168.0.1'
        ),
        'interfaces' => [
            [
                'desc' => 'eth1',
                'ip' => '192.168.1.1',
                'sys' => 'eth0',
                'netmask' => '24'
            ],
            [
                'desc' => 'eth2',
                'ip' => '192.168.2.1',
                'sys' => 'eth2',
                'netmask' => '24'
            ],
            [
                'desc' => 'eth3',
                'ip' => '192.168.3.1',
                'sys' => 'eth3',
                'netmask' => '24'
            ]
        ],
        'rules' => [],
        'netmask' => '24',
        'name' => 'host 2',
        'htype' => 1

    ),
    array(
        'id' => "f3f6565f-1ab2-4d32-b24f-cbd3b798dda1",
        'ip' => array(
            'address' => '192.168.0.1',
            'netmask' => '255.255.255.0',
            'network' => '192.168.0.1'
        ),
        'interfaces' => [
            [
                'sys' => 'eth0',
                'ip' => '192.168.0.1',
                'desc' => 'eth0',
                'netmask' => '255.255.255.0'
            ],
            [
                'desc' => 'eth1',
                'ip' => '192.168.0.2',
                'sys' => 'eth1',
                'netmask' => '24'
            ]
        ],
        'rules' => [],
        'netmask' => '24',
        'name' => 'host 3',
        'htype' => 2

    )
);
$rules = '{ "modules": [ { "sys": "limit", "desc": "Limit incoming packets", "params_available": [ {"sys": "limit", "desc": "N/interval ex. 4/minute"}, {"sys": "limit-burst", "desc": "N ex. 10, temporary enable more than limit"}, ] }, { "sys": "multiport", "desc": "Match multiple ports", "params_available": [ {"sys": "sports", "desc": "source ports: port:post or port,port,port or port:port,port,port"}, {"sys": "dports", "desc": "destination ports: port:post or port,port,port or port:port,port,port"}, {"sys": "ports", "desc": "source or destination ports: port:post or port,port,port or port:port,port,port"}, ] }, { "sys": "state", "desc": "Matching connection state (aliased to conntrack)", "params_available": [ {"sys": "state", "desc": "available: NEW,RELATED,ESTABLISHED,CLOSED"} ] }, { "sys": "tcp", "desc": "TCP, enabled automatically when -p tcp", "params_available": [ {"sys": "sport", "desc": "source port: port or port:port"}, {"sys": "dport", "desc": "destination port: port or port:port"}, {"sys": "tcp-flags", "desc": "flags for tcp. which flags to examined <space> which should be set (ALL=SYN,ACK,FIN,RST,URG,PSH) example: SYN,ACK FIN"}, ] }, { "sys": "udp", "desc": "UDP, enabled automatically when -p udp", "params_available": [ {"sys": "sport", "desc": "source port: port or port:port"}, {"sys": "dport", "desc": "destination port: port or port:port"}, ] }, { "sys": "icmp", "desc": "ICMP, enabled automatically when -p icmp", "params_available": [ {"sys": "icmp-type", "desc": "type of icmp, string or number, ex: echo-request or 8"}, ] }, ] }';

/** As simple as it is */
switch (isset($_GET['endpoint']) ? $_GET['endpoint'] : null) {
    case 'hosts':
        $response = $hosts;
        break;
    case 'rules':
        $response = $rules;
    default:
        $response = json_encode($hosts);
}


echo $response;