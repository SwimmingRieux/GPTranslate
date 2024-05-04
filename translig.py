#use https://www.freeconvert.com/pdf-to-text/download
# default gpt prompt on OpenAI accout : You are a skilled editor known for your ability to simplify complex economical and philosophical text while preserving its meaning. You have a strong understanding of readability principles and how to apply them to improve text comprehension. Your task is to rephrase the following text, making it easier to understand for individuals with basic English skills in a manner that maintains all the original sentences while ensuring it's understandable for individuals with basic English skills. make the words and phrases as simple as possible. Focus on simplifying the grammatical structure and replacing words with simpler equivalents, while ensuring the core meaning remains intact. Additionally, aim to maintain a similar length to the original text.
# set cookies file
# set book.txt file
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import PyPDF2
from PyPDF2 import PdfReader
from telegram import Bot
from telegram.error import TelegramError
from telegram.ext import Updater, CommandHandler
import logging
import os
import time
import json
import asyncio


def prompting(text):
    global prompt_count
    time.sleep(30)
    while True:
        try:
            prompt_textarea = WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.ID, "prompt-textarea")))
            prompt_textarea.send_keys(text)
            prompt_textarea.send_keys(Keys.ENTER)
            time.sleep(20)
            answers = WebDriverWait(driver1, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.markdown.prose.w-full.break-words.dark\:prose-invert.dark")))
            answer = answers[prompt_count].text
            prompt_count = prompt_count+1
            return answer
        except Exception as e:
            continue

def translate(content):
    ActionChains(driver2).move_to_element(source_element).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
    source_element.send_keys(Keys.BACKSPACE)
    source_element.send_keys(content)
    time.sleep(10)
    flg = 1
    while flg:
        try:
            dest_element = driver2.find_element(By.CSS_SELECTOR, 'span.HwtZe')
            return dest_element.text
            flg = 0
        except:
            continue


def extract_paragraphs(txt_path):
    with open(txt_path, 'r', encoding='utf-8', errors='ignore') as file:
        paragraphs = file.read().split('\n') 
    return paragraphs


async def send_message_async(text):
    try:
        await bot.send_message(chat_id=username, text=text)
    except TelegramError as e:
        print(e)


async def main():
    
    for i in range(starting_paragraph, ending_paragraph, 1):
        if len(paragraphs[i]) == 1: # if paragraph only consists of one character, combine it with the next paragraph
            paragraphs[i+1] = paragraphs[i]+ paragraphs[i+1]
            del paragraphs[i]
            i = i-1
    
    book_text = ''
    for i in range(starting_paragraph, ending_paragraph, 1):
        if len(book_text) + len(paragraphs[i]) < prompt_characters_limit:
            book_text += ' ' + paragraphs[i]
        else:
            english_answer = prompting(book_text)
            await send_message_async(english_answer)    
            book_text = ''
            persian_answer = translate(english_answer)
            await send_message_async(persian_answer)    
    if(len(book_text) > 0):
        english_answer = prompting(book_text)
        book_text = ''
        persian_answer = translate(english_answer)
        await send_message_async(persian_answer)


starting_paragraph = 0
ending_paragraph = 0
prompt_count = 0
options = webdriver.ChromeOptions()
driver2 = webdriver.Chrome(options=options)
driver2.get("https://translate.google.com/?sl=en&tl=fa&op=translate")
time.sleep(20)

source_element = driver2.find_element(By.CSS_SELECTOR, 'textarea.er8xn')


script_dir = os.path.dirname(os.path.realpath(__file__))
pdf_filename = 'cookies.json'
cookies_file_path = os.path.join(script_dir, pdf_filename)
driver1 = webdriver.Chrome(options=options)
driver1.get("https://chat.openai.com/")
with open(cookies_file_path, "r") as file:
    cookies = json.load(file)

for cookie in cookies:
    if "sameSite" in cookie:
        del cookie["sameSite"]

for cookie in cookies:
    try:
        driver1.add_cookie(cookie)
        
    except:
        print('error:' + cookie["domain"] + cookie["name"])

driver1.refresh()

time.sleep(10)

prompt_characters_limit = 20000
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
BOT_TOKEN = '1' #replace with token
username = 1 # replace with username
bot = Bot(token=BOT_TOKEN)

script_dir = os.path.dirname(os.path.realpath(__file__))
pdf_filename = 'book.txt'
txt_path = os.path.join(script_dir, pdf_filename)
paragraphs = extract_paragraphs(txt_path)

asyncio.run(main())


#end :
driver1.quit()
driver2.quit()
