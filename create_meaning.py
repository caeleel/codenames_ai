import json
import random

DIVISOR = 2

def shuffle(words):
	for i in xrange(len(words) / DIVISOR):
		j = random.randint(i, len(words)-1)
		tmp = words[i]
		words[i] = words[j]
		words[j] = tmp

associations = {}

with open('codewords.txt', 'r') as cwf:
	with open('dict.txt', 'r') as wf:
		words = wf.read().split('\n')
		words = [x for x in words if x]
		portion = len(words) / DIVISOR

		codewords = cwf.read().lower().split('\n')
		codewords = [x for x in codewords if x]
		for cw in codewords:
			shuffle(words)
			associations[cw] = words[:portion]

with open('associations.txt', 'w') as f:
	f.write(json.dumps(associations))
