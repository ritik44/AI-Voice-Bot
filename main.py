import webbrowser
import datetime
import pyttsx3  # Text-to-speech library for Windows
import speech_recognition as sr
import openai
from config import apikey
import requests

chatStr = ""
engine = pyttsx3.init()  # Initialize the text-to-speech engine

def speak(text):
    engine.say(text)
    engine.runAndWait()

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Ritik: {query}\n Friday: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(f"Friday: {response['choices'][0]['text']}")
    chatStr += f"{response['choices'][0]['text']}\n"
    speak(response['choices'][0]['text'])  # Speak the response

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            print(f"Error: {str(e)}")
            return "Some Error Occurred. Sorry from Friday"


def ai(prompt):
    openai.api_key = apikey
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    response_text = response["choices"][0]["text"]
    print(response_text)
    speak(response_text)



def format_response(weather):
    try:
        name = weather['name']
        desc = weather['weather'][0]['description']
        temp = weather['main']['temp']

        final_str = 'City: %s \nConditions: %s \nTemperature(in Degree Celsius): %s' % (name,desc,temp)
    except:
        final_str = 'There was an error retrieving that information'

    return final_str


def get_weather(city_name):
    weather_key = 'aeafdac344956ace31c5beae8cde7312'
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'APPID':weather_key, 'q':city_name, 'units':'metric'}
    response = requests.get(url,params=params)
    weather=response.json()

    formatted_weather = format_response(weather)  # Call the format_response function
    return formatted_weather


def get_news(api_key):
    news_url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    response = requests.get(news_url)
    data = response.json()

    if data["status"] == "ok":
        articles = data["articles"]
        news_headlines = "\n".join([f"{i + 1}. {article['title']}" for i, article in enumerate(articles)])
        return f"Here are the latest news headlines:\n{news_headlines}"
    else:
        return "Could not fetch news at the moment."

if __name__ == '__main__':
    print('Welcome to Friday A.I')
    speak("Friday A.I")
    while True:
        query = takeCommand().lower()  # Convert query to lowercase for easier matching

        # Predefined commands for opening websites
        if any(keyword in query for keyword in ["open youtube", "open wikipedia", "open instagram", "open facebook", "open twitter"]):
            site_name = query.split("open ")[-1]
            if site_name == "youtube":
                url = "https://www.youtube.com"
            elif site_name == "wikipedia":
                url = "https://www.wikipedia.org"
            elif site_name == "instagram":
                url = "https://www.instagram.com"
            elif site_name == "facebook":
                url = "https://www.facebook.com"
            elif site_name == "Twitter":
                url = "https://www.twitter.com"
            else:
                url = "https://www.google.com"  # Default to Google if the site is not recognized
            speak(f"Opening {site_name}...")
            webbrowser.open(url)


        # Command to check the time
        elif "the time" in query:
            time_now = datetime.datetime.now().strftime("%H:%M")
            speak(f"Sir, the time is {time_now}")

        #Command to check the weather
        elif "weather" in query:
            city_name = input("Which city's weather would you like to know? ")
            weather_response = get_weather(city_name)
            print(weather_response)
            speak(weather_response)

        #command to check latest news headline
        elif "news" in query:
            news_api_key = "6c5d7e5d41704ca9bff69b34bb25a849"
            news_response = get_news(news_api_key)
            print(news_response)
            speak(news_response)


        # Command to interact with AI
        elif "using artificial intelligence" in query:
            ai(prompt=query)

        # Quit command
        elif "Friday quit" in query:
            speak("Goodbye, Sir.")
            exit()

        # Reset chat history
        elif "reset chat" in query:
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)
