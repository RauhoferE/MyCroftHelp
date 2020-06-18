import datetime
import yagmail
import threading
import cv2
import yaml
from mycroft.audio import wait_while_speaking
from mycroft.util import record, play_wav
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_file_handler, intent_handler
from mycroft.skills.context import adds_context, removes_context

class Helperbot(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
    
    def initialize(self):
        # TODO: In eine Settings File schreiben
        self.remindUserMorning = True
        self.remindUserEvening = True
        self.set_date_times()
        #Calls function every day at 8 am
        self.schedule_repeating_event(self.say_Good_Morning, self.morning, 86400.0)
        #Calls function every day at 8 pm
        self.schedule_repeating_event(self.say_Good_Night, self.evening, 86400.0)
        self.config = yaml.safe_load(open("/opt/qbo/config.yml"))

    # This function asks the person if he needs any assistance.
    @intent_file_handler('Help.intent')
    @adds_context('HelpContext')
    def handle_helperbot(self, message):
        self.speak_dialog('doYouNeedHelp', expect_response=True)

    # This function is called if the person agreed for help
    @intent_handler(IntentBuilder('YesHelpIntent').require("Yes").
                                  require('HelpContext').build())
    @removes_context('HelpContext')
    def handle_yes_help(self, message):
        self.speak_dialog('speakMessage')
        #self.RecordMes() TODO: Recording sounds horrible
        self.SendMail() # TODO: It only sends the first 22 kb of the file, but I dont know why
        # TODO: Get Help
    
    # This function is called if the person disagreed for help
    @intent_handler(IntentBuilder('NoHelpIntent').require("No").
                                  require('HelpContext').build())
    @removes_context('HelpContext')
    def handle_no_help(self, message):
        self.speak_dialog('helpNo')

    # This function is should be called in the morning
    @adds_context('FeelContext')
    def say_Good_Morning(self):
        self.speak_dialog("hello")
        self.speak_dialog("howAreYou", expect_response=True)

    # This function is called if the eprson wants the robot to ask him how he feels - TEST
    @intent_file_handler("AskMe.intent")
    @adds_context('FeelContext')
    def ask_me(self):
        self.speak_dialog("howAreYou", expect_response=True)

    # This function should be called in the night
    def say_Good_Night(self):
        self.speak_dialog("goodNight")
        if self.remindUserEvening:
            self.take_Photo()
        

    # This function should be called if the person wants his photo taken - TEST
    @intent_file_handler("TakeMyPhoto.intent")
    def take_Photo_manually(self,message):
        self.take_Photo()

    # This function contains the text and context for taking the photo
    @adds_context('PhotoContext')
    def take_Photo(self):
        self.speak_dialog("photo", expect_response=True)
        self.makepicture()
    
    # This function is called if the user agrees to taking his photo
    @intent_handler(IntentBuilder('YesPhotoIntent').require("Yes").
                                  require('PhotoContext').build())
    @removes_context('PhotoContext')
    def handle_Photo_intent(self,message):
        self.speak_dialog("photoYes")
        for i in range(10, 0, -1):
            self.speak(str(i) + " .")
        self.speak_dialog("cheese")   
        # TODO:Take picture here

    # This function is called if the user disagrees to taking his photo
    @intent_handler(IntentBuilder('NoPhotoIntent').require("No").
                                  require('PhotoContext').build())
    @removes_context('PhotoContext')
    def handle_no_Photo_intent(self,message):
        self.speak_dialog("photoNo")
        self.schedule_event(self.take_Photo, self.set_date_time_in(10))

    # This function is called if the user disagrees to ever taking a photo
    # @intent_handler(IntentBuilder('NoPhotoIntent').require("Never").
    #                               require('PhotoContext').build())
    # @removes_context('PhotoContext')
    # def handle_never_Photo_intent(self,message):
    #     self.speak_dialog("stopAsking")
    #     self.remindUserMorning = False
    #     self.remindUserEvening = False


    # This function is called if the user has a good mood.
    @intent_handler(IntentBuilder('BadMoodIntent').require("Me").require("Good").
                                  require('FeelContext').build())
    @removes_context('FeelContext')
    def handle_pos_res_intent(self, message):
        # Handle Positive Respones
        # TODO: Make Robot Smile
        self.speak_dialog("goodMoodD")
        if self.remindUserMorning:
            self.take_Photo()
        
        
    # This function is called if the user has a bad mood.
    @intent_handler(IntentBuilder('GoodMoodIntent').require("Me").require("Bad").
                                  require('FeelContext').build())
    @removes_context('FeelContext')
    def handle_neg_res_intent(self, message):
        # Handle negative response
        # TODO: Make Robot Sad 
        self.speak_dialog("badMoodD")
        if self.remindUserMorning:
            self.take_Photo()

    # This function is called when the user doesnt want to be reminded this morning or evening.
    # TODO: Theses probably need some work
    # This function will activate the reminder again tomorrow 1 hour before the normal reminders start
    @intent_file_handler('DontRemind.intent')
    def handle_picture_remind(self, message):
        dayT = message.data.get('day')
        self.speak_dialog("stopReminding", data={"dayT": dayT})
        if dayT == "morning":
            self.remindUserMorning = False
            self.schedule_event(self.activate_morning_reminder, self.set_datetime_for_tomorrow(7))
            pass
        else:
            self.remindUserEvening = False
            self.schedule_event(self.activate_evening_reminder, self.set_datetime_for_tomorrow(19))
            pass
    
    # This function is called when the user doesnt want to be reminded every morning or evening.
    # @intent_file_handler('NeverRemind.intent')
    # def handle_never_picture_remind(self, message):
    #     dayT = message.data.get('day')
    #     self.speak_dialog("neverRemind", data={"dayT": dayT})
    #     if dayT == "morning":
    #         self.remindUserMorning = False
    #         pass
    #     else:
    #         self.remindUserEvening = False
    #         pass


    # Sets the datetime for the next 8am and the 8pm
    def set_date_times(self):
        dNow = datetime.datetime.now()
        if dNow.hour > 8:
            newDay = dNow + datetime.timedelta(days=1)
            self.morning = newDay.replace(hour=8,minute=0,second=0)
            pass
        else:
            self.morning = dNow.replace(hour=8,minute=0,second=0)
            pass
        dNow2 = datetime.datetime.now()
        if dNow2.hour > 20:
            newDay = dNow2.today().day + datetime.timedelta(days=1)
            self.evening = newDay.replace(hour=20,minute=0,second=0)
            pass
        else:
            self.evening = dNow2.replace(hour=20,minute=0,second=0)
        pass
    
    # Sets the datetime for number minutes 
    def set_date_time_in(self,number):
        dNow = datetime.datetime.now() + datetime.timedelta(minutes=1)
        #newMin = dNow.today().minute + number
        return dNow

    # Activates the morning reminders
    def activate_morning_reminder(self):
        self.remindUserMorning = True

    # Activates the evening reminders
    def activate_evening_reminder(self):
        self.remindUserEvening = True

    # Returns a datetime with tommorows date at hour1 o'clock
    def set_datetime_for_tomorrow(self, hour1):
        dt = datetime.datetime.now()
        tommorrow = dt + datetime.timedelta(days=1)
        return tommorrow.replace(hour=hour1)

    def RecordMes(self):
        wait_while_speaking()
        record("/tmp/mycroft-recording.wav", 30, 44100, 2)
        

    def SendMail(self,emailHost="smtp.gmail.com", emailPort=465, senderEmailAdress="helperbotdevacc@gmail.com", receivers= ["104609@fhwn.ac.at"], appPassword="shevsscfesztaddu"):
        # In der finalen version lässt sich der email provider einstellen
        # In der finalen version lässt sich Username und Passwort einstellen
        subject = "Help me"
        message = [
            "I have fallen and I cant get back up",
            "Please help me!",
        ]
        try:
            with yagmail.SMTP(senderEmailAdress, appPassword) as yag:
                for receiver in receivers:
                    yag.send(receiver, subject, message) 
                pass
            return True
        except:
            return False

    def makepicture(self):
        cam = cv2.cv2.VideoCapture(int(self.config['camera']))
        # 3 =  Enum for Picture Width
        cam.set(cv2.cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)  # I have found this to be about the highest-
        cam.set(cv2.cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)

        if cam.isOpened():
            _, frame = cam.read()
            now = datetime.datetime.now()
            file_name = now.strftime("%m_%d_%Y.%H_%M_%S") + ".jpg"
            cam.release()
            cv2.cv2.imwrite(file_name, frame)


def create_skill():
    return Helperbot()