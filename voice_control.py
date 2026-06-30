import speech_recognition as sr
import threading
import time
from snake_game import SnakeGame  # Only imports the game

def voice_loop(game):
    print("Starting voice loop...")
    r = sr.Recognizer()
    try:
        mic_index = 1  # or whichever device number matches your main mic
        with sr.Microphone(device_index=mic_index) as source:

            print("Microphone found. Adjusting for ambient noise (this may take a few seconds)...")
            r.adjust_for_ambient_noise(source, duration=3)  # Increased to 3 seconds for better calibration
            r.energy_threshold = 150  # Lower threshold to detect softer voices (default is ~300, try 200-400)
            print("Ready! Speak commands like 'up', 'down', etc. Say them clearly and a bit louder.")
            
            while game.running:
                try:
                    print("Listening...")
                    audio = r.listen(source, timeout=0.5, phrase_time_limit=1)
  
                    text = r.recognize_google(audio).lower()
                    print(f"Recognized: '{text}'")
                    
                    if "up" in text:
                        print("Command: UP")
                        game.set_direction("UP")
                    elif "down" in text:
                        print("Command: DOWN")
                        game.set_direction("DOWN")
                    elif "left" in text:
                        print("Command: LEFT")
                        game.set_direction("LEFT")
                    elif "right" in text:
                        print("Command: RIGHT")
                        game.set_direction("RIGHT")
                    elif "pause" in text:
                        print("Command: PAUSE")
                        game.paused = not game.paused
                    elif "restart" in text:
                        if game.game_over:
                            print("Command: RESTART")
                            game.reset()
                        else:
                            print("Restart ignored: Game not over.")
                    elif "quit" in text:
                        print("Command: QUIT")
                        game.running = False
                    
                except sr.WaitTimeoutError:
                    pass  # No audio, keep listening
                except sr.UnknownValueError:
                    print("Could not understand audio - try speaking clearer, louder, or in a quieter room.")
                except sr.RequestError as e:
                 print(f"[!] Network or Google API error: {e}")

                time.sleep(0.1)
    except Exception as e:
        print(f"Error with microphone: {e}")
if __name__ == "__main__":
    print("Starting game with voice control...")
    game = SnakeGame()
    voice_thread = threading.Thread(target=voice_loop, args=(game,), daemon=True)
    voice_thread.start()
    game.run()