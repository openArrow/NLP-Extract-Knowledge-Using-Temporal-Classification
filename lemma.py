from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost:9000')

def getLemma(word):
	res = nlp.annotate(str(word),
	               properties={
	                   'annotators': 'lemma',
	                   'outputFormat': 'json'
	               })
	return res["sentences"][0]['tokens'][0]['lemma']
    # print "%d: '%s': %s %s" % (
    #     s["index"],
    #     " ".join([t["word"] for t in s["tokens"]]),
    #     s["sentimentValue"], s["sentiment"])