import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import random

load_dotenv()

# OpenAI API 설정
key_id = os.getenv("OPENAI_API_KEY")
client = OpenAI(
    api_key=key_id
)

def generate_usernames(valid_input_names, account_type, favorite_words, number, mood):
    if mood == "Random":
        mood = random.choice(["nomal", "Cool", "Cute"])
    
    prompt = f"""
You are an expert in creating creative and personalized Instagram IDs. Please create 50 unique and attractive Instagram IDs based on the following user information and rules:

User Information:
1. Type name or word: "{valid_input_names}"
2. Account Type: {account_type}
3. Favorite words: {', '.join(favorite_words)}
4. Desired mood: {mood}
5. option number: {number}

Create ID Guidelines:

**Basic rules:**
- Length: Limited to 5-15 characters
- Available characters: English lowercase letters, numbers, underscore (_)
- Creatively combine the user's interests and favorite words, but not all words need to be used all the time
- Indirect reflection of the specified atmosphere
- Maintain the appropriate style for the selected account type
- A combination that's easy to pronounce and easy to remember
- Can include meaning or language play
- Give it a trendy, modern feel, but prefer universal expression that can be used over time
- Excluding direct abusive language or offensive expressions
- Be careful not to overlap with existing brands or brand names
- Try different approaches, such as modifying the entered name or using only a part of it
- When using numbers, use meaningful numbers or years, etc
- Maintain diversity so that all proposals do not follow the same pattern
- Don't use direct mood words
- Do not use the letter 'x' and underscore(_) at the end of the whole word
- if their is option number: {number} use it.

**Additional guidelines:**
- **Use spelling changes or numbers:** 
  - Vowel Replacement: Replace "a" with "e" and "o" with "u" to give it a unique feel
    - - 예: "strawberry" → "strowberri", "sunshine" → "senchene"
  - Add or remove letters: make words unique but still recognizable by slightly modifying them
    - For example: "cool" → "cool" or "col", "magic" → "majic" or "mgic"
  - Speech-centric spelling: Spelling words as they sound instead of traditional spelling
    - - 예: "fantasy" → "fantazee"

- **Combination of words according to account purpose:**
  - Official Account: "Official"
  - Photo Account: "pic," "photo," or "film"
  - Job Showcase Account: "works" or "portpolio"
  - Daily accounts: "diary" or "daily"

- **Favorite word combinations:**
  - Enter three favorite words and create ID by combining words with positive meaning
    - - 예: music, fashion → music_fashion, or trumpet_jean

- **Mood Settings:**
  - **nomal:** forcus on gidelines
  - **Cool:** Use "x" to emojis between words
    - - 예: JayxZ, Jay_Z
  - **Cute:** Use emoticons between words (e.g. "0_0", "o.o", "o_o", "v.v")
    - Example: jazz0.0z

- **Pretty ID conditions:**
  - French or Spanish words available
  - Can use "x" between words

- **Korean conversion:**
  - If the input is Korean, each word is translated into simple English to give an interesting effect
    - For example: 김형제 → brother.kim, 김은성 → silver_song, 영 → ZERO

Based on the rules above, generate only 50 creative and practical IDs that reflect various moods. Print all IDs in lowercase English. 
Please place the IDs made of each condition evenly and show them.

"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.9,
        )
        suggestions = response.choices[0].message.content.strip().split('\n')
        return [suggestion.strip() for suggestion in suggestions]
    except Exception as e:
        st.error(f"Error generating usernames: {str(e)}")
        return []

st.title("Instagram Username Generator")

input_name = st.text_input("이름 또는 조합하고 싶은 단어 입력(쉼표로 구분):", "").split(',')
account_type = st.selectbox("계정 유형 선택:", ["nomal", "Daily life", "Official", "Photo", "Work showcase"])
favorite_words = st.text_input("(옵션)좋아하는 단어 입력 (쉼표로 구분):", "").split(',')
number = st.text_input("(옵션)넣었으면 하는 숫자")
mood = st.radio("원하는 아이디 무드 선택:", ["Random", "nomal", "Cool", "Cute"])

if st.button("아이디 생성"):
    # input_name 리스트가 비어 있지 않은지 확인
    valid_input_names = [name.strip() for name in input_name if name.strip()]
    
    if valid_input_names:
        with st.spinner("아이디 생성 중..."):
            suggestions = generate_usernames(valid_input_names, account_type, favorite_words, number, mood)
        if suggestions:
            st.success("아이디 제안이 성공적으로 생성되었습니다!")
            if mood == "Random":
                st.info(f"랜덤으로 선택된 무드: {random.choice(['nomal','Cool', 'Cute'])}")
            cols = st.columns(3)  # 3개의 열 생성
            for index, suggestion in enumerate(suggestions):
                cols[index % 3].write(suggestion)  # 각 열에 순서대로 아이디 제안 표시
        else:
            st.warning("아이디 제안을 생성하지 못했습니다. 다시 시도해 주세요.")
    else:
        st.error("최소 하나의 유효한 이름을 입력해 주세요.")
