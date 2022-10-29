#!/usr/bin/python3

import socket
import ipaddress
import argparse

parser = argparse.ArgumentParser(description='Lookup a list of hosts and generate a TinyDNS configuration file with their addresses')
parser.add_argument('--hosts', metavar='host', nargs='+', help='Host names to look up', required = True)
parser.add_argument('--domain', '-d', help='Domain to append to each host', required = True)
parser.add_argument('--outfile', '-o', help='Output file name', required = True)

args = parser.parse_args()

with open(args.outfile, 'w') as file:
	for host in args.hosts:
		try:
			fqdn = f"{host}.{args.domain}"
			addresses = socket.getaddrinfo(fqdn, 80, type = socket.SOCK_STREAM)
			for (family, type, proto, canonname, sockaddr) in addresses:
				address = ipaddress.ip_address(sockaddr[0])

				if family == socket.AF_INET6:
					file.write(f"6{fqdn}:{address.exploded.replace(':', '')}:300\n")
				elif family == socket.AF_INET:
					file.write(f"+{fqdn}:{address}:300\n")
				else:
					print(f"Unexpected family: '{family}'")
		except socket.gaierror as e:
			print(f"{host}:'{e}'")