import tensorflow as tf
import numpy as np
#iimport matplotlib.pyplot as plt
import os
import _pickle as cPickle
#Weights for Fully Connected or Convulutional Layers of the Network
#Initialized Randomly using a Truncaded Normal Distribution
def weight_variable(shape):
   initial = tf.truncated_normal(shape, stddev=0.1)
   return tf.Variable(initial)
#Bias for Fully Connected or Convulutiona Layers 
#Initialized With a Constant Value of .1
def bias_variable(shape):
   initial = tf.constant(0.1, shape=shape)
   return tf.Variable(initial)
#Full Convolution (no skips) with an Output the Same Size as the Input
def conv2d(x,W):
   return tf.nn.conv2d(x,W,strides=[1,1,1,1], padding='SAME')
#Max Pool is Set to Half the Size across the h/w dimensions (1/4 feature map size)
def max_pool_2x2(x):
   return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')
#The acutal layer used for Convolution
#Linear Convolution (conv2d) + Bias + ReLU nonlinearity
def conv_layer(input, shape):
   W = weight_variable(shape)
   b = bias_variable([shape[3]])
   return tf.nn.relu(conv2d(input,W)+b)
#Full layer with Bias w/0 ReLU
def full_layer(input, size):
   in_size = int(input.get_shape()[1])
   W = weight_variable([in_size,size])
   b = bias_variable([size])
   return tf.matmul(input,W) + b
DATA_PATH = 'databases/flowers10'
def unpickle(file):
    with open(os.path.join(DATA_PATH, file), 'rb') as fo:
        dict = cPickle.load(fo, encoding='latin1')
    return dict
def one_hot(vec, vals=10):
	n = len(vec)
	out = np.zeros((n,vals))
	out[range(n), vec] = 1
	return out
class CifarLoader(object):
	def __init__(self, source_files):
		self.source = source_files
		self._i = 0
		self.images = None
		self.labels = None
	def load(self):
		data = [unpickle(f) for f in self.source]
		images = np.vstack([d["data"] for d in data])
		n = len(images)
		self.images = images.reshape(n, 3, 32, 32).transpose(0,2,3,1).astype(float)/255
		self.labels = one_hot(np.hstack([d["labels"] for d in data]), 10)
		return self
	def next_batch(self, batch_size):
		x, y = self.images[self._i:self._i+batch_size],self.labels[self._i:self._i+batch_size]
		self._i = (self._i + batch_size) % len(self.images)
		return x,y
class CifarDataManager(object):
	def __init__(self):
		self.train = CifarLoader(["data_batch_{}.pkl".format(i) for i in range(1,2)]).load()
		self.test = CifarLoader(["test_batch.pkl"]).load()
'''def display_cifar(images,size):
	n = len(images)
	plt.figure()
	plt.gca().set_axis_off()
	im = np.vstack([np.hstack([images[np.random.choice(n)] for i in range(size)]) for i in range(size)])
	plt.imshow(im)
	plt.show()
'''
'''d = CifarDataManager()
print("Number of Train Images: {}".format(len(d.train.images)))
print("Number of Train Labels: {}".format(len(d.train.labels)))
print("Number of Test Images: {}".format(len(d.test.images)))
print("Number of Test Labels: {U".format(len(d.test.labels)))
images = d.train.images
display_cifar(images,10)
cifar = CifarDataManager()

x = tf.placeholder(tf.float32, shape=[None, 32, 32, 3])
y_ = tf.placeholder(tf.float32, shape=[None, 10])
keep_prob = tf.placeholder(tf.float32)

conv1 = conv_layer(x,shape=[5,5,3,32])
conv1_pool = max_pool_2x2(conv1)

conv2 = conv_layer(conv1_pool, shape=[5,5,32,64])
conv2_pool = max_pool_2x2(conv2)

conv3 = conv_layer(conv2_pool, shape=[5,5,64,128])
conv3_pool = max_pool_2x2(conv3)

conv3_flat = tf.reshape(conv3_pool, [-1,4*4*128])
conv3)drop = tf.nn.dropout(conv3_flat, keep_prob=keep_prob)

full_1 = tf.nn.relu(full_layer(conv3_drop, 512))
full1_drop = tf.nn.dropout(full_1, keep_prob=keep_prob)

y_conv = full_layer(full1_drop,10)
'''
cifar = CifarDataManager()
x = tf.placeholder(tf.float32, shape=[None,32,32,3])
y_ = tf.placeholder(tf.float32, shape=[None,10])
keep_prob = tf.placeholder(tf.float32)
#try:
C1, C2, C3 = 30, 50, 80
F1 = 500
conv1_1 = conv_layer(x,shape=[3,3,3,C1])
conv1_2 = conv_layer(conv1_1, shape=[3,3,C1,C1])
conv1_3 = conv_layer(conv1_2, shape=[3,3,C1,C1])
conv1_pool = max_pool_2x2(conv1_3)
conv1_drop = tf.nn.dropout(conv1_pool, keep_prob=keep_prob)

conv2_1 = conv_layer(conv1_drop, shape=[3,3,C1,C2])
conv2_2 = conv_layer(conv2_1, shape = [3,3,C2,C2])
conv2_3 = conv_layer(conv2_2, shape = [3,3,C2,C2])
conv2_pool = max_pool_2x2(conv2_3)
conv2_drop = tf.nn.dropout(conv2_pool, keep_prob=keep_prob)

conv3_1 = conv_layer(conv2_drop, shape=[3,3,C2,C3])
conv3_2 = conv_layer(conv3_1, shape = [3,3,C3,C3])
conv3_3 = conv_layer(conv3_2, shape = [3,3,C3,C3])
conv3_pool = tf.nn.max_pool(conv3_3, ksize=[1,8,8,1], strides=[1,8,8,1], padding='SAME')
conv3_flat = tf.reshape(conv3_pool, [-1,C3])
conv3_drop = tf.nn.dropout(conv3_flat, keep_prob=keep_prob)

full1 = tf.nn.relu(full_layer(conv3_flat,F1))
full1_drop = tf.nn.dropout(full1, keep_prob=keep_prob)

y_conv = full_layer(full1_drop,10)

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y_conv,labels=y_))
train_step = tf.train.AdamOptimizer(1e-3).minimize(cross_entropy)

correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
#return accuracy
#print("ERROR")
def test(sess):
    print(cifar.test.images.shape)
    print(cifar.test.labels.shape)
    X = cifar.test.images.reshape(10,100,32,32,3)
    Y = cifar.test.labels.reshape(10,100,10)
    acc = np.mean([sess.run(accuracy, feed_dict={x: X[i], y_: Y[i], keep_prob: 1.0}) for i in range(10)])
    print("accuracy: {:.4}%".format(acc*100))
import sys
with tf.Session() as sess:
    init = tf.global_variables_initializer()
    saver = tf.train.Saver()
    try: saver.restore(sess,'./models/f10_model_final.ckpt')
    except:
        print("No Restore File")
        sess.run(init)#tf.global_variables_initializer())
    try: STEPS = int(sys.argv[1])
    except: STEPS = 500
    try: BATCH_SIZE = int(sys.argv[2])
    except: BATCH_SIZE = 100
    try: SKIP = int(sys.argv[3])
    except: SKIP = 100
    #saver = tf.train.Saver()
    print("STEPS", STEPS, "BATCH_SIZE", BATCH_SIZE, "SKIP", SKIP)
    for i in range(STEPS):
        #print(i,STEPS)
        batch = cifar.train.next_batch(BATCH_SIZE)
        sess.run(train_step, feed_dict={x:batch[0], y_: batch[1], keep_prob: 0.5})
        if(i%SKIP==0): 
            print(i)
            save_path = saver.save(sess,"./models/f10_model.ckpt")
    save_path = saver.save(sess,"./models/f10_model_final.ckpt")
    test(sess)
