import os
from PIL import Image
from resizeimage import resizeimage
def resizeImage(filepath,silent=False):
	if not silent: print(filepath)
	try:
		with open(filepath, 'r+b') as f:
		    with Image.open(f) as image:
		        cover = resizeimage.resize_cover(image, [32, 32], validate=False)
		        cover.save(filepath, image.format)
	except:	os.system('rm \"' + filepath + '\"')	
def resizeImages(folderpath):
	lis = os.listdir(folderpath)
	for i in lis: resizeImage(os.path.join(folderpath,i))
def downloadIntoFolder(folderpath,linkpath):
	os.system('mkdir \"' + folderpath + '\"')
	f = list(open(linkpath,'r'))
	for i in range(len(f)):
		try: line = f[i] 
		except: continue
		if('.jpg' in line or '.png' in line or '.gif' in line): os.system('wget ' + '--directory-prefix=\"' + folderpath + '/\" ' + line.replace('\n',''))
def renameFolder(folder):
	lis = os.listdir(folder)
	for i in range(len(lis)):
		print(os.path.join(folder,lis[i]))
		ind = 4
		if '.jpeg' in lis[i]: lis=5
		os.system("mv \"" + os.path.join(folder,lis[i]) + "\" \"" + os.path.join(folder,str(i)+lis[i][-lis:]) + "\"")
def transferFolder(folder,folderto):
	lis = os.listdir(folder)
	for i in lis:
		print(os.path.join(folder,i))
		os.system("mv \"" + os.path.join(folder,i) + "\" \"" + folderto + "\"")
	renameFolder(folderto)
def downloadFolder(folderpath,outfolder):
	lis = os.listdir(folderpath)
	for i in lis: 
		if(i != '.DS_Store'): 
			downloadIntoFolder(os.path.join(outfolder,i.replace('.txt','')),os.path.join(folderpath,i))
			resizeImages(os.path.join(outfolder,i.replace('.txt','')))
#downloadFolder('./texts')

