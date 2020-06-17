import schedule
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_file_handler, intent_handler
from mycroft.skills.context import adds_context, removes_context

class Helperbot(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.photoJob = None
        #Calls function every day at 8 am
        schedule.every().day.at("08:00").do(self.say_Good_Morning)
        # Calls function every day at 8 pm
        schedule.every().day.at("20:00").do(self.say_Good_Night)
    
    def initialize(self):
        self.register_entity_file('badMood.entity')

    @intent_file_handler('Help.intent')
    def handle_helperbot(self, message):
        self.speak_dialog('doYouNeedHelp')

    
    def say_Good_Morning(self):
        self.speak_dialog("hello")
        #self.speak_dialog("howAreYou",excpect_response=True)

    def say_Good_Night(self):
        self.speak_dialog("goodNight")

    @intent_file_handler("TakeMyPhoto.intent")
    def take_Photo_manually(self,message):
        self.take_Photo()

    @adds_context('PhotoContext')
    def take_Photo(self):
        self.photoJob = None
        self.speak_dialog("photo", expect_response=True)
    
    @intent_handler(IntentBuilder('YesPhotoIntent').require("Yes").
                                  require('PhotoContext').build())
    @removes_context('PhotoContext')
    def handle_Photo_intent(self,message):
        self.speak_dialog("photoYes")
        if self.photoJob != None:
            schedule.cancel_job(self.photoJob)        
        # Take picture here

    @intent_handler(IntentBuilder('NoPhotoIntent').require("No").
                                  require('PhotoContext').build())
    @removes_context('PhotoContext')
    def handle_no_Photo_intent(self,message):
        self.speak_dialog("photoNo")
        #self.photoJob = schedule.every(10).minutes.do(self.take_Photo)
        self.photoJob = schedule.every(1).minutes.do(self.take_Photo)


    @intent_file_handler("Good.intent")
    def handle_pos_res_intent(self, message):
        # Handle Positive Respones
        # Make Robot Smile
        self.speak_dialog("goodMoodD")
        

    @intent_file_handler("Bad.intent")
    def handle_neg_res_intent(self, message):
        # Handle Help Call
        # Make Robot Sad 
        mood = message.data.get('badMood')
        if mood is not None:
            self.speak_dialog("sorry", data={"mood": mood})
        else:
            self.speak_dialog("badMoodD")

    @intent_handler(IntentBuilder("").require("Test").require("Adapt"))
    def handle_hello_world_intent(self, message):
        # In this case, respond by simply speaking a canned response.
        # Mycroft will randomly speak one of the lines from the file
        #    dialogs/en-us/hello.world.dialog
        self.speak_dialog("test")

def create_skill():
    return Helperbot()
