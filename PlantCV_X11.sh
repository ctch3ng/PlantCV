#!/bin/bash

sudo docker run -it \
    --user=$(id -u) \
    --env="DISPLAY" \
    --volume="/home/$USER:/home/$USER" \
    --volume="/etc/group:/etc/group:ro" \
    --volume="/etc/passwd:/etc/passwd:ro" \
    --volume="/etc/shadow:/etc/shadow:ro" \
    --volume="/etc/sudoers.d:/etc/sudoers.d:ro" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --volume="$(pwd)/examples:/workspace/examples:rw" \
    --name PlantCV \
    plant_cv

sudo docker rm /PlantCV