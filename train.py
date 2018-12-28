import matplotlib as mat
mat.use("Agg")
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import img_to_array
from keras.utils import to_categorical
from Models import LeNet as CNN
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import argparse
import random
import cv2
import os
import _pickle as cPickle
ap = argparse.ArgumentParser()
ap.add_argument('-d', '--dataset', required=True, help='path to input dataset')
ap.add_argument('-m', '--model', required=True, help='path to output model')
ap.add_argument('-p', '--plot', type=str, default='plot.png', help='path to accuracy/loss plot')
ap.add_argument('-e', '--epochs', type=int, default=25, help='Number Of Epohcs To Train For')
ap.add_argument('-c', '--classes', type=int, default=10, help="Number of Classes")
ap.add_argument('-b', '--batches', type=int, default=32, help="Batch Size")
ap.add_argument('-t', '--type',type=str,default='LeNet', help='Type of Neural Network')
ap.add_argument('-r', '--ratio', type=float, default=.25, help='Percent of Images allocated for Testing')
args = vars(ap.parse_args())
if(args['type'].lower() == 'cifar'):
    from Models import Cifar as CNN
else:
    from Models import LeNet as CNN
NUMC = args['classes']
EPOCHS = args['epochs']
INIT_LR = 1e-3
BS = args['batches']

print("[INFO] loading images...")
data = []
labels = []

'''imagePaths = sorted(list(paths.list_images(args['dataset'])))
random.seed(42)
random.shuffle(imagePaths)

for imagePath in imagePaths:
	image = cv2.imread(imagePath)
	image = cv2.resize(image, (32, 32))
	image = img_to_array(image)
	data.append(image)
	label = imagePath.split(os.path.sep)[-2]
	label = 1 if label == 'santa' else 0
	labels.append(label)
'''
inp = cPickle.load(open(args['dataset'],'rb'),encoding='latin1')
data = inp['data']#np.array(data, dtype='float')/255.0
temp = []
print(data.shape)
for i in range(len(data)): 
    x = np.split(data[i],3)
    temp.append(np.hstack((x[0].reshape(len(x[0]),1),x[1].reshape(len(x[1]),1),x[2].reshape(len(x[2]),1))).flatten().reshape(32,32,3))
    temp[i]=temp[i].astype('float')/255.0
data = np.array(temp)
print(data.shape)
labels = np.array(inp['labels'])# np.array(labels)
print(labels.shape)
trainX, testX, trainY, testY = train_test_split(data, labels, test_size=args['ratio'], random_state=42)
trainY = to_categorical(trainY, num_classes=NUMC)
testY = to_categorical(testY, num_classes=NUMC)

aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1, height_shift_range=0.1, shear_range=0.2, zoom_range=0.2, horizontal_flip=True, fill_mode='nearest')

print("[INFO] compiling model...")
try: model = load_model(args['model'])
except: model = CNN.build(classes=NUMC)
opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
losstype = lambda c: 'binary_crossentropy' if c<=2 else 'categorical_crossentropy'
model.compile(loss=losstype(NUMC),optimizer=opt,metrics=['accuracy'])

print("[INFO] training network...")
H = model.fit_generator(aug.flow(trainX, trainY, batch_size=BS), validation_data=(testX, testY), steps_per_epoch=len(trainX)//BS, epochs=EPOCHS, verbose=1)

print("[INFO] serializing network...")
model.save(args['model'])

plt.style.use('ggplot')
plt.figure()
N = EPOCHS
plt.plot(np.arange(0,N), H.history['loss'], label='train_loss')
plt.plot(np.arange(0,N), H.history['val_loss'], label='val_loss')
plt.plot(np.arange(0,N), H.history['acc'], label='train_acc')
plt.plot(np.arange(0,N), H.history['val_acc'], label='val_acc')
plt.title("Training Loss and Accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend()
plt.savefig(args['plot'])

