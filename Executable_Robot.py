
#Import libraries
import pyrebase, random
import RPi.GPIO as GPIO   
import os, sys, subprocess       
from time import sleep
import pygame

pygame.init()
#Variables to play the audios
mask = "veu_bona"
no_mask = "veu_dolenta"
name = "Aleix"

#Pins that control the right electric motors
in1right = 24
in2right = 23
in3right = 26
in4right = 13
enright = 25
enright2 = 19

#Pins that control the left electric motors
in1left = 6
in2left = 5
enleft = 16
in3left = 4
in4left = 2
enleft2 = 3

temp1 = 1
GPIO.setmode(GPIO.BCM)

#Set up the GPIO for the right electric motors
GPIO.setup(in1right,GPIO.OUT)
GPIO.setup(in2right,GPIO.OUT)
GPIO.setup(enright,GPIO.OUT)
GPIO.output(in1right,GPIO.LOW)
GPIO.output(in2right,GPIO.LOW)
pright = GPIO.PWM(enright,1000)
GPIO.setup(in3right,GPIO.OUT)
GPIO.setup(in4right,GPIO.OUT)
GPIO.setup(enright2,GPIO.OUT)
GPIO.output(in3right,GPIO.LOW)
GPIO.output(in4right,GPIO.LOW)
pright2 = GPIO.PWM(enright2,1000)

#Set up the GPIO for the left electric motors
GPIO.setup(in1left,GPIO.OUT)
GPIO.setup(in2left,GPIO.OUT)
GPIO.setup(enleft,GPIO.OUT)
GPIO.output(in1left,GPIO.LOW)
GPIO.output(in2left,GPIO.LOW)
pleft = GPIO.PWM(enleft,1000)
GPIO.setup(in3left,GPIO.OUT)
GPIO.setup(in4left,GPIO.OUT)
GPIO.setup(enleft2,GPIO.OUT)
GPIO.output(in3left,GPIO.LOW)
GPIO.output(in4left,GPIO.LOW)
pleft2 = GPIO.PWM(enleft2,1000)

pright.start(25)
pleft.start(25)
pright2.start(25)
pleft2.start(25)

print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")    

#credentials for the comunication with FireBase
config = {
    "apiKey": "AIzaSyBmoAiaZ0g9Z2KPRQ6wMS92scBGW7NyBD0",
    "authDomain": "motorcontrollerrobot.firebaseapp.com",
    "databaseURL": "https://motorcontrollerrobot.firebaseio.com",
    "storageBucket": "motorcontrollerrobot.appspot.com"
}

#Initialize database

firebase = pyrebase.initialize_app(config)
db = firebase.database()



#Call the process to start broadcasting the iamges taken by the cam.
subprocess.call(['/home/pi/RPi_Cam_Web_Interface/start.sh'])


#----------------------------------
#----Code to stream to Firebase----
#----------------------------------


def stream_handler(message):
    print(message)
    screen = pygame.display.set_mode((200, 200))
     
    
    #Aquest primer if es necessari perque segons com modifiquem les 
    #dades al firebase, aquestes arriben en diferent format
    if type(message["data"]) is dict :

        if message["path"] == "/left" :
            if message["data"]['move'] > 0 :
                print("run left")
                GPIO.output(in1left,GPIO.HIGH)
                GPIO.output(in2left,GPIO.LOW)
                GPIO.output(in3left,GPIO.HIGH)
                GPIO.output(in4left,GPIO.LOW)
                pleft.ChangeDutyCycle(message["data"]['move'] * 100)
                pleft2.ChangeDutyCycle(message["data"]['move'] * 100)
                print("forward")
                
            elif message["data"]['move'] < 0 :
                print("run left")
                GPIO.output(in1left,GPIO.LOW)
                GPIO.output(in2left,GPIO.HIGH)
                GPIO.output(in3left,GPIO.LOW)
                GPIO.output(in4left,GPIO.HIGH)
                pleft.ChangeDutyCycle(message["data"]['move'] * -100)
                pleft2.ChangeDutyCycle(message["data"]['move'] * -100)
            
            else :
                print("stop left")
                GPIO.output(in1left,GPIO.LOW)
                GPIO.output(in2left,GPIO.LOW)
                GPIO.output(in3left,GPIO.LOW)
                GPIO.output(in4left,GPIO.LOW)
                
                
        elif message["path"] == "/right" : 
            if message["data"]['move'] > 0 :
                print("run right")
                GPIO.output(in1right,GPIO.HIGH)
                GPIO.output(in2right,GPIO.LOW)
                GPIO.output(in3right,GPIO.HIGH)
                GPIO.output(in4right,GPIO.LOW)
                pright.ChangeDutyCycle(message["data"]['move'] * 100)
                pright2.ChangeDutyCycle(message["data"]['move'] * 100)
                print("forward")
                
            elif message["data"]['move'] < 0 :
                print("run right")
                GPIO.output(in1right,GPIO.LOW)
                GPIO.output(in2right,GPIO.HIGH)
                GPIO.output(in3right,GPIO.LOW)
                GPIO.output(in4right,GPIO.HIGH)
                pright.ChangeDutyCycle(message["data"]['move'] * -100)
                pright2.ChangeDutyCycle(message["data"]['move'] * -100)
            
            else :
                print("stop right")
                GPIO.output(in1right,GPIO.LOW)
                GPIO.output(in2right,GPIO.LOW)
                GPIO.output(in3right,GPIO.LOW)
                GPIO.output(in4right,GPIO.LOW)
        #The robot will play different audios depending on whether the user is wearing a mask or not.
        elif message["path"] == "/mask" :
                if message["data"] == true :
                        os.system('omxplayer /home/pi/Music/veu1.mp3')
                else :
                        os.system('omxplayer /home/pi/Music/veu2.mp3')
            
        else :
                print("Primera iteracio")
            
    else:
                          
        if message["path"] == "/right/move":
                if message["data"] > 0 :
                        GPIO.output(in1right,GPIO.HIGH)
                        GPIO.output(in2right,GPIO.LOW)
                        GPIO.output(in3right,GPIO.HIGH)
                        GPIO.output(in4right,GPIO.LOW)
                        print(message["data"])
                        pright.ChangeDutyCycle(message["data"] * 100)
                        pright2.ChangeDutyCycle(message["data"] * 100)
                elif message["data"] < 0 :
                        GPIO.output(in1right,GPIO.LOW)
                        GPIO.output(in2right,GPIO.HIGH)
                        GPIO.output(in3right,GPIO.LOW)
                        GPIO.output(in4right,GPIO.HIGH)
                        pright.ChangeDutyCycle(message["data"] * -100)
                        pright2.ChangeDutyCycle(message["data"] * -100)
                else :
                        GPIO.output(in1right,GPIO.LOW)
                        GPIO.output(in2right,GPIO.LOW)
                        GPIO.output(in3right,GPIO.LOW)
                        GPIO.output(in4right,GPIO.LOW)
                        
        elif message["path"] == "/left/move":
                print("FUNCIONA")
                if message["data"] > 0 :
                        print("FUNCIONA")
                        GPIO.output(in1left,GPIO.HIGH)
                        GPIO.output(in2left,GPIO.LOW)
                        GPIO.output(in3left,GPIO.HIGH)
                        GPIO.output(in4left,GPIO.LOW)
                        pleft.ChangeDutyCycle(message["data"] * 100)
                        pleft2.ChangeDutyCycle(message["data"] * 100)
                        print("forward")
                elif message["data"] < 0 :
                        GPIO.output(in1left,GPIO.LOW)
                        GPIO.output(in2left,GPIO.HIGH)
                        GPIO.output(in3left,GPIO.LOW)
                        GPIO.output(in4left,GPIO.HIGH)
                        pleft.ChangeDutyCycle(message["data"] * -100)
                        pleft2.ChangeDutyCycle(message["data"] * -100)
                else :
                        print("stop left")
                        GPIO.output(in1left,GPIO.LOW)
                        GPIO.output(in2left,GPIO.LOW)
                        GPIO.output(in3left,GPIO.LOW)
                        GPIO.output(in4left,GPIO.LOW)
                        
                        
        elif message["path"] == "/mask":

                num = str(random.randrange(1,5))
                image0 = pygame.image.load("/home/pi/Pictures/happy.png")
                image1 = pygame.image.load("/home/pi/Pictures/angry.png")
                
                width  = pygame.display.Info().current_w
                height = pygame.display.Info().current_h
                #Adecuem la imatge a la m,ida de la pantalla
                image0 = pygame.transform.scale(image0, (width,height))
                image1 = pygame.transform.scale(image1, (width,height))
               
                
                if message["data"] == True :
                        screen.blit(image0,(0,0))
                        pygame.display.update()
                        audio = "omxplayer /home/pi/Music/" + mask + num + ".mp3"
                        print(audio)
                        os.system('omxplayer /home/pi/Music/veu1.mp3')
                        screen.fill((0,0,0))
                        pygame.display.update()
                        
                else :
                        screen.blit(image1,(0,0))
                        pygame.display.update()
                        
                        audio = "omxplayer /home/pi/Music/" + no_mask + num + ".mp3"
                        os.system('omxplayer /home/pi/Music/veu1.mp3')
                        screen.fill((0,0,0))
                        pygame.display.update()
    
        elif message["path"] == "/finish":
                if message["data"] == True:
                        subprocess.call(['/home/pi/RPi_Cam_Web_Interface/stop.sh'])
                        sys.exit()
    

try:
        my_stream = db.stream(stream_handler)

except KeyboardInterrupt:
        print('interrupted')
        subprocess.call(['/home/pi/RPi_Cam_Web_Interface/stop.sh'])
        my_stream.close()
        sys.exit()


