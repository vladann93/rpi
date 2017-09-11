#!/usr/bin/python
from twitter import *
from time import sleep
import twitter
import spidev
import RPi.GPIO as GPIO


me = "vladanivic"
my_device = 'def_not_kappa'

Cns_key = "mDQkuep5oCrO2VWeDOgsN2JGw"
Cns_sec = "diOQ0Pljw3QfM4bOGp5m34MJ6hfqA2F3TaaCOUoEcF7wO9pYyY"
A_token = "2971602155-UAgjfLf8g7iI3KsZ3E9TPqWeivLcDuHrl5w7WJO"
A_secrt = "nOH84PBHeVZryAlr5SbsgyjblSwef9FRprUf8lZtReu6q"

_FAN = 2           # GPIO no for FAN output
_LIGHT = 3	   # GPIO no for LIGHT output
_AC = 4            # GPIO no for A.C. output

def slice_rsponc(main_string):          # If the response from the user contains two tasks, 
    main_string=main_string.lower()     # this function divides and returns them as individual
    sl_indx = 0
    if ' and ' in main_string:
        sl_indx = main_string.find('and')
    elif ' & ' in main_string:
        sl_indx = main_string.find('&')
    return(main_string[0:sl_indx],main_string[sl_indx:len(main_string)])

def take_action(i,Pi_buddy):       # This function desides what action has to be taken and responses to the user
    if (len(i)==0):
        return
    elif 'status' in i:
        status = { 0:'OFF' , 1:'ON'}
        FAN = GPIO.input(_FAN)
        LIGHT = GPIO.input(_LIGHT)
        AC = GPIO.input(_AC)
        Pi_buddy.direct_messages.new(user=me,text= ("FAN = " + status[FAN]+"\nLight = "+
                                             status[LIGHT]+"\nAC = "+status[AC]+"\nTemperature = "+
                                              str(get_temp())+unichr(176)+'C'))
        return
    elif 'temp' in i or 'temperature' in i:
        Pi_buddy.direct_messages.new(user=me,text='It is '+str(get_temp())+unichr(176)+'C')
        return
    elif 'on' in i:
        seg0 = 'ON'
        if 'fan'in i:
            print ("ON the fan")                    # ON the fan
            seg1 = 'FAN'
        elif 'light'in i:
            print ("ON the bulb")                  # ON the bulb
            seg1 = 'Light'
        elif 'a.c.'in i:
            print ("ON the ac")                     # ON the ac
            seg1 = 'air conditioner'
        else:
            Pi_buddy.direct_messages.new(user=me,text="Incomplete??")
            return
    elif 'off' in i:
        seg0 = 'OFF'
        if 'fan'in i:
            print ("OFF the fan")                  # OFF the fan
            seg1 = 'FAN'
        elif 'light'in i:
            print ("OFF the bulb")                # OFF the bulb
            seg1 = 'Light'
        elif 'a.c.'in i:
            print ("OFF the ac")                   # OFF the ac
            seg1 = 'air conditioner'
        elif('all' in i):
            print ("OFF SVE")
            Pi_buddy.direct_messages.new(user=me,text= "All is OFF now")
            return
        else:
            Pi_buddy.direct_messages.new(user=me,text= "Incomplete??")
            return
    else :
        Pi_buddy.direct_messages.new(user=me,text="Can't understand!!!\nafterall I am machine :(")
        return
    Pi_buddy.direct_messages.new(user=me,text='Now your '+seg1+' is '+seg0+' :)')

def main():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(_LIGHT,GPIO.OUT)
    GPIO.setup(_FAN,GPIO.OUT) 
    GPIO.setup(_AC,GPIO.OUT)
    
    GPIO.output(_FAN,False)
    GPIO.output(_LIGHT,False)
    GPIO.output(_AC,False)

    Pi_buddy = Twitter(auth=OAuth(A_token,A_secrt,Cns_key,Cns_sec))
    Pi_Buddy_rec = twitter.OAuth(consumer_key=Cns_key,
                                 consumer_secret=Cns_sec,
                                 token=A_token,token_secret=A_secrt)
    
    stream = twitter.stream.TwitterStream(auth=Pi_Buddy_rec, domain='userstream.twitter.com')
    sen_msg="Hey,\nHow Can I help you?"
    Pi_buddy.direct_messages.new(user=me,text=sen_msg)
    for msg in stream.user():
        if 'direct_message' in msg:
            new_msg = msg ['direct_message']['text']
            if(msg['direct_message']['sender_screen_name']!=my_device):
                for i in slice_rsponc(new_msg):
                    take_action(i, Pi_buddy)
                
if __name__ == '__main__':main()
    
