# PlantCV
Dockerfile (Ubuntu, gedit, wget, git, PlantCV with examples)

The aim of this repository is to prepare a docker image for running [PlantCV](http://plantcv.readthedocs.io/en/latest/).

**The following procedures are for Ubuntu 16.04 with Docker 17.12.0-ce installed**

In the terminal:
```
sudo chmod u+x PlantCV_build.sh
sudo chmod u+x PlantCV_X11.sh 

#Create a docker image plant_cv
./PlantCV_build.sh 

#Create a container PlantCV using the docker image plant_cv
./PlantCV_X11.sh 
```
**The following procedures are for macOS 10.13.3 with Docker 17.12.0-ce installed**

[XQuartz](https://www.xquartz.org/): Preferences -> Security -> (Check) Allow connections from network clients

In the terminal:
```
sudo chmod u+x PlantCV_build.sh
sudo chmod u+x PlantCV_XQuartz.sh 

#Create a docker image plant_cv
./PlantCV_build.sh 

#Create a container PlantCV using the docker image plant_cv
./PlantCV_XQuartz.sh 
```
**The following procedures are for running [Tutorial: VIS Image Pipeline](http://plantcv.readthedocs.io/en/latest/vis_tutorial/)**. 

Inside the container: 
```
#Download the sample image from the tutorial
wget http://plantcv.readthedocs.io/en/latest/img/tutorial_images/vis/original_image.jpg -O /workspace/examples/input/sample0.jpg

#Run the VIS Pipeline tutorial
cd /workspace/examples
python vis_tutorial.py -i ./input/sample0.jpg -o ./output -r result.txt -w True
```
Outcomes are stored in ```/workspace/examples/output```.

To exit the container, type ```exit```.
