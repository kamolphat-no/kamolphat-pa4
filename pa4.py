import streamlit as st
import openai
import json
import pandas as pd

# Get the API key from the sidebar called OpenAI API key
user_api_key = st.sidebar.text_input("OpenAI API key", type="password")

client = openai.OpenAI(api_key=user_api_key)
prompt = """ Act as a song analyst. You will receive full lyrics of the song 
            and you will give the song key message, theme, interesting words that support this theme
            and other songs related with this theme. 
            Give me a list of key message in 1 to 2 sentences and theme in 3 words in JSON array
            And List 10 intersting words in JSON array, one word per line.
            Each word should have 3 fields:
            - "word" - word in lyrics that support song theme or key message. If word is not in english, 
                       give that word in original language
            - "definition" - definition if that word. If the word is in english, give the definition in english.
                             but if the word is in other langauges, give the english translation.
            - "description" - a description why that word support the theme
            And give me a list of 5 other recommended songs with artist in JSON array.
            Give entire response in JSON array as this structure :
            [ {'key_message' : ' ' } , {'theme' : ' word, word and word '} , 
            {'interesting_words' : [{'word' : ' ' , 'definition' : ' ' , 'description' : ' '} , ..... ,
            {'word' : ' ' , 'definition' : ' ' , 'description' : ' '}] } ,
            {'related_songs' : ['song name - artist' , ' ' , ' ' , ' ' , ' ' ]} ]
            Don't say anything at first. Wait for the user to say something.
        """

# write the streamlit input page
st.title('Song message')
st.markdown('Input **full lyrics** of the song you want. \n\
            The AI will give you key message and theme of the song. \n\
            Interesting word list and other recommended songs will also be provided.')

user_input = st.text_area("Enter full lyrics only : ", " Typing here... ")

# submit button after text input
if st.button('Send'):
    if user_input :
        messages_so_far = [
            {"role": "system", "content": prompt},
            {'role': 'user', 'content': user_input},
        ]
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_so_far
        )
        # Show the response from the AI in a box
        st.write('**AI response :**')
        ai_response = response.choices[0].message.content

        # st.write(ai_response)

        response_dict = json.loads(ai_response)

        # st.write(response_dict)

        st.subheader('Key Message')
        key_message = response_dict[0].get('key_message',[])
        st.write(key_message)

        st.subheader('\n Theme')
        theme = response_dict[1].get('theme', [])
        st.write(theme)

        st.subheader('\n Interesting word list')
        vocab = response_dict[2].get('interesting_words', [])
        vocab_df = pd.DataFrame.from_dict(vocab)
        vocab_df.index = ['1','2','3','4','5','6','7','8','9','10']
        st.dataframe(vocab_df)

        st.subheader('\n Other recommended songs')
        other_songs = response_dict[3].get('related_songs', [])
        for index, song in enumerate(other_songs) :
            num = index + 1
            st.write(f'{num}. {song}')

    else:
        st.warning('Please enter the full lyrics of the song!')


