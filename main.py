from tkinter import *
from random import randint
import time
from time import sleep
from math import cos

G = 6.67408 * (10 ** -11)
Sun = 1.9891 * 10 ** 30
Earth = 5.972 * 10 ** 24

class Object:
    def __init__(self, id, main, x, y, vx, vy, mass, image, star):
        self.id = id
        self.main = main
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = 0
        self.ay = 0
        self.mass = mass
        self.image = image
        self.star = star
    def draw(self, scale):
        x = self.x - 250
        y = self.y - 200
        x = 250 + (x / scale)
        y = 200 + (y / scale)
        self.main.canvas.create_image(x, y, anchor="center", image=self.main.images[self.image])

def inverse(x, isy=0):
    if isy:
        x = x - 200
        x = 200 + (x * main.scale)
    else:
        x = x - 250
        x = 250 + (x * main.scale)
    return x


class Main:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Solar System Simulation by Ron Lauterbach")
        self.canvas = Canvas(self.tk, height=500, width=500, highlightthickness=0)
        self.canvas.pack()
        self.objects = []
        self.time = time.time()
        self.tk.bind_all("<Button-1>", self.click)
        self.out = 0
        self.add = 0
        self.create = 0
        self.click1 = 0
        self.click2 = 0
        self.scale = 1
        self.down = 0
        self.button = 0
        self.pos = [0,0]
        self.zoomin = 0
        self.zoomout = 0
        images = ["", "m", "k", "g", "f", "a", "asteroid", "dwarf_planet", "terrestrial_planet", "gas_giant", "brown_dwarf"]
        self.images = [""]
        i = 1
        while i < len(images):
            self.images.append(PhotoImage(file=images[i] + ".gif"))
            i += 1
        self.example()
    def up(self, event):
        i = 0
        while i < len(self.objects):
            self.objects[i].y += 200 * self.scale
            i += 1
    def mainloop(self):
        while 1:
            self.canvas.delete("all")
            if not (self.add or self.create):
                self.update()
                self.canvas.create_rectangle(0, 0, 500, 400, fill="black", width=0)
                self.draw()
                self.canvas.create_rectangle(0, 400, 500, 500, fill="#3d80ee", width=0)
                self.canvas.create_rectangle(0, 400, 500, 403, fill="#aaaaaa", width=0)
                self.canvas.create_rectangle(10, 410, 90, 490, fill="#0d50bb", width=3)
                self.canvas.create_text(50, 450, text="+", font=("Courier", 50))
                self.canvas.create_rectangle(320, 410, 400, 490, fill="#0d50bb", width=3)
                self.canvas.create_text(360, 450, text="Zoom In", font=("Courier", 10))
                self.canvas.create_rectangle(410, 410, 490, 490, fill="#0d50bb", width=3)
                self.canvas.create_text(450, 450, text="Zoom Out", font=("Courier", 10))
                self.tk.update()
                self.tk.update_idletasks()
                self.out = 0
            elif self.create:
                self.out = 1
                self.canvas.create_rectangle(0, 0, 500, 400, fill="black", width=0)
                self.draw()
                self.canvas.create_rectangle(0, 400, 500, 500, fill="#3d80ee", width=0)
                if not self.click1:
                    self.canvas.create_text(250, 450, text="Click the screen to set the position of the object.", font=("Courier", 10, "bold"))
                    self.tk.update()
                else:
                    if not self.click2:
                        self.click2 = [0, 0]
                    else:
                        masses = [0, 0.3, 0.8, 1.1, 1.7, 3.2, 10 ** -15, 10**-8, 10 ** -6, 10**-4, 0.08]
                        self.objects.append(Object(len(self.objects), self, inverse(self.click1[0]), inverse(self.click1[1], 1), inverse(self.click2[0] - self.click1[0]), inverse(self.click2[1] - self.click2[1], 1), masses[self.create] * Sun, self.create, self.create <= 5)) #f
                        self.create = 0
                        self.click1 = 0
                        self.click2 = 0
                        self.add = 0
                self.tk.update()
            elif self.add:
                self.out = 1
                k = 50
                self.canvas.create_rectangle(0, 0, 500, 500, fill="#3d80ee", width=0)
                self.canvas.create_text(250, 30 + k, text="Stars", font=("Courier", 40, "bold"))
                self.canvas.create_rectangle(10, 10, 60, 60, fill="#bb0000")
                self.canvas.create_text(35, 35, text="X", font=("Courier", 40, "bold"))
                for i in range(5):
                    self.canvas.create_rectangle(98 * i + 15, 60 + k, 98 * i + 93, 138 + k, fill="#0d50bb", width=5)
                    self.canvas.create_image(54+ 98 * i, 99 + k, anchor="center", image=self.images[i+1])
                self.canvas.create_text(54, 150 + k, text="M-Type", font=("Courier", 20))
                self.canvas.create_text(152, 150 + k, text="K-Type", font=("Courier", 20))
                self.canvas.create_text(250, 150 + k, text="G-Type", font=("Courier", 20))
                self.canvas.create_text(348, 150 + k, text="F-Type", font=("Courier", 20))
                self.canvas.create_text(446, 150 + k, text="A-Type", font=("Courier", 20))
                j = 200
                self.canvas.create_text(250, 30 + k + j, text="Planets", font=("Courier", 40, "bold"))
                for i in range(5):
                    self.canvas.create_rectangle(98 * i + 15, 60 + k + j, 98 * i + 93, 138 + k + j, fill="#0d50bb", width=5)
                    self.canvas.create_image(54 + 98 * i, 99 + k + j, anchor="center", image=self.images[i+6])
                self.canvas.create_text(54, 150 + k + j, text="Asteroid", font=("Courier", 10))
                self.canvas.create_text(152, 150 + k + j, text="Dwarf Planet", font=("Courier", 10))
                self.canvas.create_text(250, 150 + k + j, text="Terrestrial Planet", font=("Courier",  6))
                self.canvas.create_text(348, 150 + k + j, text="Gas Giant", font=("Courier", 10))
                self.canvas.create_text(446, 150 + k + j, text="Brown Dwarf", font=("Courier", 10))
                self.tk.update()
    def click(self, event):
        self.down = 1
        if not self.create:
            boxes = []
            boxes.append(["add", 1, 10, 410, 90, 490, 0])
            boxes.append(["add", 0, 10, 10, 60, 60, 1])
            boxes.append(["create", 1, 98 * 0 + 15, 110, 98 * 0 + 93, 188, 1])
            boxes.append(["create", 2, 98 * 1 + 15, 110, 98 * 1 + 93, 188, 1])   
            boxes.append(["create", 3, 98 * 2 + 15, 110, 98 * 2 + 93, 188, 1])   
            boxes.append(["create", 4, 98 * 3 + 15, 110, 98 * 3 + 93, 188, 1])   
            boxes.append(["create", 5, 98 * 4 + 15, 310, 98 * 4 + 93, 188, 1])
            boxes.append(["create", 6, 98 * 0 + 15, 310, 98 * 0 + 93, 388, 1]) #planet
            boxes.append(["create", 7, 98 * 1 + 15, 310, 98 * 1 + 93, 388, 1])   
            boxes.append(["create", 8, 98 * 2 + 15, 310, 98 * 2 + 93, 388, 1])   
            boxes.append(["create", 9, 98 * 3 + 15, 310, 98 * 3 + 93, 388, 1])   
            boxes.append(["create", 10, 98 * 4 + 15, 310, 98 * 4 + 93, 388, 1])
            boxes.append(["zoomin", 1, 320, 410, 400, 490, 0])
            boxes.append(["zoomout", 1, 410, 410, 490, 490, 0])
            self.printinfo()
            for box in boxes:
                if event.x >= box[2] and event.x <= box[4] and event.y >= box[3] and event.y <= box[5] and ((not box[6] and not self.add) or (box[6] and self.add)):
                    exec("self." + box[0] + "=" + str(box[1]))
            if self.zoomin:
                self.scale /= 2
                self.zoomin = 0
            if self.zoomout:
                self.scale *= 2
                self.zoomout = 0
        else:
            self.click1 = [event.x, event.y]
    def update(self):
        if self.out:
            self.time = time.time()
        t = (time.time() - self.time) * 1000
        self.time = time.time()
        initial = self.objects
        for moved in initial:
            for applied in initial:
                if moved.id == applied.id:
                    continue
                d = (((applied.x - moved.x) ** 2) + ((applied.y - moved.y) ** 2)) ** (1/2)
                a = applied.mass / ((d) ** 2)
                if d < 300:
                    pass
                x = applied.x - moved.x
                y = applied.y - moved.y
                self.objects[moved.id].ax = a * cos(x / d)
                self.objects[moved.id].ay = a * cos(y / d)
                if moved.x > applied.x:
                    self.objects[moved.id].ax *= -1
                if moved.y > applied.y:
                    self.objects[moved.id].ay *= -1
                if self.objects[moved.id].ax > x:
                    self.objects[moved.id].ax = 0
                if self.objects[moved.id].ay > y:
                    self.objects[moved.id].ay = 0
                self.objects[moved.id].vx += self.objects[moved.id].ax * t  
                self.objects[moved.id].vy += self.objects[moved.id].ay * t
                self.objects[moved.id].x += moved.vx * t 
                self.objects[moved.id].y += moved.vy * t
    def draw(self):
        for objects in self.objects:
            objects.draw(self.scale)
    def new(self, x, y, vx, vy, m, img, isstar):
        self.objects.append(Object(len(self.objects), self, x, y, vx , vy, m, img, isstar))
    def example(self):
        return
        factor = 1
        self.new(250, 350, 0, 0, 0.01, 5, 1)
        self.new(100, 150, 0.01, 0, 0.01, 5, 0)
    def printinfo(self):
        return
        print("Start")
        for objects in self.objects:
            print(objects.x )
            print(objects.y)
            print(objects.vx)
            print(objects.vy)
            print(objects.ax)
            print(objects.ay)
            print("Next")

main = Main()
main.mainloop()
