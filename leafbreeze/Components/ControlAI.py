from leafbreeze.Components.Constants.constants import *
import openai
import threading

from gtts import gTTS # type: ignore
import os

openai.api_key = API_KEY

low_health_prompt = "I want you to decide some superpowers for the leaf, like going invisible, teleporting away, and climbing back into the tree, or you can choose it to do nothing, and you should give it a small percent of cases when it actually is choosing a superpower, but just when it is kinda down, with just one word (teleporting, invisibility, resetting or nothing). The idea is, that when the player compleates most of the Simon Says, the leaf gets superpowers to try to save itself."

class AI():
    def __init__(self, constants: Constants):
        self.constants = constants

        self.last_percent = -1
        self.last_finger = -1
        self.first_word = "Simon"


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
        ])
    
        task_output = ""
        for chunk in response:
            if chunk.choices[0].delta.get('content'):
                task_output += chunk.choices[0].delta['content']
                #print(chunk.choices[0].delta['content'], end="")
        
        return task_output
    
    def generate_dialogue(self, finger: int, lives: int, catch_streak: int, position_x: int):
        response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "user", "content": "I want you to generate the best ever 10 word 'Simon Says' prompts, but be exact 95 percent of the times. Always start with the formula Simion Says, but you should change the name sometimes, to confuze the player, rerely, to be similar but not noticed. You also need to include the number of fingers the player needs to rise, which is {0}, try to not mess with those, keep them exact. Very rare. Oh yeah, and you should alert the player ocasionally how many times does it need to still try and catch the leave befor actually doing it, here is the number {1}. You can mention {2}, also being subtile. And tell them ocasionally that their position is wrong. In a veeery short mesage, of 1 sentance only, like 10 or so words. Don't talk about other body parts, besides the palm. Use just fingers, and JUST fingers., Try to be 95 percent serious and not do any emotional harm to them".format(finger, lives, catch_streak)}
        ],
        stream=  True)
    
        task_output = ""
        for chunk in response:
            if chunk.choices[0].delta.get('content'):
                task_output += chunk.choices[0].delta['content']
                print(chunk.choices[0].delta['content'], end="")
        
        self.first_word = task_output.split()[0]
        return task_output

    def play_audio(self, file_path):
        # Initialize pygame mixer
        pygame.mixer.init()

        # Load and play the audio file
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        pygame.mixer.music.unload()


    def setLast(self, percent: int, finger: int):
        self.last_percent = percent
        self.last_finger = finger

    def speak(self, text):
        tts = gTTS(text = text, lang='en')

        try:
            tts.save("output.mp3")
            pygame.mixer.init()
            pygame.mixer.music.load("output.mp3")

            audio_thread = threading.Thread(target = self.play_audio, args=("output.mp3",))
            audio_thread.start()
        except: 
            pass
    
    def lastPromptWasSimon(self):
        return self.first_word == "Simon"

    

