MORSE = dict(zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ', [
    '.-', '-...', '-.-.', '-..', '.', '..-.', '--.', '....',
    '..', '.---', '-.-', '.-..', '--', '-.', '---', '.--.',
    '--.-', '.-.', '...', '-', '..-', '...-', '.--', '-..-',
    '-.--', '--..'
]))

# Read a file containing A-Z only English words, one per line.
WORDS = set(word.strip().upper() for word in open('./words.txt').readlines())
# A set of all possible prefixes of English words.
PREFIXES = set(word[:j+1] for word in WORDS for j in range(len(word)))

def translate(msg, c_sep=' ', w_sep=' / '):
    """Turn a message (all-caps space-separated words) into morse code."""
    return w_sep.join(c_sep.join(MORSE[c] for c in word)
                      for word in msg.split(' '))

def encode(msg):
    """Turn a message into timing-less morse code."""
    return translate(msg, '', '')

def c_trans(morse):
    """Construct a map of char transitions.

    The return value is a dict, mapping indexes into the morse code stream
    to a dict of possible characters at that location to where they would go
    in the stream. Transitions that lead to dead-ends are omitted.
    """
    result = [{} for i in range(len(morse))]
    for i_ in range(len(morse)):
        i = len(morse) - i_ - 1
        for c, m in MORSE.items():
            if i + len(m) < len(morse) and not result[i + len(m)]:
                continue
            if morse[i:i+len(m)] != m: continue
            result[i][c] = i + len(m)
    return result

def find_words(ctr, i, prefix=''):
    """Find all legal words starting from position i.

    We generate all possible words starting from position i in the
    morse code stream, assuming we already have the given prefix.
    ctr is a char transition dict, as produced by c_trans.
    """
    if prefix in WORDS:
        yield prefix, i
    if i == len(ctr): return
    for c, j in ctr[i].items():
        if prefix + c in PREFIXES:
            for w, j2 in find_words(ctr, j, prefix + c):
                yield w, j2

def w_trans(ctr):
    """Like c_trans, but produce a word transition map."""
    result = [{} for i in range(len(ctr))]
    for i_ in range(len(ctr)):
        i = len(ctr) - i_ - 1
        for w, j in find_words(ctr, i):
            if j < len(result) and not result[j]:
                continue
            result[i][w] = j
    return result

def shortest_sentence(wt):
    """Given a word transition map, find the shortest possible sentence.

    We find the sentence that uses the entire morse code stream, and has
    the fewest number of words. If there are multiple sentences that
    satisfy this, we return the one that uses the smallest number of
    characters.
    """
    result = [-1 for _ in range(len(wt))] + [0]
    words = [None] * len(wt)
    for i_ in range(len(wt)):
        i = len(wt) - i_ - 1
        for w, j in wt[i].iteritems():
            if result[j] == -1: continue
            if result[i] == -1 or result[j] + 1 + len(w) / 30.0 < result[i]:
                result[i] = result[j] + 1 + len(w) / 30.0
                words[i] = w
    i = 0
    result = []
    while i < len(wt):
        result.append(words[i])
        i = wt[i][words[i]]
    return result

def sentence_count(wt):
    result = [0] * len(wt) + [1]
    for i_ in range(len(wt)):
        i = len(wt) - i_ - 1
        for j in wt[i].itervalues():
            result[i] += result[j]
    return result[0]

msg = 'JACK AND JILL WENT UP THE HILL'
chal = '-.-----..-.-...-..-...---........-.-----.-.....-.-.----...'


#print sentence_count(w_trans(c_trans(encode(msg))))
#print shortest_sentence(w_trans(c_trans(encode(msg))))
#print sentence_count(w_trans(c_trans(chal)))
print(w_trans(c_trans(chal)))