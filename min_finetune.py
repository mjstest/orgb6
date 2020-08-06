import argparse, time, logging, os, sys, math

import numpy as np
import mxnet as mx
import gluoncv as gcv
from mxnet import gluon, nd, init, context
from mxnet import autograd as ag
from mxnet.gluon import nn
from mxnet.gluon.data.vision import transforms
#from mxboard import SummaryWriter
# from mxnet.contrib import amp

from gluoncv.data.transforms import video
from gluoncv.data import UCF101, Kinetics400, SomethingSomethingV2, HMDB51, VideoClsCustom
from gluoncv.model_zoo import get_model
from gluoncv.utils import makedirs, LRSequential, LRScheduler, split_and_load, TrainingHistory
from gluoncv.data.sampler import SplitSampler, ShuffleSplitSampler
#from prep_dataset import download_videos, remove_files

#from categories import categories

def parse_args():
    parser = argparse.ArgumentParser(description="Test a model")
    parser.add_argument("--model", type=str, required=True, help="pretrained model to load and test")
    parser.add_argument("--num-classes", type=int, required=True, help="number of classes in dataset")
    parser.add_argument("--num-gpus", type=int, help="number of gpus to use", default=0)
    parser.add_argument("--batch-size", type=int, help="batch size", default=25)
    args = parser.parse_args()
    return args
        


def main():
    args = parse_args()

    #set up env
    num_gpus = args.num_gpus
    batch_size = args.batch_size
    batch_size *= max(1, num_gpus)
    ctx = [mx.gpu(i) for i in range(num_gpus)] if num_gpus > 0 else [mx.cpu()]
    num_workers = 4

    # get data
    #train_data, val_data = get_data(args, batch_size, num_workers)

    #load model (could give option to load params if training wasn't finished)
    net = get_model(name=args.model, nclass=args.num_classes, use_kinetics_pretrain=True)#, num_segments=args.num_segments)
    net.collect_params().reset_ctx(ctx)
    #if args.params is not None:
    #    net.load_parameters(args.params, ctx=ctx, allow_missing=True, ignore_extra=True)
    net.hybridize()
    print("Loaded {} model".format(args.model))
            


if __name__ == "__main__":
    main()
