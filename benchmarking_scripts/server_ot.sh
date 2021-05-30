#!/bin/bash
awk -F "\"*;\"*" '{print $6}' $1 | tail -n +2 >> test_parsed.txt
tshark -i enp0s8 -a duration:10 >> pcap.txt &
sleep 3
time ./demo.exe -r 0 -p 3 -a 192.168.1.3 -f test_parsed.txt >> output.txt
sleep 10
echo 'Sent packets \n'
cat pcap.txt | grep '→ 7766' | wc -l
echo 'Received packets \n'
cat pcap.txt | grep '7766 → ' | wc -l
cat output.txt | grep 'Found'
rm pcap.txt
rm test_parsed.txt
rm output.txt
