# joojanta200

## Two different docker files, two different purposes. 

### Dockerfile.joojanta200.bulkProcess 

for people that want to remove backgrounds in bulk. fill **dirOfInputImages** with files that you want background removal. Output files will appear in **dirToWriteImages**

download TVG_CRFRNN_COCO_VOC.caffemodel  model somewhere and pass directory holding it to the container.
```
wget -O TVG_CRFRNN_COCO_VOC.caffemodel http://goo.gl/j7PrPZ 
``` 
  Build:
```
  docker build -f Dockerfile.joojanta200.bulkProcess .
```
  Run:
```
  docker run -v /dirOfInputImages:/work/inputImages \
             -v /dirToWriteImages:/work/outputImages \
             -v /dir/to/500megModel:/work/model 
```
  
### Dockerfile.joojanta200.notebook 

jupyter notebook for looking under the covers

assign **somePort** to an unused port on your machine.  The container will spew forth a webpage to go to. replace the 8888 in the webpage with **somePort** 

  Build:
```
  docker build -f Dockerfile.joojanta200.notebook .
```
  Run:
```
  docker run -v /dir/to/500megModel:/work/model \
             -p<somePort>:8888 <containerid>
```

### how not to screw things up in the future..
things work with the following versions
  1. https://github.com/BVLC/caffe/tree/master/docker commit 4db619aec9cd384b11a1c55fac257d14b704bb15
  1. https://github.com/torrvision/crfasrnn commit 3b9c6b61e5416d2d38b5c6cdf6f8dcc02fafcc43 [done]
  1. https://github.com/torrvision/caffe commit e7f25fa2bdbb291a067930d60f337d305c128583 [done]
