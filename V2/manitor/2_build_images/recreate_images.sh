echo ""
echo ""
echo "**************************************************"
sudo docker build -t "manitor_beacon_scan:V1.0" "1_baliza_scan"
echo ""
echo ""
echo "**************************************************"
sudo docker build -t "manitor_reproduce_audio:V1.0" "2_reproduce_audio"
echo ""
echo ""
echo "**************************************************"
sudo docker build -t "manitor_send_mqtt:V1.0" "3_send_mqtt"
echo ""
echo ""
echo "**************************************************"
sudo docker build -t "manitor_nombre_persona:V1.0" "4_person_name"
echo ""
echo ""
echo "**************************************************"
sudo docker build -t "manitor_interfaz_video:V1.0" "5_interfaz_video"
echo ""
echo ""
echo "**************************************************"
sudo docker build -t "manitor_move_front_cam:V1.0" "6_move_front_cam"
echo ""
echo ""
echo "**************************************************"
sudo docker build -t "manitor_vector:V1.0" "7_vector"
echo ""
echo ""
sudo docker build -t "manitor_brain:V1.0" "8_BRAIN"
echo ""
echo ""
echo "**************************************************"