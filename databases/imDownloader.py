from selenium import webdriver
from splinter import Browser
from time import sleep
import mousePy as mouse
def closePopUps(b):
	wins = b.windows
	for i in wins:
		if i != wins.current: i.close()
class ImageDownloader:
	def __init__(self):
		self.searchPage = Browser('chrome')
		self.downloadPage = self.searchPage#Browser('chrome')
	def search(self,name,url='https://images.google.com'):
		b = self.searchPage
		b.visit(url)
		b.fill('q', name+"\n")
		for l in range(10):
			b.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			sleep(.5)
		try:
			b.find_by_id('smb')[0].click()
			for l in range(10): 
				b.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				sleep(.5)
		except: print("Scroll Further Buton Not Found")

		el = [i['href'] for i in b.find_by_css('a') if i['jsname']=='hSRGPd' and i['href']!=None]
		print(len(el))
		links = []
		l = 0
		for i in el:
			b.visit(i)
			sleep(.1)
			imgs = b.find_by_css('img')#[i['src'] for i in b.find_by_css('img') if i.has_class('irc_mi') and i['src'] != None]
			if len(imgs) == 0: 
				print('Case',l,'Failed')
				l+=1
				continue
			for j in imgs:
				try: 
					if(j['class']!='irc_mi'): continue
					print('Case',l,'Passed')
					links.append(j['src'])
				except: 
					print('Case',l,'Failed')
				l+=1
		return links
	def manDownload(self,link,i):
		b = self.downloadPage
		b.visit(link)
		mouse.rightclick(600,500)
		sleep(.25)
		mouse.leftclick(610,520)
		sleep(2)
		if(i==1): mouse.leftclick(720,300)
		else: mouse.leftclick(722,275) 
		sleep(.25)
	def download(self,link,timeToSleep=5):
		b = self.downloadPage
		b.visit('https://image.online-convert.com/convert-to-jpg')
		now = b.url
		b.fill('external_url',link+'\n')
		while(b.url == now): sleep(.05)
		#raw_input('done?')
		sleep(timeToSleep)
	def downloadFile(self,file):
		f = open(file,'r')
		j = 1
		for i in f: 
			print(j)
			self.manDownload(i,j)#self.download(i)
			j+=1
		f.close()
	def toFile(self,searchterm,prefix=""):
		f = open(prefix+searchterm+'.txt','w')
		links = self.search(searchterm)
		for i in links:
			f.write(i+'\n')
		f.close()
	def downloadFiles(self,file):
		f = open(file,'r')
		for i in f:
			i = i.replace('\n','') + " flower"
			self.toFile(i,prefix='FlowerImages/')
			#self.downloadFile('FlowerImages/'+i+'.txt')
			#raw_input("Transfer Files and Click Enter")
	def close(self):
		self.searchPage.quit()
		self.submitPage.quit()
class Flower():
	def __init__(self):
		self.submitPage = None#Browser('chrome')
		self.imageDownloader = ImageDownloader()
	def flowerToLinks(self):
		self.imageDownloader.toFile(raw_input('Which Flower? '))
	def flowersToLinks(self):
		self.imageDownloader.downloadFiles(raw_input('Which File? '))
	def fileToImages(self):
		self.imageDownloader.downloadFile(raw_input('Which File? '))
	def flowerToImages(self):
		flower = raw_input("Which Flower? ")
		self.imageDownloader.toFile(flower)
		self.imageDownloader.downloadFile(flower+'.txt')
	def login(self,usr,psd,url='https://user.tjhsst.edu/cvupload/'):
		b = self.submitPage
		b.visit(url)
		b.find_link_by_partial_href('authorize')[0].click()
		b.fill('username',usr)
		b.fill('password',psd+"\n")
		b.find_by_value('Authorize')[0].click()
	def close(self):
		self.submitPage.quit()
		self.imageDownloader.close()
if __name__ == '__main__':
	fl = Flower()
	i = int(raw_input("0 for Flower => Links, 1 for File => Images, 2 for both"))
	if i == 0: fl.flowerToLinks()
	elif i == 1: fl.fileToImages()
	elif i == 2: fl.flowertoImages() 
	elif i == 3: fl.flowersToLinks()
	fl.close()
'''Fl = Flower()
Fl.downloadFiles('flowers.txt')
Fl.close()'''

#<img class="rg_ic rg_i" id="ZdJ7EqYJZAjdwM:" name="ZdJ7EqYJZAjdwM:" jsaction="load:str.tbn" alt="Image result for Rose" onload="typeof google==='object'&amp;&amp;google.aft&amp;&amp;google.aft(this)" style="width: 185px; height: 185px; margin-left: -3px; margin-right: -2px; margin-top: 0px;" src="data:image/jpeg;base64,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">
