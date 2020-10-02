#!/usr/bin/env python
#title           :AI_News.py
#description     :Dependency Package of get_user_response.py
#author          :Dipendu Choudhury
#date            :2020-APR-27
#version         :1.0
#usage           :python AI_News.py
#python_version  :3.6.5 
#email           :dipenduc39@gmail.com
#licence         :Own
#copyright       :copyright 2019-2020
#====================================================================
#====================================================================

#Import all required Lib
from tkinter import *
import time
from bs4 import BeautifulSoup as bs
import requests
import speech_recognition as sr
import pyttsx3
import time as t
import platform
import socket
import pygame
from pygame.mixer import music
import random
import os

#Initialize the pyttsx3 class
engine = pyttsx3.init()
#Get the Default voices from your computer
voices = engine.getProperty('voices')
#Set the voice using voice id, It may different in your Computer. According to my PC voice id = 0; means female voice. 
engine.setProperty('voice', voices[0].id)
#Set the Speech rate per minute 
engine.setProperty('rate', 130)
#For more Information on pyttsx3 refer to this link - https://pyttsx3.readthedocs.io/en/latest/engine.html

###############Get the Computer Name
computer_name = platform.node()

#Create Speech Recognizer Object
#For more Information on Speech Recognizer refer to this link - https://pypi.org/project/SpeechRecognition/
r = sr.Recognizer()

################## Background Music Part
#Mixer Initialize
pygame.mixer.init()
#Load the background Music file
music.load("News_Music/news_background_music.mp3")
#Set the Music Volume
music.set_volume(0.1)

#Create a speak function 
def speak(text):
    engine.say(text)
    #Run the speech and wait 
    engine.runAndWait()
    
  
def popular_ai_news(app,var):  
    """ Scrap the News headlines from website and speak """
    while True:
            try:
                #Check the Internet Connection
                socket.create_connection(("Google.com",80))
                #Send the request to the News website
                base_page = requests.get("https://artificialintelligence-news.com/news/")
                #Extract all page text
                bp_text = bs(base_page.text,'lxml')
                ####Play Background News Music
                music.play()
                var.set("Hey {}, \nHere is the top Headlines for today".format(computer_name))
                app.update()
                speak("Hey {}, Here is the top Headline for today".format(computer_name))
                #Create empty list to store news headlines for later use
                saved_headline = []
                #Search all link which under class "widget techforge-post-types"
                for base_links in bp_text.find("div", {"class": "widget techforge-post-types"}).findAll("a", href = True):
                      #Find the top headlines
                      headlines = base_links.find("h3")
                      if headlines is not None:
                        #print(headlines.text)
                        #Tkinter part
                        var.set(headlines.text)
                        app.update()
                        #Call the speak function
                        speak(headlines.text)
                        #Store the headlines for later use
                        saved_headline.append(headlines.text)
                      else:
                        continue
                      t.sleep(1)
                #Stop the background music
                music.stop()
            except OSError:
                print("No Internet Connection Found")
                t.sleep(5)
                continue
            #Return the scraped news headline for reuse  
            return saved_headline
            app.destroy()
            break
        
    
def start_news(app,var,Label,img1,img2,img3):
    """ Start the AI News Function """
    saved_headline = popular_ai_news(app,var)
    wait_count = 0
    while True: 
        try:
            var.set("Do you want to listen again?")
            app.update()
            speak("Do you want to listen again")
            Label.configure(image=img2,borderwidth=0,compound="center",highlightthickness = 0,padx=0,pady=0)
            var.set("Listening.....")
            app.update()
            with sr.Microphone() as source:
                #Listen the audio through Microphone
                #r.adjust_for_ambient_noise(source)
                audio = r.listen(source,phrase_time_limit=1.5)
                Label.configure(image=img1,borderwidth=0,compound="center",highlightthickness = 0,padx=0,pady=0)
                var.set(r.recognize_google(audio))
                app.update()
            if "yes" in r.recognize_google(audio):
                ##Play Background News Music
                music.play()
                var.set("Oky \nHere is the top Headlines for today")
                app.update()
                speak("Oky, Here is the top headline for today")
                for headline in saved_headline:
                    var.set(headline)
                    app.update()
                    speak(headline)
                    t.sleep(1)
                ##Stop Background Music
                music.stop()
            else:
                var.set("Oky  \nHave a nice day")
                app.update()
                speak("Oky, Have a nice day")
                app.destroy()
                break
        except KeyboardInterrupt as k:
            app.destroy()
            break
        except:
            if wait_count<3:
                if wait_count != 2:
                     Label.configure(image=img1,borderwidth=0,compound="center",highlightthickness = 0,padx=0,pady=0)
                     var.set("Sorry \nI can't listen properly")
                     app.update()
                     speak("Sorry, I can't listen properly")
                     wait_count+=1
                     continue
                else:
                    wait_count+=1
                    continue
            else:
                Label.configure(image=img3,borderwidth=0,compound="center",highlightthickness = 0,padx=0,pady=0)
                var.set("Sorry \nDue to no response I am closed the programmme")
                app.update()
                speak("Sorry, Due to no response I am closed the programmme")
                app.destroy()
                break           
    app.mainloop()

def main():
        ######### GUI PART Using Tkinter
        #Define Global Variable
        global app,var,Update_Label
        #Create window
        app = Tk()
        #Set to active tkinter window all time
        app.wm_attributes("-topmost", 1)
        app.focus_force()
        # Add title of the window
        app.title("Security Chheck")
        #Set the window as full screen
        app.attributes('-fullscreen', True) 
        #Set the window resize false
        app.resizable(0,0)
        #Set window background color black
        app.configure(bg="black")
        #Set window transperency 
        app.wm_attributes('-alpha',0.85)
        #Define a variable for updating label text
        var = StringVar()
        ### Create Frame 
        #This Frame is for showing logo of the window
        logo_fram = Frame(app)
        logo_fram.pack(side= TOP,pady=80)
        #This Frame is Visualizing all label text
        text_fram = Frame(app)
        text_fram.pack(side= TOP)

        ####Load the logo images  
        #load speaking logo
        img1 = PhotoImage(file="logo/Cortana.png")
        #load listing image
        img2 = PhotoImage(file="logo/listen.png")
        #load not response image
        img3 = PhotoImage(file="logo/not_respond.png")
        #Create a Label widget for showing our logo
        Update_Label = Label(logo_fram,image=img1,borderwidth=0,compound="center",highlightthickness = 0,padx=0,pady=0)
        #Pack the label, without pack it can't be vizalble
        Update_Label.pack()
        
        #Text Label
        text_label=Label(text_fram,font='Times 28 bold',bg='black',fg='white',textvariable=var,highlightcolor='white',highlightbackground='black')
        text_label.pack()

        ##Start the News 
        start_news(app,var,Update_Label,img1,img2,img3)
     
if __name__ == "__main__":
    main()
