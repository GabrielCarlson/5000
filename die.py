# die.py

from graphics import*
from time import sleep
from random import randint

class Die:
    def __init__(self, window, x, y, side, size, 
                 dieColor, dotColor, highlightColor, isHighlighted):
        
        self.win = window
        self.x = x
        self.y = y
        self.side = side
        self.size = size
        self.dieColor = dieColor
        self.dotColor = dotColor
        self.highlightColor = highlightColor
        
        self.isHighlighted = isHighlighted

        self.borderWidth = 3

        r = self.size/2
        self.xMin = self.x - r
        self.xMax = self.x + r
        self.yMin = self.y - r
        self.yMax = self.y + r

        self.body = self.createBody()
        self.dots = self.createDots()
        self.highlight = self.createHighlight()




    def isClicked(self, click):
        return self.xMin < click.getX() < self.xMax and \
            self.yMin < click.getY() < self.yMax



    def move(self, x, y):
        self.undraw()
        self.x += x
        self.y += y
        self.recreateAttributes()
        self.draw()



    def recreateAttributes(self):
        r = self.size/2
        self.xMin = self.x - r
        self.xMax = self.x + r
        self.yMin = self.y - r
        self.yMax = self.y + r
        self.body = self.createBody()
        self.dots = self.createDots()
        self.highlight = self.createHighlight()
                

        
    def setWindow(self, newWin):
        self.win = newWin
        self.recreateAttributes()

    def setLocation(self, x, y):
        self.x = x
        self.y = y
        self.recreateAttributes()

    def setSide(self, n):
        self.side = n
        self.dots = self.createDots()
        
    def setSize(self, s):
        self.size = s
        self.recreateAttributes()

    def setDieColor(self, color):
        self.dieColor = color
        self.body = self.createBody()

    def setDotColor(self, color):
        self.dotColor = color
        self.dots = self.createDots()
    
    def setHighlightColor(self, color):
        self.highlightColor = color
        self.highlight = self.createHighlight()

    def setBorderWidth(self, newWidth):
        self.borderWidth = newWidth
        self.body = self.createBody()

    def toggleHighlight(self):
        if self.isHighlighted:
            self.highlight.undraw()
        else:
            self.highlight.draw(self.win)
        self.isHighlighted = not self.isHighlighted



    def create(self):
        self.body = self.createBody()
        self.dots = self.createDots()
        self.highlight = self.createHighlight()
    
    def createBody(self):
        r = self.size/2
        body = Rectangle(Point(self.x - r, self.y - r), 
                         Point(self.x + r, self.y + r))
        body.setWidth(self.borderWidth)
        body.setFill(self.dieColor)
        return body

    def createDots(self):
        p = self.size/4
        x, y = self.x, self.y
        dot1 = self.createDot(x, y)
        dot2 = self.createDot(x + p, y - p)
        dot3 = self.createDot(x + p, y + p)
        dot4 = self.createDot(x - p, y + p)
        dot5 = self.createDot(x - p, y - p)
        if self.side == 1:
            dots = [dot1]
        elif self.side == 2:
            dots = [dot2, dot4]
        elif self.side == 3:
            dots = [dot1, dot3, dot5]
        elif self.side == 4:
            dots = [dot2, dot3, dot4, dot5]
        elif self.side == 5:
            dots = [dot1, dot2, dot3, dot4, dot5]
        else:
            d = 0.85 * p
            dot11 = self.createDot(x + d, y)
            dot22 = self.createDot(x - d, y)
            dot33 = self.createDot(x + d, y + d)
            dot44 = self.createDot(x + d, y - d)
            dot55 = self.createDot(x - d, y + d)
            dot66 = self.createDot(x - d, y - d)
            dots = [dot11, dot22, dot33, dot44, dot55, dot66]
        return dots
    
    def createDot(self, x, y):
        dot = Circle(Point(x, y), self.size/17)
        dot.setFill(self.dotColor)
        if self.dieColor != 'white':
            dot.setOutline(self.dotColor)
        return dot

    def createHighlight(self):
        d = self.size
        highlight = Rectangle(Point(self.x - d/2, self.y - d/2), 
                              Point(self.x + d/2, self.y + d/2))
        highlight.setWidth(d/20)
        highlight.setOutline(self.highlightColor)
        return highlight



    def draw(self):
        self.body.draw(self.win)
        self.drawDots()
        if self.isHighlighted:
            self.highlight.draw(self.win)
    
    def drawDots(self):
        for dot in self.dots:
            dot.draw(self.win)


    
    def undraw(self):
        self.body.undraw()
        self.undrawDots()
        if self.isHighlighted:
            self.highlight.undraw()

    def undrawDots(self):
        for dot in self.dots:
            dot.undraw()


    def rollDie(self):
        s = randint(1, 6)
        self.undrawDots()
        time.sleep(0.08)
        self.setSide(s)
        self.drawDots()
        time.sleep(0.08)