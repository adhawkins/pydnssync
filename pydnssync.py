#!/usr/bin/python3

import socket
import ipaddress
from pprint import pprint

hosts = [
	"andy-pc-new",
	"andy-xo",
	"nas",
	"pfsense",
	"synology",
	"twitch-websocket",
	"xcp-dev",
	"xcp-docker-amd",
	"xcp-mailnews",
	"xcp-mbserver-docker",
	"xcp-media",
	"xcp-xo-amd",
	"xcp-xo-tmp",
]

with open('gently.org.uk-internal.txt', 'w') as file:
	for host in hosts:
		try:
			fqdn = f"{host}.gently.org.uk"
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