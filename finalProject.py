# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 18:06:50 2020

@author: MuhammedSalah, Email: Mohammed.salahadinf18@komar.edu.iq
@author: AbdulrahmanTawffqe, Email: abdulrahman.tofiqf18@komar.edu.iq

"""

import tkinter 
from tkinter import messagebox, Canvas, Tk
import numpy as np
import cv2
import turtle
from turtle import TurtleScreen
import time
import random


#to open a window using turtle
window=turtle.Screen()
#to make the window unresizable
window.cv._rootwindow.resizable(False, False)
#giving tilte to that window
window.title("Goalkeeper")

#Python Turtle.Terminator
#After some research on the turtle library We have found a variable called TurtleScreen._RUNNING, 
#if this variable is set to True a turtle window opens, if not you get the turtle.Terminator error. 
#Every time you close a turtle screen, 
#But to avoid that, we need TurtleScreen._RUNNING = True
TurtleScreen._RUNNING=True


#icon the logo of the window
imgicon = tkinter.Image("photo", file="images/glove.png")
turtle._Screen._root.iconphoto(True, imgicon)



#half Screen Size to have width to our game window 
#GetSystemMetrics(0)
gameScreenWidth=int(1280/2)
#half Screen Size to have height to our game window
#GetSystemMetrics(1)
gameScreenHeight=int(720/2)

#half of game window width
halfGameScreenWidth=int(gameScreenWidth/2)
#half of game window height
halfGameScreenHeight=int(gameScreenHeight/2)

#quarter of game window width
quarterGameScreenWidth=int(gameScreenWidth/4)
#quarter of game window height
quarterGameScreenHeight=int(gameScreenHeight/4)

#third one of game window width
thirdOfhalfGameScreenWidth=int(halfGameScreenWidth/3)
#third one of game window height
thirdOfhalfGameScreenHeight=int(halfGameScreenHeight/3)





#our game window is the half size of the current screen size
window.setup(width=gameScreenWidth,height=gameScreenHeight)

#the background color
window.bgcolor("#0c3a4f")



#separeted method to add any object to decrease code dublication
#the code inside this method was repeated for all the shapes in the game
#but now, it is a method to be called and the code became more organized
#accepts the object(turtle), goto(x,y), and the gif(shape) parameters
def add_object(Object,x,y,gif):
    # the speed that turtle module draws the shape on screen whenever it moves to let us see it
    Object.speed(0)#to let the shape updated in the maximum speed 
    #no drawing when the turtle object is moving
    Object.penup()
    #position of the Object
    Object.goto(x,y)
    #turtle model has these shapes ['arrow', 'blank', 'circle', 'classic', 'square', 'triangle', 'turtle']
    #but we can add a shape as gif image using the addshape method
    turtle.addshape(name=gif,shape=None)
    #we use the shape method to get the shape on the window and we use our shape instead of the ready shapes like shape("square")
    Object.shape(gif)
    # to be appeared and visible on the screen at the same time
    Object.showturtle()




#===================================Function to start the game when be called==================================
def start(data, context):
    #once the game starts, the play button will be disappeared
    playButton.hideturtle()
    
    
 
    #to check if the image is existed, means the game opened before and the playground is created
    #so, no need to go through the code again. if an exception accured, it will go to except part
    #to create it from scratch
    try:
        window.bgpic("images/backgroundDay.png")
    except:
        #image to appear after open the game and disappears when the loading be finished
        window.bgpic("images/goal.png")
        window.update()
        #Creating a black image in the background with the same size of the game window
        #it is colored with ch=3
        blackBackground=np.ones((gameScreenHeight,gameScreenWidth,3),dtype="uint8")
        
        
        
        #We are drawing shapes over the black image that we created
        
        #1- Green Rectangle is over the blackBackground
        playGround=cv2.rectangle(blackBackground,(0,0),(gameScreenWidth,gameScreenHeight),(80, 160, 54),-1)
        
        #2- Outer Border rectangle
        playGround=cv2.rectangle(playGround,(10,10),(gameScreenWidth-20,gameScreenHeight-20),(255,255,255),1)
        
        #3- play Ground Middle Line
        playGround=cv2.line(playGround,(halfGameScreenWidth,10),(halfGameScreenWidth,gameScreenHeight-20),(255,255,255),1)
        
        #4- middle circle
        playGround=cv2.circle(playGround,(halfGameScreenWidth,halfGameScreenHeight),80,(255,255,255),1)
        
        #5- center point
        playGround=cv2.circle(playGround,(halfGameScreenWidth,halfGameScreenHeight),3,(255,255,255),-1)
        
        #6- penalty area 1
        playGround=cv2.rectangle(playGround,(gameScreenWidth-thirdOfhalfGameScreenWidth,quarterGameScreenHeight),(gameScreenWidth-20,gameScreenHeight-quarterGameScreenHeight),(255,255,255),1)
        
        #7- penalty area 2
        playGround=cv2.rectangle(playGround,(10,quarterGameScreenHeight),(thirdOfhalfGameScreenWidth-10,gameScreenHeight-quarterGameScreenHeight),(255,255,255),1)
        
        #because imread method goes with the GBR, we convert the image to RGB
        #As well as, the background color of playGround was 54, 160, 80 with BGR and we edited it to 80, 160, 54 RGB above 
        RGB_Image=cv2.cvtColor(playGround,cv2.COLOR_BGR2RGB)
        
        #saving the new background img that we created as normal img in images directory
        cv2.imwrite("images/backgroundDay.png",RGB_Image)
    
    #to check if the image is existed, means the game opened before and the night image is created
    #so, no need to go through the code again. if an exception accured, it will go to except part
    #to create it
    try:
        window.bgpic("images/backgroundNight.png")
    except:
        #Creating the night mood image and save it with backgroundNight name in images directory
        RGB_Image2=cv2.imread("images/backgroundDay.png")
        for r in range(RGB_Image2.shape[0]):
            for c in range(RGB_Image2.shape[1]):
                for ch in range(RGB_Image2.shape[2]):
                    RGB_Image2[r][c][ch]=RGB_Image2[r][c][ch]*0.45 #decrease 55% of the value of each color R, G, B to make them colse to the 0 (black) to get the night mood
        cv2.imwrite("images/backgroundNight.png",RGB_Image2)
    
    #adding effects (bluring and scaling)
    F_blur=50
    F_scale=2
    while F_blur>1:
        try:
            #if the app opened before, means all the picyures are in the dir and no need to create them again
            #this try to check the image if it is not found it will go to the exception and if not it gose to finally
            window.bgpic("images/bluring/background"+str(F_blur)+".png")
        except:
            #if the error of file not found accures, this code is going to be executed to create all the images.
            RGB_Image=cv2.imread("images/backgroundDay.png")
            #make the bg img blured
            blured=cv2.blur(RGB_Image, (F_blur,F_blur))
            #scaling it
            bluredScaled=cv2.resize(blured, None,fx=F_scale,fy=F_scale)
            #saving it with the new properties in new name and in the bluring directory
            cv2.imwrite("images/bluring/background"+str(F_blur)+".png",bluredScaled)
            #make it as bg in the window
            #we created this amount of images with new name for each image as this bgpic wont be updated if
            #we pass the same name to it
            window.bgpic("images/bluring/background"+str(F_blur)+".png")  
        finally:
            #this part is going to be excuted in all cases, so the update, increasing values, and sleep is here
            
            #decreasing the properties
            F_blur-=1
            F_scale-=0.02
            #updating the window to see the live changing
            window.update()
            #adding some delay after importing the time above
            time.sleep(0)
        
    #by default the day background image is set
    window.bgpic("images/backgroundDay.png")
    
    

    
    
    
    #the turtle is hidden till the showturtle() method will be called to avoid the arrow to be shown
    goalKeeper=turtle.Turtle(visible=False)#it is a turtle object
    add_object(goalKeeper,360,0,"images/goalkeeper.gif")
    
    ball=turtle.Turtle(visible=False)
    add_object(ball,-345,0,"images/ball.gif")
    
    machine=turtle.Turtle(visible=False)
    add_object(machine,-360,10,"images/machine.gif")
    
    
    
    
    
    
    
    
    
    
    
    
   
    
    # x coordinates for them before the loop of the animation
    loop=0
    keeper_w=360
    ball_w=-345
    machine_w=-360
    #animation loop for the goalkeeper, ball, and the machine objects
    while loop<25 :
        time.sleep(0.015)
        goalKeeper.goto(keeper_w,0)
        ball.goto(ball_w,0)
        machine.goto(machine_w,10)
        keeper_w-=3.5
        ball_w+=8.5
        machine_w+=8.5
        loop+=1
        window.update()
        
    # =============================================================================
    # x coordinates for them after the loop of the animation
    #
    # goalKeeper.xcor()
    # xcor: 276.0
    # 
    # ball.xcor()
    # xcor: -141.0
    # 
    # machine.xcor()
    # xcor: -156.0
    # =============================================================================
    




    #method to change to the night background image
    def night():
        window.bgpic("images/backgroundNight.png")
     
    #method to change to the day background image
    def day():
        window.bgpic("images/backgroundDay.png")
    
    window.onkey(night,"1")
    window.onkey(day,"2")
    window.listen() #method related to turtle model to wait for the user to press the key
    
    
    
    
  
    
    #button to change to day mode
    sun=turtle.Turtle(visible=False)
    add_object(sun,-209.2, 150,"images/sun.gif") #method we created it above
    sun.onclick(day)
    
    #button to change to night mode
    moon=turtle.Turtle(visible=False)
    add_object(moon,-184.6, 150,"images/moon.gif") #method we created it above
    moon.onclick(night)
    
    
    
    
    
    
    def close_animation():
        window2=Tk()
        window2.geometry("640x360+320+180")
        canvas=Canvas(window2,bg="black",width=640,height=360)
        canvas.pack()
        
        firstx=0
        firsty=0
        
        
        
        file=open("images/line.txt",'r')
        value=file.readline()
        x1=value.split()[0]
        y1=value.split()[1]
        i=0
        while(i<335):
            value=file.readline()
            
            x2=value.split()[0]
            y2=value.split()[1]
            canvas.create_line(x1,y1,x2,y2,fill="yellow",width=20)
            x1=x2
            y1=y2
            i+=1
            window2.update()
            time.sleep(0.001)
        
        x1=0
        y1=0
        x2=640
        y2=360
        while(x1<=320):
            if(x1%5==0):
                canvas.create_oval(x1,y1,x2,y2,width=10,fill="white",outline="black")
            x1+=1
            y1+=0.5
            x2-=1
            y2-=0.5
            window2.update()
        window2.destroy()
    
    
    
    

    

    
    #Function to exit the game and close the window if close shape is pressed
    #by using messagebox when we import everything from tkinter to have confiramtion
    def exitprogram(x, y):
        option=messagebox.askquestion("Close", "Are You Sure?", icon='warning')
        if (option=='yes'):
            window.bye()
            close_animation()
            
    
    
    #button to close the window
    close=turtle.Turtle(visible=False)
    add_object(close,-135.7, 150,"images/close.gif") #method we created it above
    close.onclick(exitprogram)



    
    
    
    
    
    
    
  
    
    
    
    
    #Function to exit the game and close the window if pause shape is pressed
    def pause_game(x, y):
        option=messagebox.showinfo('Paused', 'Click ok to continue.')
        if (option=='ok'):
            pass
    
    
    #button to puase the game
    pause=turtle.Turtle(visible=False)
    add_object(pause,-111.1, 150,"images/pause.gif") #method we created it above
    pause.onclick(pause_game)
    
    
    
    
   
    

    #method to open the file and return the value in the first line or second line
    def file_read_line(path, line, exceptValue):
        try: 
            file=open(path,'r')
            if(line==1):
                value=float(file.readline())
                file.close()
                return value #return the first line
            elif(line==2):
                value=float(file.readline())
                value2=float(file.readline())
                file.close()
                return value2 #return the second line
        except: #if the file is not found to be created and the value to be returned as well
            file_create_then_write(path, exceptValue) #write the initial value in it
            file=open(path,'r')
            if(line==1):
                value=float(file.readline())
                file.close()
                return value #return the first line
            elif(line==2):
                value=float(file.readline())
                value2=float(file.readline())
                file.close()
                return value2 #return the second line
        
    #method to create the file if not exists, then to write in it
    def file_create_then_write(path, value):
        fileWrite=open(path,'w+')
        fileWrite.write(value)
        fileWrite.close()
    
    
    
    
    #to return the speed of the gaolkeeper from the file.
    #if the file is not exists, it will be craeted and be 3.5px initially
    #when the player press w or s keys to call the goalKeeper_up() or goalKeeper_down()
    #methods to change the position of him, this method 'goalKeeper_speed()' will be called there instead of
    #having a specific value we write it ourself, it will be gotten from the file
    def goalKeeper_speed():
        speed=file_read_line("images/goalkeeperSpeedFile.txt",1,"3.5") #method we defined it above
        return speed
    
    
    #to return the speed and direction 'x & y' of the ball from the file.
    #if the file is not exists, it will be craeted and be 0.3px for x and 0.1171366594px as range for y initially
    def ball_speed_direction():
        ball_x=file_read_line("images/ballSpeedFile.txt",1, "0.3\n0.1171366594") #reading the first line
        ball_y=file_read_line("images/ballSpeedFile.txt",2, "0.3\n0.1171366594") # call again to read the second line
        return ball_x, ball_y
        
    
    
    
    
    
    
    
    
    #function to increase the level of the goalkeeper after he catches a specific
    #number of balls respectively accoring to the last level he got
    #To open the file and update the old value and put the new one 
    #comming by the param 'levelUp'
    
    #to icrease the speed of the goalkeeper as well by updating it in the file "goalkeeperSpeedFile"
    #by calling goalKeeper_speed() to get the last value in the file and increase it by 0.01
    def level_up(levelUp):
        #the file will be created by the level method before, but we can put try and catch
        #to make sure about avoiding the errors of IOError
        try:
            file_create_then_write("images/levelFile.txt", levelUp)
        
            #reading the old speed value
            old_goalKeeper_speed=goalKeeper_speed()
            #updating thr speed and store it in the file instead of the old value
            file_create_then_write("images/goalkeeperSpeedFile.txt", str(old_goalKeeper_speed+0.01))
            
            #reading the old x and y of the ball for the speed and range of direction
            old_ball_x=ball_speed_direction()[0]
            old_ball_y=ball_speed_direction()[1]
            #updating thr speed and store it in the file instead of the old value
            #example
            #by using the equation      x=0.3          ===> x=0.31
                                 #      y=0.1171366594 ===> z
                                 #      z= (0.31 * 0.1171366594)/0.3
            file_create_then_write("images/ballSpeedFile.txt", str(old_ball_x+0.01) + "\n" + str(    ((old_ball_x+0.01)*old_ball_y )     /      old_ball_x    )   )
        except IOError:
            pass
        
    
    #method to get the level of the goalkeeper once the game starts to show it on the 
    #screen, if the file is not exists, it will be created and the initial level will be 1
    def get_level():
        #if the file is not found, will be created and the except param "1" will be inserted in the file as the initial value
        levelValue=int(file_read_line("images/levelFile.txt", 1, "1")) #cast the level to int
        #return the value
        return levelValue
    
    
    
    
    
    
    
    
    
    
    #the level will be shown on the screen as text using turtle by using write method
    level = turtle.Turtle()
    level.hideturtle()
    level.penup()
    level.goto(100, 140)
    #we put {} then format it to have a changable value on the screen according to the
    #variable, it will be not fixed as the 'Level:' str
    level.write("Level: {}".format(int(get_level())),align="center",font=("Courier", 13, "normal"))
    
    
    #if the level is 10, then he should catchs 10 balls respectively to make the level up to 11
    #from 1 to 10 "his progess" will be shown on the screen
    #if he reachs 9 and lose the last one, the progress will be 0 as he must catches 10
    #balls respectively to make his level increases if the level was 10
    progress = turtle.Turtle()
    progress.hideturtle()
    progress.penup()
    progress.goto(220, 140)
    progress.write("Progress: 0",align="center",font=("Courier", 13, "normal")) 
    
    
    
    
    
    #Functions to move the object (goalkeeper)
    def goalKeeper_up():    
        y = goalKeeper.ycor() #to get the current y coordinate of the goalkeeper object
        y = y + goalKeeper_speed() #to increase current y coordinate by pixcels that the goalKeeper_speed() returns each time we move the goalkeeper up
        goalKeeper.sety(y) # to set the new y coordinate which is the old + specific px
        if (y>=145):
            y=145
            goalKeeper.sety(y)
        
    def goalKeeper_down():  
        y = goalKeeper.ycor() #to get the current y coordinate of the goalkeeper object
        y = y - goalKeeper_speed() #to decrease current y coordinate by pixcels that the goalKeeper_speed() returns each time we move the goalkeeper down
        goalKeeper.sety(y) # to set the new y coordinate which is the old - specific px
        if (y<=-140):
            y=-140
            goalKeeper.sety(y)
    #End Functions of moving the object(goalkeeper)      
    window.onkeypress(goalKeeper_up,"w")
    window.onkeypress(goalKeeper_down,"s")
    
    window.onkeypress(goalKeeper_up,"Up")
    window.onkeypress(goalKeeper_down,"Down")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    goalkeeper_height= 67
    goalkeeper_width= 25
    
    #ball_height= 25
    #ball_width= 25
    
    
    
    #by this, the ball will be pushed according to the height for the playgroung. Not going to hit the width of it
    value_changing_x_ball=ball_speed_direction()[0] #this value will be added to x cor of the ball
    #this random value in this range will be added to y cor of the ball
    value_changing_y_ball=random.uniform(-ball_speed_direction()[1],ball_speed_direction()[1]) 

    time.sleep(0.7)
    
    #number of balls the goalkeeper catches respectively    
    he_catches=0
    while (True):
        
        
        #value will be added to the current xcor of the ball
        ball.setx(ball.xcor()+value_changing_x_ball)
        
        #random value chosen value from a specific range before the loop will be added to the current ycor of the ball
        ball.sety(ball.ycor()+value_changing_y_ball)
        
        #the two values above will be added for each loop and xcor, ycor will change till this condition be true
        #if the ball xcor is more than the width of the window
        if (ball.xcor()>360):
            
            he_catches=0
            #clear the presvious one
            progress.clear()
            #the new progress once he lose the ball
            progress.write("P: {}".format(he_catches),align="center",font=("Courier", 13, "normal"))
            
            ball.goto(-141.0,0) #the ball pos to return to the original
            #a value will be added to x cor of the ball as it is fixed                                                       ##################
            #choose another random value to be added to ycor to change its value                                             #      only      #
            value_changing_y_ball=random.uniform(-ball_speed_direction()[1],ball_speed_direction()[1])                       #   y changes    # 
            #incase of loosing any ball, the progress will be 0 as he should catches the ball respectively                   ##################
            #till he reaches the number of the level to make it inceased
        
        #goalkeeper_height= 67
        #goalkeeper_width= 25
        #current position on x always: 276.0
        
        #ball height= 67
        #ball width= 25
        #initial position: (-141.0, 0)
        if (ball.xcor() > (276.0-(goalkeeper_width/2)) and ball.xcor() < (276.0+(goalkeeper_width/2)) and ball.ycor() < (goalKeeper.ycor()+(goalkeeper_height/2)) and ball.ycor() > (goalKeeper.ycor()-(goalkeeper_height/2))):
            
            
            
            #once he catches any ball, the progress will increase                                                            
            he_catches+=1                                                                                                    
            #once the progress equals the current level, the level will increase by 1
            #and will be saved in the file and the progress will be 0 to start again 
            #to equal the next level
            if(float(he_catches)==get_level()):
                level_up(str(get_level()+1))
                he_catches=0
                #clearing the previous level to write the new one
                level.clear()
                level.write("Level: {}".format(int(get_level())),align="center",font=("Courier", 13, "normal"))
            #clearing the previous progress to write the new one
            progress.clear()
            progress.write("P: {}".format(he_catches),align="center",font=("Courier", 13, "normal")) 
            
            #if the level equals 20, an Gongradulations message will appeares and the game will starts from beginning with  
            #the initial values for the goalkeeper speed, ball speed, and the level
            if(get_level()==20):
                level.clear()
                progress.clear()
                
                level.write("Gongradulations, ",align="center",font=("Courier", 13, "normal"))
                progress.write("You win! ",align="center",font=("Courier", 13, "normal"))
                
                time.sleep(3)
                
                level.clear()
                progress.clear()
                
                
                file_create_then_write("images/goalkeeperSpeedFile.txt","3.5")
                file_create_then_write("images/levelFile.txt","1")
                file_create_then_write("images/ballSpeedFile.txt","0.3\n0.1171366594")
            
            ball.setx(276.0)
            ball.sety(goalKeeper.ycor()+(goalkeeper_height/2))
            window.update() 
            time.sleep(0.15)  
                                                                                                                             ##################
            ball.goto(-141, 0)                                                                                               #      y & x     # 
            value_changing_x_ball=ball_speed_direction()[0]                                                                  #     changes    #
            value_changing_y_ball=random.uniform(-ball_speed_direction()[1],ball_speed_direction()[1])                       ##################
                
        window.update()      
                
            
     
           
        
        
       
        
            
        
       
            
            
            
        

#======================================End of Function of starting the game===================================== 















#play button to call the start method of to start playing the game   
playButton = turtle.Turtle(visible=False)
add_object(playButton,0, 0, "images/playButton.gif")


playButton.onclick(start)

















#method related to turtle model to wait for the user to press the key
#because there are keys to be clicked from the user useing the keyboard
window.listen() 





#Stops the window from updating automatically
#we added here to let the window updates to show the effects in the begining of the game
#then here it will be stopeed when the user starts playing
#we can notice now that the goalkeeper is not blinking when hitting the top edge
window.tracer(0)


  
window.mainloop() 
        
       
        
        
        
        
        
        
        
        
        
        
        
        
        
        