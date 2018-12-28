from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument('-m', '--model', required=True, help='path to trained model')
ap.add_argument('-i', '--image', required=True, help='path to input image')
ap.add_argument('-l', '--labels', required=True, help='path to label text file')
args = vars(ap.parse_args())

model = load_model(args['model'])
image = cv2.imread(args['image'])
orig = image.copy()
infile = open(args['labels'],'r')

image = np.expand_dims(img_to_array(cv2.resize(image, (32,32)).astype('float')/255.0),axis=0)
p = model.predict(image)
names = []
i = 0
for line in infile:
    names.append((line.split(', ')[0], p[0][i]))
    i+=1
names = sorted(names, key=lambda k: -k[1])
for i in names: print(i[0],i[1])
print("Best Guess:", names[0][0], "\nConfidence:", names[0][1])
#print(names[max([i for i in range(len(p[0]))], key = lambda i: p[0][i])])
