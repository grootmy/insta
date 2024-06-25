import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI API 설정
key_id = os.getenv("OPENAI_API_KEY")
client = OpenAI(
    api_key= key_id
)

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
        response = client.chat.completions.create(
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

input_name = st.text_input("이름 또는 단어 입력:", "")
account_type = st.selectbox("계정 유형 선택:", ["Daily life", "Official", "Photo", "Work showcase"])
favorite_words = st.text_input("좋아하는 단어 3개 입력 (쉼표로 구분):", "").split(',')
mood = st.radio("원하는 아이디 무드 선택:", ["일반","Cool", "Cute"])

if st.button("아이디 생성"):
    if input_name and len(input_name.strip()) >= 3:
        with st.spinner("아이디 생성 중..."):
            suggestions = generate_usernames(input_name.strip(), account_type, favorite_words, mood)
        if suggestions:
            st.success("아이디 제안이 성공적으로 생성되었습니다!")
            for suggestion in suggestions:
                st.write(suggestion)
        else:
            st.warning("아이디 제안을 생성하지 못했습니다. 다시 시도해 주세요.")
    else:
        st.error("최소 3글자 이상의 유효한 이름을 입력해 주세요.")