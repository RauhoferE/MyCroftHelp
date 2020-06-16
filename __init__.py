# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.

# Below is the list of outside modules you'll be using in your skill.
# They might be built-in to Python, from mycroft-core or from external
# libraries.  If you use an external library, be sure to include it
# in the requirements.txt file so the library is installed properly
# when the skill gets installed later by a user.
import schedule
from datetime import datetime
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG

# Each skill is contained within its own class, which inherits base methods
# from the MycroftSkill class.  You extend this class as shown below.

# TODO: Change "Template" to a unique name for your skill
class HelpSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(HelpSkill, self).__init__(name="HelpSkill")
        
        # Initialize working variables used within the skill.
        self.count = 0

        # Calls function every day at 8 am
        schedule.every().day.at("08:00").do(self.say_Good_Morning)

        # Calls function every day at 8 pm
        schedule.every().day.at("20:00").do(self.say_Good_Night)

    # The "handle_xxxx_intent" function is triggered by Mycroft when the
    # skill's intent is matched.  The intent is defined by the IntentBuilder()
    # pieces, and is triggered when the user's utterance matches the pattern
    # defined by the keywords.  In this case, the match occurs when one word
    # is found from each of the files:
    #    vocab/en-us/Hello.voc
    #    vocab/en-us/World.voc
    # In this example that means it would match on utterances like:
    #   'Hello world'
    #   'Howdy you great big world'
    #   'Greetings planet earth'
    @intent_handler(IntentBuilder("").require("Hello").require("World"))
    def handle_hello_world_intent(self, message):
        # In this case, respond by simply speaking a canned response.
        # Mycroft will randomly speak one of the lines from the file
        #    dialogs/en-us/hello.world.dialog
        self.speak_dialog("test.world")

    @intent_handler(IntentBuilder("").require("Count").require("Dir"))
    def handle_count_intent(self, message):
        if message.data["Dir"] == "up":
            self.count += 1
        else:  # assume "down"
            self.count -= 1
        self.speak_dialog("count.is.now", data={"count": self.count})
    
    @intent_handler(IntentBuilder("").require("Help").require("Me"))
    def handle_help_intent(self, message):
        # Handle  Help Call
        self.speak_dialog("test")
        pass

    @intent_handler(IntentBuilder("").require("Good"))
    def handle_pos_res_intent(self, message):
        # Handle Positive Respones
        # Make Robot Smile
        self.speak_dialog("test")
        pass

    @intent_handler(IntentBuilder("").require("Bad"))
    def handle_neg_res_intent(self, message):
        # Handle Help Call
        # Make Robot Sad 
        self.speak_dialog("test")
        pass

    def say_Good_Morning(self):
        self.speak_dialog("hello.world")
        self.speak_dialog("how.are.you")

    def say_Good_Night(self):
        self.speak_dialog("good.night")
        # Here comes the photo part

    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, there is no need to override it.  If you DO
    # need to implement stop, you should return True to indicate you handled
    # it.
    #
    # def stop(self):
    #    return False

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return HelpSkill()
