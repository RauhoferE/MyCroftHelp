import datetime
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_file_handler, intent_handler
from mycroft.skills.context import adds_context, removes_context

#TODO: Die Schedule Threads funktionieren nicht
class Helperbot(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        #Calls function every day at 8 am
        self.schedule_repeating_event(self.say_Good_Morning, datetime.time(8), 86400)
        self.schedule_repeating_event(self.say_Good_Night, datetime.time(20), 86400)
    
    def initialize(self):
        self.register_entity_file('badMood.entity')

    @intent_file_handler('Help.intent')
    @adds_context('HelpContext')
    def handle_helperbot(self, message):
        self.speak_dialog('doYouNeedHelp')

    @intent_handler(IntentBuilder('YesHelpIntent').require("Yes").
                                  require('HelpContext').build())
    @removes_context('HelpContext')
    def handle_yes_help(self, message):
        self.speak_dialog('help')
        # Get Help

    @intent_handler(IntentBuilder('NoHelpIntent').require("No").
                                  require('HelpContext').build())
    @removes_context('HelpContext')
    def handle_no_help(self, message):
        self.speak_dialog('helpNo')

    @adds_context('FeelContext')
    def say_Good_Morning(self):
        self.speak_dialog("hello")
        self.speak_dialog("howAreYou")

    def say_Good_Night(self):
        self.speak_dialog("goodNight")

    @intent_file_handler("TakeMyPhoto.intent")
    def take_Photo_manually(self,message):
        self.take_Photo()

    @adds_context('PhotoContext')
    def take_Photo(self):
        self.speak_dialog("photo", expect_response=True)
    
    @intent_handler(IntentBuilder('YesPhotoIntent').require("Yes").
                                  require('PhotoContext').build())
    @removes_context('PhotoContext')
    def handle_Photo_intent(self,message):
        self.speak_dialog("photoYes")
        for i in range(10, 0, -1):
            self.speak(str(i) + " .")
        self.speak_dialog("cheese")   
        # Take picture here

    @intent_handler(IntentBuilder('NoPhotoIntent').require("No").
                                  require('PhotoContext').build())
    @removes_context('PhotoContext')
    def handle_no_Photo_intent(self,message):
        self.speak_dialog("photoNo")
        self.schedule_event(self.take_Photo, datetime.datetime.now(), 60)


    @intent_handler(IntentBuilder('BadMoodIntent').require("Me").require("Bad").
                                  require('FeelContext').build())
    @removes_context('FeelContext')
    def handle_pos_res_intent(self, message):
        # Handle Positive Respones
        # Make Robot Smile
        self.speak_dialog("goodMoodD")
        

    @intent_handler(IntentBuilder('GoodMoodIntent').require("Me").require("Good").
                                  require('FeelContext').build())
    @removes_context('FeelContext')
    def handle_neg_res_intent(self, message):
        # Handle Help Call
        # Make Robot Sad 
        self.speak_dialog("badMoodD")

    @intent_handler(IntentBuilder("").require("Test").require("Adapt"))
    def handle_hello_world_intent(self, message):
        # In this case, respond by simply speaking a canned response.
        # Mycroft will randomly speak one of the lines from the file
        #    dialogs/en-us/hello.world.dialog
        self.speak_dialog("test")

def create_skill():
    return Helperbot()
