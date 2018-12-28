from PIL import Image
import numpy as np
import os
import _pickle as cPickle
def unpickle(file):
    with open(file, 'rb') as fo:
        dict = cPickle.load(fo, encoding='latin1')
    return dict
def save_image(filepath,label,silent=False):
	if not silent: print(filepath)
	im = Image.open(filepath)
	im = (np.array(im))
	if(im.ndim == 2):
		im = im.tolist()
		for i in range(len(im)):
			for j in range(len(im[0])): im[i][j] = [im[i][j]]*3
		im = np.array(im)
	#print(im.shape)
	#print(im[0][0])
	r = im[:,:,0].flatten()
	g = im[:,:,1].flatten()
	b = im[:,:,2].flatten()

	img = np.array(list(r) + list(g) + list(b),np.uint8)
	labels = [label]
	return img, label
def save_group(folderpath,label,silent=False,lower=0,upper=0):
	if not upper: fnames = os.listdir(folderpath)
	else: fnames = sorted(os.listdir(folderpath))[lower:upper]
	extensions = ['.jpg','.gif','.png','.jpeg']
	fnames = [i for i in fnames if i != '.DS_Store' and (i[-4:].lower() in extensions or i[-5:].lower() in extensions)]
	#print(upper)
	n = len(fnames)
	images = np.zeros((n,3072),np.uint8)
	labels = [label for i in range(n)]
	if not silent: print(folderpath,n)
	for i in range(n):	
		img, lbl = save_image(os.path.join(folderpath,fnames[i]),label)
		images[i] = img
	return images,labels, fnames	
def read_labels(labelfile):
	nTl = {}
	lTn = {}
	with open(labelfile, 'r') as f:
		for line in f:
			name, label = line.replace("\n",'').split(", ")
			name = name.lower()
			label = int(label)
			nTl[name] = label 
			lTn[label] = name
	return nTl, lTn
def save_batch(batchpath,labelfile,outfile,lower=0,upper=0):
	nTl, lTn = read_labels(labelfile)
	groups = os.listdir(batchpath)
	images = np.zeros((1,3072),np.uint8)
	labels = []
	fnames = []
	#print(upper)
	for i in groups:
		if i.lower() not in nTl: 
			print(i,"not found")
			continue
		#print(upper)
		ims, lbls, nam = save_group(os.path.join(batchpath,i),nTl[i.lower()],lower=lower,upper=upper)
		fnames+=nam
		images = np.vstack([images,ims])
		labels+=lbls
	images = images[1:]
	dic = {}
	dic["data"] = images
	dic["filenames"] = fnames
	dic["labels"] = labels
	cPickle.dump(dic,open(outfile,'wb'))
def save_batches(datapath,labelfile,numbatches,numper):
	for i in range(numbatches): save_batch(datapath,labelfile,'data_batch_{}.pkl'.format(i+1),numper*i,numper*(i+1))
def genLabelFiles(batchpath,outfile,skip=0):
	groups = sorted(os.listdir(batchpath))[skip:]
	f = open(outfile,'w')
	for i in range(len(groups)): f.write(groups[i]+", "+str(i)+"\n")
	f.close()
#genLabelFiles('./flowers/data_batch_1','labels.txt',1)
#save_batch('./flowers/data_batch_1','labels.txt','./flowers/data_batch_1.pkl',0,10)
#dic = unpickle('./flowers/data_batch_1.pkl')
#print(dic['data'])
#print(dic['data'].shape)
