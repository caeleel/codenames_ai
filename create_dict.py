with open('20k.txt', 'r') as f:
	for line in f.read().split('\n'):
		if len(line) > 3:
			print line
