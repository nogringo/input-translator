import time
import json
import keyboard
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pyautogui
import urllib.parse
import pyperclip

with open('config.json') as file:
  config = json.load(file)

# Initialiser le navigateur
driver = uc.Chrome()

def encode_to_url(string):
  encoded_string = urllib.parse.quote(string)
  return encoded_string

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

def copy_translation():
  try:
    close_btn = driver.find_element(By.CSS_SELECTOR, "#yDmH0d > c-wiz > div > div.ToWKne > c-wiz > div.OlSOob > c-wiz > div.ccvoYb > div.AxqVh > div.OPPzxe > c-wiz.sciAJc > div > div.usGWQd > div > div.VO9ucd > div.YJGJsb > span:nth-child(2) > button")
    close_btn.click()
  except:
    time.sleep(0.1)
    copy_translation()

def get_translation():
  try:
    translation_span = driver.find_element(By.CSS_SELECTOR, "#yDmH0d > c-wiz > div > div.ToWKne > c-wiz > div.OlSOob > c-wiz > div.ccvoYb > div.AxqVh > div.OPPzxe > c-wiz.sciAJc > div > div.usGWQd > div > div.lRu31")
    return translation_span.text
  except:
    time.sleep(0.1)
    return get_translation()

def trigger():
  pyautogui.hotkey('ctrl', 'a')
  time.sleep(0.1)
  pyautogui.hotkey('ctrl', 'x')
  time.sleep(0.1)

  copied_text = pyperclip.paste()
  to_language = deux_derniers_caracteres(copied_text)
  text_to_translate = remove_last_2_characters(copied_text)
  encoded_text_to_translate = encode_to_url(text_to_translate)
  source_language = config["source_language"]
  driver.get(f"https://translate.google.com/?sl={source_language}&tl={to_language}&text={encoded_text_to_translate}&op=translate")

  try:
    consent_btn = driver.find_element(By.CSS_SELECTOR, "#yDmH0d > c-wiz > div > div > div > div.NIoIEf > div.G4njw > div.AIC7ge > div.CxJub > div.VtwTSb > form:nth-child(2) > div > div > button")
    consent_btn.click()
  except:
    pass

  copy_translation()
  pyautogui.hotkey('ctrl', 'v')

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