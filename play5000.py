# play5000.py

from graphics import*
from die import Die
from star import Star
from button import Button
from random import randint
import time

X = 800
Y = 500

GUIDANCES = ['You rolled no points!\nYour turn is over.', #0
             'Click dice to make\nyour selection.', #1
             'To score from a triple,\nyou must select 3+\nof that die.', #2
             'You must select\nat least 1 die', #3
             "That die can't score", #4
             "That's a bad roll" #5
             ]

DIECOLORS = [['white', 'black', 'red'], 
             ['black', 'red', 'red'], 
             ['navy', 'coral', 'yellow'],
             ['deep pink', 'midnight blue', 'white'],
             ['black', 'yellow', 'red'],
             ['white', 'blue', 'yellow'],
             ['dark violet', 'aquamarine', 'yellow']]

COLORINDEX = 0

def advanceColorIndex():
    global COLORINDEX
    if COLORINDEX == (len(DIECOLORS) - 1):
        COLORINDEX = 0
    else:
        COLORINDEX += 1


def main():
    menu = GraphWin('5000 Menu', X, Y)
    menu.setBackground('turquoise')
    die, stars, buttonList = drawMenu(menu)
    quit = False
    while not quit:
        for star in stars:
            star.twinkle()
        click = menu.checkMouse()
        if click is not None:
            choice = getMenuChoice(click, buttonList)
            if choice == 1:
                menu.close()
                playGame()
            elif choice == 2:
                displayInstructions()
            elif choice == 3:
                quit = True
                break
            else:
                if die.xMin < click.getX() < die.xMax and \
                        die.yMin < click.getY() < die.yMax:
                    die.undraw()
                    advanceColorIndex()
                    die.setDieColor(DIECOLORS[COLORINDEX][0])
                    die.setDotColor(DIECOLORS[COLORINDEX][1])
                    die.draw()
                else:
                    die.rollDie()
    

def drawMenu(win):
    font = 'helvetica'
    title, underline = createTitle(font, win)
    playButton = Button(X/4, Y - Y/2, Y/6, X/5, 'green', 5, 'black', 
                        'PLAY', int(X/25), 'black', font, 'bold', win)
    instructionsButton = Button(X/2, Y - Y/5, Y/6, X/4, 'dodger blue', 5, 'black', 
                        'INSTRUCTIONS', int(X/45), 'black', font, 'bold', win)
    quitButton = Button(X - X/4, Y - Y/2, Y/6, X/5, 'red', 5, 'black', 
                        'QUIT', int(X/25), 'black', font, 'bold', win)
    for obj in [title, underline, playButton, instructionsButton, quitButton]:
        obj.draw(win)
    stars = []
    for i in range(2):
        for j in range(2):
            x = (X/5) * (1 + 3*i)
            y = (Y/5) * (1 + 3*j)
            star = Star(x, y, 60, 'yellow', win)
            star.draw(win)
            stars.append(star)
    die = Die(win, X/2, Y/2, randint(1, 6), 80, DIECOLORS[COLORINDEX][0], 
              DIECOLORS[COLORINDEX][1], DIECOLORS[COLORINDEX][2], False)
    die.draw()
    return die, stars, [playButton, instructionsButton, quitButton]

def createTitle(face, win):
    title = Text(Point(X/2, Y/5), '5000')
    title.setFace(face)
    size = int(Y/14)
    if size < 5:
        title.setSize(5)
    elif size <= 36:
        title.setSize(size)
    else:
        title.setSize(36)
    title.setStyle('bold')
    underline = Line(Point(X/2 - 2.5*X/size, Y/5 + size), 
                     Point(X/2 + 2.5*X/size, Y/5 + size))
    underline.setWidth(3)
    return title, underline


def displayInstructions():
    size = 600
    inst = GraphWin('5000 Instructions', size, size)
    title = Text(Point(size/2, size/12), 'Instructions')
    title.setStyle('bold')
    title.setSize(int(size/30))
    title.setFill('blue')
    title.draw(inst)
    # file = open('instructions.txt', 'r')
    # body = Text(Point(size/2, size/2), file.read())
    # body.draw(inst)


#######################################################################################
# gameplay
#######################################################################################


def drawWinEles():
    win = GraphWin('Table', X, Y)
    win.setBackground('cyan')
    # draw backgrounds for text
    playerMat = Rectangle(Point(X/16, Y/10), Point(5*X/16, Y/3))
    playerMat.setFill('white')
    computerMat = playerMat.clone()
    computerMat.move(5*X/8, 0)
    playerBox = Rectangle(Point(X/16 + X/12, Y/5), Point(5*X/16 - X/12, Y/4))
    playerBox.setFill('light yellow')
    computerBox = playerBox.clone()
    computerBox.move(5*X/8, 0)
    for i in [playerMat, computerMat, playerBox, computerBox]:
        i.draw(win)
    # draw text items
    title = Text(Point(X/2, Y/10), '5000')
    playerText = Text(Point(3*X/16, Y/7), 'You')
    compText = Text(Point(13*X/16, Y/7), 'Computer')
    for i in [title, playerText, compText]:
        i.setSize(18)
        title.setSize(30)
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
    playerScoreText = getPlayerScoreText(playerScore)
    playerScoreText.draw(win)
    npcScoreText = getNpcScoreText(npcScore)
    npcScoreText.draw(win)

    # basic gameplay loop
    while playerScore < 5000 and npcScore < 5000:
        playerHighlight.draw(win)
        playerScore += playerTurn(win, playerScore, playerTurnScoreText, \
                                  playerButtons, guidance)
        playerScoreText.setText(str(playerScore))
        playerHighlight.undraw()
        if playerScore >= 5000:
            celebrateWin(win)
            break
        npcHighlight.draw(win)
        npcScore += npcTurn(win, guidance, npcTurnScoreText, playerScore, npcScore)
        npcScoreText.setText(str(npcScore))
        npcHighlight.undraw(win)
    if npcScore >= 5000:
        mournLoss(win)


#######################################################################################

        
def playerTurn(win, playerScore, playerTurnScoreText, \
                            playerButtons, guidance):
    # initialize variables
    numDice = 5
    fullScoringDice = [1]
    turnScore = 0
    askIfKeep = False
    keepButton = playerButtons[2]
    dice = []
    miniDice = []

    # draw player turn score text
    playerTurnScoreText.draw(win)

    # main loop
    turnOver = False
    while not turnOver:

        # draw roll button
        for ele in playerButtons[0]:
            ele.draw(win)
        # if conditions are met, allow the player to keep their score
        if askIfKeep:
            keepButton.draw(win)   
        # wait for click on roll button
        go = False
        while not go:
            click = win.getMouse()
            x, y = click.getX(), click.getY()
            if (X/2 - X/16 <= x <= X/2 + X/16) and (Y/6 <= y <= Y/4):
                go = True
                keepButton.undraw()
                for ele in playerButtons[0]:
                    ele.undraw()
                if dice:
                    for die in dice:
                        die.undraw()
            elif askIfKeep and keepButton.xMin < x < keepButton.xMax and \
                                    keepButton.yMin < y < keepButton.yMax:
                go = True
                turnOver = True
                break
        if turnOver:
            playerTurnScoreText.undraw()
            keepButton.undraw()
            for ele in playerButtons[0]:
                ele.undraw()
            for die in dice:
                die.undraw()
            break
        # roll dice and create list of ints representing the sides (1-6)
        dice = rollDie(win, numDice)
        rollList = diceToInt(dice)

        # manipulate a temporary list to see if the dice rolled can actually score
        tempList = fullScoringDice.copy()
        possibleTripleScore, tempList = calculateTriples(rollList, tempList)
        rollScore = countScore(rollList, tempList, possibleTripleScore)
        # if the dice cannot score, let the player know and end turn
        if rollScore == 0:
            turnOver = True
            time.sleep(0.5)
            guidance = warnPlayer(guidance, 0, win)
            guidance.draw(win)
            time.sleep(1.5)
            guidance.undraw()
            playerTurnScoreText.undraw()
            time.sleep(0.5)
            turnScore = 0
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
            tripleScore, fullScoringDice = calculateTriples(keptList, fullScoringDice)
            keptScore = countScore(keptList, fullScoringDice, tripleScore)
            # add roll score to turn score
            turnScore += keptScore
            # adjust turn score asset
            playerTurnScoreText.setText('Turn Score: %d' % (turnScore))
            # undraw all dice for reroll and redraw kept dice
            for die in keptDice:
                die.undraw()
            miniDice = drawMiniDice(keptDice, win)
            # once conditions are met, toggle allowance for the player to keep score
            if (playerScore + turnScore) >= 300:
                askIfKeep = True
            # if out of dice to roll, reset to rolling all of the dice
            if numDice == 0 and turnOver != True:
                for die in miniDice:
                    die.undraw()
                miniDice = []
                numDice = 5

    return turnScore

#######################################################################################

def warnPlayer(message, i, win):
    message.setText(GUIDANCES[i])
    message.setTextColor('red')
    return message


def getDieSelection(win, confirm, dice, tempList, fullScoringDice, guidance):
    confirm.draw(win)
    keepers = []
    selecting = True
    guidance.setText(GUIDANCES[1])
    guidance.setTextColor('black')
    guidance.draw(win)
    while selecting:
        reset = True
        click = win.getMouse()
        x, y = click.getX(), click.getY()
        if confirm.xMin < x < confirm.xMax and confirm.yMin < y < confirm.yMax:
            reset = False
            valid = True
            for die in dice:
                if die.isHighlighted:
                    keepers.append(die)
            nums = diceToInt(keepers)
            if keepers == []:
                warnPlayer(guidance, 3, win)
                valid = False
            for n in nums:
                if (n in tempList) and (n not in fullScoringDice) and \
                                        (n != 5) and nums.count(n) < 3:
                    warnPlayer(guidance, 2, win)
                    valid = False
            if valid:
              confirm.undraw()
              selecting = False 
              break
        else:
            for die in dice:
                if die.xMin < x < die.xMax and die.yMin < y < die.yMax:
                    reset = False
                    if die.side in tempList or die.side == 5:
                        die.toggleHighlight()
                        # set instructions player
                        guidance.setText(GUIDANCES[1])
                        guidance.setTextColor('black')
                    else:
                        badSelection(click, win, X/20)
                        guidance.setText(GUIDANCES[4])
                        guidance.setTextColor('red')
        if reset:
            guidance.setText(GUIDANCES[1])
            guidance.setTextColor('black')
    return keepers, nums


def drawMiniDice(dice, win):
    return


#######################################################################################


def npcTurn(win, guidance, npcTurnScoreText, playerScore, npcScore):
    time.sleep(1)
    numDice = 5
    fullScoringDice = ['1']
    turnScore = 0
    turnOver = False
    while not turnOver:
        time.sleep(2)
        rollList = rollDie(numDice)
        tripleScore, fullScoringDice = calculateTriples(rollList, fullScoringDice)
        keptList = []
        for die in rollList:
            if die in fullScoringDice or die == '5':
                keptList.append(die)
        rollScore = countScore(keptList, fullScoringDice, tripleScore)
        turnScore += rollScore
        numDice -= len(keptList)
        if rollScore == 0:
            time.sleep(0.5)
            guidance = warnPlayer(guidance, 5, win)
            guidance.draw(win)
            time.sleep(1.5)
            guidance.undraw()
            time.sleep(0.5)
            turnScore = 0
            turnOver = True
            break
        elif numDice == 0:
            numDice = 5
        elif (npcScore + turnScore) >= 300:
            numScoringDice = len(fullScoringDice) + 1
            if '5' in fullScoringDice:
                numScoringDice -= 1
            if numScoringDice < 4 and playerScore < 4500:
                if numDice == 1 or (numDice == 2 and turnScore >= 500) or \
                        (numDice == 3 and turnScore >= 1500):
                    turnOver = True
            elif 4000 < playerScore < (npcScore + turnScore) < 4800:
                turnOver = True
        print('Turn Score: ' + str(turnScore) + '\nComputer Score: ' + str(npcScore))
    return turnScore


#######################################################################################
# methods used by both playerTurn and npcTurn methods
#######################################################################################


def rollDie(win, numDice):
    dieSize = X/10
    locationList = getRollLocations(dieSize, numDice)
    dice = []
    for loc in locationList:
        die = Die(win, loc.getX(), loc.getY(), randint(1, 6), dieSize,
                  DIECOLORS[COLORINDEX][0], DIECOLORS[COLORINDEX][1],
                    DIECOLORS[COLORINDEX][2], False)
        die.draw()
        dice.append(die)
    return dice


def getRollLocations(size, n):
    locations = []
    xMinRoll = int(X/16 + size/2)
    xMaxRoll = int(X - X/16 - size/2)
    yMinRoll = int(Y/3 + Y/10 + size/2)
    yMaxRoll = int(Y - Y/16 - size/2)
    while n > 0:
        x, y = randint(xMinRoll, xMaxRoll), randint(yMinRoll, yMaxRoll)
        clear = True
        for point in locations:
            if abs(x - point.getX()) < (size + size/4) and \
                    abs(y - point.getY()) < (size + size/4):
                clear = False
        if clear:
            locations.append(Point(x, y))
            n -= 1
    return locations


def calculateTriples(dieList, fullScorers):
    tripleScore = 0
    for die in dieList:
        if dieList.count(die) >= 3:
            if die == 1:
                tripleScore = 1000
            elif die not in fullScorers:
                tripleScore = die * 100
                fullScorers.append(die)
            break
    return tripleScore, fullScorers


def countScore(dieList, fullScoringDice, tripleScore):
    score = 0
    for die in dieList:
        if die in fullScoringDice:
            score += 100
        elif die == 5:
            score += 50
    if tripleScore > 0:
        score += (tripleScore - 300)
    return score



#######################################################################################
# getters for assets created once, then manipulated
#######################################################################################


def getButtonSuite(win):
    confirmButton = Button(X/2, Y/5, Y/12, X/8, 'black', '3', 'white', \
                'Confirm', int(X/60), 'white', 'helvetica', 'bold', win)
    keepButton = Button(X/2, Y/3, Y/12, X/7, 'black', '3', 'white', \
                'Keep Dice', int(X/60), 'white', 'helvetica', 'bold', win)
    rollButton = Oval(Point(X/2 - X/16, Y/6), Point(X/2 + X/16, Y/4))
    rollButton.setFill('spring green')
    rollText = Text(Point(X/2, 5*Y/24), 'ROLL')
    rollText.setStyle('bold')
    rollText.setSize(int(X/60))
    return [rollButton, rollText], confirmButton, keepButton



def getBoxHighlight(x):
    highlight = Rectangle(Point(x - X/8, Y/10), Point(x + X/8, Y/3))
    highlight.setOutline('yellow')
    highlight.setWidth(5)
    return highlight


def getGuidanceText():
    guidance = Text(Point(X/2, Y/3), '__')
    guidance.setSize(int(X/45))
    guidance.setStyle('bold')
    return guidance


def getTurnScoreText(x):
    turnScoreText = Text(Point(x, Y/3 - Y/20), 'Turn Score: 0')
    turnScoreText.setSize(int(X/70))
    turnScoreText.setFace('courier')
    return turnScoreText

def getPlayerScoreText(playerScore):
    playerScoreText = Text(Point(3*X/16, 9*Y/40), str(playerScore))
    playerScoreText.setSize(int(X/45))
    playerScoreText.setStyle('bold')
    return playerScoreText

def getNpcScoreText(npcScore):
    npcScoreText = Text(Point(X - 3*X/16, 9*Y/40), str(npcScore))
    npcScoreText.setSize(int(X/45))
    npcScoreText.setStyle('bold')
    return npcScoreText



#######################################################################################
# reuseable methods
#######################################################################################


def getMenuChoice(click, buttons):
    x, y = click.getX(), click.getY()
    for i in range(len(buttons)):
        if buttons[i].xMin < x < buttons[i].xMax and \
                buttons[i].yMin < y < buttons[i].yMax:
            return i + 1
    return ''


def badSelection(click, win, size):
    r = size/2
    x, y = click.getX(), click.getY()
    line1 = Line(Point(x - r, y - r), Point(x + r, y + r))
    line2 = Line(Point(x + r, y - r), Point(x - r, y + r))
    for ele in [line1, line2]:
        ele.setWidth(size/5)
        ele.setFill('red')
        ele.draw(win)
    time.sleep(0.5)
    line1.undraw()
    line2.undraw()


def diceToInt(dice):
    intList = []
    for die in dice:
        intList.append(die.side)
    return intList


def getAllDice(win):
    allDice = []
    for i in [1, 2, 3, 4, 5, 6]:
        die = Die(win, X/2, Y/2, i, X/10, DIECOLORS[COLORINDEX][0], 
            DIECOLORS[COLORINDEX][1], DIECOLORS[COLORINDEX][2], False)
        allDice.append(die)
    return allDice


def randomColor():
    r = randint(0,255)
    g = randint(0,255)
    b = randint(0,255)
    color = color_rgb(r,g,b)
    return color



#######################################################################################
# endgame features
#######################################################################################


def celebrateWin(win):
    drawOverlay('green', win)
    winText = Text(Point(X/2, Y/2), 'YOU WON!!!')
    drawEndgameText(winText, win)
    giveOptions(win)

def mournLoss(win):
    drawOverlay('red', win)
    lossText = Text(Point(X/2, Y/2), 'YOU LOST :(')
    drawEndgameText(lossText, win)
    giveOptions(win)


def drawOverlay(color, win):
    if X > Y:
        r = Y/2
    else:
        r = X/2
    overlay = Circle(Point(X/2, Y/2), r)
    overlay.setFill(color)
    overlay.draw(win)

def drawEndgameText(text, win):
    text.setSize(30)
    text.setStyle('bold')
    text.draw(win)


def giveOptions(win):
    time.sleep(1)
    newGameButton = Button(X/2, Y/3, Y/7, X/6, 'cyan', 3, 'black', 
                'Play Again', int(X/50), 'black', 'helvetica', 'bold', win)
    quitButton = Button(X/2, Y - Y/3, Y/7, X/6, 'black', 3, 'white', 
                'QUIT', int(X/50), 'white', 'helvetica', 'bold', win)
    menuButton = Button(X/10, Y/10, Y/12, X/10, 'coral', 3, 'black', 
                '<= MENU', int(X/70), 'black', 'helvetica', 'bold', win)
    for button in [newGameButton, quitButton, menuButton]:
        button.draw(win)
    getEndgameChoice(win, [newGameButton, quitButton, menuButton])


def getEndgameChoice(win, buttons):
    close = False
    while not close:
        click = win.checkMouse()
        if click is not None:
            choice = getMenuChoice(click, buttons)
            if choice == 1:
                close = True
                win.close()
                playGame()
            elif choice == 2:
                close = True
                win.close()
            elif choice == 3:
                close = True
                win.close()
                main()

main()