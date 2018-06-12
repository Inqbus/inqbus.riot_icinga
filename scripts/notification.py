#!/usr/bin/env python3
# coding: utf8

import argparse
import sys

from matrix_client.client import MatrixClient
from matrix_client.room import Room


# CONFIGURATION
# Riot / Matrix Settings
USERNAME = "@name:test.riot.de"
SERVER = "https://test.riot.de:443"
ROOMID = "!room_id:test.riot.de"

# must provide password or token
TOKEN = ""
PASSWORD = ""

# ARGUMENTS

# arguments set by command-config
parser = argparse.ArgumentParser()
command_line_required = {
    # Required parameters:
    '-d': 'LONGDATETIME (\$icinga.long_date_time\$)',
    '-e': 'SERVICENAME (\$service.name\$)',
    '-l': 'HOSTNAME (\$host.name\$)',
    '-n': 'DISPLAYNAME (\$host.display_name\$)',
    '-s': 'SERVICESTATE (\$service.state\$)',
    '-t': 'NOTIFICATIONTYPE (\$notification.type\$)',
    '-u': 'SERVICEDISPLAYNAME (\$service.display_name\$)',
    '-o': 'HOSTOUTPUT (\$host.output\$)',
}
command_line_not_required = {
    '-ip4': 'HOSTADDRESS (\$address\$)',
    '-ip6': 'HOSTADDRESS6 (\$address6\$)',
    '-b': 'NOTIFICATIONAUTHORNAME (\$notification.author\$)',
    '-c': 'NOTIFICATIONCOMMENT (\$notification.comment\$)',
    '-so': 'SERVICEOUTPUT (\$service.output$\)',
}

for x in command_line_required.keys():
    parser.add_argument(x, help=command_line_required[x], required=True)

for x in command_line_not_required.keys():
    parser.add_argument(x, help=command_line_not_required[x], required=False)

args = parser.parse_args()

# MESSAGE GENERARION
# message string
message = u'''{icon} Service: {service_display} is {state}; 
When: {time}; 
Info: {service}; 
Hostname: {host_display}({host}); 
Output: {host_output}'''

# icons
warn_ico=u"⚠"
error_ico=u"❌"
ok_ico=u"🆗"
question_ico=u"❓"

state = args.s.lower()

if state in ['up', 'ok']:
    icon = ok_ico
elif state in ['down', 'critical']:
    icon = error_ico
elif state in ['unknown']:
    icon = question_ico
elif state in ['warning']:
    icon = warn_ico
else:
    icon = ''

message = message.format(
    state=state,
    icon=icon,
    service_display=args.u,
    time=args.d,
    service=args.e,
    host=args.l,
    host_display=args.n,
    host_output=args.o,
)

if args.ip4:
    message += 'IPv4: {ip4}; '.format(ip4=args.ip4)
if args.ip6:
    message += 'IPv6: {ip6}; '.format(ip6=args.ip6)
if args.c:
    message += 'Comment: {c}; '.format(c=args.c)
if args.b:
    message += 'Comment by: {b}; '.format(b=args.b)
if args.so:
    message += 'Service Output: {so}; '.format(so=args.so)

print(message)

# MESSAGE SENDING
if PASSWORD:
    client = MatrixClient(SERVER)
    token = client.login_with_password(USERNAME, PASSWORD)
elif TOKEN:
    client = MatrixClient(SERVER, token=TOKEN, user_id=USERNAME)
else:
    sys.exit(0)

if ROOMID:
    room = Room(client, ROOMID)
    room.send_text(message)