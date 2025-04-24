import plotly.express as px
import pandas as pd
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pickle
import requests
from io import BytesIO

st.set_page_config(layout="wide")


@st.cache_resource()
def load_model_1(model_name_1):
    dead_df = pd.read_csv(model_name_1)
    return (dead_df)

dead_df = load_model_1('https://raw.githubusercontent.com/uroplatus666/adaptation/master/data/dead_df.csv')


@st.cache_resource()
def load_model_2(model_name_2):
    injured_df = pd.read_csv(model_name_2)
    return (injured_df)


injured_df = load_model_2('https://raw.githubusercontent.com/uroplatus666/adaptation/master/data/injured_df.csv')

@st.cache_resource()
def load_model_3(model_name_3):
    money_df = pd.read_csv(model_name_3)
    return (money_df)


money_df = load_model_3('https://raw.githubusercontent.com/uroplatus666/adaptation/master/data/money_df.csv')

@st.cache_resource()
def load_model_4(model_name_4):
    phenomena_df = pd.read_csv(model_name_4)
    return (phenomena_df)


phenomena_df = load_model_4('https://raw.githubusercontent.com/uroplatus666/adaptation/master/data/phenomena_df.csv')

@st.cache_resource()
def load_model_5(model_name_5):
    sub_df = pd.read_csv(model_name_5)
    return (sub_df)


sub_df = load_model_5('https://raw.githubusercontent.com/uroplatus666/adaptation/master/data/sub_df.csv')

@st.cache_resource()
def load_model_6(model_name_6):
    loc_df = pd.read_csv(model_name_6)
    return (loc_df)


loc_df = load_model_6('https://raw.githubusercontent.com/uroplatus666/adaptation/master/data/loc_df.csv')

@st.cache_resource()
def load_model_7(model_name_7):
    # Загружаем файл по URL
    response = requests.get(model_name_7)
    response.raise_for_status()  # Проверка на ошибки запроса

    # Загружаем данные из байтового потока
    sub_ph_dict = pickle.load(BytesIO(response.content))
    return sub_ph_dict

sub_ph_dict = load_model_7('https://raw.githubusercontent.com/uroplatus666/adaptation/master/data/sub_ph_dict.pkl')

@st.cache_resource()
def load_model_8(model_name_8):
    # Загружаем файл по URL
    response = requests.get(model_name_8)
    response.raise_for_status()  # Проверка на ошибки запроса

    # Загружаем данные из байтового потока
    ph_sub_dict = pickle.load(BytesIO(response.content))
    return ph_sub_dict

ph_sub_dict = load_model_8('https://raw.githubusercontent.com/uroplatus666/adaptation/master/data/ph_sub_dict.pkl')

st.header('***:blue[База данных Опасные природные явления]***',anchor='center')
st.subheader('***:gray[Россия]  2018 - 2024***')
st.write('---')
with st.container():
    st.subheader('***Облака слов для всей базы данных***',
                 divider='blue')

    col1, col2 = st.columns([7, 2])

    with col2:
        category = st.radio(
            "**:blue[Выберите категорию]**",
            ['ОПЯ', 'Субъект', 'Локация'])
    with col1:
        if category == 'ОПЯ':
            cloud = phenomena_df.copy()
        elif category == 'Субъект':
            cloud = sub_df.copy()
        elif category == 'Локация':
            cloud = loc_df.copy()
        cloud.columns = ['word', 'num']
        cloud_drop = cloud[cloud['word'] != 'nothing']

        wordcloud = WordCloud(
            width=800,
            height=400,
            colormap='BrBG',
            background_color='black',
            min_font_size=2,
            max_font_size=70
        ).generate_from_frequencies(dict(zip(cloud_drop['word'], cloud_drop['num'])))

        # Создание фигуры и отображение облака слов
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        nan = cloud.loc[cloud['word'] == 'nothing', 'num']
        if len(nan)>0:
            count = round(nan.values[0]/30056*100, 2)
        else:
            count = 0
        st.write(f'**Доля пропущенных значений :red[{count} %]**')
        st.pyplot(fig)

st.write('---')

with st.container():
    st.subheader('***Опасные природные явления в выбранном субъекте РФ***',
                 divider='blue')
    col1, col2 = st.columns([7, 3])
    with col1:
        selected_key = 'г. Москва'
        selected_key = st.selectbox("Выберите субъект:", sub_ph_dict.keys())
        wordcloud = WordCloud(
            width=800,
            height=400,
            colormap='BrBG',
            background_color='black',
            min_font_size=2,
            max_font_size=70
        ).generate_from_frequencies(sub_ph_dict[selected_key])

        # Создание фигуры и отображение облака слов
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')

        st.pyplot(fig)
    with col2:
        if selected_key in sub_ph_dict:
            # Создаем DataFrame
            data = pd.DataFrame(list(sub_ph_dict[selected_key].items()), columns=["ОПЯ", "Количество"])


            # Сортируем по убыванию по колонке 'Количество'
            data = data.sort_values(by='Количество', ascending=False)

            # Отображаем таблицу в Streamlit
            st.dataframe(data, hide_index = True)
        else:
            st.write("Выбранный ключ отсутствует в словаре.")
st.write('---')

with st.container():
    st.subheader('***Субъекты РФ, в которых встречалось выбранное опасное природное явлени***',
                 divider='blue')
    col1, col2 = st.columns([7, 3])
    with col1:
        selected_key = 'наводнение'
        selected_key = st.selectbox("Выберите ОПЯ:", ph_sub_dict.keys())
        wordcloud = WordCloud(
            width=800,
            height=400,
            colormap='BrBG',
            background_color='black',
            min_font_size=2,
            max_font_size=70
        ).generate_from_frequencies(ph_sub_dict[selected_key])

        # Создание фигуры и отображение облака слов
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')

        st.pyplot(fig)
    with col2:
        if selected_key in ph_sub_dict:
            # Создаем DataFrame
            data = pd.DataFrame(list(ph_sub_dict[selected_key].items()), columns=["Субъект", "Количество"])


            # Сортируем по убыванию по колонке 'Количество'
            data = data.sort_values(by='Количество', ascending=False)

            # Отображаем таблицу в Streamlit
            st.dataframe(data, hide_index = True)
        else:
            st.write("Выбранный ключ отсутствует в словаре.")
st.write('---')
with st.container():
    st.subheader('***Количество ОПЯ и ущерб***',
                 divider='blue')
    category = st.selectbox(
        '**:gray[Выберите тип ущерба:]**',
        ('Погибшие', 'Пострадавшие',
         'Материальный ущерб'))
    if category == 'Погибшие':
        st.dataframe(dead_df, hide_index = True)
    elif category == 'Пострадавшие':
        st.dataframe(injured_df, hide_index = True)
    elif category == 'Материальный ущерб':
        st.dataframe(money_df, hide_index = True)
st.write('---')
