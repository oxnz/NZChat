#-*- coding: utf-8 -*-

import json
import time

class NZEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, NZMessage):
			d = {'__class__': obj.__class__.__name__,
				'__module__':obj.__module__,
				'time': obj.time,
				'content': obj.content,
			}
			d.update(obj.__dict__)
			return d
		else:
			return json.JSONEncoder.default(self, obj)

class NZDecoder(json.JSONDecoder):
#	def __init__(self):
#		pass
#		json.JSONDecoder.__init__(self, object_hook = self.dict2obj)
	def dict2obj(self, d):
		print 'starting...'


from NZMessage import NZMessage
if __name__ == '__main__':
	encoder = NZEncoder()
#	decoder = NZDecoder()
	m = NZMessage()
#	x = '[{"s": "instance value goes here", "__module__": "NZMessage", "__class__": "NZMessage"}]'
	print encoder.encode(m)
#	print decoder.decode(x)
