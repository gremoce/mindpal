from django.shortcuts import render
from transformers import pipeline
import google.generativeai as genai
import os
import markdown

# Set up Google Gemini API key and model
os.environ["GOOGLE_API_KEY"] = "AIzaSyAG-DOggIMop4WNv-zpGUgSpPnBnuV6Qic"  # Replace with your actual API key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.0-flash')


# Load emotion classification model
emotion_pipeline = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions")
mood = ""

def home_view(request):
    global mood
    quote = ""  

    # Detect mood
    if request.method == "POST":
        user_input = request.POST.get("user_input")
        if user_input:
            mood_result = emotion_pipeline(user_input)[0]  
            mood = mood_result.get("label") 
            # Get a quote
            quote = generate_gemini_quote()
    
    # Testing
    print("Mood: ", mood, "quote: ", quote)

    return render(request, "home.html", {"mood": mood, "quote": quote})

def pomodoro(request):
    message = generate_timer_message()
    return render(request, "pomodoro.html", {"message": message})

def chat(request):    
    response = ""
    
    if request.method == "POST":
        question = request.POST.get("user_input")
        if question:
            response = generate_resources(question)

    return render(request, "chat.html", {"response": markdown.markdown(response)})


# Generates an inspirational quote based on the detected mood
def generate_gemini_quote():
    global mood
    prompt = f"give me a single fresh, original, and unique inspirational quote for someone who is feeling {mood}. without italics. Avoid repeating past responses"

    response = model.generate_content(prompt)

    if hasattr(response, "text"):
        return response.text.strip()
    return "Stay strong and believe in yourself!"

def generate_timer_message():
    global mood
    prompt = f"generate a 1-2 sentence encouragement study message for someone who is feeling {mood}. Avoid repeating past responses."

    response = model.generate_content(prompt)

    if hasattr(response, "text"):
        return response.text.strip()
    return "Stay strong and believe in yourself!"

def resources_page(request):
    resources = {
        "Mental Health & Emotional Well-being": [
            {
                "title": "Mental health of adolescents – WHO",
                "url": "https://www.who.int/news-room/fact-sheets/detail/adolescent-mental-health",
                "type": "Article",
            },
            {
                "title": "Mental Health Resources for Teens – Kids Help Phone",
                "url": "https://kidshelpphone.ca/get-info/",
                "type": "Article",
            },
            {
                "title": "We All Have Mental Health",
                "url": "https://www.youtube.com/watch?v=DxIDKZHW3-E",
                "type": "Video",
            },
            {
                "title": "Brain Basics: Anxiety Explained",
                "url": "https://www.youtube.com/watch?v=eG0YVforP84",
                "type": "Video",
            },
        ],
        "Study Tips & Time Management": [
            {
                "title": "Studying 101: Study Smarter Not Harder – University of North Carolina",
                "url": "https://learningcenter.unc.edu/tips-and-tools/studying-101-study-smarter-not-harder/",
                "type": "Article",
            },
            {
                "title": "3 Tips On How to Study Effectively – TED-Ed",
                "url": "https://www.youtube.com/watch?v=TjPFZaMe2yw",
                "type": "Video",
            },
            {
                "title": "The 9 BEST Scientific Study Tips – AsapSCIENCE",
                "url": "https://www.youtube.com/watch?v=TjPFZaMe2yw",
                "type": "Video",
            },
        ],
        "Stress Management & Self-Care": [
            {
                "title": "Stress management – Mayo Clinic",
                "url": "https://www.mayoclinic.org/healthy-lifestyle/stress-management/in-depth/stress-relievers/art-20047257",
                "type": "Article",
            },
            {
                "title": "Stress Management Tools – Small Steps",
                "url": "https://www.smallsteps.org.nz/app/deep-breathing",
                "type": "Tool",
            },
            {
                "title": "Understanding Stress and How to Manage It - HealthTexas Medical Group",
                "url": "https://www.youtube.com/watch?v=9Hto1HeMrYQ",
                "type": "Video",
            },
        ],
        "Support & Helplines": [
            {
                "title": "Kids Help Phone (Canada)",
                "url": "https://kidshelpphone.ca",
                "type": "Support",
            },
            {
                "title": "Crisis Text Line",
                "url": "https://www.crisistextline.org/",
                "type": "Support",
            },
        ]
    }
    return render(request, "resources.html", {"resources": resources})


def generate_resources(prompt):
    prompt = f"{prompt} keep it short, and provide some video links if possible"
    response = model.generate_content(prompt)

    if hasattr(response, "text"):
        return response.text.strip()
    return ""

from django.shortcuts import render

