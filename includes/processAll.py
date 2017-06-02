#!/usr/bin/env python
# coding: utf-8

"""
This package contains code for the "CRF-RNN" semantic image segmentation method, published in the
ICCV 2015 paper Conditional Random Fields as Recurrent Neural Networks. Our software is built on
top of the Caffe deep learning library.

Contact:
Shuai Zheng (szheng@robots.ox.ac.uk), Sadeep Jayasumana (sadeep@robots.ox.ac.uk), Bernardino Romera-Paredes (bernard@robots.ox.ac.uk)

Supervisor:
Philip Torr (philip.torr@eng.ox.ac.uk)

For more information about CRF-RNN, please vist the project website http://crfasrnn.torr.vision.
"""

import sys
import time
import getopt
import os
import numpy as np
from PIL import Image as PILImage

# Path of the Caffe installation.
_CAFFE_ROOT = "/work/crfasrnn/caffe"

# Model definition and model file paths
_MODEL_DEF_FILE = "/work/crfasrnn/python-scripts/TVG_CRFRNN_new_deploy.prototxt.dg"  # Contains the network definition
_MODEL_FILE = "/work/model/TVG_CRFRNN_COCO_VOC.caffemodel"  # Contains the trained weights. Download from http://goo.gl/j7PrPZ

sys.path.insert(0, _CAFFE_ROOT + "/python")
sys.path.insert(0, _CAFFE_ROOT + "/python/caffe")
import os

os.environ['PYCAFFE_ROOT'] = _CAFFE_ROOT
os.environ['CAFFE_ROOT'] = _CAFFE_ROOT
os.environ['PYTHONPATH'] = _CAFFE_ROOT + "/python"
os.environ['CAFFE_ROOT'] = _CAFFE_ROOT
os.environ['PATH'] = '/work/crfasrnn/caffe/build/tools:/work/crfasrnn/caffe/python:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'

import caffe

_MAX_DIM = 500

def apply_mask(img,mask,color):
    len_x = mask.shape[0]
    len_y = mask.shape[1]
    for x in range(len_x):
        for y in range(len_y):
            if mask[x,y] != color:
                img[x,y][0] = 0
                img[x,y][1] = 0
                img[x,y][2] = 0
    return img


def get_palette(num_cls):
    """ Returns the color map for visualizing the segmentation mask.

    Args:
        num_cls: Number of classes

    Returns:
        The color map
    """

    n = num_cls
    palette = [0] * (n * 3)
    for j in xrange(0, n):
        lab = j
        palette[j * 3 + 0] = 0
        palette[j * 3 + 1] = 0
        palette[j * 3 + 2] = 0
        i = 0
        while lab:
            palette[j * 3 + 0] |= (((lab >> 0) & 1) << (7 - i))
            palette[j * 3 + 1] |= (((lab >> 1) & 1) << (7 - i))
            palette[j * 3 + 2] |= (((lab >> 2) & 1) << (7 - i))
            i += 1
            lab >>= 3
    return palette


def crfrnn_segmenter(model_def_file, model_file, gpu_device, inputs):
    """ Returns the segmentation of the given image.

    Args:
        model_def_file: File path of the Caffe model definition prototxt file
        model_file: File path of the trained model file (contains trained weights)
        gpu_device: ID of the GPU device. If using the CPU, set this to -1
        inputs: List of images to be segmented 

    Returns:
        The segmented image
    """
    
    assert os.path.isfile(model_def_file), "File {} is missing".format(model_def_file)
    assert os.path.isfile(model_file), ("File {} is missing. Please download it using "
                                        "./download_trained_model.sh").format(model_file)

    if gpu_device >= 0:
        caffe.set_device(gpu_device)
        caffe.set_mode_gpu()
    else:
        caffe.set_mode_cpu()

    net = caffe.Net(model_def_file, model_file, caffe.TEST)

    num_images = len(inputs)
    num_channels = inputs[0].shape[2]
    assert num_channels == 3, "Unexpected channel count. A 3-channel RGB image is exptected."
    
    caffe_in = np.zeros((num_images, num_channels, _MAX_DIM, _MAX_DIM), dtype=np.float32)
    for ix, in_ in enumerate(inputs):
        caffe_in[ix] = in_.transpose((2, 0, 1))

    start_time = time.time()
    out = net.forward_all(**{net.inputs[0]: caffe_in})
    end_time = time.time()

    print("Time taken to run the network: {:.4f} seconds".format(end_time - start_time))
    predictions = out[net.outputs[0]]

    return predictions[0].argmax(axis=0).astype(np.uint8)


def run_crfrnn(input_file, output_file, gpu_device):
    """ Runs the CRF-RNN segmentation on the given RGB image and saves the segmentation mask.

    Args:
        input_file: Input RGB image file (e.g. in JPEG format)
        output_file: Path to save the resulting segmentation in PNG format
        gpu_device: ID of the GPU device. If using the CPU, set this to -1
    """

    input_image = 255 * caffe.io.load_image(input_file)
    input_image = resize_image(input_image)

    image = PILImage.fromarray(np.uint8(input_image))
    image = np.array(image)

    palette = get_palette(256)
    #PIL reads image in the form of RGB, while cv2 reads image in the form of BGR, mean_vec = [R,G,B] 
    mean_vec = np.array([123.68, 116.779, 103.939], dtype=np.float32)
    mean_vec = mean_vec.reshape(1, 1, 3)

    # Rearrange channels to form BGR
    im = image[:, :, ::-1]
    # Subtract mean
    im = im - mean_vec

    # Pad as necessary
    cur_h, cur_w, cur_c = im.shape
    pad_h = _MAX_DIM - cur_h
    pad_w = _MAX_DIM - cur_w
    im = np.pad(im, pad_width=((0, pad_h), (0, pad_w), (0, 0)), mode='constant', constant_values=0)

    # Get predictions
    segmentation = crfrnn_segmenter(_MODEL_DEF_FILE, _MODEL_FILE, gpu_device, [im])
    segmentation = segmentation[0:cur_h, 0:cur_w]

    output_im = PILImage.fromarray(segmentation)

    #compute and mask everything but humans
    output_im.putpalette(palette)
    

    real_output = apply_mask(image,segmentation,15)
    output_im = PILImage.fromarray(real_output)
    output_im.save(output_file)

    
    #return (image,segmentation)

def resize_image(image):
    """ Resizes the image so that the largest dimension is not larger than 500 pixels.
        If the image's largest dimension is already less than 500, no changes are made.

    Args:
        Input image

    Returns:
        Resized image where the largest dimension is less than 500 pixels
    """

    width, height = image.shape[0], image.shape[1]
    max_dim = max(width, height)

    if max_dim > _MAX_DIM:
        if height > width:
            ratio = float(_MAX_DIM) / height
        else:
            ratio = float(_MAX_DIM) / width
        image = PILImage.fromarray(np.uint8(image))
        image = image.resize((int(height * ratio), int(width * ratio)), resample=PILImage.BILINEAR)
        image = np.array(image)

    return image

def run_ppl_only(in_filename, out_filename):
    run_crfrnn(in_filename,out_filename,-1)
    
def find_images(topdir):
    retval = []
    exten = ['jpg', 'bmp', 'png']

    for dirpath, dirnames, files in os.walk(topdir):
        for name in files:
            if name.lower().split('.')[-1] in exten:
                retval.append(name)
                #retval.append(os.path.join(dirpath, name))
    return retval

def main():
    print 'Starting'

    if len(sys.argv) != 1:
        run_crfrnn('/work/flask/static/top.jpg','/work/flask/static/bottom.bmp',-1)
        return 0

    work_in = '/work/inputImages'
    work_out = '/work/outputImages'
    work_items = find_images(work_in)
    
    for work_item in work_items:
        in_filename = os.path.join(work_in,work_item)
        out_work_item = work_item.split('.')[0]
        out_work_item += '.png'
        print(work_item,out_work_item)
        out_filename = os.path.join(work_out,out_work_item)
        print(in_filename,out_filename)
        run_ppl_only(in_filename,out_filename)


if __name__ == '__main__':
    main()
