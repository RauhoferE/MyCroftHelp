import datetime
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_file_handler, intent_handler
from mycroft.skills.context import adds_context, removes_context

class Helperbot(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
    
    def initialize(self):
        self.set_date_times()
        #Calls function every day at 8 am
        self.schedule_repeating_event(self.say_Good_Morning, self.morning, 86400.0)
        #Calls function every day at 8 pm
        self.schedule_repeating_event(self.say_Good_Night, self.evening, 86400.0)

    # This function asks the person if he needs any assistance.
    @intent_file_handler('Help.intent')
    @adds_context('HelpContext')
    def handle_helperbot(self, message):
        self.speak_dialog('doYouNeedHelp')

    # This function is called if the person agreed for help
    @intent_handler(IntentBuilder('YesHelpIntent').require("Yes").
                                  require('HelpContext').build())
    @removes_context('HelpContext')
    def handle_yes_help(self, message):
        self.speak_dialog('help')
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
        self.speak_dialog("howAreYou")

    # This function is called if the eprson wants the robot to ask him how he feels - TEST
    @intent_file_handler("AskMe.intent")
    @adds_context('FeelContext')
    def ask_me(self):
        self.speak_dialog("howAreYou", expect_response="good")

    # This function should be called in the night
    def say_Good_Night(self):
        self.speak_dialog("goodNight")

    # This function should be called if the person wants his photo taken - TEST
    @intent_file_handler("TakeMyPhoto.intent")
    def take_Photo_manually(self,message):
        self.take_Photo()

    # This function contains the text and context for taking the photo
    @adds_context('PhotoContext')
    def take_Photo(self):
        self.speak_dialog("photo", expect_response=True)
    
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
        self.schedule_event(self.take_Photo, self.set_date_time_in(1))

    # This function is called if the user has a good mood.
    @intent_handler(IntentBuilder('BadMoodIntent').require("Me").require("Good").
                                  require('FeelContext').build())
    @removes_context('FeelContext')
    def handle_pos_res_intent(self, message):
        # Handle Positive Respones
        # TODO: Make Robot Smile
        self.speak_dialog("goodMoodD")
        
    # This function is called if the user has a bad mood.
    @intent_handler(IntentBuilder('GoodMoodIntent').require("Me").require("Bad").
                                  require('FeelContext').build())
    @removes_context('FeelContext')
    def handle_neg_res_intent(self, message):
        # Handle negative response
        # TODO: Make Robot Sad 
        self.speak_dialog("badMoodD")
    
    # Sets the datetime for the next 8am and the 8pm
    def set_date_times(self):
        dNow = datetime.datetime.now()
        if dNow.hour > 8:
            newDay = dNow.today().day + 1
            self.morning = dNow.replace(day=newDay, hour=8,minute=0,second=0)
            pass
        else:
            self.morning = dNow.replace(hour=8,minute=0,second=0)
            pass
        dNow2 = datetime.datetime.now()
        if dNow2.hour > 20:
            newDay = dNow2.today().day + 1
            self.evening = dNow2.replace(day=newDay, hour=20,minute=0,second=0)
            pass
        else:
            self.evening = dNow2.replace(hour=20,minute=0,second=0)
        pass
    
    # Sets the datetime for number minutes 
    def set_date_time_in(self,number):
        dNow = datetime.datetime.now()
        newMin = dNow.today().minute + number
        return dNow.replace(minute=newMin, second=0)

def create_skill():
    return Helperbot()
