import os
import torch
import argparse
import cv2
import detect_utils
import numpy as np
import time
from PIL import Image
from model import get_model

# Construct the argument parser.
parser = argparse.ArgumentParser()
parser.add_argument(
    '-i', '--input', default='input/image_1.jpg', 
    help='path to input input image'
)
parser.add_argument(
    '-t', '--threshold', default=0.5, type=float,
    help='detection threshold'
)
parser.add_argument(
    '-m', '--model', default='v2', 
    help='faster rcnn resnet50 fpn or fpn v2',
    choices=['v1', 'v2', 'v3']
)
args = vars(parser.parse_args())

# Define the computation device.
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = get_model(device, args['model'])
# Read the image.
image = Image.open(args['input']).convert('RGB')
# Create a BGR copy of the image for annotation.
image_bgr = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
# Detect outputs.
with torch.no_grad():
    # Record the start time
    start_time = time.time()    
    boxes, classes, labels = detect_utils.predict(image, model, device, args['threshold'])
    # Record the end time
    end_time = time.time()

# Calculate the duration
duration = end_time - start_time
print(f'Duration {duration}')
# Draw bounding boxes.
image = detect_utils.draw_boxes(boxes, classes, labels, image_bgr)
save_name = f"{args['input'].split('/')[-1].split('.')[0]}_t{''.join(str(args['threshold']).split('.'))}_{args['model']}"

output_folder = 'output'

try:
    os.makedirs(output_folder)
    print(f"Directory '{output_folder}' created.")
except FileExistsError:
    print(f"Directory '{output_folder}' already exists.")
except Exception as e:
    print(f"Failed to create directory '{output_folder}'. Error: {e}")

cv2.imwrite(f"{output_folder}/{save_name}.jpg", image)
