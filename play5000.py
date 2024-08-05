# play5000.py

from graphics import*
from die import Die
from star import Star
from button import Button
from random import randint
from time import sleep
from math import sin, cos, radians
import os

# need to set the directory to where this file currently resides
current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
os.chdir(current_directory)


# set window size for scaling
X = 800
Y = 500


# dialogues from the computer to the player
DIALOGUES = ['You rolled no points!\nYour turn is over.', #0
             'Click dice to make\nyour selection.', #1
             'The entire triple\nmust be kept to score it.', #2
             'You must select\nat least 1 die.', #3
             "That die can't score.", #4
             ["That's a bad roll!", 
              "I guess I need\nmore practice.", 
              "I forgot to put on\nmy lucky socks today.", 
              "Apparently these dice\ndon't like me."] #5
             ]


# list of possible die colors [background, dots, highlight]
DIECOLORS = [['white', 'black', 'red'], 
             ['black', 'red', 'red'],
             ['yellow', 'navy', 'red'], 
             ['maroon', 'white', 'white'],
             ['deep pink', 'midnight blue', 'sea green'],
             ['navy', 'white', 'yellow'],
             ['orange red', 'sky blue', 'sea green'],
             ['black', 'white', 'red'],
             ['dodger blue', 'red', 'red'],
             ['forest green', 'purple', 'white'],
             ['purple', 'yellow', 'yellow'],
             ['white', 'blue', 'red'],
             ['dark violet', 'aquamarine', 'yellow']]

COLORINDEX = 0      # to be iterated

# method to set the index to the next set of colors
def advanceColorIndex():
    global COLORINDEX
    if COLORINDEX == (len(DIECOLORS) - 1):
        COLORINDEX = 0  # resets to zero when the end of the list is reached
    else:
        COLORINDEX += 1



# controls main menu
def main():
    # open window, set background
    menu = GraphWin('5000 Menu', X, Y)
    menu.setBackground('cyan')
    # draw window, save visual assets
    die, stars, buttonList = drawMenu(menu)

    # main loop - animations while looking for a click
    quit = False
    while not quit:
        # animate stars
        for star in stars:
            star.twinkle()
        # look for click
        click = menu.checkMouse()
        # if click is detected, call function that detects hits
        if click is not None:
            choice = getMenuChoice(click, buttonList)
            if choice == 1: # button list index 0
                menu.close()
                playGame()
                break
            elif choice == 2: # index 1
                displayInstructions()
            elif choice == 3: # index 2
                quit = True
                break
            else: # if no buttons clicked
                if die.isClicked(click):
                    die.undraw()
                    advanceColorIndex()
                    die.setDieColor(DIECOLORS[COLORINDEX][0])
                    die.setDotColor(DIECOLORS[COLORINDEX][1])
                    die.draw()
                else: # if click didn't hit a button or center die
                    currentSide = die.side
                    while die.side == currentSide: # ensures a change
                        die.rollDie() # shuffles the number on the die
    

# creates, draws, and returns visual assets used in the menu
def drawMenu(win):  # takes window as arg
    # set variables that are the same across buttons
    font = 'helvetica'
    textColor = 'black'
    lineColor = 'black'
    # construct title text object+
    title, underline = createTitle(font)
    # construct button objects
    playButton = Button(X/4, Y - Y/2, Y/6, X/5, 'green', round(X/200), lineColor, 
                        'PLAY', round(X/25), textColor, font, True, win)
    instructionsButton = Button(X/2, Y - Y/5, Y/6, X/4, 'dodger blue', round(X/200), lineColor, 
                        'INSTRUCTIONS', round(X/50), textColor, font, True, win)
    quitButton = Button(X - X/4, Y - Y/2, Y/6, X/5, 'red', round(X/200), lineColor, 
                        'QUIT', round(X/25), textColor, font, True, win)
    # draw buttons and title
    for obj in [title, underline, playButton, instructionsButton, quitButton]:
        obj.draw(win)
    # construct, draw, and save four stars in each quadrant
    stars = []
    for i in range(2):
        for j in range(2):
            x = (X/5) * (1 + 3*i)
            y = (Y/5) * (1 + 3*j)
            star = Star(x, y, 60, 'yellow', win)
            star.draw(win)
            stars.append(star)
    # construct and draw die
    die = Die(win, X/2, Y/2, randint(1, 6), X/10, DIECOLORS[COLORINDEX][0], 
              DIECOLORS[COLORINDEX][1], DIECOLORS[COLORINDEX][2], False)
    die.draw()
    return die, stars, [playButton, instructionsButton, quitButton]

# constructs title asset including underline
def createTitle(face):  # takes a font style as an arg
    #
    title = Text(Point(X/2, Y/5), '5000')
    title.setFace(face)
    size = round(Y/14)
    # account for minimum size depending on window size
    if size < 20:
        title.setSize(20)
    elif size <= 36:
        title.setSize(size)
    else: # if size > 36
        title.setSize(36) # set to library max
    title.setStyle('bold')
    # construct underline object
    underline = Line(Point(X/2 - 2.5*X/size, Y/5 + size), 
                     Point(X/2 + 2.5*X/size, Y/5 + size))
    underline.setWidth(3)
    # return both objects
    return title, underline


# pulls up window with gameplay instructions
def displayInstructions():
    # set window values
    x = 1000
    y = 600
    # construct and open window
    inst = GraphWin('5000 Instructions', x, y)
    # construct and draw title
    title = Text(Point(x/2, y/12), 'Instructions')
    title.setStyle('bold')
    title.setSize(int(y/30))
    title.setFill('blue')
    title.draw(inst)
    # read instructions from .txt
    file = open('instructions.txt', 'r')
    body = Text(Point(x/2, y/2 + Y/12), file.read())
    body.setFace('helvetica')
    body.setStyle('bold')
    body.draw(inst)


#######################################################################################
# gameplay + table
#######################################################################################


# draws many elements that will not be moved during gameplay
def drawWinEles():
    # construct and open window
    win = GraphWin('Table', X, Y)
    win.setBackground('cyan')
    # backgrounds for text and scores
    playerMat = Rectangle(Point(X/16, Y/10), Point(5*X/16, Y/3))
    playerMat.setFill('white')
    computerMat = playerMat.clone()
    computerMat.move(5*X/8, 0)
    # background boxes for total score
    playerBox = Rectangle(Point(X/16 + X/12, Y/5), Point(5*X/16 - X/12, Y/4))
    playerBox.setFill('light yellow')
    computerBox = playerBox.clone()
    computerBox.move(5*X/8, 0)
    # background for title
    titleBubble = Oval(Point(X/2 - X/10, Y/20), Point(X/2 + X/10, 3*Y/20))
    titleBubble.setFill('spring green')
    # draw all assets
    for i in [playerMat, computerMat, playerBox, computerBox, titleBubble]:
        i.draw(win)
    # construct and draw text items
    title = Text(Point(X/2, Y/10), '5000')
    playerText = Text(Point(3*X/16, Y/7), 'You')
    compText = Text(Point(13*X/16, Y/7), 'Computer')
    for i in [title, playerText, compText]:
        i.setSize(int(Y/28))
        title.setSize(int(Y/20))
        i.setStyle('bold')
        i.setFace('courier')
        i.draw(win)
    return win

#######################################################################################

def playGame():
    # make window
    win = drawWinEles()
    # set scores to 0
    playerScore = 0
    npcScore = 0
    # generate all the text etc. that can draw and undraw during each turn
    playerButtons = getButtonSuite(win)
    playerTurnScoreText = getTurnScoreText(3*X/16)
    npcTurnScoreText = getTurnScoreText(X - 3*X/16)
    guidance = getGuidanceText()
    playerHighlight = getBoxHighlight(3*X/16)
    npcHighlight = getBoxHighlight(X - 3*X/16)
    # generate and draw overall score assets
    playerScoreText = getTotalScoreText(playerScore, 3*X/16) 
    npcScoreText = getTotalScoreText(npcScore, X - 3*X/16)
    playerScoreText.draw(win)
    npcScoreText.draw(win)

    # basic gameplay loop
    while playerScore < 5000 and npcScore < 5000: # runs while no win has occured
        # draw highlight around player mat
        playerHighlight.draw(win)
        # cover small marks made by bug in graphics library undraw function
        coverMarks(win)
        # add the score after each turn to player's score
        playerScore += playerTurn(win, playerScore, playerTurnScoreText, \
                                  playerButtons, guidance)
        # change the text object to reflect new score
        playerScoreText.setText(str(playerScore))
        playerHighlight.undraw()
        # check to see if a win has been achieved
        if playerScore >= 5000:
            celebrateWin(win) # game-end function in case of win
            break
        # same mechanisms for computer's turn
        npcHighlight.draw(win)
        coverMarks(win)
        npcScore += npcTurn(win, guidance, npcTurnScoreText, playerScore, npcScore)
        npcScoreText.setText(str(npcScore))
        npcHighlight.undraw()
    # check allows program to exit gracefully
    if npcScore >= 5000: 
        mournLoss(win) # game-end function in case of loss
    

# covers small lines left by bug in library undraw() function
def coverMarks(win): 
    cover = Rectangle(Point(0, Y/3 + Y/10), Point(X, Y))
    cover.setFill('cyan')
    cover.setOutline('cyan')
    cover.draw(win)


#######################################################################################
# Player's turn
#######################################################################################

# Handles a single turn by the user
# Accepts window, current total score for player, and visual elements as args
# Returns the score for the turn
def playerTurn(win, playerScore, playerTurnScoreText, \
                            playerButtons, guidance):
    # initialize variables
    numDice = 5     # 5 dice = one hand of dice
    fullScoringDice = [1]   # at the start, only a 1 scores 100
    turnScore = 0
    askIfKeep = False # eligibility for player to end turn and keep score
    dice = []
    miniDice = []
    rollButton = playerButtons[0]
    # draw player turn score text
    playerTurnScoreText.setText('Turn Score: %d' % (turnScore))
    playerTurnScoreText.draw(win)

    # draw roll button, wait for click to initiate turn
    rollButton.draw(win)
    play = False
    while not play:
        click = win.getMouse()
        if rollButton.isClicked(click):
            play = True
            rollButton.undraw()

    # main loop
    turnOver = False
    while not turnOver:
        # roll dice and create list of ints representing the sides (1-6)
        dice = rollDie(win, numDice)
        rollList = diceToInt(dice)
        # manipulate a temporary list to see if the dice rolled can actually score
        tempList = fullScoringDice.copy()
        possibleTripleScore, tempList, multiTriple2 = \
                    calculateTriples(rollList, tempList)
        rollScore = countScore(rollList, tempList, 
                    possibleTripleScore, multiTriple2)
        # if the dice cannot score, let the player know and end turn
        if rollScore == 0:
            # change sentinel boolean
            turnOver = True
            turnScore = 0
            # handle end-of-turn GUI elements
            endTurn(guidance, DIALOGUES[0], [playerTurnScoreText, 
                                             dice, miniDice], win)
            break
        # if dice can score, get the selection of keepable dice from player
        else:
            # allow player to select dice then undraw instructions
            keptDice, keptList = getDieSelection(win, playerButtons[1],
                            dice, tempList, fullScoringDice, guidance)
            guidance.undraw()
            # adjust number of dice to reroll
            numDice -= len(keptList)
            # calculate actual roll score based on dice kept
            tripleScore, fullScoringDice, multiTriple2 = \
                calculateTriples(keptList, fullScoringDice)
            keptScore = countScore(keptList, fullScoringDice, 
                                   tripleScore, multiTriple2)
            # add roll score to turn score
            turnScore += keptScore
            # adjust turn score asset
            playerTurnScoreText.setText('Turn Score: %d' % (turnScore))
            # undraw all dice for reroll and redraw kept dice
            for die in keptDice:
                die.undraw()
            miniDice = drawMiniDice(miniDice, keptDice, True)
            # set boolean that triggers the availability of the keep dice functionality
            if playerScore > 0 or turnScore >= 300:
                askIfKeep = True
            # get a choice from the user
            turnOver = getButtonClick(win, playerButtons, dice, miniDice, askIfKeep)
            # if the user ends turn, undraw relevant objects
            if turnOver:
                undrawObjects([playerTurnScoreText, playerButtons, dice, miniDice])
                break
            # if out of dice to roll, reset to rolling all 5 dice (one 'hand')
            if numDice == 0 and turnOver != True:
                for die in miniDice:
                    die.undraw()
                miniDice = []
                numDice = 5
    # return current score to be saved in game score
    return turnScore


# Handles click by user on either roll or end turn buttons
# Accepts window, button, and die objects as args
# Last parameter is a boolean True iff player is allowed to end turn and retain score
# Returns boolean True iff turn is ended intentionally
def getButtonClick(win, playerButtons, dice, miniDice, askIfKeep):
    # assign names for buttons
    rollButton, endTurnButton = playerButtons[0], playerButtons[2]
    # draw roll button
    rollButton.draw(win)
    # if conditions are met, allow the player to keep their score
    if askIfKeep:
        endTurnButton.draw(win)   
    # set default outcome
    turnOver = False
    # loop waits for click on roll button
    go = False
    while not go:
        click = win.getMouse()
        if rollButton.isClicked(click):
            # change sentinel
            go = True
            # undraw button objects to prep for new roll
            undrawObjects(playerButtons)
            if dice: # accounts for first roll when list is empty
                for die in dice:
                    # undraws big dice for new roll
                    if die not in miniDice:
                        die.undraw()
                    # toggles highlight for mini dice
                    elif die.isHighlighted:
                        die.toggleHighlight()  
        # if player clicks on 'keep dice', end turn
        elif askIfKeep and endTurnButton.isClicked(click):
            go = True
            turnOver = True
            break
    return turnOver

#######################################################################################

# Handles selection of dice to keep by the user
# Accepts window, buttons, and dice objects + text object 'guidance'
# Accepts two lists of ints:
# tempList regulates what can be selected
# fullScoringDice updates based on what is actually kept
# Returns list of dice kept as die objects and list as ints
def getDieSelection(win, keepButton, dice, tempList, fullScoringDice, guidance):
    # draw button that allows player to confirm the dice they want to keep
    keepButton.draw(win)
    # draw instrctions for player to click dice to select them
    guidance.setText(DIALOGUES[1])
    guidance.setTextColor('black')
    guidance.draw(win)
    # while loop waits for click on either button or dice
    selecting = True
    while selecting:
        # boolean to reset instructional messgae
        # sets to true each time through loop (in case of stray clicks)
        reset = True
        click = win.getMouse()
        if keepButton.isClicked(click):
            # toggle boolean to keep error message up until next valid click
            reset = False
            # Call to function handling validity of the selection 
            # Compiles and returns lists of dice kept, the numbers associated,
            # and a boolean of whether keeping dice 
            keepers, nums, valid = handleKeepClick(dice, guidance, 
                                        tempList, fullScoringDice)
            # if the selection is valid, undraw button, exit loop
            if valid:
              keepButton.undraw()
              selecting = False
              break
        else: # if click is elsewhere, check if it's on a die
            for die in dice:
                if die.isClicked(click):
                    # returns boolean for wether the die can be kept
                    reset = handleDieClick(die, tempList, guidance, click, win)
        if reset:
            # reset instructions back to default (as opposed to error)
            guidance.setText(DIALOGUES[1])
            guidance.setTextColor('black')
    # return list of dice kept and the sides of said dice
    return keepers, nums


# Handles a click on the Keep Dice button
# Accepts a list of all dice for the hand (5 dice), and a text object (guidance)
# Accepts two lists of ints:
# tempList regulates what can be selected
# fullScoringDice updates based on what is actually kept
# Returns list of dice kept as die objects and list as ints,
# and a boolean for whether or not the button click is appropriate
def handleKeepClick(dice, guidance, tempList, fullScoringDice):
    # initialize variables
    valid = True
    keepers = []
    # append all selected die to list
    for die in dice:
        if die.isHighlighted:
            keepers.append(die)
    # handle click on keep button if no dice are selected
    if keepers == []:
        getWarning(guidance, DIALOGUES[3])
        valid = False
    # create list of numbers on selected dice
    nums = diceToInt(keepers)
    for n in nums:
        # case: a triple is rolled that is not a repeat of a prior triple
        # handles if in this case, the player has not selected the entire triple
        if (n in tempList) and (n not in fullScoringDice) and \
                                (n != 5) and nums.count(n) < 3:
            getWarning(guidance, DIALOGUES[2])
            valid = False
    # return both lists and boolean of whether button press is valid
    return keepers, nums, valid


# Handles whether or not a die is available to be kept
# Accepts the die clicked on, a list of dice that can be kept,
# a text object for communicating validity of selections,
# a click (point obj), and a window
def handleDieClick(die, tempList, guidance, click, win):
    # check if the die can score
    if die.side in tempList or die.side == 5:
        die.toggleHighlight()
        # set instructions player
        guidance.setText(DIALOGUES[1])
        guidance.setTextColor('black')
        return True
    else:
        # draw red X at point of click and explain the error
        badSelection(click, X/20, win)
        getWarning(guidance, DIALOGUES[4])



#######################################################################################
# computer's turn
#######################################################################################


# Handles a single turn by the computer
# Accepts window, visual elements, and scores for both players as args
# Returns total score for the turn
def npcTurn(win, guidance, npcTurnScoreText, playerScore, npcScore):
    sleep(0.5)
    # initialize variables
    numDice = 5
    fullScoringDice = [1]
    turnScore = 0
    dice = []
    miniDice = []
    # draw turn score text
    npcTurnScoreText.setText('Turn Score: %d' % (turnScore))
    npcTurnScoreText.draw(win)

    # main loop
    turnOver = False
    while not turnOver:
        sleep(1.5)
        # check if list is not empty (as in first roll)
        if dice:
            for die in dice:
                # undraw all the big dice
                if die not in miniDice:
                    die.undraw()
        # roll dice visually and calculate value of triples
        dice = rollDie(win, numDice)
        rollList = diceToInt(dice)
        tripleScore, fullScoringDice, multiTriple2 = \
            calculateTriples(rollList, fullScoringDice)
        keptList = []
        keptDice = []
        # keep all dice that score, append to list of dice and list of ints
        for die in dice:
            if die.side in fullScoringDice or die.side == 5:
                keptList.append(die.side)
                keptDice.append(die)
                die.toggleHighlight()
                sleep(0.5)
        # calculate scores from lists of ints
        # track bug case of multiple rolls of triple 2s in the same turn
        rollScore = countScore(keptList, fullScoringDice, tripleScore, multiTriple2)
        # adjust score for turn and display in GUI
        turnScore += rollScore
        npcTurnScoreText.setText('Turn Score: %d' % (turnScore))
        # adjust number of dice to be rerolled
        numDice -= len(keptList)
        # undraw selected big dice and redraw them as minis
        undrawObjects(keptDice)
        miniDice = drawMiniDice(miniDice, keptDice, False)
        # handle case of no points rolled
        if rollScore == 0:
            turnOver = True
            turnScore = 0
            endTurn(guidance, DIALOGUES[5][randint(0, 3)], 
                    [npcTurnScoreText, miniDice, dice], win)
            break
        # if the whole hand has been rolled, reset number of dice to 5
        # and undraw the hand of minis
        elif numDice == 0:
            numDice = 5
            undrawObjects(miniDice)
            miniDice = []
        # check if the computer can keep it's score
        elif (npcScore + turnScore) >= 300:
            turnOver = npcDecisionTree(fullScoringDice, turnScore, 
                                       npcScore, playerScore, numDice)
        # undraw objs if turn ends
        if turnOver:
            undrawObjects([npcTurnScoreText, dice, miniDice])
    # return score to be totalled
    return turnScore


# Case-by-case algo for whether th computer will keep its score and end turn
# Accepts list dice that score 100, current score for the turn,
# both players' total scores, and the number of dice left to roll as args
# Returns boolean for whether the turn will end
def npcDecisionTree(fullScoringDice, turnScore, npcScore, playerScore, numDice):
    # set int value for number of dice that can be kept
    numScoringDice = len(fullScoringDice)
    # check for absense of triple 5's before accounting for their scoring ability
    if 5 not in fullScoringDice:
        numScoringDice += 1
    # if the computer wins by keeping score, it will always end turn
    if (npcScore + turnScore) >= 5000:
        return True
    # plays safe/ends turn if approaching a win while player is sufficiently behind
    elif (npcScore + turnScore) >= 4500 and playerScore <= 3500 and \
                numScoringDice < 5 and numDice < 3:
        return True
    # cases for when half or fewer sides of dice can score
    # and player is not about to win
    elif numScoringDice < 4 and playerScore < 4500:
        # ends based on number of dice to roll and current turn score (risk-reward)
        if numDice == 1 or (numDice == 2 and turnScore >= 500) or \
                (numDice == 3 and turnScore >= 1500):
            return True
    # cases where 4 dice can score yet risk is still high with a lot to lose
    elif numScoringDice < 5 and numDice == 1 and turnScore >= 2500:
        # pushes for win only if the player is close to a win
        if playerScore < 4500:
            return True
        # will play safe in cases where it catches up in one turn 
        # and player has a decent chance on busting before winning next roll
        elif 4500 <= playerScore < 4750 and (npcScore + turnScore) > playerScore:
            return True
    # won't risk even a 1/6 chance bust on one die as long as it's winning
    elif numDice == 1 and numScoringDice < 6 and (npcScore + turnScore) > playerScore:
        return True
    # ends turn if the game is close but the computer is ahead
    # most other cases where this is a bad play are caught by prior ifs
    elif 4000 < playerScore < (npcScore + turnScore) < 4800:
        return True
    # if no cases catch a reason to end, it will reroll
    return False


#######################################################################################
# methods used by both player and computer turn sections
#######################################################################################


# Rolls dice (randomizes number and constructs based on locations)
# Returns list of all die objects
# Accepts window and int number of dice as args
def rollDie(win, numDice):
    # set size of dice based on window X-value
    dieSize = X/10
    # get random, non-overlapping locations
    locationList = getRollLocations(dieSize, numDice)
    # initialize, construct, draw, and append
    dice = []
    for loc in locationList:
        die = Die(win, loc.getX(), loc.getY(), randint(1, 6), dieSize,
                  DIECOLORS[COLORINDEX][0], DIECOLORS[COLORINDEX][1],
                    DIECOLORS[COLORINDEX][2], False)
        die.draw()
        dice.append(die)
    return dice

# Method that returns locations for dice being rolled
# Accepts size and number of dice as args
def getRollLocations(size, n):
    # initialize list
    locations = []
    # set border values so dice appear on screen
    xMin = int(X/16 + size/2)
    xMax = int(X - X/16 - size/2)
    yMin = int(Y/3 + Y/10 + size/2)
    yMax = int(Y - Y/16 - size/2)
    # loops through until it has a location for each die
    while n > 0:
        # generates random ints inside perimeter
        x, y = randint(xMin, xMax), randint(yMin, yMax)
        # check if die are overlapping
        clear = True
        for point in locations:
            if abs(x - point.getX()) < (size + size/4) and \
                    abs(y - point.getY()) < (size + size/4):
                clear = False
        # if die does not overlap with any others, it gets added to the list
        if clear:
            locations.append(Point(x, y))
            n -= 1  # iterate sentinel variable
    return locations


def drawMiniDice(priorMinis, newDice, isPlayer):
    # set basic relative size of mini dice and the margin between them
    size = X/25
    margin = X/80
    spacing = size + margin
    # account for whether it's the player's turn or the computer's
    if isPlayer == True:
        npcInc = 0
    else:
        npcInc = 5*X/8
    # establish starting position based on whose turn it is
    startX = X/16 + size/2 + npcInc
    # set factor for spacing based on what is already drawn
    n = len(priorMinis)
    # set attributes of each new die to be drawn and draw it
    for die in newDice:
        if not isPlayer:
            die.toggleHighlight()
        die.setSize(size)
        die.setLocation(startX + n * spacing, Y/3 + spacing/2)
        die.setBorderWidth(1)
        die.draw()
        sleep(0.3)
        n += 1 # iterate factor
    # prepare the return variable as the new list of drawn mini dice
    dice = priorMinis + newDice
    return dice


# Calulates and returns value of a roll of a triple
# Accepts int list of die values and list of dice nums that score 100
# Also returns potentially altered list of dice sides/faces scoring 100,
# and boolean that catches fringe case
def calculateTriples(dieList, fullScorers):
    # intitialize
    multiTriple2 = True
    tripleScore = 0
    # iterate through dice values
    for die in dieList:
        # checks if it appears 3+ times
        if dieList.count(die) >= 3:
            # scores 1000 if triples are 1s
            if die == 1:
                tripleScore = 1000
            # otherwise it scores the number on the die x100
            else:
                tripleScore = die * 100
                # append value/num of the triple to dice scoring 100
                if die not in fullScorers:
                    fullScorers.append(die)
                    # account for scoring error when player rolls 
                    # more than one triple of 2s in one turn
                    if die == 2:
                        multiTriple2 = False 
    return tripleScore, fullScorers, multiTriple2

# Method that returns the score for a roll
# Accepts list of dice rolled, updated list of dice scoring 100,
# score from triples, and a fringe case of multiple triple 2s in a turn
def countScore(dieList, fullScoringDice, tripleScore, multiTriple2):
    # intitialize
    score = 0
    for die in dieList:
        # add 100 for each die in list
        if die in fullScoringDice:
            score += 100
        # if a 5 is rolled and it's not in prior list, add 50
        elif die == 5:
            score += 50
    if tripleScore > 0:
        # add score from triple, accounting for the 300 already given above
        score += (tripleScore - 300)
    if tripleScore == 200 and multiTriple2: 
        # add in 100 if the player has already rolled a triple of 2s
        score += 100
    return score


# sets and returns text object to display error message, coloring it red
def getWarning(message, text):
    message.setText(text)
    message.setTextColor('red')
    return message


# Handles the end of a turn
# Accepts dialogue obj and text, objects to undraw, and window as args
def endTurn(guidance, text, objs, win):
    sleep(0.5)
    # draw a big red X on screen
    badSelection(Point(X/2, Y/2), X/2, win)
    sleep(0.5)
    # alert user of turn end
    guidance = getWarning(guidance, text)
    guidance.draw(win)
    sleep(1.5)
    undrawObjects([guidance, objs])
    sleep(0.5)
    


#######################################################################################
# getters for assets created once, then drawn/undrawn and/or manipulated
#######################################################################################


# accepts window as arg and returns button objects used in player's turn
def getButtonSuite(win):
    rollButton = Button(X/2, Y/4 - Y/50, Y/12, 2*X/17, 'white', round(X/400), 'black', \
                    'Roll', round(X/70), 'black', 'helvetica', True, win)
    keepButton = Button(X/2, Y/4 - Y/50, Y/12, 2*X/17, 'black', round(X/400), 'white', \
                    'Keep Dice', round(X/70), 'white', 'helvetica', True, win)
    endTurnButton = Button(X/2, Y/3, Y/12, 2*X/17, 'black', round(X/400), 'white', \
                    'End Turn', round(X/70), 'white', 'helvetica', True, win)
    return [rollButton, keepButton, endTurnButton]


# returns text object for dialogue/instructions
def getGuidanceText():
    guidance = Text(Point(X/2, Y/3), '__')
    guidance.setSize(int(X/45))
    guidance.setStyle('bold')
    return guidance


# accepts a center x value and returns yellow box around player mat
def getBoxHighlight(x):
    highlight = Rectangle(Point(x - X/8, Y/10), Point(x + X/8, Y/3))
    highlight.setOutline('yellow')
    highlight.setWidth(X/160)
    return highlight


# accepts a center x value and returns a text object for score on current turn
def getTurnScoreText(x):
    turnScoreText = Text(Point(x, Y/3 - Y/20), 'Turn Score: 0')
    turnScoreText.setSize(int(X/70))
    turnScoreText.setFace('courier')
    return turnScoreText


# accpets a score and returns text object for the total score of player
def getTotalScoreText(score, x):
    scoreText = Text(Point(x, 9*Y/40), str(score))
    scoreText.setSize(int(X/45))
    scoreText.setStyle('bold')
    return scoreText



#######################################################################################
# other reuseable methods
#######################################################################################


# accepts a list of any objects and unpacks/undraws
def undrawObjects(objList):
    # undraw all objects passed in
    for obj in objList:
        if isinstance(obj, (list, tuple)):
            undrawObjects(obj)
            # recursive call to undraw elements in list
        else:
            obj.undraw()
    # if asked to undraw something that's not drawn, it will do nothing


# Accepts a click and a list of button objects and 
# Returns an int representing the position in the list of the button clicked
def getMenuChoice(click, buttons):
    for i in range(len(buttons)):
        if buttons[i].isClicked(click):
            return i + 1
    return ''


# Accepts a click (point), an int for size, and a window as args
# Draws and undraws a red X based on given size and position of click
def badSelection(click, size, win):
    r = size/2
    x, y = click.getX(), click.getY()
    # construct two lines based on size and center
    line1 = Line(Point(x - r, y - r), Point(x + r, y + r))
    line2 = Line(Point(x + r, y - r), Point(x - r, y + r))
    for ele in [line1, line2]:
        ele.setWidth(size/5)
        ele.setFill('red')
        ele.draw(win)
    sleep(0.5)
    line1.undraw()
    line2.undraw()


# takes a list of dice and converts it to a list of its values
def diceToInt(dice):
    intList = []
    for die in dice:
        intList.append(die.side)
    return intList


# takes win as arg and returns list of dice 1-6 at center position
def getAllDice(win):
    allDice = []
    for i in [1, 2, 3, 4, 5, 6]:
        die = Die(win, X/2, Y/2, i, X/20, DIECOLORS[COLORINDEX][0], 
            DIECOLORS[COLORINDEX][1], DIECOLORS[COLORINDEX][2], False)
        allDice.append(die)
    return allDice


# returns a color based on random rgb values
def randomColor():
    r = randint(0,255)
    g = randint(0,255)
    b = randint(0,255)
    color = color_rgb(r,g,b)
    return color



#######################################################################################
# endgame features
#######################################################################################


# accepts window arg and handles calls to won-game end features
def celebrateWin(win):
    drawOverlay('green', win)
    winText = Text(Point(X/2, Y/2), 'YOU WON!!!')
    drawEndgameText(winText, win)
    giveOptions(win)

# accepts window arg and handles calls to lost-game end features
def mournLoss(win):
    drawOverlay('red', win)
    lossText = Text(Point(X/2, Y/2), 'YOU LOST :(')
    drawEndgameText(lossText, win)
    giveOptions(win)


# accepts a color and window and draws an overlay of that color
def drawOverlay(color, win):
    background = Rectangle(Point(0, 0), Point(X, Y))
    background.setFill('cyan')
    background.setOutline('cyan')
    background.draw(win)
    if X > Y:
        r = Y/2
    else:
        r = X/2
    overlay = Circle(Point(X/2, Y/2), r)
    overlay.setFill(color)
    overlay.draw(win)

# accepts a text object and a window, and formats/draws that text obj
def drawEndgameText(text, win):
    text.setSize(30)
    text.setStyle('bold')
    text.draw(win)


# accepts window and draws nav buttons for user
def giveOptions(win):
    sleep(1)
    newGameButton = Button(X/2, Y/3, Y/7, X/6, 'cyan', round(X/400), 'black', 
                'Play Again', round(X/50), 'black', 'helvetica', True, win)
    quitButton = Button(X/2, Y - Y/3, Y/7, X/6, 'black', round(X/400), 'white', 
                'QUIT', round(X/50), 'white', 'helvetica', True, win)
    menuButton = Button(X/10, Y/10, Y/11, X/8, 'coral', round(X/800), 'black', 
                '<= MENU', round(X/70), 'black', 'helvetica', True, win)
    for button in [newGameButton, quitButton, menuButton]:
        button.draw(win)
    # call function to handle selection and animations
    getEndgameChoice(win, [newGameButton, quitButton, menuButton])


# Accepts an angle in degrees, a list of dice and stars, and a window
# Draws each obj in each list based on position based on given angle
def circleCycle(ang, dice, stars, win):
    # set radius based on size of overlay circle and dice
    r = Y/2 - dice[0].size
    for i in range(len(dice)):
        # polar coords formula w/conversion to rads
        x = X/2 + r * cos(radians(ang + 60*i))
        y = Y/2 + r * sin(radians(ang + 60*i))
        dice[i].setLocation(x, y)
        dice[i].draw()
    for i in range(len(stars)):
        x = X/2 + r * cos(radians(ang + 30 + 60*i))
        y = Y/2 + r * sin(radians(ang + 30 + 60*i))
        stars[i].setLocation(x, y)
        stars[i].draw(win)


# takes win arg and returns list of dice and stars
def getAnimationElements(win):
    # initialize
    stars = []
    # call method that returns dice 1-6
    dice = getAllDice(win)
    # set random color
    for die in dice:
        die.setDieColor(randomColor())
    # construct and append stars
    for i in range(6):
        star = Star(X, Y, X/20, 'yellow', win)
        stars.append(star)
    return dice, stars



# Accepts window and list of buttons as args
# Loops through animations while waiting for a click on a button
def getEndgameChoice(win, buttons):
    # get assets
    dice, stars = getAnimationElements(win)
    # initialize angle for starting position of assets
    ang = 0
    # loop for animations and clicks
    close = False
    while not close:
        # undraw then redraw in a new position
        undrawObjects([dice, stars]) # does nothing first time through
        circleCycle(ang, dice, stars, win)
        # reset angle to zero if it will hit a full turn 
        # (avoid too large int if left running)
        if ang == 355:
            ang = 0
        else:
            ang += 5
        # look for click
        click = win.checkMouse()
        if click is not None:
            # call function that handles hitboxes
            choice = getMenuChoice(click, buttons)
            if choice == 1: # replay button clicked
                close = True
                win.close()
                playGame()
            elif choice == 2: # quit button clicked
                close = True
                win.close()
                break
            elif choice == 3: # menu button clicked
                close = True
                win.close()
                main()



main()