import os
import sys
import datetime
import numpy as np
import skimage.draw


from config import *
from utils import Dataset
import model as modellib
from annotate_image import annotate_image


class BubbleConfig(Config):
    NAME = 'bubble'
    IMAGES_PER_GPU = 2
    STEPS_PER_EPOCH = 100
    NUM_CLASSES = 2 # background + bubble
    DETECTION_MIN_CONFIDENCE = 0.9
            
            
class BubbleDataset(Dataset):
    
    def load_bubble(self, dataset_dir):
        self.add_class("bubble", 1, "bubble")
        dir_path = os.path.join(IMAGE_BASE_DIR, dataset_dir)
        # Comment out this line and uncomment the following line if you want to include excel (.xls) files as well as csv files.
        paths = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and '.csv' in f]
        # paths = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and '.csv' in f or '.xls' in f]
        for path in paths:
            annotations = annotate_image(os.path.join(dataset_dir, path))
            image_path = annotations['filename']
            image = skimage.io.imread(image_path)
            height, width = image.shape[:2]
            polygons = [r['shape_attributes'] for r in annotations['regions'].values()]
            
            self.add_image(
                "bubble",
                image_id=annotations['filename'],
                path=image_path,
                width=width,
                height=height,
                polygons=polygons)
    
    def load_mask(self, image_id):
        info = self.image_info[image_id]
        mask = np.zeros([info['height'], info['width'], len(info['polygons'])], dtype=np.uint8)
        with open('/home/tug74186/Desktop/polygons.txt', 'w') as f:
            f.write(str(info['polygons']))
        for i, p in enumerate(info['polygons'][:-1]):# I was getting an array index out of bounds error with i being one too big, so I'm trying to go to the second to last instead of all the way for i.
            rr, cc = skimage.draw.polygon(p['all_points_y'], p['all_points_x'])
            mask[rr, cc, i] = 1  
        return mask.astype(np.bool), np.ones([mask.shape[-1]], dtype=np.int32)

    def image_reference(self, image_id):
        info = self.image_info[image_id]
        return info["path"]

def train(model):
    dataset_train = BubbleDataset()
    for directory in args.train_dirs:
        dataset_train.load_bubble(directory)
    dataset_train.prepare()
    
    dataset_val = BubbleDataset()
    for directory in args.val_dirs:
        dataset_val.load_bubble(directory)
    dataset_val.prepare()
    
    
    print('About to train network')
    model.train(dataset_train, dataset_val,
                learning_rate=config.LEARNING_RATE,
                epochs=30,
                layers='heads')
  


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--train_dirs", required=True,
                        nargs='+')
    parser.add_argument("--val_dirs", required=True,
                        nargs='+')
    parser.add_argument("--weights", required=True)
    parser.add_argument("--logs", required=False)
    

    args = parser.parse_args()

    config = BubbleConfig()
    config.display()
    
    model = modellib.MaskRCNN(mode='training', config=config,
                              model_dir=args.logs)

    print ("Weights: ", args.weights)
    print ('Dataset: ', args.train_dirs)
    print ("Logs: ", args.logs)

    if args.weights.lower() == 'last':
        weights_path = model.find_last()[1]
    elif args.weights.lower() == 'imagenet':
        weights_path = model.get_imagenet_weights()
    else:
        weights_path = args.weights

    print("Loading weights ", weights_path)
    model.load_weights(weights_path, by_name=True)

    train(model)
