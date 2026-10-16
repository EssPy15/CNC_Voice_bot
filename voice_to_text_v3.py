import speech_recognition as sr
import serial
import time
import os

#Hardware Configuration
SERIAL_PORT = 'COM5'
BAUD_RATE = 115200

# Text Layout Rules
LINE_HEIGHT = 12
LETTER_WIDTH = 8
LETTER_SPACING = 4
SPACE_WIDTH = 15

# 20cm x 20cm Board Limits
MAX_LINE_WIDTH = 250 
MAX_Y_DEPTH = -180 

# Drawing Speed 
DRAW_SPEED = 400 

# State Variables - Start exactly at the zeroed coordinate
current_x = 0
current_y = 0

#SERVO COMMANDS FOR Z-AXIS
PEN_UP = "M3 S25\nG4 P0.3\n"     
PEN_DOWN = "M3 S17\nG4 P0.3\n"

OUTPUT_FILENAME = "voice_backup_2.gcode"

# Hardcoding every character
def get_letter_gcode(char, x, y):
    char = str(char).lower() 
    gcode = ""
    w = LETTER_WIDTH
    h = LINE_HEIGHT - 5  

    def move(dx, dy):
        return f"G0 X{int(round(x + dx))} Y{int(round(y + dy))}\n"
    
    def line(dx, dy):
        return f"G1 X{int(round(x + dx))} Y{int(round(y + dy))} F{DRAW_SPEED}\n"

    if char == 'a':
        gcode += move(0,0) + PEN_DOWN + line(w/2, h) + line(w, 0) + PEN_UP
        gcode += move(w/4, h/2) + PEN_DOWN + line(w*0.75, h/2) + PEN_UP
    elif char == 'b':
        gcode += move(0,0) + PEN_DOWN + line(0, h) + line(w, h*0.75) + line(0, h/2) + line(w, h*0.25) + line(0, 0) + PEN_UP
    elif char == 'c':
        gcode += move(w,h) + PEN_DOWN + line(0, h) + line(0, 0) + line(w, 0) + PEN_UP
    elif char == 'd':
        gcode += move(0,0) + PEN_DOWN + line(0, h) + line(w, h/2) + line(0, 0) + PEN_UP
    elif char == 'e':
        gcode += move(w,0) + PEN_DOWN + line(0, 0) + line(0, h) + line(w, h) + PEN_UP
        gcode += move(0, h/2) + PEN_DOWN + line(w*0.8, h/2) + PEN_UP
    elif char == 'f':
        gcode += move(0,0) + PEN_DOWN + line(0, h) + line(w, h) + PEN_UP
        gcode += move(0, h/2) + PEN_DOWN + line(w*0.8, h/2) + PEN_UP
    elif char == 'g':
        gcode += move(w,h) + PEN_DOWN + line(0, h) + line(0, 0) + line(w, 0) + line(w, h/2) + line(w/2, h/2) + PEN_UP
    elif char == 'h':
        gcode += move(0,h) + PEN_DOWN + line(0, 0) + PEN_UP
        gcode += move(0, h/2) + PEN_DOWN + line(w, h/2) + PEN_UP
        gcode += move(w, h) + PEN_DOWN + line(w, 0) + PEN_UP
    elif char == 'i':
        gcode += move(0,h) + PEN_DOWN + line(w, h) + PEN_UP
        gcode += move(w/2, h) + PEN_DOWN + line(w/2, 0) + PEN_UP
        gcode += move(0,0) + PEN_DOWN + line(w, 0) + PEN_UP
    elif char == 'j':
        gcode += move(0,h) + PEN_DOWN + line(w, h) + PEN_UP
        gcode += move(w/2, h) + PEN_DOWN + line(w/2, 0) + line(0, 0) + line(0, h/3) + PEN_UP
    elif char == 'k':
        gcode += move(0,h) + PEN_DOWN + line(0, 0) + PEN_UP
        gcode += move(w,h) + PEN_DOWN + line(0, h/2) + line(w, 0) + PEN_UP
    elif char == 'l':
        gcode += move(0,h) + PEN_DOWN + line(0, 0) + line(w, 0) + PEN_UP
    elif char == 'm':
        gcode += move(0,0) + PEN_DOWN + line(0, h) + line(w/2, h/2) + line(w, h) + line(w, 0) + PEN_UP
    elif char == 'n':
        gcode += move(0,0) + PEN_DOWN + line(0, h) + line(w, 0) + line(w, h) + PEN_UP
    elif char == 'o':
        gcode += move(0,0) + PEN_DOWN + line(0, h) + line(w, h) + line(w, 0) + line(0, 0) + PEN_UP
    elif char == 'p':
        gcode += move(0,0) + PEN_DOWN + line(0, h) + line(w, h) + line(w, h/2) + line(0, h/2) + PEN_UP
    elif char == 'q':
        gcode += move(0,0) + PEN_DOWN + line(0, h) + line(w, h) + line(w, 0) + line(0, 0) + PEN_UP
        gcode += move(w/2, h/2) + PEN_DOWN + line(w, 0) + PEN_UP
    elif char == 'r':
        gcode += move(0,0) + PEN_DOWN + line(0, h) + line(w, h) + line(w, h/2) + line(0, h/2) + line(w, 0) + PEN_UP
    elif char == 's':
        gcode += move(w,h) + PEN_DOWN + line(0, h) + line(0, h/2) + line(w, h/2) + line(w, 0) + line(0, 0) + PEN_UP
    elif char == 't':
        gcode += move(0,h) + PEN_DOWN + line(w, h) + PEN_UP
        gcode += move(w/2, h) + PEN_DOWN + line(w/2, 0) + PEN_UP
    elif char == 'u':
        gcode += move(0,h) + PEN_DOWN + line(0, 0) + line(w, 0) + line(w, h) + PEN_UP
    elif char == 'v':
        gcode += move(0,h) + PEN_DOWN + line(w/2, 0) + line(w, h) + PEN_UP
    elif char == 'w':
        gcode += move(0,h) + PEN_DOWN + line(w/4, 0) + line(w/2, h/2) + line(3*w/4, 0) + line(w, h) + PEN_UP
    elif char == 'x':
        gcode += move(0,h) + PEN_DOWN + line(w, 0) + PEN_UP
        gcode += move(w,h) + PEN_DOWN + line(0, 0) + PEN_UP
    elif char == 'y':
        gcode += move(0,h) + PEN_DOWN + line(w/2, h/2) + line(w, h) + PEN_UP
        gcode += move(w/2, h/2) + PEN_DOWN + line(w/2, 0) + PEN_UP
    elif char == 'z':
        gcode += move(0,h) + PEN_DOWN + line(w, h) + line(0, 0) + line(w, 0) + PEN_UP

    elif char == '0':
        gcode += move(0,h) + PEN_DOWN + line(w,h) + line(w,0) + line(0,0) + line(0,h) + line(w,0) + PEN_UP
    elif char == '1':
        gcode += move(w/2,h) + PEN_DOWN + line(w/2,0) + line(w/4,0) + line(3*w/4,0) + PEN_UP
    elif char == '2':
        gcode += move(0,h) + PEN_DOWN + line(w,h) + line(w,h/2) + line(0,h/2) + line(0,0) + line(w,0) + PEN_UP
    elif char == '3':
        gcode += move(0,h) + PEN_DOWN + line(w,h) + line(w,0) + line(0,0) + PEN_UP
        gcode += move(0,h/2) + PEN_DOWN + line(w,h/2) + PEN_UP
    elif char == '4':
        gcode += move(0,h) + PEN_DOWN + line(0,h/2) + line(w,h/2) + PEN_UP + move(w,h) + PEN_DOWN + line(w,0) + PEN_UP
    elif char == '5':
        gcode += move(w,h) + PEN_DOWN + line(0,h) + line(0,h/2) + line(w,h/2) + line(w,0) + line(0,0) + PEN_UP
    elif char == '6':
        gcode += move(w,h) + PEN_DOWN + line(0,h) + line(0,0) + line(w,0) + line(w,h/2) + line(0,h/2) + PEN_UP
    elif char == '7':
        gcode += move(0,h) + PEN_DOWN + line(w,h) + line(w/2,0) + PEN_UP
    elif char == '8':
        gcode += move(0,h/2) + PEN_DOWN + line(w,h/2) + line(w,h) + line(0,h) + line(0,0) + line(w,0) + line(w,h/2) + PEN_UP
    elif char == '9':
        gcode += move(w,0) + PEN_DOWN + line(w,h) + line(0,h) + line(0,h/2) + line(w,h/2) + PEN_UP

    # --- PUNCTUATION & SPACES ---
    elif char == '.':
        gcode += move(w/2, 0) + PEN_DOWN + line(w/2, 1) + PEN_UP 
    elif char == ',':
        gcode += move(w/2, 1) + PEN_DOWN + line(w/4, -2) + PEN_UP 
    elif char == '!':
        gcode += move(w/2, h) + PEN_DOWN + line(w/2, 3) + PEN_UP
        gcode += move(w/2, 0) + PEN_DOWN + line(w/2, 1) + PEN_UP
    elif char == '?':
        gcode += move(0, h*0.75) + PEN_DOWN + line(0, h) + line(w, h) + line(w, h/2) + line(w/2, h/2) + line(w/2, 2) + PEN_UP
        gcode += move(w/2, 0) + PEN_DOWN + line(w/2, 1) + PEN_UP
    elif char == ' ':
        pass 
    else:
        # Fallback for unknown characters
        gcode += move(0, h/2) + PEN_DOWN + line(w, h/2) + PEN_UP
        
    return gcode

#Layout Control
def carriage_return():
    global current_x, current_y
    current_x = 0 
    
    # Check if dropping down a line exceeds the board
    if (current_y - LINE_HEIGHT) < MAX_Y_DEPTH:
        print("!!! WARNING: Reached the bottom edge of the board. Stopping layout advance !!!")
        return ""
        
    current_y -= LINE_HEIGHT 
    return f"G0 X{current_x} Y{current_y}\n"

def new_paragraph():
    global current_x, current_y
    current_x = 0
    
    if (current_y - (LINE_HEIGHT * 2)) < MAX_Y_DEPTH:
        print("!!! WARNING: Cannot add paragraph, reached bottom edge of the board !!!")
        return carriage_return() 
        
    current_y -= (LINE_HEIGHT * 2) 
    return f"G0 X{current_x} Y{current_y}\n"

def process_text_to_gcode(spoken_text):
    global current_x, current_y
    full_gcode = ""
    
    words = spoken_text.split()
    for word in words:
        if word == "paragraph":
            full_gcode += new_paragraph()
            continue
            
        word_width = len(word) * (LETTER_WIDTH + LETTER_SPACING)
        # Wrap to next line if it exceeds max width
        if (current_x + word_width) > MAX_LINE_WIDTH:
            full_gcode += carriage_return()
            
        for char in word:
            full_gcode += get_letter_gcode(char, current_x, current_y)
            current_x += (LETTER_WIDTH + LETTER_SPACING)
            
        current_x += SPACE_WIDTH
        
    return full_gcode

# send and helper function
def send_and_save(arduino, file, gcode_string):
    if not gcode_string:
        return
        
    lines = gcode_string.split('\n')
    for line in lines:
        line = line.strip()
        if line: 
            file.write(line + '\n')
            file.flush()
            print(f"  Machine: {line}")
            
            arduino.write((line + '\n').encode())
            
            # Robust listening loop with Dead-Silence detection
            silence_counter = 0
            while True:
                # readline() waits up to 2 seconds (based on your main() setup)
                response = arduino.readline().decode('utf-8', errors='ignore').strip()
                
                if response:
                    silence_counter = 0 # Reset counter if Arduino says anything
                    if 'ok' in response.lower():
                        break  
                    elif 'error' in response.lower() or 'alarm' in response.lower():
                        print(f"  !!! GRBL ALERT: {response}")
                        break  
                else:
                    silence_counter += 1
                    if silence_counter >= 5:
                        print("\n  !!! CRITICAL: Arduino stopped responding.")
                        print("  !!! This usually means the board lost power or reset.")
                        break # Force break so Python doesn't freeze forever

def main():
    print(f"Connecting to Arduino on {SERIAL_PORT}...")
    try:
        arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
        time.sleep(2) 
        arduino.write(b"\r\n\r\n") 
        time.sleep(2)
        arduino.flushInput() 
        print("Connected successfully!\n")
    except Exception as e:
        print(f"Connection Error: {e}")
        print("Make sure UGS is CLOSED and the COM port is correct.")
        return

    recognizer = sr.Recognizer()

    with open(OUTPUT_FILENAME, "w") as file:
        print(f"Created backup file: {OUTPUT_FILENAME}")
        
        file.write("; --- SETUP ---\n")

        print("  Unlocking GRBL Alarm...")
        arduino.write(b"$X\n")
        time.sleep(1) 
        arduino.flushInput()
        
        send_and_save(arduino, file, "G92 X0 Y0 Z0\n") 
        send_and_save(arduino, file, "G90\nG21\n")     
        send_and_save(arduino, file, PEN_UP)

        file.write("; --- START DRAWING ---\n")

        with sr.Microphone() as source:
            print("Calibrating background noise... please wait 2 seconds.")
            recognizer.adjust_for_ambient_noise(source)
            
            print("\nReady! Say something to write, 'paragraph' to skip lines, or 'stop' to finish.")
            
            while True:
                # Break out of loop if we hit the Y limit
                if current_y <= MAX_Y_DEPTH:
                    print("\n[!] Reached maximum board space. Ending session.")
                    break
                    
                print("\nListening...")
                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    text = recognizer.recognize_google(audio).lower()
                    print(f"--> You said: '{text}'")
                    
                    if "stop" in text:
                        print("Stop command detected. Finishing up...")
                        
                        clean_text = text.replace("stop", "").strip()
                        if clean_text: 
                            file.write(f"; Spoken: {clean_text}\n")
                            gcode_block = process_text_to_gcode(clean_text)
                            send_and_save(arduino, file, gcode_block)
                        
                        print("Stopping in place and lifting pen...")
                        file.write("; --- END OF DRAWING ---\n")
                        
                        send_and_save(arduino, file, PEN_UP) 
                        break
                    
                    file.write(f"; Spoken: {text}\n")
                    gcode_block = process_text_to_gcode(text)
                    send_and_save(arduino, file, gcode_block)
                    print("--> Finished drawing phrase.")
                    
                except sr.WaitTimeoutError:
                    pass 
                except sr.UnknownValueError:
                    print("Didn't catch that. Please repeat.")
                except sr.RequestError:
                    print("Internet error. Speech recognition requires an active connection.")

    arduino.close()
    print(f"\nMachine disconnected safely.")
    print(f"Your backup G-code is saved in {os.path.abspath(OUTPUT_FILENAME)}")

if __name__ == "__main__":
    main()