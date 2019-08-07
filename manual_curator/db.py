from tinydb import TinyDB, Query, where
import os


Label = Query()


class ImageDB(object):
	def __init__(self, dbName: str, imgFolder: str):
		self.images = set()
		self.imgFolder = imgFolder
		self.dbName = dbName
		self.db = TinyDB(dbName)
		self.coins = self.db.table('coins')
		self.index()
	
	def index(self):
		"""Index images in dir"""
		print(f'Indexing dir {self.imgFolder}')
		for file in os.listdir(self.imgFolder):
			print(f'Consider {file}')
			if not (file.endswith('.jpg') or file.endswith('.png')):
				continue
			fname = os.path.join(self.imgFolder, file)
			print(f'Found image {fname} ({file})')
			self.images.add(file)
	
	def __next__(self) -> str:
		while len(self.images) > 0:
			image = next(iter(self.images))
			if (where('name') == image) in self.coins:
				self.images.remove(image)
				print(f'Already labelled {image}')
				continue
			return image
		raise StopIteration()
		
	def label(self, name: str, type: str, face: str, user: str = '?'):
		self.images.remove(name)
		self.coins.insert({'name': name, 'type': type, 'face': face, 'user': user})
