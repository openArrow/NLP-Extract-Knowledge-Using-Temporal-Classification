import xmltodict
import pickle
from os import listdir
from os.path import isfile, join
import lemma
from copy import deepcopy

pairs = {}

def opposite(relation):
	if relation == 'AFTER':
		return 'BEFORE'
	if relation == 'BEFORE':
		return 'AFTER'

def doFileOp(file):
	id_verp_map = {}
	with open(file, 'r') as fd:
		doc = xmltodict.parse(fd.read())
		#print doc['TimeML']
		try :
			
			if type(doc['TimeML']['EVENT']) != type([]):
				doc['TimeML']['EVENT'] = [doc['TimeML']['EVENT']]
			
			for i in doc['TimeML']['EVENT']:
				#print i
				id_verp_map[i['@eid']] = i['#text']

			if type(doc['TimeML']['TLINK']) != type([]):
				doc['TimeML']['TLINK'] = [doc['TimeML']['TLINK']]

			for i in doc['TimeML']['TLINK']:
				if '@relatedToEvent' in i:

					verb1 = lemma.getLemma(id_verp_map[i['@eventID']])
					verb2 = lemma.getLemma(id_verp_map[i['@relatedToEvent']])
					keyA = (verb1, verb2)
					keyB = (verb2, verb1)
					relation = i['@relType']
					if keyA in pairs:
						pairs[keyA][relation] += 1
					elif keyB in pairs:
						pairs[keyB][opposite(relation)] += 1
					else:
						pairs[keyA] = {'AFTER':0, 'BEFORE':0}
						pairs[keyA][relation] += 1
		except:
			print '------ Error'
			return ''
	return ''

def main():
	mypath = "/home/vatsal/Desktop/Input/"
	files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	#print files

	for f in files:
		if len(f.split('.')) != 1:
			print f
			doFileOp(mypath + f)
	print pairs
	pickle_file = "/home/vatsal/Desktop/pairs_temporal.pkl"
	fo = open(pickle_file, 'wb') 
	pickle.dump(pairs, fo)
	fo.close()

	# fileObject = open(file_Name,'r')  	
	# b = pickle.load(fileObject) 

	return None

if __name__ == "__main__" : main()