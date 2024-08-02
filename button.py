# button.py

from graphics import*

class Button:
    def __init__(self, x, y, height, width, 
                 fillColor, borderWidth, borderColor, 
                 text, textSize, textColor, font, style, win):
        
        self.x = x
        self.y = y

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
        self.textSize = textSize
        self.textColor = textColor
        self.font = font
        self.style = style

        self.win = win

        self.rect = self.createRect()
        self.text = self.createText()


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


    def draw(self, win):
        self.rect.draw(win)
        self.text.draw(win)
        
    def undraw(self):
        self.rect.undraw()
        self.text.undraw()
    

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