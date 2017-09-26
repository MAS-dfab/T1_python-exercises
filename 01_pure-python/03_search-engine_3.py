folderpath = '../resources/mybooks/'
titles = ['austen-emma.txt',
    'austen-persuasion.txt',
    'austen-sense.txt',
    'bible-kjv.txt',
    'blake-poems.txt',
    'bryant-stories.txt',
    'burgess-busterbrown.txt',
    'carroll-alice.txt',
    'chesterton-ball.txt',
    'chesterton-brown.txt',
    'chesterton-thursday.txt',
    'edgeworth-parents.txt',
    'melville-moby_dick.txt',
    'milton-paradise.txt',
    'shakespeare-caesar.txt',
    'shakespeare-hamlet.txt',
    'shakespeare-macbeth.txt',
    'whitman-leaves.txt']

punctuation = '.,;:?!-_()"\'[]\\/{}*&<>'
numbers = '0123456789'
stopwords = ['the', 'to', 'and', 'he', 'she', 'her', 'him', 'is',
    'of', 'then', 'so', 'a', 'it', 'his', 'i', 'you', 'in', 'an',
    'on', 'at', 'for', 'that', 'my', 'was', 'with', 'be', 'not', 'as',
    'but', 'had', 'all', 'very', 'this', 'by', 'from', 'or', 'they', 'which']

for title in titles:
    f = open(folderpath + title, 'r')
    text = f.read()
    f.close()

    # demo print
    print(title)
    print('.....................................')
    #print(text[:500])
    print('.....................................')

    # cleaning up
    text = text.lower()
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')

    #before = len(text)
    for c in punctuation:
        text = text.replace(c,'')
    #after = len(text)
    #print('number of punctuation characters replaced: '+str(before-after))

    for c in numbers:
        text = text.replace(c, '')

    #print(text[:500])
    print('.....................................')

    # split into separate words
    words = text.split() # same as split(' ')

    words = [w for w in words if w not in stopwords]

    word_occurrences = {}
    # loop through all the words and count them
    for w in words:
        #if w in word_occurrences:
        #    word_occurrences[w] += 1
        #else:
        #    word_occurrences[w] = 1
        word_occurrences[w] = word_occurrences.get(w,0) + 1

    #for w in word_occurrences:
    #    print(w,word_occurrences[w])
    print('number of unique words in ' + title + ': '+str(len(word_occurrences)))

    c = 0
    for w in sorted(word_occurrences, key=word_occurrences.get, reverse=True):
        print(w,word_occurrences[w])
        c+=1
        if c>20:
            break
