<?php

header('content-type: application/json; charset=utf-8');

$response = array(
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

echo json_encode($response);