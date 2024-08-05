# button.py

from graphics import*

class Button:
    def __init__(self, x, y, height, width, 
                 fillColor, borderWidth, borderColor, 
                 text, textSize, textColor, font, is3D, win):
        
        self.x = x
        self.y = y

        self.is3D = is3D

        self.height = height
        self.width = width
        self.xMin = self.x - self.width/2
        self.xMax = self.x + self.width/2
        self.yMin = self.y - self.height/2
        self.yMax = self.y + self.height/2

        self.fillColor = fillColor
        self.borderWidth = borderWidth
        self.borderColor = borderColor

        self.text = text
        if textSize > 36:
            textSize = 36
        elif textSize < 5:
            textSize = 5
        self.textSize = textSize
        self.textColor = textColor
        self.font = font
        self.style = 'bold'

        self.win = win

        self.rect = self.createRect()
        self.dimEles = self.make3D()
        self.text = self.createText()



    def isClicked(self, click):
        return self.xMin < click.getX() < self.xMax and \
            self.yMin < click.getY() < self.yMax
    


    def createRect(self):
        rect = Rectangle(Point(self.xMin, self.yMin), 
                         Point(self.xMax, self.yMax))
        rect.setFill(self.fillColor)
        rect.setWidth(self.borderWidth)
        rect.setOutline(self.borderColor)
        return rect

    def createText(self):
        text = Text(Point(self.x, self.y), self.text)
        text.setSize(self.textSize)
        text.setFace(self.font)
        text.setStyle(self.style)
        text.setTextColor(self.textColor)
        return text
    
    def make3D(self): # draws inner box and 'corner' lines
        # set variables for each corner of inner box
        x1 = self.x - 0.45*self.width
        y1 = self.y - 0.4*self.height
        x2 = self.x + 0.45*self.width
        y2 = self.y + 0.4*self.height 
        # set points in clockwise order starting at tope left
        p1 = Point(x1, y1)
        p2 = Point(x2, y1)
        p3 = Point(x2, y2)
        p4 = Point(x1, y2)
        # draw inner rectangle
        rect2 = Rectangle(p1, p3)
        rect2.setWidth(self.borderWidth*1.5)
        rect2.setOutline(self.borderColor)
        # establish corner lines
        line1 = Line(Point(self.xMin, self.yMin), p1)
        line2 = Line(Point(self.xMax, self.yMin), p2)
        line3 = Line(Point(self.xMax, self.yMax), p3)
        line4 = Line(Point(self.xMin, self.yMax), p4)
        for line in [line1, line2, line3, line4]:
            line.setWidth(self.borderWidth)
            line.setFill(self.borderColor)
        return [rect2, line1, line2, line3, line4]
    


    def draw(self, win):
        self.rect.draw(win)
        self.text.draw(win)
        if self.is3D:
            for ele in self.dimEles:
                ele.draw(win)
        
    def undraw(self):
        self.rect.undraw()
        self.text.undraw()
        if self.is3D:
            for ele in self.dimEles:
                ele.undraw()

    


    def toggle3D(self):
        if self.is3D:
            for ele in self.dimEles:
                ele.undraw()
        else:
            for ele in self.dimEles:
                ele.draw(self.win)
        self.is3D = not self.is3D



    def changeColor(self, newColor):
        self.undraw()
        self.color = newColor
        self.rect = self.createRect()
        self.draw(self.win)

    def changeBorderWidth(self, newWidth):
        self.undraw()
        self.borderWidth = newWidth
        self.rect = self.createRect()
        self.draw(self.win)

    def changeBorderColor(self, newColor):
        self.undraw()
        self.borderColor = newColor
        self.rect = self.createRect()
        self.draw(self.win)


    def changeText(self, newText):
        self.text.undraw()
        self.text = newText
        self.createText()
        self.draw(self.win)

    def changeTextColor(self, newColor):
        self.text.undraw()
        self.textColor = newColor
        self.createText()
        self.draw(self.win)

    def changeFont(self, newFont):
        self.text.undraw()
        self.font = newFont
        self.createText()
        self.draw(self.win)
    
    def changeStyle(self, newStyle):
        self.text.undraw()
        self.style = newStyle
        self.createText()
        self.draw(self.win)