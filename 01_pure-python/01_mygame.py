# set up some variables that we need for the game
secret = 'digitalfabrication'
guesses = []
trials = 0

# repeat asking for guesses as long as the there are less than
# 5 unsuccessful trials
while trials < 5:
    # prompt the player for input (python3: g = input('...'))
    g = raw_input('guess a letter: ')

    # sanitize input
    g = g.lower()

    # if the player enters more than one character, ask which one (index)
    ix = 0
    if len(g)>1:
        print('dear player, you entered more than one letter.')
        print(list(g))
        ix = raw_input('which one do you mean? ')
    ix = int(ix)
    g = g[ix]

    # if the letter typed by the player has already been guessed before,
    # let him/her guess another one, else add it to the list of guesses
    if g in guesses:
        print('you already tried ' + g)
        continue
    else:
        guesses.append(g)

    # test if the guessed letter is in the secret word
    # if yes, tell the the player how successful he/she was
    # if not, increase the number of trials and tell how many are left
    if g in secret:
        # count = 0
        # for c in secret:
        #     if c==g:
        #         count+=1
        sl = list(secret)
        c = sl.count(g)
        print('success, '+g+' appears '+str(c)+' times')
    else:
        trials += 1
        print('not there, '+str(5-trials)+' trials left')

    # put together a string with _ for still secret letters
    # and print it to the console
    out = ''
    for c in secret:
        if c in guesses:
            out += c
        else:
            out += '_'

    print(out)

    # if the player correctly guessed all the letters, announce WIN and exit
    if out==secret:
        print("YOU WIN!!!")
        break

# if still not correctly guessed after 5 trials, player loses
if trials==5:
    print('YOU LOSE!')
