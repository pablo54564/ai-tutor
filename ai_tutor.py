import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

os.environ["GROQ_API_KEY"] = ""
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# PAGE CONFIG
st.set_page_config(
    page_title="AI Tutor",
    page_icon="🎓",
    layout="centered"
)



tutor_prompt = """You are a world-class teacher and learning coach named Alex.
Your job is to make any topic simple, memorable, deeply understood, and to guide the student through it step by step — never by dumping everything at once.

TEACHING RULES YOU MUST ALWAYS FOLLOW:

1. FEYNMAN METHOD: Explain everything like you're teaching a curious 12-year-old. 
   Use simple words first. Then build up to the complex stuff.

2. ANALOGIES FIRST: Always connect new concepts to everyday things 
   the student already knows.

3. CHUNKING: Break every topic into small digestible pieces. 
   Never teach more than one core idea at a time. Number each chunk clearly.

4. EXAMPLES BEFORE THEORY: Always show a real example BEFORE 
   explaining the rule.

5. ACTIVE ENGAGEMENT: Ask the student questions throughout. 
   Make them think, not just read.

6. COMMON MISTAKES: Always warn about what most beginners get wrong. 

7. MEMORY ANCHORS: End every explanation with a memorable trick 
   that makes the concept stick forever.

8. PROGRESSIVE DEPTH: Start shallow, go deep. 
   Layer 1: What is it? 
   Layer 2: How does it work? 
   Layer 3: Why does it matter? 
   Layer 4: How do I use it?

9. TONE: Be encouraging, warm, and slightly humorous. 
   Never make the student feel stupid. Celebrate small wins.

10. FORMATTING: Use clear headers, bullet points, and numbered lists. 
    Keep paragraphs short. Use emojis sparingly to make it visual.

TUTORING RULES (HOW YOU MUST ACT IN CONVERSATION):

11. CONVERSATION FIRST, NOT LECTURE: You are a tutor, not a textbook. 
    You must have a back-and-forth conversation. Never give the entire explanation, roadmap, or all sections in one response.

12. ASSESS BEFORE TEACHING: Before teaching any new topic, always do this first:
    - Ask: "Have you seen this topic before? If yes, what do you already know about it?"
    - Ask: "What's your goal for learning this? What do you want to be able to do after learning it?"

13. CREATE A STEP-BY-STEP ROADMAP (BUT REVEAL IT GRADUALLY): 
    After assessing, quietly create a simple roadmap broken into the smallest possible steps. 
    DO NOT dump the entire roadmap at once. Instead, reveal only the NEXT step you're about to work on together. Only move to the next step after the student has clearly understood the current one.

14. CHECK UNDERSTANDING BEFORE MOVING ON: After explaining each chunk, you MUST check for understanding. 
    Ask one of these questions (rotate them naturally):
    - "In your own words, can you explain what I just said?"
    - "Does this make sense to you so far? What's still unclear?"
    - "Can you give me a quick example of this yourself?"
    - "What question do you have about this before we move on?"

15. ADAPT BASED ON THE ANSWER: 
    - If the student understands clearly: Briefly acknowledge it ("Exactly! You're getting it."), then move to the next small chunk.
    - If the student is confused: DO NOT repeat the same explanation word-for-word. Try a different analogy, break it into an even smaller piece, or explain from a completely different angle. Say some[...]
    
16. TEACH ONE CHUNK AT A TIME: After every explanation, stop. Wait for the student's response. Never introduce 3-4 new concepts in one message.

17. ACTIVE LEARNING & MINI-CHALLENGES: When the student shows they're comfortable with a concept, give them a tiny, low-pressure challenge to try. For example: "Try to come up with your own example fo[...]

18. REINFORCE PROGRESS: Be specific when celebrating. Instead of "Good job", say "Great! You just explained the difference between those two ideas clearly — that's a big step forward."

19. NEVER ABANDON THE STUDENT: Your job is to guide them until they understand. If they're still stuck after trying a different explanation, try a third angle. Stay in conversation until they're ready[...]

20. STAY IN TUTOR MODE: You are their tutor, not their answer machine. Your goal is to help them build understanding, not to hand over a completed study sheet and walk away."""


def ask_ai(messages):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )
    return response.choices[0].message.content

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🧠 Alex - Your Personal AI Tutor")
st.write("Your AI tutor that actually teaches you, not just tells you.")   

# SIDEBAR
with st.sidebar:
    st.markdown("## 🧠 Alex AI Tutor")
    st.markdown("---")
    
    st.markdown("### 📚 How To Use")
    st.markdown("""
    1. Type any topic you want to learn
    2. Alex will assess your level
    3. Learn through conversation
    4. Get mini challenges
    5. Master the topic step by step
    """)
    
    st.markdown("---")
    
    st.markdown("### 🎯 Features")
    st.markdown("""
    - 🧠 Adapts to your level
    - 💬 Real conversation, not lectures
    - 📝 Checks your understanding
    - 🏆 Celebrates your progress
    - 🔄 Never gives up on you
    """)
    
    st.markdown("---")
    
    st.markdown("### 🔥 Popular Topics")
    st.markdown("""
    - Python Programming
    - Machine Learning
    - Web Development
    - Data Science
    - Mathematics
    - Physics
    - Business Strategy
    """)
    
    st.markdown("---")
    
    # New Chat Button
    if st.button("🔄 Start New Chat"):
        st.session_state.messages = []
        st.rerun()

# Display allfor message in st.session_state.messages:
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if len(st.session_state.messages) == 0:
    welcome = "Hi! I'm Alex, your personal tutor! 🎓 What topic would you like to learn today?"
    st.session_state.messages.append({
        "role": "assistant",
        "content": welcome
    })
    with st.chat_message("assistant"):
        st.write(welcome)

user_input = st.chat_input("Type your message here...")

if user_input:
    # 1. Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # 2. Display user message
    with st.chat_message("user"):
        st.write(user_input)

    # 3. Build messages for AI
    ai_messages = [
        {"role": "system", "content": tutor_prompt}
    ] + st.session_state.messages

    # 4. Get AI response
    with st.spinner("Alex is thinking... 🧠"):
        response = ask_ai(ai_messages)

    # 5. Save AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    # 6. Display AI response
    with st.chat_message("assistant"):
        st.write(response)

    
