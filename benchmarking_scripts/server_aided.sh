#!/bin/bash
tshark -i enp0s8 -a duration:10 >> pcap.txt &
sleep 3 
time ./demo.exe -r 0 -p 1 -f empty.txt -a 192.168.1.1 >> output.txt
sleep 10
echo 'Exchanged packets'
cat pcap.txt | grep '7766' | wc -l
cat output.txt | grep 'Found'
rm pcap.txt
rm output.txt
