import streamlit as st
import random
import string
import os
from openai import OpenAI
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
load_dotenv()
# OpenAI API 키 설정 (실제 사용 시 보안에 주의하세요)
# openai.api_key = st.secrets["openai_api_key"]
key_id = os.getenv("OPENAI_API_KEY")
client = OpenAI(
    api_key=key_id
)
def generate_rule_based_ids(name, account_type, number, mood, additional_words):
    ids = set()

    def generate_basic_id():
        id = name.lower().replace(' ', '')
        if number:
            id += str(number)
        if account_type == 'official':
            id += '.official'
        elif account_type == 'portfolio':
            id += '.portfolio'
        return id

    def apply_mood(id):
        if mood == 'cool':
            id = 'x'.join(id)
            id = id[:15]
        elif mood == 'cute':
            cute_suffixes = ['_uwu', '_kawaii', '_chu']
            id += random.choice(cute_suffixes)
        return id

    def generate_with_additional_words():
        words = [word.strip() for word in additional_words.split(',')]
        for word in words:
            ids.add(apply_mood(f"{name}_{word}{number}"))

    while len(ids) < 25:  # 규칙 기반으로 25개 생성
        if len(ids) < 10:
            ids.add(apply_mood(generate_basic_id()))
        elif len(ids) < 20 and additional_words:
            generate_with_additional_words()
        else:
            random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))
            ids.add(apply_mood(f"{name}_{random_suffix}{number}"))

    return list(ids)

def generate_ai_based_ids(name, account_type, mood, additional_words):
    prompt = f"Create 5 unique and creative Instagram usernames based on the following:\nName: {name}\nAccount type: {account_type}\nMood: {mood}\nAdditional words: {additional_words}\nEnsure the usernames are appropriate for Instagram and reflect the given mood."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a creative assistant specialized in generating unique and appealing Instagram usernames."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.8,
    )

    ai_generated_ids = response.choices[0].message['content'].strip().split('\n')
    return [id.split('. ')[-1] for id in ai_generated_ids if '. ' in id]

@st.cache_data
def generate_ids(name, account_type, number, mood, additional_words):
    rule_based_ids = generate_rule_based_ids(name, account_type, number, mood, additional_words)
    
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(generate_ai_based_ids, name, account_type, mood, additional_words) for _ in range(5)]
        ai_based_ids = [id for future in as_completed(futures) for id in future.result()]

    all_ids = rule_based_ids + ai_based_ids
    return list(set(all_ids))  # 중복 제거

# Streamlit UI
st.title('고급 인스타그램 아이디 생성기')

name = st.text_input('원하는 이름 또는 단어를 입력하세요')
account_type = st.selectbox('계정 유형을 선택하세요', ['일상', '공식', '포트폴리오'])
number = st.text_input('원하는 숫자를 입력하세요 (선택사항)')
mood = st.selectbox('원하는 아이디 무드를 선택하세요', ['일반', 'cool', 'cute'])
additional_words = st.text_input('추가로 좋아하는 단어들을 입력하세요 (쉼표로 구분)')

if st.button('아이디 생성'):
    if name:
        with st.spinner('아이디를 생성 중입니다...'):
            generated_ids = generate_ids(name, account_type, number, mood, additional_words)
        st.subheader('생성된 아이디:')
        cols = st.columns(5)
        for i, id in enumerate(generated_ids):
            cols[i % 5].write(id)
    else:
        st.error('이름 또는 단어를 입력해주세요.')