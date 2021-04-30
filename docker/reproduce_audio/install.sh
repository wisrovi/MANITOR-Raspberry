
docker build -t "audio_play:v1" .

docker container  run -d --device /dev/snd --name=test_audio  audio_play:v1
