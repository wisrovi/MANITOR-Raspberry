sudo docker build -t "manitor_beacon_scan:latest" "1_baliza_scan"
sudo docker build -t "manitor_reproduce_audio:latest" "2_reproduce_audio"
sudo docker build -t "manitor_send_mqtt:latest" "3_send_mqtt"
sudo docker build -t "manitor_nombre_persona:latest" "4_person_name"

sudo docker build -t "manitor_move_front_cam:latest" "6_move_front_cam"