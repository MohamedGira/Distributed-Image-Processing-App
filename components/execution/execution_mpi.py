from mpi4py import MPI
import numpy as np
import cv2
import numpy as np
from utils.Storage import s3_storage,disk_storage
from utils.Database.database import RedisDatabase
from dotenv import load_dotenv
import sys
from utils.helpers import np_array_to_BytesIO_stream
import uuid
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process images.')
    parser.add_argument('--access_means', type=str, help='Path to input image file',required=True)
    parser.add_argument('--output_dir', type=str, help='dir to save processed image',required=True)
    parser.add_argument('--output_name', type=str, help='name to save processed image',required=True)
    parser.add_argument('--operation', type=str, help='Operation to perform on the image',required=True)
    parser.add_argument('--extension', type=str, help='File extension for the output image',required=True)
    parser.add_argument('--shared_storage', type=str, help='File shared_storage for the output image',required=True)
    return parser.parse_args()

args = parse_arguments()

location_on_disk = args.access_means
operation = args.operation

#get the first argv as operation
def split_image(image):
    # Get the dimensions of the image
    height, width, channels = image.shape
    
    # Calculate the size of each part
    part_width = width // 2
    part_height = height // 2
    
    # Split the image into four parts
    parts = [
        image[:part_height, :part_width],
        image[:part_height, part_width:],
        image[part_height:, :part_width],
        image[part_height:, part_width:]
    ]
    return parts
def process_image(image: np.ndarray, operation: str):
    if image is None:
        print("Error: Unable to load the image.")
        return None
    # Perform Specified Operation
    if operation == "grayscale":
        result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif operation == "edge_detection":
        result = cv2.Canny(image, 100, 200)
    elif operation == "thresholding":
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, result = cv2.threshold(gray_image, 100, 255, cv2.THRESH_BINARY)
    elif operation == "inversion":
        result = cv2.bitwise_not(image)
    elif operation == "blurring":
        result = cv2.GaussianBlur(image, (21, 21), 0)
    elif operation == "sharpening":
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        result = cv2.filter2D(image, -1, kernel)
    elif operation == "smoothing":
        result = cv2.medianBlur(image, 5)
    elif operation == "dilation":
        kernel = np.ones((5, 5), np.uint8)
        result = cv2.dilate(image, kernel, iterations=1)
    elif operation == "erosion":
        kernel = np.ones((5, 5), np.uint8)
        result = cv2.erode(image, kernel, iterations=1)
    elif operation == "convert_RGB":
        result = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    else:
        print("Invalid Operation")
        return

    return result



# MPI setup
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Load the image (assuming it's named 'input_image.jpg')
storage= disk_storage.DiskStorage(args.shared_storage)
input_image = storage.load_to_memory(location_on_disk)
decoded=cv2.imdecode(input_image, cv2.IMREAD_COLOR)
num_parts = 4

# Calculate the size of each part
part_size = decoded // num_parts
# Scatter the image parts to different processes
if rank == 0:
    image_parts = split_image(decoded)
else:
    image_parts = None

image_parts = comm.scatter(image_parts, root=0)
# Process the image part
processed_part = process_image(image_parts, operation)
# Gather the processed parts to the root process
newData = comm.gather(processed_part, root=0)

# Root process combines the processed parts

if rank == 0:
    top=np.concatenate(newData[0:2], axis=1)
    bottom=np.concatenate(newData[2:4], axis=1)
    output=np.concatenate([top,bottom],axis=0)
    storage.save(np_array_to_BytesIO_stream(output,f".{args.extension}"),name=args.output_name,path=args.output_dir)
   

