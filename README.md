# joojanta200

## Three different docker files, Three different purposes. 

all the dockers need the model.

download TVG_CRFRNN_COCO_VOC.caffemodel model somewhere and pass directory holding it to the container.

```
wget -O TVG_CRFRNN_COCO_VOC.caffemodel http://goo.gl/j7PrPZ 
``` 

### Dockerfile.joojanta200.bulkProcess 

for people that want to remove backgrounds in bulk. 

  Build:
```
  docker build -f Dockerfile.joojanta200.bulkProcess .
```
  Run:
  1. **dirOfInputImages** - directory of images to process
  1. **dirToWriteImages** - directory to write processed images
  1. **dirTo500megModel** - directory containing TVG_CRFRNN_COCO_VOC.caffemodel
  1. **containerid** - containerid from the build

```
  docker run -v /dirOfInputImages:/work/inputImages \
             -v /dirToWriteImages:/work/outputImages \
             -v /dirTo500megModel:/work/model <containerid>
```
  
### Dockerfile.joojanta200.notebook 

jupyter notebook for looking under the covers

The container will spew forth a webpage to go to. replace the 8888 in the webpage with **somePort** 

  Build:

```
  docker build -f Dockerfile.joojanta200.notebook .
```
  Run:
  1. **somePort** - local port to listen on
  1. **dirTo500megModel** - directory containing TVG_CRFRNN_COCO_VOC.caffemodel
  1. **containerid** - containerid from the build

```
  docker run -v /dirTo500megModel:/work/model \
             -p <somePort>:8888 <containerid>
```
### Dockerfile.joojanta200.flask

Simple webapp, user pastes image uri, container downloads image, processes and displays original image over processed image.

  Build:
```
  docker build -f Dockerfile.joojanta200.flask .
``` 
  Run:
  1. **somePort** - local port to listen on
  1. **dirTo500megModel** - directory containing TVG_CRFRNN_COCO_VOC.caffemodel
  1. **containerid** - containerid from the build 

```
  docker run -v /dirTo500megModel:/work/model \
             -p <somePort>:5000 <containerid>
```

### how not to screw things up in the future..
things work with the following versions
  1. https://github.com/BVLC/caffe/tree/master/docker commit 4db619aec9cd384b11a1c55fac257d14b704bb15
  1. https://github.com/torrvision/crfasrnn commit 3b9c6b61e5416d2d38b5c6cdf6f8dcc02fafcc43 [done]
  1. https://github.com/torrvision/caffe commit e7f25fa2bdbb291a067930d60f337d305c128583 [done]
  1. TVG_CRFRNN_COCO_VOC.caffemodel bc4926ad00ecc9a1c627db82377ecf56  (md5sum)
