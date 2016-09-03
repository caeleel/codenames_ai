import json
import sys
import itertools

def load_words(filename):
	with open(filename, 'r') as f:
		return json.loads(f.read())

if __name__ == '__main__':
	print 'loading board file'
	board_file = sys.argv[1]
	with open(board_file, 'r') as f:
		lines = f.read().split('\n')
		board = lines[0].split(' ')
		red = lines[1].split(' ')
		blue = lines[2].split(' ')
		black = lines[3].split(' ')
		white = [x for x in board if x not in red + blue + black]

	print 'board :: {}'.format(board)
	print 'red :: {}'.format(red)
	print 'blue :: {}'.format(blue)
	print 'black :: {}'.format(black)

	print 'loading word meanings...'
	assoc = load_words('associations.txt')
	print 'creating meaning sets...'
	meaning_sets = {}
	meaning_index = {}
	for k, v in assoc.iteritems():
		meaning_sets[k] = set(v)
		#for i, s in enumerate(v):
		#	meaning_index[k + '-' + s] = i

	print 'validating board'
	for word in board:
		if word not in meaning_sets:
			print '{} not known!'.format(word)
			sys.exit(1)
	for word in red + blue + black:
		if word not in board:
			print '{} is not on the board!'.format(word)
			sys.exit(1)

	combos = itertools.combinations(red, 4)
	word_pool = set()

	print 'creating word pool'
	for test_set in combos:
		available = meaning_sets[test_set[0]]
		for x in test_set[1:]:
			available = available.intersection(meaning_sets[x])
		word_pool = word_pool.union(available)
	
	print 'counting candidates'
	counts = []
	for x in word_pool:
		words = []
		red_count = 0
		blue_count = 0
		black_count = 0
		white_count = 0
		index = -1
		for b in red:
			if x in meaning_sets[b]:
				red_count += 1
				#index *= meaning_index[b + '-' + x]
				words.append(b)
		for b in blue:
			if x in meaning_sets[b]:
				blue_count += 1
				words.append(b)
		for b in black:
			if x in meaning_sets[b]:
				black_count += 1
				words.append(b)
		for b in white:
			if x in meaning_sets[b]:
				white_count += 1
				words.append(b)
	
		counts.append([red_count, index, -black_count, -blue_count, -white_count, x, words])
	
	counts.sort()
	counts.reverse()
	for count in counts[:200]:
		print 'Distribution: ({} => {}) R:{} / b!:{} / B:{} / W:{}'.format(count[1], count[5], count[0], count[2], count[3], count[4])
	#	for test_set in itertools.combinations(count[6], count[0]):
	#		index = -1
	#		for word in test_set:
	#			index *= meaning_index[word + '-' + count[5]]
	#		print 'COMPARING {} -> {}'.format(index, count[1])
	#		if index > count[1]:
	#			break
