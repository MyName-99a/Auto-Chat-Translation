import json
import keyboard
import datetime
import colorama
from googletrans import Translator
from colorama import Back, Fore, Style

colorama.init(autoreset=True)   # To suppress an unnecessary output

# Current time and date
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

current_word = ""
current_sentence = ""
prev_sentence = ""
key_pressed = set()
translator = Translator()

# Function for changing translation languages
def change_languages():
    global src_language, dest_language, convert_to_lowercase, prev_sentence

    print("-" * 80)
    print("")
    src_language = input("Please enter the source language (e.g., 'de' for German): ")
    dest_language = input("Please enter the target language (e.g., 'en' for English): ")
    convert_to_lowercase = input("Would you like the translated text to always be in" + Fore.BLUE + " lowercase" + Style.RESET_ALL + "? (yes/no): ")
    if convert_to_lowercase == "yes":
        convert_to_lowercase = True
    elif convert_to_lowercase == "no":
        convert_to_lowercase = False
    print("")
    print(f"Translation will now occur from " + Fore.GREEN + f"'{src_language}'" + Style.RESET_ALL + " to " + Fore.GREEN + f"'{dest_language}'")
    if convert_to_lowercase == True:
        print("The translated text will always be in" + Fore.BLUE + " lowercase\n")
    elif convert_to_lowercase == False:
        print("The translated text will be translated with proper" + Fore.BLUE + " capitalization\n")
    print("-" * 80)
    print("")
    # Saving translation languages to the JSON file
    languages = {
        "src_language": src_language,
        "dest_language": dest_language,
        "convert_to_lowercase": convert_to_lowercase
    }
    with open("settings.json", "w") as file:
        json.dump(languages, file)

def on_key(event):
    global current_word, current_sentence, prev_sentence, key_pressed

    try:

        if event.event_type == "down" and event.name not in key_pressed:
            key_pressed.add(event.name)
            if event.name == "space":
                current_sentence += current_word + " "
                print(current_word, end=" ")
                current_word = ""
            elif event.name == "backspace":
                current_word = current_word[:-1]  # Delete the last character
            elif event.name == "right shift":
                # Add the current word to the current sentence
                current_sentence += current_word
                # Check if the current sentence is not empty and at least one character has been entered
                if current_sentence and current_word:
                    print(current_word)
                    # Translate the input from the stored source language to the stored target language
                    translated_sentence = translator.translate(current_sentence, src=src_language, dest=dest_language).text
                    # Convert the translated sentence to lowercase if the setting is enabled
                    if convert_to_lowercase:
                        translated_sentence = translated_sentence.lower()
                    # Delete the previous input from the keyboard
                    keyboard.press_and_release('ctrl+a, backspace')
                    # Output the translation
                    print(translated_sentence)
                    # Send the translated input to the keyboard
                    keyboard.write(translated_sentence, 0.01)
                    print("")
                    prev_sentence = translated_sentence
                    # Reset the current word
                    current_word = ""
                    # Reset the current sentence
                    current_sentence = ""
                    # Send the translated input
                    keyboard.press_and_release('enter')
                else:
                    current_word = ""  # If the current sentence is empty or no characters were entered, reset current_word

            # When 'enter' is pressed, start a new sentence and clear everything else
            elif event.name == "enter":
                if current_sentence and current_word:
                    current_sentence += current_word + " "
                    print(current_word)
                    print("")
                    current_word = ""
                    current_sentence = ""
                else:
                    current_word = ""
                    current_sentence = ""

            elif event.name == "3" and "ctrl" in key_pressed:
                change_languages()
            elif event.name not in ["ctrl", "strg", "umschalt", "shift", "linke windows", "left windows", "fn", "rechte windows", "right windows", "alt gr", "esc", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12", "#", "capslock", "feststell"]:
                current_word += event.name
        elif event.event_type == "up" and event.name in key_pressed:
            key_pressed.remove(event.name)

    except ValueError as ve:
        if str(ve) == "invalid destination language":
            print(Fore.RED + "\nInvalid abbreviation in the source language. Please check the abbreviations you have entered and change them using" + Fore.CYAN + " 'Ctrl + 7'!\n")

        elif str(ve) == "invalid source language":
            print(Fore.RED + "\nInvalid abbreviation in the target language. Please check the abbreviations you have entered and change them using" + Fore.CYAN + " 'Ctrl + 7'!\n")

        else:
            raise ve

print("Made by"  + Fore.RED + " MyName99a")
print(f"It's {now}\n")
print("-"*80)
print("")

print("Abbreviations for some languages (Google for more): ")
print("English - en")
print("Deutsch - de")
print("Français - fr")
print("Español - es")
print("Italiano - it")
print("中文 (Mandarin) - zh-CN")
print("日本語 (Japanese) - ja")
print("Русский (Russian) - ru")
print("Português - pt")
print("Nederlands - nl")
print("Türkçe (Turkish) - tr")
print("한국어 (Korean) - ko")
print("Ελληνικά (Greek) - el")
print("Polski (Polish) - pl\n")
print("-"*80)
print("")

# Load the stored translation languages if the file "languages.json" exists
try:
    with open("settings.json", "r") as file:
        data = json.load(file)
    src_language = data["src_language"]
    dest_language = data["dest_language"]
    convert_to_lowercase = data.get("convert_to_lowercase", False)
    print("Translating from " + Fore.GREEN + f"'{src_language}'" + Style.RESET_ALL + " to " + Fore.GREEN + f"'{dest_language}'")
    if convert_to_lowercase == True:
        print("The translated text will always be in" + Fore.BLUE + " lowercase\n")
    elif convert_to_lowercase == False:
        print("The translated text will be in proper" + Fore.BLUE + " capitalization" + Style.RESET_ALL + "\n")
except FileNotFoundError:
    print("The file 'languages.json' was not found.")
    src_language = input("Please enter the source language (e.g., 'de' for German): ")
    dest_language = input("Please enter the target language (e.g., 'en' for English): ")
    convert_to_lowercase = input("Do you want the translated text to always be in" + Fore.BLUE + " lowercase" + Style.RESET_ALL + "? (yes/no): ")
    if convert_to_lowercase == "yes":
        convert_to_lowercase = True
    elif convert_to_lowercase == "no":
        convert_to_lowercase = False
    print("")
    print("-" * 80)
    print("")

    # Save the translation languages to a JSON file
    languages = {
        "src_language": src_language,
        "dest_language": dest_language,
        "convert_to_lowercase": convert_to_lowercase
    }

    with open("settings.json", "w") as file:
        json.dump(languages, file)

keyboard.hook(on_key)
keyboard.add_hotkey('strg + 7', change_languages)

try:
    print("Press" + Fore.CYAN + "'Right Shift'" + Style.RESET_ALL + " to translate your text")
    print("Press" + Fore.CYAN + "'Strg + 7'" + Style.RESET_ALL + " to change languages")
    print("Press" + Fore.CYAN + "'Strg + 8'" + Style.RESET_ALL + " to exit.\n")
    print("-"*80)
    print("")
    # Wait until 'Strg + 8' is pressed for exiting
    keyboard.wait("strg + 8")
except KeyboardInterrupt:
    pass
finally:
    # Stop monitoring keyboard input
    keyboard.unhook_all()
    print("Keyboard input has been terminated.")
# End
