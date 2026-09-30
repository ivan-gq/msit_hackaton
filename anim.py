import sys
import time
import os
import pyfiglet

def animate_word_letter_by_letter(word: str, font: str = "slant", letter_delay: float = 0.3):
    current_text = ""
    
    for char in word:
        current_text += char
        
        # Move cursor to home / clear terminal
        sys.stdout.write("\033[H\033[2J")
        sys.stdout.flush()
        
        # Print cumulative ASCII banner
        rendered = pyfiglet.figlet_format(current_text, font=font)
        print(rendered)
        
        time.sleep(letter_delay)

# Usage
if __name__ == "__main__":
    animate_word_letter_by_letter("HELLO", font="slant", letter_delay=0.25)