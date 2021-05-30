from flask import Flask, request
import subprocess
import os
import time
from scapy.all import *
app = Flask(__name__)
Conncounter = 0
computationDone = 0
data1 = 0
data2 = 0
output = 0
proc_time = 0

def compute():
	global proc_time
	f = open('data1.txt', 'w+')
	f2 = open('data2.txt', 'w+')
	for row in data1['values']:
		f.write(row + '\n')
	for row2 in data2['values']:
		f2.write(row2 + '\n')
	f.close()
	f2.close()
	if data1['alg'] != data2['alg']:
		return
	if int(data1['alg']) == 0:  # Naive hashing
		command1 = '/home/sp/Desktop/PSI/demo.exe -r 0 -p 0 -f data1.txt'
		output1 = subprocess.Popen(command1, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
		command2 = '/home/sp/Desktop/PSI/demo.exe -r 1 -p 0 -f data2.txt'
		t = AsyncSniffer(iface="lo", filter="port 7766")
		time_start=time.time()
		t.start()
		output2 = subprocess.Popen(command2, shell=True, stdout=subprocess.PIPE).stdout.read()
		proc_time = time.time() - time_start
		t.stop()
		print('Computation done in %s' % (proc_time))
		output2 = output2.decode('utf-8') + 'Computation time: ' + str(proc_time) + ' Exchanged data (received and sent): ' + str(len(t.results))
		index = output2.find('Found')
		return output2[index:]
	elif int(data1['alg']) == 2:
		command1 = '/home/sp/Desktop/PSI/demo.exe -r 0 -p 2 -f data1.txt '
		output1 = subprocess.Popen(command1, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
		command2 = '/home/sp/Desktop/PSI/demo.exe -r 1 -p 2 -f data2.txt'
		t = AsyncSniffer(iface="lo", filter="port 7766")
		time_start=time.time()
		t.start()
		output2 = subprocess.Popen(command2, shell=True, stdout=subprocess.PIPE).stdout.read()
		proc_time = time.time() - time_start
		t.stop()
		print('Computation done in %s' % (proc_time))
		output2 = output2.decode('utf-8') + 'Computation time: ' + str(proc_time) + ' Exchanged data (received and sent): ' + str(len(t.results))
		index = output2.find('Found')
		return output2[index:]
	elif int(data1['alg']) == 3:
		command1 = '/home/sp/Desktop/PSI/demo.exe -r 0 -p 3 -f data1.txt'
		output1 = subprocess.Popen(command1, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
		command2 = '/home/sp/Desktop/PSI/demo.exe -r 1 -p 3 -f data2.txt'
		t = AsyncSniffer(iface="lo", filter="port 7766")
		time_start=time.time()
		t.start()
		output2 = subprocess.Popen(command2, shell=True, stdout=subprocess.PIPE).stdout.read()
		proc_time = time.time() - time_start
		t.stop()
		print('Computation done in %s' % (proc_time))
		output2 = output2.decode('utf-8') + 'Computation time: ' + str(proc_time) + ' Exchanged data (received and sent): ' + str(len(t.results))
		index = output2.find('Found')
		return output2[index:]
	else:
		time_start = time.time()
		inter = [value for value in data1['values'] if value in data2['values']]
		proc_time = time.time() - time_start
		output_txt = ""
		for ele in inter:
			output_txt += ele + '\n'
		tamanho_lista = len(inter)
		output_txt = output_txt + 'Number of intersections: ' + str(tamanho_lista) + '\nComputation done in: ' + str(proc_time)
		return output_txt

@app.route('/', methods=['POST'])
def result():
	global Conncounter, data2, data1, output, computationDone
	Conncounter += 1
	if Conncounter == 1:
		data1 = request.json
		return ('Received, waiting on the second party!')
	if Conncounter == 2:
		data2 = request.json
		output = compute()
		computationDone = 1
		return('Received, starting computation!')


@app.route('/', methods=['GET'])
def result2():
	global computationDone, output
	if computationDone == 1:
        	return output
	else:
        	return "Not yet done", 400
@app.route('/flushdata', methods=['GET'])
def clear():
	global computationDone, output, data1, data2, Conncounter, proc_time
	computationDone = 0
	output = 0
	data1 = 0
	data2 = 0
	Conncounter = 0
	proc_time = 0
	return('Data flushed')
