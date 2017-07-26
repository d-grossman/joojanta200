# joojanta200

Named after the glasses worn by [Zaphod Beeblebrox in Hitch hikers guide to the galaxy](http://hitchhikers.wikia.com/wiki/Joo_Janta_200_Super-Chromatic_Peril_Sensitive_Sunglasses).  

The project utilizes [CRF as RNN model](http://www.robots.ox.ac.uk/~szheng/papers/CRFasRNN.pdf) to assign labels to pixels.  The demo preserves pixels assigned to people while blacking out all other labels. (Think of it as automating background removal around people)

## Three different docker files, Three different purposes. 

all the dockers need the model.  The docker containers appear to be memory pigs during inference. I havent tested the lower bounds of their memory lust, but >= 4Gig ram makes things run smoothly.

download TVG_CRFRNN_COCO_VOC.caffemodel model somewhere and pass directory holding it to the container.

```
wget -O TVG_CRFRNN_COCO_VOC.caffemodel http://goo.gl/j7PrPZ 
``` 

### Dockerfile.joojanta200.bulkProcess 

for people that want to remove backgrounds in bulk. 

  Build:
```
  docker build -t jj.bulk -f Dockerfile.joojanta200.bulkProcess .
```
  Run:
  1. **dirOfInputImages** - directory of images to process
  1. **dirToWriteImages** - directory to write processed images
  1. **dirTo500megModel** - directory containing TVG_CRFRNN_COCO_VOC.caffemodel
  1. **containerid** - containerid from the build

```
  docker run -v /dirOfInputImages:/work/inputImages \
             -v /dirToWriteImages:/work/outputImages \
             -v /dirTo500megModel:/work/model jj.bulk
```
  
### Dockerfile.joojanta200.notebook 

jupyter notebook for looking under the covers

The container will spew forth a webpage to go to. replace the 8888 in the webpage with **somePort** 

  Build:

```
  docker build -t jj.notebook -f Dockerfile.joojanta200.notebook .
```
  Run:
  1. **somePort** - local port to listen on
  1. **dirTo500megModel** - directory containing TVG_CRFRNN_COCO_VOC.caffemodel
  1. **containerid** - containerid from the build

```
  docker run -v /dirTo500megModel:/work/model \
             -p <somePort>:8888 jj.notebook
```
### Dockerfile.joojanta200.flask

Simple webapp, user pastes image uri, container downloads image, processes and displays original image over processed image.

  Build:
```
  docker build -t jj.flask -f Dockerfile.joojanta200.flask .
``` 
  Run:
  1. **somePort** - local port to listen on
  1. **dirTo500megModel** - directory containing TVG_CRFRNN_COCO_VOC.caffemodel
  1. **containerid** - containerid from the build 

```
  docker run -v /dirTo500megModel:/work/model \
             -p <somePort>:5000 jj.flask
```

### how not to screw things up in the future..
things work with the following versions
  1. https://github.com/BVLC/caffe/tree/master/docker commit 4db619aec9cd384b11a1c55fac257d14b704bb15
  1. https://github.com/torrvision/crfasrnn commit 3b9c6b61e5416d2d38b5c6cdf6f8dcc02fafcc43 [done]
  1. https://github.com/torrvision/caffe commit e7f25fa2bdbb291a067930d60f337d305c128583 [done]
  1. TVG_CRFRNN_COCO_VOC.caffemodel bc4926ad00ecc9a1c627db82377ecf56  (md5sum)
