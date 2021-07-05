#!/usr/bin/env python3
import sys
from impacket import uuid, version
from impacket.dcerpc.v5 import transport, epm

####################
#
# Title   : print_spool_check.py
# Author  : @Uncle-Fester-69
# Version : 1.0
#
# Takes in a line separated list of hostnames/IP's in "HOSTNAME_FILE" then simply checks the RPC interface to see if PrintSpooler is active.
# Outputs information in CSV compatable format, pipe to a CSV and enjoy.
#
# Credit where due to Authors of impacket for handling the backend magic.
#

HOSTNAME_FILE = "hosts.txt"

def Check_Spooler(remoteHost):
    try:
        stringbinding = "ncacn_ip_tcp:"+remoteHost+"[135]"
        rpctransport = transport.DCERPCTransportFactory(stringbinding)
        dce = rpctransport.get_dce_rpc()
        dce.connect()
        entries = epm.hept_lookup(None, dce=dce)
        dce.disconnect()

        Status = "DISABLED"
        for entry in entries:
            binding = epm.PrintStringBinding(entry['tower']['Floors'])
            tmpUUID = str(entry['tower']['Floors'][0])
            if tmpUUID[:36] in epm.KNOWN_PROTOCOLS and epm.KNOWN_PROTOCOLS[tmpUUID[:36]] == "[MS-RPRN]: Print System Remote Protocol":
                 Status = "ENABLED"
        print("%s, %s" % (remoteHost, Status))

    except Exception as e:
        print("%s, ERROR, %s" % (remoteHost, e))

def main():
    fh = open(HOSTNAME_FILE, 'r')
    Hosts = fh.read().splitlines()

    for host in Hosts:
        Check_Spooler(host)

main()
