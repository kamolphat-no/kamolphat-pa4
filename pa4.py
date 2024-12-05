import streamlit as st
import openai
import json
import pandas as pd

# Get the API key from the sidebar called OpenAI API key
user_api_key = st.sidebar.text_input("OpenAI API key", type="password")

client = openai.OpenAI(api_key=user_api_key)
prompt = """ Act as a song analyst. You will receive a song name and full lyrics 
            and you will give the song key message, theme, interesting words that support this theme
            and other songs related with this theme. Give me a list of key message and theme in JSON string.
            And List 10 intersting words in JSON array, one word per line.
            Each word should have 3 fields:
            - "word" - word that support song theme or key message if word is not in english, 
                       give that word in original language
            - "definition" - if the word is in english, give the definition in english 
                             but if the word is in other langauges, give the english translation
            - "description" - a description why that word support the theme
            And give me a list of other recommended songs in JSON string.
            The key message should be 1 to 2 sentences only. The theme should be only 3 words.
            Other related songs should be 3 to 5 songs only.
            Don't say anything at first. Wait for the user to say something.
        """

# write the streamlit input page
st.title('Song message')
st.markdown('Input name of the song with full lyrics. \n\
            The AI will give you key message and theme of the songs. \n\
            Interesting word list and other recommended songs will be also provided.')

user_input = st.text_area("Enter song name and lyrics : ", " Typing here... ")

# submit button after text input
if st.button('Send'):
    messages_so_far = [
        {"role": "system", "content": prompt},
        {'role': 'user', 'content': user_input},
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_so_far
    )
    # Show the response from the AI in a box
    st.subheader('**AI response :**')
    ai_response = response.choices[0].message.content

    response_dict = json.loads(ai_response)

    st.write(response_dict)

    key_message = response_dict['key_message']
    st.write('**Key Message**')
    st.write(key_message)

    theme = response_dict['theme']
    st.write('\n **Theme**')
    st.write(theme)

    # vocab_df = pd.DataFrame.from_dict(response_dict)
    # st.table(vocab_df)

    other_song = response_dict['related_songs']
    st.write('\n **Other recommended songs**')
    st.write(other_song)


