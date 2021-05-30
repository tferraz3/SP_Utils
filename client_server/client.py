import csv
import argparse
import requests
import json
import time

parser=argparse.ArgumentParser()
parser.add_argument("file")
parser.add_argument("pos")
parser.add_argument("srv")
parser.add_argument("alg")
args = parser.parse_args()

srv='http://' + args.srv + ':5000/'
f=open(args.file)
csv_f = csv.reader(f, delimiter=';')
fields = []
dict = {}
for row in csv_f:
	fields.append(row[int(args.pos)])
fields.pop(0)
dict["values"] = fields
dict["alg"] = args.alg
print('Connecting to ' + srv)
r = requests.post(srv, json= dict, timeout=60)
if r.ok:
	print('Request sent, entering polling mode!')
else:
	print(str(r))
while(1):
	r = requests.get(srv)
	if r.ok:
	   print('Computation done, printing result')
	   print(r.content.decode("utf-8"))
	   print('Clearing data')
	   time. sleep(5)
	   srv= 'http://' + args.srv + ':5000/flushdata'
	   r = requests.get(srv)
	   exit()
	else:
	   time.sleep(2)



		
