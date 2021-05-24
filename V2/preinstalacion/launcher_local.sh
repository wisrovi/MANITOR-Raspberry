cd 1_baliza_scan/src/
sudo nohup python3 service.py &

cd ../../2_reproduce_audio/src
nohup python3 service.py &

cd ../../3_send_mqtt/src
nohup python3 service.py &

cd ../../4_person_name/src
nohup python3 service.py &

cd ../../5_interfaz_video/src
nohup python3 service.py &

cd ../../6_move_front_cam/src
nohup python3 service.py &

cd ../../7_vector/src
nohup python3 service.py &