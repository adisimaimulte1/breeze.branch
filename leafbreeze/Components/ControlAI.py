from leafbreeze.Components.Constants.constants import *
import openai

openai.api_key = API_KEY

low_health_prompt = "I want you to decide some superpowers for the leaf, like going invisible, teleporting away, and climbing back into the tree, or you can choose it to do nothing, and you should give it a small percent of cases when it actually is choosing a superpower, but just when it is kinda down, with just one word (teleporting, invisibility, resetting or nothing). The idea is, that when the player compleates most of the Simon Says, the leaf gets superpowers to try to save itself."

class AI():
    def __init__(self, constants: Constants):
        self.constants = constants

        self.last_percent = -1
        self.last_finger = -1
    
    def generate_simon_stays_task(self):
        response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "user", "content": "Generate a 'Simon Says' task where the player has to move their hand into specific positions and raise different numbers of fingers. I want it to give me only two simple things: a random percent from 0 to 100 and a random value from 0 to 5. I also want the percent values to be at least 30 percent apart, each two consecutive ones. The answer needs to be only the two integers, separated by one space. The absolute difference of the percent you choose and the value {0} needs to be grated than 40 and the finger not to be {1}".format(self.last_percent, self.last_finger)}
        ],
        stream=  True)
    
        task_output = ""
        for chunk in response:
            if chunk.choices[0].delta.get('content'):
                task_output += chunk.choices[0].delta['content']
                #print(chunk.choices[0].delta['content'], end="")
        
        return task_output
    
    def generate_endgame_prompt(self):
        response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "user", "content": low_health_prompt}
        ],
        stream=  True)
    
        task_output = ""
        for chunk in response:
            if chunk.choices[0].delta.get('content'):
                task_output += chunk.choices[0].delta['content']
                #print(chunk.choices[0].delta['content'], end="")
        
        return task_output
    
    def setLast(self, percent: int, finger: int):
        self.last_percent = percent
        self.last_finger = finger

    

    

