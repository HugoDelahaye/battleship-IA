# -*- coding: utf-8 -*-
from tkinter import *
from random import randint
from copy import deepcopy
import numpy as np
import math
import time
import threading
from PIL import ImageGrab
from PIL import Image



def norm_func(x):             
    return 1.0/(1+math.exp(-x))   #sigmoïde
    
def der_norm_func(x):
    y = math.exp(-x)               #dérivée de la sigmoïde
    return y/(1+y)**2
    

    
class App():
    def __init__(self, parent):
        self.root = parent
        self.root.bind('<Right>', lambda event: app._right(self.table,self.scorevar.get(),True))
        self.root.bind('<Left>', lambda event: app._left(self.table,self.scorevar.get(),True))
        self.root.bind('<Down>', lambda event: app._down(self.table,self.scorevar.get(),True))
        self.root.bind('<Up>', lambda event: app._up(self.table,self.scorevar.get(),True))
        self.size = 4
        self.pixels = 80
        self.width = self.size*self.pixels
        self.table = [[0 for i in range(self.size)] for j in range(self.size)]
        self.score = 0
        self.scorevar = StringVar()
        self.scorevar.set(self.score)
        self.gameframe = Frame(self.root)
        self.gameframe.pack()
        self.canvas = Canvas(self.gameframe, width=self.width, height=self.width, bg='white')
        self.canvas.pack()
        self.scoreframe = Frame(self.root)
        self.scoreframe.pack()
        Label(self.scoreframe, text="Score :").pack(side=LEFT)
        Label(self.scoreframe, textvariable=self.scorevar).pack(side=LEFT)
        AIb = Button(self.scoreframe, text="AI", command=self.IA)
        AIb.pack(side=RIGHT, pady=20, padx=20)
        restartb = Button(self.scoreframe, text="Restart", command=self.restartb)
        restartb.pack(side=RIGHT, pady=20, padx=20)
        self.spawn_cells(3,True,self.table,self.score,True)
        self.draw_canvas()
        
    def run(self):
        self.root.mainloop()
        
    def draw_canvas(self):
        self.canvas.delete("all")
        for i in range(1,self.size):
            self.canvas.create_line(i*self.pixels, 0, i*self.pixels, self.width)
            self.canvas.create_line(0, i*self.pixels, self.width, i*self.pixels)
        for x in range(self.size):
            for y in range(self.size):
                if self.table[x][y]==2:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#ff0')
                if self.table[x][y]==4:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#fe0')
                if self.table[x][y]==8:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#fd0')
                if self.table[x][y]==16:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#fc0')
                if self.table[x][y]==32:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#fb0')
                if self.table[x][y]==64:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#fa0')
                if self.table[x][y]==128:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#f90')
                if self.table[x][y]==256:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#f80')
                if self.table[x][y]==512:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#f70')
                if self.table[x][y]==1024:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#f60')
                if self.table[x][y]==2048:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#f50')
                if self.table[x][y]==4096:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#f40')
                if self.table[x][y]==8192:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#f30')
                if self.table[x][y]==16384:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#f20')
                if self.table[x][y]==32768:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#f10')
                if self.table[x][y]==65536:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#f00')
                if self.table[x][y]==131072:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#e00')
                if self.table[x][y]==262144:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#d00')
                if self.table[x][y]==524288:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#c00')
                if self.table[x][y]==1048576:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#b00')
                if self.table[x][y]==2097152:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#a00')
                if self.table[x][y]==4194304:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#900')
                if self.table[x][y]==8388608:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#800')
                if self.table[x][y]==16777216:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#700')
                if self.table[x][y]==33554432:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#600')
                if self.table[x][y]==67108864:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#500')
                if self.table[x][y]==134217728:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#400')
                if self.table[x][y]==268435456:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#300')
                if self.table[x][y]==536870912:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#200')
                if self.table[x][y]==1073741824:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#100')
                if self.table[x][y]==2147483648:
                    self.canvas.create_rectangle(x*self.pixels, y*self.pixels, x*self.pixels+self.pixels, y*self.pixels+self.pixels, fill='#000')
                if self.table[x][y]!=0:
                    self.canvas.create_text(x*self.pixels+self.pixels/2, y*self.pixels+self.pixels/2, text=self.table[x][y], font="Arial 16", fill="black")
        
    def spawn_cells(self,n,change,table,score,update):
        espace_libre = False
        for x in range(self.size):
            for y in range(self.size):
                if table[x][y]==0:
                    espace_libre = True
        if espace_libre==True: 
            if change==True:
                for i in range(n):
                    while True:
                        x,y = randint(0,self.size-1),randint(0,self.size-1)
                        v = randint(1,4)
                        if v<4:
                            v = 2
                        if table[x][y]!=0:
                            continue
                        table[x][y] = v
                        break
        else:
            table,score = self.restart(table,score,update)
        return table,score
    
    def restartb(self):
        self.restart(self.table,self.score,True)         
                               
    def restart(self,table,score,update):
        if update==True:
            self.scorevar.set(0)
            self.table = [[0 for i in range(self.size)] for j in range(self.size)]
            self.spawn_cells(3,True,self.table,score,update)
            self.draw_canvas()
        score = 0
        table = [[0 for i in range(self.size)] for j in range(self.size)]
        table,score = self.spawn_cells(3,True,table,score,update)
        return table,score
    
    def _right(self,table,score,update_score):
        table_copy = deepcopy(table)
        for x in reversed(range(self.size)):
            for y in range(self.size):
                if table[x][y]!=0:
                    s = x
                    while s<self.size-1:
                        if table[s+1][y]!=0 and table[s][y]==table[s+1][y]:
                            table[s+1][y] = 2*table[s+1][y]
                            table[s][y] = 0
                            score = int(score) + table[s+1][y]
                            s += 1
                            break
                        elif table[s+1][y]!=0:
                            break
                        else:
                            table[s+1][y] = table[s][y]
                            table[s][y] = 0
                            s += 1
        if table_copy!=table:                   
            table,score = self.spawn_cells(1,True,table,score,update_score)
        else:
            table,score = self.spawn_cells(1,False,table,score,update_score) 
        if update_score==True:
            self.scorevar.set(score)    
            self.draw_canvas()
        return table,score
        
    def _left(self,table,score,update_score):
        table_copy = deepcopy(table)
        for x in range(self.size):
            for y in range(self.size):
                if table[x][y]!=0:
                    s = x
                    while s>0:
                        if table[s-1][y]!=0 and table[s][y]==table[s-1][y]:
                            table[s-1][y] = 2*table[s-1][y]
                            table[s][y] = 0
                            score = int(score) + table[s-1][y]
                            s -= 1
                            break
                        elif table[s-1][y]!=0:
                            break
                        else:
                            table[s-1][y] = table[s][y]
                            table[s][y] = 0
                            s -= 1
        if table_copy!=table:                   
            table,score = self.spawn_cells(1,True,table,score,update_score)
        else:
            table,score = self.spawn_cells(1,False,table,score,update_score) 
        if update_score==True:
            self.scorevar.set(score)    
            self.draw_canvas()
        return table,score
        
    def _down(self,table,score,update_score):
        table_copy = deepcopy(table)
        for x in range(self.size):
            for y in reversed(range(self.size)):
                if table[x][y]!=0:
                    s = y
                    while s<self.size-1:
                        if table[x][s+1]!=0 and table[x][s]==table[x][s+1]:
                            table[x][s+1] = 2*table[x][s+1]
                            table[x][s] = 0
                            score = int(score) + table[x][s+1]
                            s += 1
                            break
                        elif table[x][s+1]!=0:
                            break
                        else:
                            table[x][s+1] = table[x][s]
                            table[x][s] = 0
                            s += 1
        if table_copy!=table:                   
            table,score = self.spawn_cells(1,True,table,score,update_score)
        else:
            table,score = self.spawn_cells(1,False,table,score,update_score) 
        if update_score==True:
            self.scorevar.set(score)    
            self.draw_canvas()
        return table,score
        
    def _up(self,table,score,update_score):
        table_copy = deepcopy(table)
        for x in range(self.size):
            for y in range(self.size):
                if table[x][y]!=0:
                    s = y
                    while s>0:
                        if table[x][s-1]!=0 and table[x][s]==table[x][s-1]:
                            table[x][s-1] = 2*table[x][s-1]
                            table[x][s] = 0
                            score = int(score) + table[x][s-1]
                            s -= 1
                            break
                        elif table[x][s-1]!=0:
                            break
                        else:
                            table[x][s-1] = table[x][s]
                            table[x][s] = 0
                            s -= 1
        if table_copy!=table:                   
            table,score = self.spawn_cells(1,True,table,score,update_score)
        else:
            table,score = self.spawn_cells(1,False,table,score,update_score) 
        if update_score==True:
            self.scorevar.set(score)    
            self.draw_canvas()
        return table,score

    def IA(self):
        score1 = self.scorevar.get()
        score2 = self.scorevar.get()
        second = False
        third = False
        while True:
            table_act = deepcopy(self.table)
            n_moves = (self.size**2-sum([self.table[i].count(0) for i in range(self.size)]))/2-2
            if n_moves<4:
                n_moves = 4
            if n_moves>7:
                n_moves = 7
            #n_moves = 5
            score_act = int(self.scorevar.get())
            scores = 4**n_moves*[0]
            for i in range(4**n_moves):
                move_suite = np.base_repr(i, base=4, padding=n_moves)[-n_moves:]
                table = deepcopy(table_act)
                score = score_act
                for move in move_suite:
                    if move=='0':
                        table,score = self._right(table,score,False) 
                    if move=='1':
                        table,score = self._left(table,score,False) 
                    if move=='2':
                        table,score = self._down(table,score,False) 
                    if move=='3':
                        table,score = self._up(table,score,False)
                    if score<score_act or table==table_act:
                        break
                scores[i] = score
                
            next_move1 = np.base_repr(scores.index(max(scores)), base=4, padding=n_moves)[-n_moves:][0]
            
            scores_moy = [sum(scores[:4**n_moves/4]),sum(scores[4**n_moves/4:4**n_moves/2]),sum(scores[4**n_moves/2:3*4**n_moves/4]),sum(scores[3*4**n_moves/4:])]    
            next_move2 = str(scores_moy.index(max(scores_moy)))
            
            score1 = self.scorevar.get()
            lose_win = [0 if i<int(score1) else 1 for i in scores]
            lose_win_moy = [sum(lose_win[:4**n_moves/4]),sum(lose_win[4**n_moves/4:4**n_moves/2]),sum(lose_win[4**n_moves/2:3*4**n_moves/4]),sum(lose_win[3*4**n_moves/4:])]
            next_move3 = str(lose_win_moy.index(max(lose_win_moy)))
            if second==True:
                lose_win_moy = [0 if m==lose_win_moy.index(max(lose_win_moy)) else lose_win_moy[m] for m in range(4)]
                next_move3 = str(lose_win_moy.index(max(lose_win_moy)))
            if third==True:
                lose_win_moy = [0 if m==lose_win_moy.index(max(lose_win_moy)) else lose_win_moy[m] for m in range(4)]
                next_move3 = str(lose_win_moy.index(max(lose_win_moy)))
            
            next_move = next_move1
            #print next_move
            '''snapshot = ImageGrab.grab()
            save_path = "C:\\Users\\Hugo\\Documents\\python\\2048_screenshots\\screenshot_"+str(s)+".jpg"
            snapshot.save(save_path)'''
            table_act_act = deepcopy(self.table)
            if next_move=='0':
                table,score = self._right(self.table,self.scorevar.get(),True) 
            if next_move=='1':
                table,score = self._left(self.table,self.scorevar.get(),True) 
            if next_move=='2':
                table,score = self._down(self.table,self.scorevar.get(),True) 
            if next_move=='3':
                table,score = self._up(self.table,self.scorevar.get(),True)   
            score2 = self.scorevar.get() 
            if int(score2)<int(score1):
                print score1
                break
            if table_act_act==self.table and second is True:
                third = True
            if table_act_act==self.table and second is False:
                second = True
                third = False
            if table_act_act!=self.table:
                second = False
                third = False
            self.root.update()
        

          
                                                                                      
app = App(Tk())
app.run()

'''for i in range(1279):
    path = "C:\\Users\\Hugo\\Documents\\python\\2048_screenshots\\screenshot_"+str(i)+".jpg"
    img = Image.open(path)
    cropped_img = img.crop((88,301,508,809))
    save_path = "C:\\Users\\Hugo\\Documents\\python\\2048_screenshots\\screenshot_resized_"+str(i)+".jpg"
    cropped_img.save(save_path)'''
    