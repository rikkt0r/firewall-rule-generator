# coding: utf-8
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv4_address


def validate_ip_bool(address):
    try:

        validate_ipv4_address(address)
        return True
    except ValidationError:
        return False


def validate_ip(address):
    validate_ipv4_address(address)


def validate_netmask(netmask):
    if netmask is not None and not 32 >= netmask >= 0:
        raise ValidationError('Netmask is not valid')
