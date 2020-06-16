import schedule
from mycroft import MycroftSkill, intent_file_handler


class Helperbot(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        #Calls function every day at 8 am
        schedule.every().day.at("08:00").do(self.say_Good_Morning)
        # Calls function every day at 8 pm
        schedule.every().day.at("20:00").do(self.say_Good_Night)
    
    def initialize(self):
        self.register_entity_file('badMood.entity')

    @intent_file_handler('Help.intent')
    def handle_helperbot(self, message):
        self.speak_dialog('help')

    def say_Good_Morning(self):
        self.speak_dialog("hello")
        self.speak_dialog("howAreYou")

    def say_Good_Night(self):
        self.speak_dialog("goodNight")
        # Here comes the photo part


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

def create_skill():
    return Helperbot()
