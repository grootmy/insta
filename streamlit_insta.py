import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI API 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_usernames(input_name, account_type, favorite_words, mood):
    prompt = f"""Create a list of 30 creative Instagram username suggestions based on the following criteria:

Input name or word: "{input_name}"
Account type: {account_type}
Favorite words: {', '.join(favorite_words)}
Desired mood: {mood}

Please follow these guidelines:
Please follow these guidelines:
** Change the Spelling or Use Numbers:

Replace letters with similar-looking numbers: Use numbers that resemble certain letters (e.g., 3 for E, 4 for A, 0 for O, 1 for I, 5 for S, 7 for T).

Examples: "nature" → "natur3", "elite" → "3lit3"
Substitute vowels: Change the spelling of vowels to create a unique look. This can include replacing "a" with "e", "o" with "u", and so on.

Examples: "strawberry" → "strowberri", "sunshine" → "senchene"
Alternate capitalization: Use a mix of uppercase and lowercase letters to create a distinctive appearance.

Examples: "yellow" → "yellOw", "flower" → "fLoWer"
Add or remove letters: Slightly alter the word by adding or removing letters to make it unique but still recognizable.

Examples: "cool" → "coool" or "col", "magic" → "majic" or "mgic"
Phonetic spelling: Spell the word based on how it sounds rather than its conventional spelling.

Examples: "photo" → "foto", "fantasy" → "fantazee"
Replace similar-sounding letters: Swap out letters that sound similar (e.g., "c" with "k", "ph" with "f").

Examples: "cat" → "kat", "phone" → "fone"
Use non-English alphabets: Incorporate characters from other alphabets that look similar to English letters.

Examples: "M" → "М" (Cyrillic), "A" → "Α" (Greek)
Combine the techniques: Use a mix of the above methods to create a truly unique spelling.

Examples: "creative" → "kr3ativ3", "hello" → "h3lL0w"
** Account Purpose:
Combine words based on the purpose of the account.

Official account: "official" or "verified"
Photo account: "pic", "photo" or "film"
Work showcase account: "works" or "portfolio"
Daily life account: "diary" or "daily"
** Favorite Words Combination:
Input three favorite words (e.g., favorite color, artist, hobby, etc.).
Combine the selected words.

Example: music, fashion → music_fashion
** Setting the Mood of the ID:
Set the desired mood for the ID.

For a cool mood: Use "x", "." and avoid using emoticons or underscores between words (e.g., JayZ, xJayZ).
For a cute mood: Incorporate emoticons like "0_0", "o.o", "..", "o_o" between words (e.g., bom..bit).
** Beautiful ID Conditions:

If the ID is 5-6 characters long, using underscores is acceptable.
If the ID is 7 or more characters long, avoid using underscores except for separating words (excluding emoticons).
Avoid using underscores before numbers.
Using French or Spanish words can be a nice touch.
** Converting Korean to English:
If the input is in Korean, translate each word to simple English for a playful effect.

Example: 김형제 → brother.kim, 김은송 → silver_song, 영 → ZERO
Please provide exactly 30 username suggestions, each on a new line. Ensure they are unique, trendy, and appealing and only output is English.

Now, generate 30 username suggestions based on the provided criteria. Show results randomly."""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            n=1,
            stop=None,
            temperature=0.8,
        )
        suggestions = response.choices[0].message.content.strip().split('\n')
        return [suggestion.strip() for suggestion in suggestions]
    except Exception as e:
        st.error(f"Error generating usernames: {str(e)}")
        return []

st.title("Instagram Username Generator")

input_name = st.text_input("Enter a name or word:", "")
account_type = st.selectbox("Select account type:", ["Official", "Photo", "Work showcase", "Daily life"])
favorite_words = st.text_input("Enter three favorite words (comma-separated):", "").split(',')
mood = st.radio("Select desired mood:", ["Cool", "Cute"])

if st.button("Generate Usernames"):
    if input_name and len(input_name.strip()) >= 3:
        with st.spinner("Generating usernames..."):
            suggestions = generate_usernames(input_name.strip(), account_type, favorite_words, mood)
        if suggestions:
            st.success("Username suggestions generated successfully!")
            for suggestion in suggestions:
                st.write(suggestion)
        else:
            st.warning("No username suggestions were generated. Please try again.")
    else:
        st.error("Please provide a valid name with at least 3 characters.")