cd 1_baliza_scan/src/
sudo nohup python3 service.py &

cd ../../2_reproduce_audio/src
nohup python3 service.py &

cd ../../3_send_mqtt/src
nohup python3 service.py &

cd ../../4_person_name/src
nohup python3 service.py &