import matplotlib.pyplot as plt
import streamlit as st
from wordcloud import WordCloud


@st.cache_data
def visualize_barchart(_counter, num_words):
    plt.rc("font", family="Malgun Gothic")
    plt.rc("axes", unicode_minus=False)

    most_common = _counter.most_common(num_words)
    word_list = [w for w, _ in most_common]
    count_list = [c for _, c in most_common]

    fig, ax = plt.subplots()
    ax.barh(word_list[::-1], count_list[::-1])
    st.pyplot(fig)


@st.cache_data
def visualize_wordcloud(_counter, num_words):
    font_path = "C:/Windows/Fonts/malgun.ttf"
    wc = WordCloud(
        background_color="ivory",
        width=800,
        height=600,
        max_words=num_words,
        font_path=font_path,
    )
    wc = wc.generate_from_frequencies(dict(_counter))

    fig, ax = plt.subplots()
    ax.imshow(wc)
    ax.axis("off")
    st.pyplot(fig)