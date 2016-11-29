import pickle
import json

pairs_temporal = {(u'verb1', u'verb2'): {'AFTER': 0, 'BEFORE': 1}}

# dict = {
# 	"eventChains" : [
# 		{
# 			"eventChain" :  [
# 				{
# 					"subject" : "B",
# 					"verb" : "verb1",
# 					"object" : "A"
# 				},
# 				{
# 					"subject" : "A",
# 					"verb" : "verb2",
# 					"object" : "B"
# 				},
# 				{
# 					"subject" : "A",
# 					"verb" : "verb3",
# 					"object" : "B"
# 				}
# 			]
# 		},

# 		{
# 			"eventChain" :  [
# 				{
# 					"subject" : "A",
# 					"verb" : "verb1",
# 					"object" : "B"
# 				},
# 				{
# 					"subject" : "A",
# 					"verb" : "verb1",
# 					"object" : "B"
# 				},
# 				{
# 					"subject" : "A",
# 					"verb" : "verb1",
# 					"object" : "B"
# 				}
# 			]
# 		},
# 	]
# }

def findCauseAndAction(verb1, verb2):
	global pairs_temporal

	cause = ''
	action = ''

	key = ''
	if (verb1, verb2) in pairs_temporal:
		key = (verb1, verb2)
	elif (verb2, verb1) in pairs_temporal:
		key = (verb2, verb1)
	else:
		return None

	after = pairs_temporal[key]['AFTER']
	before = pairs_temporal[key]['BEFORE']

	if before > after:
		return {'cause' : key[0], 'action' : key[1]}
	else:
		return {'cause' : key[1], 'action' : key[0]}

def printKnowledgeTemplate(ordered_pair, obj_c, subj_c, obj_a, subj_a):
	cause_args = set([obj_c, subj_c])
	action_args = set([obj_a, subj_a])

	head_word = cause_args.intersection(action_args)

	for w in head_word:
		print w + "." + ordered_pair['cause'] + " = true may cause execution of " + ordered_pair['action'] + " [" + obj_a + "," + subj_a + "]"
		if w  == obj_c:
			print w + "_object" + "." + ordered_pair['cause'] + " = true may cause execution of " + ordered_pair['action'] + " [" + obj_a + "_object" + "," + subj_a + "_subject" +"]"
		if w  == subj_c:
			print w + "_subject" + "." + ordered_pair['cause'] + " = true may cause execution of " + ordered_pair['action'] + " [" + obj_a + "_object" + "," + subj_a + "_subject" +"]"
		print '\n'

def createKnowledgeTemplates(event_pairs):
	pairs = event_pairs['pairs']
	unordered_events = event_pairs['unordered_events']
	if len(pairs) == 0:
		return
	for p in pairs:

		verb1 = unordered_events[p[0]]['verb']
		obj1 = unordered_events[p[0]]['object']
		subj1 = unordered_events[p[0]]['subject']
		
		verb2 = unordered_events[p[1]]['verb']
		obj2 = unordered_events[p[1]]['object']
		subj2 = unordered_events[p[1]]['subject']

		ordered_pair = findCauseAndAction(verb1, verb2)
		if ordered_pair== None:
			continue

		if ordered_pair['cause'] == verb1:
			printKnowledgeTemplate(ordered_pair, obj1, subj1, obj2, subj2)
		else:
			printKnowledgeTemplate(ordered_pair, obj2, subj2, obj1, subj1)
		#print p


def makePair(unordered_events):
	s = set()
	dict = {}
	for i,v in enumerate(unordered_events):
		dict[i]=v

	for k1, v1 in dict.items():
		for k2, v2 in dict.items():
			if k1!=k2 and v1['verb']!=v2['verb']:
				if (k1,k2) not in s:
					s.add((k2,k1))
	return {'pairs':s, 'unordered_events': dict}

def main():
	global pairs_temporal

	fileObject = open('pairs_temporal.pkl','r')  	
	pairs_temporal = pickle.load(fileObject) 
	#print b

	data_file = open('unordered_event.json', 'r')
	dict = json.load(data_file)

	for i in dict["eventChains"]:
		event_pairs =  makePair(i['eventChain'])
		createKnowledgeTemplates(event_pairs)
	return None

if __name__ == "__main__" : main() 