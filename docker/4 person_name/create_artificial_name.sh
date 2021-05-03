var=$(cat /sys/class/net/eth0/address)

curl http://localhost:5003/send?msg=WilliamRodriguez&topic=/SPINPLM/manitor/$var/nombre