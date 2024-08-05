# star.py

from graphics import*

class Star:
    def __init__(self, x, y, size, color, win):
        self.x = x
        self.y = y
        self.scale = size
        self.color = color
        self.win = win
        self.star = self.createStar()

    def createStar(self):
        x = self.x
        y = self.y
        s = self.scale
        pt0 = Point(x, y - s/2)
        pt1 = Point(x - s/8, y - s/8)
        pt2 = Point(x - s/1.9, y - s/8)
        pt3 = Point(x - s/5, y + s/10)
        pt4 = Point(x - s/3, y + s/2)
        pt5 = Point(x, y + s/4)
        pt6 = Point(x + s/3, y + s/2)
        pt7 = Point(x + s/5, y + s/10)
        pt8 = Point(x + s/1.9, y - s/8)
        pt9 = Point(x + s/8, y - s/8)
        star = Polygon(pt0, pt1, pt2, pt3, pt4, 
                       pt5, pt6, pt7, pt8, pt9)
        star.setFill(self.color)
        star.setOutline(self.color)
        return star

    def draw(self, win):
        self.star.draw(win)

    def undraw(self):
        self.star.undraw()

    def move(self, x, y):
        self.undraw()
        self.x += x
        self.y += y
        self.star = self.createStar()
        self.draw(self.win)

    def changeScale(self, size):
        self.undraw()
        self.scale = size
        self.star = self.createStar()
        self.draw(self.win)

    def setLocation(self, x, y):
        self.x = x
        self.y = y
        self.star = self.createStar()

    def twinkle(self):
        biggest = self.scale
        smallest = self.scale/2
        while self.scale > smallest:
            self.changeScale(0.9 * self.scale)
            time.sleep(0.005)
        while self.scale < biggest:
            self.changeScale(1.1 * self.scale)
            time.sleep(0.005)
            if self.scale > biggest:
                self.scale = biggest
                break
            
