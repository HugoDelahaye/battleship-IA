# -*- coding: utf-8 -*-
from tkinter import *
from random import randint
from copy import deepcopy
import numpy as np
import string


class App():
    def __init__(self, parent):
        self.root = parent
        self.pixels = 40
        self.width = 11*self.pixels
        self.gameframe1 = Frame(self.root)
        self.gameframe1.pack()
        Label(self.gameframe1, text="Joueur 1").pack()
        self.message = StringVar()
        self.message.set('')
        Label(self.gameframe1, textvariable=self.message).pack()
        self.canvas11 = Canvas(self.gameframe1, width=self.width, height=self.width, bg='white')
        self.canvas11.pack(side=LEFT, padx=20)
        self.canvas12 = Canvas(self.gameframe1, width=self.width, height=self.width, bg='white')
        self.canvas12.pack(side=RIGHT, padx=20)
        self.buttonframe = Frame(self.root)
        self.buttonframe.pack(pady=10)
        Button(self.buttonframe, text='New Game', command=self.new_game).pack(side=LEFT, padx=10)
        Button(self.buttonframe, text='Place Ships', command=self.place_ships).pack(side=LEFT, padx=10)
        Button(self.buttonframe, text='Start Game', command=self.start_game).pack(side=LEFT, padx=10)
        self.gameframe2 = Frame(self.root)
        self.gameframe2.pack()
        Label(self.gameframe2, text="Joueur 2").pack()
        self.canvas21 = Canvas(self.gameframe2, width=self.width, height=self.width, bg='white')
        self.canvas21.pack(side=LEFT, padx=20)
        self.canvas22 = Canvas(self.gameframe2, width=self.width, height=self.width, bg='white')
        self.canvas22.pack(side=RIGHT, padx=20)
        self.new_game()
        
    def run(self):
        self.root.mainloop()
        
    def draw_lines(self):
        for i in range(12):
            self.canvas11.create_line(i*self.pixels, 0, i*self.pixels, self.width, fill='black')
            self.canvas11.create_line(0, i*self.pixels, self.width, i*self.pixels, fill='black')
            self.canvas21.create_line(i*self.pixels, 0, i*self.pixels, self.width, fill='black')
            self.canvas21.create_line(0, i*self.pixels, self.width, i*self.pixels, fill='black')
            self.canvas12.create_line(i*self.pixels, 0, i*self.pixels, self.width, fill='black')
            self.canvas12.create_line(0, i*self.pixels, self.width, i*self.pixels, fill='black')
            self.canvas22.create_line(i*self.pixels, 0, i*self.pixels, self.width, fill='black')
            self.canvas22.create_line(0, i*self.pixels, self.width, i*self.pixels, fill='black')
        
    def new_game(self):
        self.canvas11.delete("all")
        self.canvas12.delete("all")
        self.canvas21.delete("all")
        self.canvas22.delete("all")
        self.ships = [5,4,3,3,2]
        self.lastx = 0
        self.lasty = 0
        self.rotation = 0
        self.indice = 0
        self.table1 = [[0 for i in range(10)] for j in range(10)]
        self.table2 = [[0 for i in range(10)] for j in range(10)]
        self.ships1 = []
        self.ships2 = []
        self.draw_lines()
        self.buttons1 = [[0 for i in range(10)] for j in range(10)]
        self.buttons2 = [[0 for i in range(10)] for j in range(10)]
        self.IA_shots = [[0 for i in range(10)] for j in range(10)]
        self.remaining_ships = self.ships
        self.battlegrid = [[0 for i in range(10)] for j in range(10)]
        for i in range(1,11):
            self.canvas11.create_text(self.pixels/2, i*self.pixels+self.pixels/2, text=str(i-1), font="Arial 12", fill="black")
            self.canvas11.create_text(i*self.pixels+self.pixels/2, self.pixels/2, text=string.ascii_uppercase[i-1], font="Arial 12", fill="black")
            self.canvas21.create_text(self.pixels/2, i*self.pixels+self.pixels/2, text=str(i-1), font="Arial 12", fill="black")
            self.canvas21.create_text(i*self.pixels+self.pixels/2, self.pixels/2, text=string.ascii_uppercase[i-1], font="Arial 12", fill="black")
            self.canvas12.create_text(self.pixels/2, i*self.pixels+self.pixels/2, text=str(i-1), font="Arial 12", fill="black")
            self.canvas12.create_text(i*self.pixels+self.pixels/2, self.pixels/2, text=string.ascii_uppercase[i-1], font="Arial 12", fill="black")
            self.canvas22.create_text(self.pixels/2, i*self.pixels+self.pixels/2, text=str(i-1), font="Arial 12", fill="black")
            self.canvas22.create_text(i*self.pixels+self.pixels/2, self.pixels/2, text=string.ascii_uppercase[i-1], font="Arial 12", fill="black")
            for j in range(1,11):
                self.buttons1[i-1][j-1] = Button(self.canvas12, command=lambda x=(i-1, j-1): self.shoot(x))
                self.canvas12.create_window(i*self.pixels+self.pixels/2, j*self.pixels+self.pixels/2, height=0.9*self.pixels, width=0.9*self.pixels, window=self.buttons1[i-1][j-1])
                self.buttons1[i-1][j-1]['state'] = 'disabled'
                self.buttons1[i-1][j-1]['relief'] = 'flat'
                self.buttons2[i-1][j-1] = Button(self.canvas22)
                self.canvas22.create_window(i*self.pixels+self.pixels/2, j*self.pixels+self.pixels/2, height=0.9*self.pixels, width=0.9*self.pixels, window=self.buttons2[i-1][j-1])
                self.buttons2[i-1][j-1]['state'] = 'disabled'
                self.buttons2[i-1][j-1]['relief'] = 'flat' 
        
    def place_ships(self):
        self.canvas11.bind_all("<Motion>",self.motion)
        self.canvas11.bind_all("<MouseWheel>",self.rotate)
        self.canvas11.bind_all("<Button-1>",self.place_ship)
        if self.indice>=len(self.ships):
            self.canvas11.unbind_all("<Motion>")
            self.canvas11.unbind_all("<MouseWheel>")
            self.canvas11.unbind_all("<Button-1>")
            for i in self.ships:
                r = randint(0,1)
                if r==0:
                    while True:
                        m,n = randint(0,9-i+1),randint(0,9)
                        x,y = (m+1)*self.pixels,(n+1)*self.pixels
                        emplacement1 = np.array(self.table2)[np.ix_([m+l for l in range(i)],[n])]
                        if [1] in emplacement1:
                            continue
                        self.canvas21.create_rectangle(x, y, x+i*self.pixels, y+self.pixels, outline='black', fill='gray', width=3)
                        for j in range(i):
                            self.table2[m+j][n] = 1
                        self.ships2.append([[m+j,n,1] for j in range(i)])
                        break
                if r==1:
                    while True:
                        m,n = randint(0,9),randint(0,9-i+1)
                        x,y = (m+1)*self.pixels,(n+1)*self.pixels
                        emplacement2 = np.array(self.table2)[m],[np.ix_([n+l for l in range(i)])]
                        if 1 in emplacement2[0]:
                            continue
                        self.canvas21.create_rectangle(x, y, x+self.pixels, y+i*self.pixels, outline='black', fill='gray', width=3)
                        for j in range(i):
                            self.table2[m][n+j] = 1
                        self.ships2.append([[m,n+j,1] for j in range(i)])
                        break  
                self.draw_lines()     
        
    def motion(self,event):
        x,y = self.pixels*(event.x/self.pixels), self.pixels*(event.y/self.pixels)
        m,n = x/self.pixels-1,y/self.pixels-1
        try:
            if (x==self.lastx and y==self.lasty) and (self.pixels<=x and self.pixels<=y):
                if self.rotation==0:
                    emplacement1 = np.array(self.table1)[np.ix_([m+i for i in range(self.ships[self.indice])],[n])]
                    if x<=(11-self.ships[self.indice])*self.pixels and [1] not in emplacement1:
                        self.canvas11.create_rectangle(x, y, x+self.ships[self.indice]*self.pixels, y+self.pixels, outline='red')
                if self.rotation==1:
                    emplacement2 = np.array(self.table1)[np.ix_([m],[n+i for i in range(self.ships[self.indice])])]
                    if y<=(11-self.ships[self.indice])*self.pixels and 1 not in emplacement2[0]:
                        self.canvas11.create_rectangle(x, y, x+self.pixels, y+self.ships[self.indice]*self.pixels, outline='red')
            else:
                self.draw_lines()
        except IndexError:
            pass
        self.lastx = x
        self.lasty = y
        
    def rotate(self,event):
        if event.delta>0:
            self.rotation = 0
        else:
            self.rotation = 1
        self.draw_lines()
        
    def place_ship(self,event):
        x,y = self.pixels*(event.x/self.pixels), self.pixels*(event.y/self.pixels)
        m,n = x/self.pixels-1,y/self.pixels-1
        try:
            if self.pixels<=x and self.pixels<=y:
                if self.rotation==0:
                    emplacement1 = np.array(self.table1)[np.ix_([m+i for i in range(self.ships[self.indice])],[n])]
                    if x<=(11-self.ships[self.indice])*self.pixels and [1] not in emplacement1:
                        self.canvas11.create_rectangle(x, y, x+self.ships[self.indice]*self.pixels, y+self.pixels, outline='black', fill='gray', width=3)
                        for i in range(self.ships[self.indice]):
                            self.table1[m+i][n] = 1
                        self.ships1.append([[m+j,n,1] for j in range(self.ships[self.indice])])
                        self.indice += 1
                if self.rotation==1:
                    emplacement2 = np.array(self.table1)[np.ix_([m],[n+i for i in range(self.ships[self.indice])])]
                    if y<=(11-self.ships[self.indice])*self.pixels and 1 not in emplacement2[0]:
                        self.canvas11.create_rectangle(x, y, x+self.pixels, y+self.ships[self.indice]*self.pixels, outline='black', fill='gray', width=3)
                        for j in range(self.ships[self.indice]):
                            self.table1[m][n+j] = 1
                        self.ships1.append([[m,n+j,1] for j in range(self.ships[self.indice])]) 
                        self.indice += 1
        except IndexError:
            pass
        self.place_ships()
        
    def start_game(self):
        self.message.set("Start")
        for x in range(10):
            for y in range(10):
                self.buttons1[x][y]['state'] = 'normal'
                self.buttons1[x][y]['relief'] = 'raised'
                self.buttons2[x][y]['state'] = 'normal'
                self.buttons2[x][y]['relief'] = 'raised'
        
    def shoot(self,xy):
        x,y = xy[0],xy[1]
        self.buttons1[x][y]['state'] = 'disabled'
        self.buttons1[x][y]['relief'] = 'flat' 
        self.buttons1[x][y]['text'] = 'x' 
        self.buttons1[x][y]['disabledforeground'] = 'red'
        self.buttons1[x][y]['font'] = 'Arial 12'
        self.canvas21.create_text((x+1)*self.pixels+self.pixels/2, (y+1)*self.pixels+self.pixels/2, text='x', font="Arial 12", fill="red")
        if self.table2[x][y]==1:
            self.message.set('Touché !')
            self.buttons1[x][y]['bg'] = 'black'
            self.canvas21.create_oval((x+1)*self.pixels+5, (y+1)*self.pixels+5, (x+1)*self.pixels+self.pixels-5, (y+1)*self.pixels+self.pixels-5, outline='black', fill='orange', width=0)
            self.canvas21.create_text((x+1)*self.pixels+self.pixels/2, (y+1)*self.pixels+self.pixels/2, text='x', font="Arial 12", fill="red")
            for ship in self.ships2:
                for case in ship:
                    if x==case[0] and y==case[1]:
                        case[2] = -1
                        touched_ship = self.ships2[self.ships2.index(ship)]
            status = -1
            for case in touched_ship:
                if case[2]==1:
                    status = 1
            if status==-1:
                self.ships2.remove(touched_ship)
                self.canvas21.create_rectangle((touched_ship[0][0]+1)*self.pixels+1, (touched_ship[0][1]+1)*self.pixels+1, (touched_ship[-1][0]+2)*self.pixels-1, (touched_ship[-1][1]+2)*self.pixels-1, fill='brown')
                self.message.set('Bateau de longeur '+str(len(touched_ship))+' coulé !')
                if self.ships2==[]:
                    self.message.set('Gagné !')
                    self.won()
        elif (x+1<=9 and self.table2[x+1][y]==1) or (y+1<=9 and self.table2[x][y+1]==1) or (x-1>=0 and self.table2[x-1][y]==1) or (y-1>=0 and self.table2[x][y-1]==1): 
            self.message.set('En vue')
            self.buttons1[x][y]['bg'] = 'gray'
        else:
            self.buttons1[x][y]['bg'] = 'blue'
            self.message.set("Dans l'eau")
        self.IA()
        
    def IA(self):
        while True:
            x,y = randint(0,9),randint(0,9)
            proba = [[0 for i in range(10)] for j in range(10)]
            for i in range(10):
                for j in range(10):
                    for ship in self.remaining_ships:
                        proba = self.ship_fits(i,j,ship,self.battlegrid,proba,self.IA_shots)
            proba = np.reshape(proba,100)
            coord = list(proba).index(max(list(proba)))
            x,y = coord/10,coord%10
            if self.IA_shots[x][y]==1:
                continue
            self.IA_shots[x][y] = 1
            self.buttons2[x][y]['state'] = 'disabled'
            self.buttons2[x][y]['relief'] = 'flat' 
            self.buttons2[x][y]['text'] = 'x' 
            self.buttons2[x][y]['disabledforeground'] = 'red'
            self.buttons2[x][y]['font'] = 'Arial 12'
            self.canvas11.create_text((x+1)*self.pixels+self.pixels/2, (y+1)*self.pixels+self.pixels/2, text='x', font="Arial 12", fill="red")
            if self.table1[x][y]==1:
                self.buttons2[x][y]['bg'] = 'black'
                self.battlegrid[x][y] = 'ship'
                self.canvas11.create_oval((x+1)*self.pixels+5, (y+1)*self.pixels+5, (x+1)*self.pixels+self.pixels-5, (y+1)*self.pixels+self.pixels-5, outline='black', fill='orange', width=0)
                self.canvas11.create_text((x+1)*self.pixels+self.pixels/2, (y+1)*self.pixels+self.pixels/2, text='x', font="Arial 12", fill="red")
                for ship in self.ships1:
                    for case in ship:
                        if x==case[0] and y==case[1]:
                            case[2] = -1
                            touched_ship = self.ships1[self.ships1.index(ship)]
                status = -1
                for case in touched_ship:
                    if case[2]==1:
                        status = 1
                if status==-1:
                    self.ships1.remove(touched_ship)
                    self.canvas11.create_rectangle((touched_ship[0][0]+1)*self.pixels+1, (touched_ship[0][1]+1)*self.pixels+1, (touched_ship[-1][0]+2)*self.pixels-1, (touched_ship[-1][1]+2)*self.pixels-1, fill='brown')
                    self.remaining_ships.remove(len(touched_ship))
                    for case in touched_ship:
                        self.battlegrid[case[0]][case[1]] = 'sunk'
                    if self.ships1==[]:
                        self.message.set('Perdu !')
                        self.loss()
            elif (x+1<=9 and self.table1[x+1][y]==1) or (y+1<=9 and self.table1[x][y+1]==1) or (x-1>=0 and self.table1[x-1][y]==1) or (y-1>=0 and self.table1[x][y-1]==1):
                self.buttons2[x][y]['bg'] = 'gray'
                self.battlegrid[x][y] = 'sight'
            else:
                self.buttons2[x][y]['bg'] = 'blue'
                self.battlegrid[x][y] = 'water'
            break
    
    def ship_fits(self,x,y,ship,grid,proba,shots):
        fits_vertical = True
        fits_horizontal = True
        for i in range(ship):
            if x+i>9 or grid[x+i][y]=='water' or grid[x+i][y]=='sight' or grid[x+i][y]=='sunk' or shots[x+i][y]==1:
                fits_horizontal = False
            if y+i>9 or grid[x][y+i]=='water' or grid[x][y+i]=='sight' or grid[x][y+i]=='sunk' or shots[x][y+i]==1:
                fits_vertical = False
            if (x+1<=9 and y+i<=9 and grid[x+1][y+i]=='water') or (x-1>=0 and y+i<=9 and grid[x-1][y+i]=='water') or (0<=y+i-1<=9 and grid[x][y+i-1]=='water') or (y+i+1<=9 and grid[x][y+i+1]=='water'):
                fits_vertical = False
            if (x+i<=9 and y+1<=9 and grid[x+i][y+1]=='water') or (x+i<=9 and y-1>=0 and grid[x+i][y-1]=='water') or (0<=x+i-1<=9 and grid[x+i-1][y]=='water') or (x+i+1<=9 and grid[x+i+1][y]=='water'):
                fits_horizontal = False
        if fits_vertical==True:
            for i in range(ship):
                proba[x][y+i] += 1
        if fits_horizontal==True:
            for i in range(ship):
                proba[x+i][y] += 1
        for i in range(ship):
            if ((x+i<=9 and grid[x+i][y]=='ship') or (x-i>=0 and grid[x-i][y]=='ship')) and shots[x][y]==0:
                proba[x][y] += 10
        for i in range(ship):
            if ((y+i<=9 and grid[x][y+i]=='ship') or (y-i>=0 and grid[x][y-i]=='ship')) and shots[x][y]==0:
                proba[x][y] += 10
        if ((x+1<=9 and grid[x+1][y]=='sight') or (x-1>=0 and grid[x-1][y]=='sight')) and shots[x][y]==0:
                proba[x][y] += 2
        if ((y+1<=9 and grid[x][y+1]=='sight') or (y-1>=0 and grid[x][y-1]=='sight')) and shots[x][y]==0:
                proba[x][y] += 2
        return proba
        
    def loss(self):
        lose = Toplevel()
        lose.title('Perdu !')
        Label(lose, text='Vous avez perdu.').pack()
        def fermerlose():
            lose.destroy()
            self.new_game()
        f = Frame(lose)
        Button(f, text="En effet, rejouons.", command=fermerlose).pack()
        f.pack()
        
    def won(self):
        win = Toplevel()
        win.title('Gagné !')
        Label(win, text='Vous avez gagné.').pack()
        def fermerwin():
            win.destroy()
            self.new_game()
        f = Frame(win)
        Button(f, text="En effet, rejouons.", command=fermerwin).pack()
        f.pack()   
            
app = App(Tk())
app.run()
        