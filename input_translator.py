import json
import time
import keyboard
import pyautogui
import requests
import pyperclip

from secret import API_KEY

PARENT = f"projects/input-translator-417713"

with open('config.json') as file:
  config = json.load(file)

def translate_text(text, source_language, target_language):
  if source_language == target_language:
    return text

  url = f'https://translation.googleapis.com/language/translate/v2?key={API_KEY}'

  # Request payload
  data = {
    'q': text,
    "source": source_language,
    "target": target_language,
    "format": "text"
  }

  # Send POST request to the API

  response = requests.post(url, data=data)
  json_response = response.json()
  if 'error' in json_response:
    print("Your IP is:")
    print(response.json()['error']['message'].split("(")[1].split(")")[0])
    # print("Press ESCAPE to close this window")
    keyboard.wait("esc")
    exit()

  # Parse response JSON
  translation = json_response['data']['translations'][0]['translatedText']

  return translation

def remove_last_2_characters(s):
  if len(s) < 2:
    return s  # Retourner la chaîne inchangée si elle contient moins de 3 caractères
  else:
    return s[:-2]  # Retourner tous les caractères sauf les trois derniers
  
def deux_derniers_caracteres(chaine):
  if len(chaine) >= 2:
    return chaine[-2:]
  else:
    return chaine  # Si la chaîne est trop courte, retourne la chaîne entière

def trigger():
  pyautogui.hotkey('ctrl', 'a')
  time.sleep(0.1)
  pyautogui.hotkey('ctrl', 'x')
  time.sleep(0.1)

  copied_text = pyperclip.paste()
  target_language = deux_derniers_caracteres(copied_text)
  text_to_translate = remove_last_2_characters(copied_text).strip()

  translated_text = translate_text(text_to_translate, config["source_language"], target_language)
  keyboard.write(translated_text)

hotkey_pressed = False
ctrl_pressed = False
alt_pressed = False

def test_end_hotkey():
  global ctrl_pressed
  global alt_pressed
  global hotkey_pressed
  if not ctrl_pressed and not alt_pressed and hotkey_pressed:
    hotkey_pressed = False
    trigger()

def on_triggered():
  global ctrl_pressed
  global alt_pressed
  global hotkey_pressed
  ctrl_pressed = True
  alt_pressed = True
  hotkey_pressed = True

def on_ctrl_release(event):
  global ctrl_pressed
  global alt_pressed
  if event.name == 'ctrl':
    ctrl_pressed = False
    test_end_hotkey()
    

def on_alt_release(event):
  global ctrl_pressed
  global alt_pressed
  if event.name == 'alt':
    alt_pressed = False
    test_end_hotkey()

# Add event listeners for Ctrl and Alt release
keyboard.on_release(on_ctrl_release)
keyboard.on_release(on_alt_release)

keyboard.add_hotkey(config["translate_shortcut"], on_triggered)
keyboard.wait()