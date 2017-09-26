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

punctuation = '.,;:?!-_()"\'[]\\/{}'
numbers = '0123456789'
for title in titles:
    f = open(folderpath + title, 'r')
    text = f.read()
    f.close()

    # demo print
    print(title)
    print('.....................................')
    print(text[:500])
    print('.....................................')

    # cleaning up
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')

    #before = len(text)
    for p in punctuation:
        text = text.replace(p,'')
    #after = len(text)
    #print('number of punctuation characters replaced: '+str(before-after))

    for n in numbers:
        text = text.replace(n, '')

    print(text[:500])
    print('.....................................')
