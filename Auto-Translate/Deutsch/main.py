import json
import keyboard
import datetime
import colorama
from googletrans import Translator
from colorama import Back, Fore, Style

colorama.init(autoreset=True)   # To suppress a not necessary output in CMD

# Aktuelle Zeit und Datum
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

current_word = ""
current_sentence = ""
prev_sentence = ""
key_pressed = set()
translator = Translator()

# Funktion zum Ändern der Übersetzungssprachen
def change_languages():
    global src_language, dest_language, convert_to_lowercase, prev_sentence

    print("-"*80)
    print("")
    # Clear the previous sentence
    prev_sentence = ""
    src_language = input("Bitte geben Sie die Quellsprache ein (z.B. 'de' für Deutsch): ")
    dest_language = input("Bitte geben Sie die Zielsprache ein (z.B. 'en' für Englisch): ")
    convert_to_lowercase = input("Möchten sie den übersetzten Text immer in" + Fore.BLUE + "Kleinbuchstaben" + Style.RESET_ALL + " haben? (ja/nein): ")
    if convert_to_lowercase == "ja":
        convert_to_lowercase = True
    elif convert_to_lowercase == "nein":
        convert_to_lowercase = False
    print("")
    print(f"Es wird jetzt übersetzt von " + Fore.GREEN + f"'{src_language}'" + Style.RESET_ALL + " nach " + Fore.GREEN + f"'{dest_language}'")
    if convert_to_lowercase == True:
        print("Der Übersetzte Text wird immer" + Fore.BLUE + " Kleingeschrieben\n")
    elif convert_to_lowercase == False:
        print("Der Übersetzte Text wird mit richtiger" + Fore.BLUE + " Rechtschreibung" + Style.RESET_ALL + " Rechtschreibung übersetzt\n")
    print("-"*80)
    print("")
    # Speichern der Übersetzungssprachen in der JSON-Datei
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
                current_word = current_word[:-1]  # Lösche das letzte Zeichen
            elif event.name == "right shift":
                # Hinzufügen des aktuellen Worts zum aktuellen Satz
                current_sentence += current_word
                # Prüfen, ob der aktuelle Satz nicht leer ist und mindestens ein Zeichen eingegeben wurde
                if current_sentence and current_word:
                    print(current_word)
                    # Übersetzen der Eingabe von der gespeicherten Quellsprache zur gespeicherten Zielsprache
                    translated_sentence = translator.translate(current_sentence, src=src_language, dest=dest_language).text
                    # Umwandeln des übersetzten Satzes in Kleinbuchstaben, falls die Einstellung aktiviert ist
                    if convert_to_lowercase:
                        translated_sentence = translated_sentence.lower()
                    # Löschen der vorherigen Eingabe von der Tastatur
                    keyboard.press_and_release('ctrl+a, backspace')
                    # Ausgabe der Ausgabe
                    print(translated_sentence)
                    # Senden der übersetzten Eingabe an die Tastatur
                    keyboard.write(translated_sentence, 0.01)
                    print("")
                    prev_sentence = translated_sentence
                    # Zurücksetzen des aktuellen Wortes
                    current_word = ""
                    # Zurücksetzen des aktuellen Satzes
                    current_sentence = ""
                    # Abschicken der übersetzten Eingabe
                    keyboard.press_and_release('enter')
                else:
                    current_word = ""  # Wenn der aktuelle Satz leer ist oder kein Zeichen eingegeben wurde, setzen wir current_word zurück

            # Wenn 'enter' gedrückt wurde wird ein neuer Satz angefangen und alles andere gelöscht
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
            print(Fore.RED + "\nFalsche Abkürzung in der Ausgangssprache. Bitte überprüfe die abkürzungen, die sie eingegeben haben und ändern sie diese mit" + Fore.CYAN+ " 'Strg + 7'!\n")

        elif str(ve) == "invalid source language":
            print(Fore.RED + "\nFalsche Abkürzung in der Ursprungssprache. Bitte überprüfe die abkürzungen, die sie eingegeben haben und ändern sie diese mit" + Fore.CYAN+ " 'Strg + 7'!\n")

        else:
            raise ve

print("Made by" + Fore.RED + " MyName99a")
print(f"It's {now}\n")
print("-"*80)
print("")

print("Abkürzungen für einige Sprachen (Google für mehr): ")
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

# Laden der gespeicherten Übersetzungssprachen, falls die Datei "languages.json" vorhanden ist
try:
    with open("settings.json", "r") as file:
        data = json.load(file)
    src_language = data["src_language"]
    dest_language = data["dest_language"]
    convert_to_lowercase = data.get("convert_to_lowercase", False)
    print("Es wird übersetzt von " + Fore.GREEN + f"'{src_language}'" + Style.RESET_ALL + " nach " + Fore.GREEN + f"'{dest_language}'")
    if convert_to_lowercase == True:
        print("Der Übersetzte Text wird immer" + Fore.BLUE + " Kleingeschrieben\n")
    elif convert_to_lowercase == False:
        print("Der Übersetzte Text wird mit richtiger" + Fore.BLUE + " Rechtschreibung" + Style.RESET_ALL + " übersetzt\n")
except FileNotFoundError:
    print("Die Datei 'languages.json' wurde nicht gefunden.")
    src_language = input("Bitte geben Sie die Quellsprache ein (z.B. 'de' für Deutsch): ")
    dest_language = input("Bitte geben Sie die Zielsprache ein (z.B. 'en' für Englisch): ")
    convert_to_lowercase = input("Möchten sie den übersetzten Text immer in" + Fore.BLUE + " Kleinbuchstaben" + Style.RESET_ALL + " haben? (ja/nein): ")
    if convert_to_lowercase == "ja":
        convert_to_lowercase = True
    elif convert_to_lowercase == "nein":
        convert_to_lowercase = False
    print("")
    print("-"*80)
    print("")

    # Speichern der Übersetzungssprachen in einer JSON-Datei
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
    # Warten 'Strg + 8' zum beenden
    keyboard.wait("strg + 8")
except KeyboardInterrupt:
    pass
finally:
    # Beenden der Tastaturüberwachung
    keyboard.unhook_all()
    print("Tastatureingabe wurde beendet.")
