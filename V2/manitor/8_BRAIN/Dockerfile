FROM arm32v7/python:3.6.13-buster

WORKDIR /code_video

RUN echo brain

RUN pip3 install requests

# 6) copiamos la carpeta del codigo y todos sus recursos
COPY src .

RUN chmod -R +777 /code_video

# CMD ["tail","-f","/dev/null"]
CMD ["python3", "./service.py" ]
