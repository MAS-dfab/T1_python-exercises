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
for title in titles:
    f = open(folderpath + title, 'r')
    text = f.read()
    f.close()
    print(title)
    print('.....................................')
    print(text[:500])
    print('.....................................')
