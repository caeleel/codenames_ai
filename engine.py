import json
import random
import sys
import itertools

def load_words(filename):
	with open(filename, 'r') as f:
		return json.loads(f.read())

def possible_words(combos, meaning_sets):
	print 'creating word pool'
	word_pool = set()

	for test_set in combos:
		available = meaning_sets[test_set[0]]
		for x in test_set[1:]:
			available = available.intersection(meaning_sets[x])
		word_pool = word_pool.union(available)
	
	return word_pool

def shuffle(words, n):
	for i in xrange(n):
		j = random.randint(i, len(words)-1)
		tmp = words[i]
		words[i] = words[j]
		words[j] = tmp
	return words[:n]

if __name__ == '__main__':
	print 'loading board file'
	if len(sys.argv) > 1:
		board_file = sys.argv[1]
		with open(board_file, 'r') as f:
			lines = f.read().split('\n')
			board = lines[0].split(' ')
			red = lines[1].split(' ')
			blue = lines[2].split(' ')
			black = lines[3].split(' ')
			other = [x for x in board if x not in red]
	else:
		with open('codewords.txt', 'r') as f:
			codewords = f.read().lower().split('\n')
			codewords = [x for x in codewords if x]
			board = shuffle(codewords, 25)
			red = shuffle(board, 9)
			blue = board[9:17]
			black = [board[17]]
			other = board[9:]

	print 'board :: {}'.format(board)
	print 'red :: {}'.format(red)
	print 'blue :: {}'.format(blue)
	print 'black :: {}'.format(black)

	print 'loading word meanings...'
	assoc = load_words('associations.txt')
	print 'creating meaning sets...'
	meaning_sets = {}
	for k, v in assoc.iteritems():
		meaning_sets[k] = set(v)

	print 'validating board'
	for word in board:
		if word not in meaning_sets:
			print '{} not known!'.format(word)
			sys.exit(1)
	for word in red + blue + black:
		if word not in board:
			print '{} is not on the board!'.format(word)
			sys.exit(1)

	combos = itertools.combinations(red, 6)
	word_pool = possible_words(combos, meaning_sets)
	
	print 'counting candidates'
	counts = []
	for x in word_pool:
		words = []
		other_words = []
		word_count = 0
		other_count = 0
		for b in red:
			if x in meaning_sets[b]:
				word_count += 1
				words.append(b)
		for b in other:
			if x in meaning_sets[b]:
				other_count += 1
				other_words.append(b)
	
		counts.append([word_count, -other_count, x, words, other_words])
	
	counts.sort()
	counts.reverse()
	for count in counts[:10]:
		print 'Distribution: ({}) W:{} / OW:{}'.format(count[2], count[0], count[1])
		other_words = count[4]
		other_word_pool = possible_words([other_words], meaning_sets)
		negative = other_word_pool.difference(word_pool)
		if negative:
			print 'Negative word: {}'.format(negative.pop())
			sys.exit(0)
