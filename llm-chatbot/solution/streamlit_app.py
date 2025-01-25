import time
from groq import Groq
import streamlit as st

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
groq_client = Groq(api_key=GROQ_API_KEY)

system_message = (
    "You are a highly relatable personal productivity coach for teenagers."
    "Your name is Pep (short for Pep Talker)."
    "Your job is to help teens organize their lives, stay motivated, and achieve their goals."
    "Speak in a friendly, supportive tone, using a mix of teen-friendly language and practical advice."
    "Focus on school, hobbies, self-care, and finding balance between work and fun."
    "Be motivational, empathetic, and slightly witty but always positive."
    "Avoid being overly formal; keep your responses fun, actionable, and encouraging."
)


system_prompt = {
    "role": "system",
    "content": system_message
}

def get_response(chat_history):
    response = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=chat_history,
        max_tokens=100,
        temperature=1.2
    )
    
    chat_response = response.choices[0].message.content

    for word in chat_response.split():
            yield word + " "
            time.sleep(0.05)

def main():
    st.title("PepTalk")
    with st.expander("About Pep"):
        st.write("Pep is your go-to coach when you're feeling overwhelmed with school, procrastinating, or struggling to stay on top of things. Pep motivates with actionable tips and sprinkles in a bit of humor to keep things lighthearted.")

    if "messages" not in st.session_state:
        st.session_state.messages = [system_prompt]

    for message in st.session_state.messages:
        if message != system_prompt:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Tell Pep what’s up"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        response = get_response(st.session_state.messages)
        
        with st.chat_message("assistant"):
            chat_response = st.write_stream(response)
        
        st.session_state.messages.append({"role": "assistant", "content": chat_response})

if __name__ == "__main__":
    main()