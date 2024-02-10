import subprocess
import pyperclip
import pyautogui
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def main():

    driver = loadPage()
    #test(driver)
    name = enterName()
    newLifeAlphabet = enterAlphabet()
    waitForStart()
    startGame(name, driver, newLifeAlphabet)

# def test(driver):
    
#     input("\nWaiting...\n")
#     iframe = driver.find_elements(By.TAG_NAME, "iframe")[0]
#     driver.switch_to.frame(iframe)
    
#     # Replace 'your_variable_name' with the actual name of your JavaScript variable
#     variable_name = 'players'

#     # Wait for the variable to be defined or truthy
#     variable_value = wait_for_variable(driver, variable_name)

#     # Now you can use the variable_value in your code
#     print(variable_value)

#     # while True:
#     #     print(driver.execute_script("return players;"))

# def wait_for_variable(driver, variable_name, timeout=10):
#     """
#     Wait for a JavaScript variable to be defined or truthy in the global scope.
    
#     Args:
#         driver (WebDriver): The Selenium WebDriver instance.
#         variable_name (str): The name of the JavaScript variable to wait for.
#         timeout (int): Maximum time to wait in seconds.
    
#     Returns:
#         The value of the JavaScript variable.
#     """
#     return WebDriverWait(driver, timeout).until(
#         lambda d: d.execute_script(f"return (typeof {variable_name} !== 'undefined' && {variable_name} !== null);")
#     )

def makeDictionary():
    
    textFiles = ["compounds.txt", "dict.txt", "longs.txt", "minerals.txt", "sowpods.txt", "sub1.txt", "words.txt"]
    words = list()

    for fileName in textFiles:
        with open(fileName, 'r') as file:
            words.extend(file.read().split("\n"))

    words = list(set(words))
    words.sort()
    words = ["" + word.upper() + "\n" for word in words]
    
    with open("ALLWORDS.txt", 'w') as file:
        file.writelines(words)


def enterName():

    print("\nEnter the name you are using on BombParty:")
    return input("\n>>> ")

def loadPage():

    site = 'https://jklm.fun/'
    
    driver = webdriver.Firefox()
    driver.get(site)

    return driver

def enterAlphabet():

    print("\nChoose an option for the required letters for a new life:")
    print("[1] Standard Alphabet")
    print("[2] Standard Alphabet without \'Z\'")
    print("[3] Enter Included Letters")
    print("[4] Enter Excluded Letters")

    choice = input("\n>>> ")
    choice = int(choice)

    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    if (choice == 1):
        return alphabet
    elif (choice == 2):
        alphabet.remove("Z")
        return alphabet
    elif (choice == 3):
        print("\nEnter included letters:")
        included_letters = input("\n>>> ")
        included_letters = included_letters.upper()
        return list(included_letters)
    elif (choice == 4):
        print("\nEnter excluded letters:")
        excluded_letters = input("\n>>> ")
        excluded_letters = list(excluded_letters.upper())
        alphabet = [letter for letter in alphabet if letter not in excluded_letters]
        return alphabet
    
def waitForStart():
    
    print("\nEverything is ready. Press \'Enter\' once the game has started.")
    input("...")

def startGame(name, driver, newLifeAlphabet):
    
    iframe = driver.find_elements(By.TAG_NAME, "iframe")[0]
    driver.switch_to.frame(iframe)
    
    with open('dict.txt', 'r') as file:
        raw_dic = file.read()
        dic_list = raw_dic.split("\n")

    used_letters = []
    used_words = []
    desired_letters = ""

    while True:

        time.sleep(0.1)
        other_player_turn = driver.find_element(By.CSS_SELECTOR, "span[class=\'player\']").text
        if other_player_turn != "":
            continue

        desired_letters = driver.find_element(By.CSS_SELECTOR, "div[class=\'syllable\']").text
        desired_letters = desired_letters.upper()

        matching_words = []

        for i in range(len(dic_list)):
            if desired_letters in dic_list[i]:
                matching_words.append(dic_list[i])

        matching_words = [word for word in matching_words if word not in used_words]

        best_index = 0
        max_score = 0 
        for (i, word) in enumerate(matching_words):
            contained_letters = list(set(list(word)))
            similars = 0
            for letter in contained_letters:
                if letter in used_letters:
                    similars += 1
            score = len(contained_letters) - similars
            if score > max_score:
                best_index = i
                max_score = score

        best_word_choice = matching_words[best_index]
        used_words.append(best_word_choice)
        used_letters.extend(set(list(best_word_choice)))
        used_letters = list(set(used_letters))
        if (set(used_letters) == set(newLifeAlphabet)):
            used_letters = []

        print("\nPrompt:", desired_letters)
        print("Use this word:", best_word_choice)
        copy_to_clipboard(best_word_choice)
        autoType()

def copy_to_clipboard(txt):
    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)

def autoType():

    delay = 0.1
    randomization = random.randint(1, 5)
    
    time.sleep(delay * randomization)
    
    copied_text = pyperclip.paste()

    for char in copied_text:
        delay = 0.0001
        randomization = random.randint(1, 200)
        pyautogui.write(char, delay * randomization)

if __name__ == "__main__":
    main()