# Finished Haiku Bot

import requests
from bs4 import BeautifulSoup
import syllables
import random

# Your Discord Webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1339685758273061016/COYZDNyTFckb1PX2PDalu-LUnaea-BEIeQsG9c4ca1my9x2dZTmITiFinjRkjN0Dhini"

def get_jokes(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the webpage.")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    jokes = []
    
    for paragraph in soup.find_all('p'):
        text = paragraph.get_text(strip=True).lower()
        if text and text.startswith("q:"):
            text = text[2:].strip()  # Remove 'Q:' prefix
        if text and text.endswith('?'):
            jokes.append(text[:-1])  # Remove the '?' at the end
    
    return jokes

def extract_words(texts):
    words = []
    for text in texts:
        words.extend(text.split())
    return words

def construct_haiku(words):
    def get_line(syllable_count):
        line = []
        count = 0
        while count < syllable_count and words:
            word = random.choice(words).lower()
            word_syllables = syllables.estimate(word)
            if count + word_syllables <= syllable_count:
                line.append(word)
                count += word_syllables
        return " ".join(line)
    
    return f"{get_line(5)}\n{get_line(7)}\n{get_line(5)}"

def send_to_discord(haiku):
    payload = {"content": f"**Generated Haiku:**\n```{haiku}```"}
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    
    if response.status_code == 204:
        print("Haiku sent to Discord successfully!")
    else:
        print(f"Failed to send haiku: {response.status_code}, {response.text}")

def main():
    url = "https://www.comicrelief.org/posts/150-jokes-for-kids"
    jokes = get_jokes(url)
    if not jokes:
        return
    
    words = extract_words(jokes)
    haiku = construct_haiku(words)
    print("Generated Haiku:")
    print(haiku)

    send_to_discord(haiku)

if __name__ == "__main__":
    main()