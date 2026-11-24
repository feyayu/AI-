import streamlit as st
import mylib.myTextAnalyzer as ta
import mylib.myStreamlitVisualizer as sv


@st.dialog("데이터 확인하기", width="large")
def show_data_dialog(df):
    num_rows = st.number_input(
        "확인할 데이터 수",
        min_value=1,
        max_value=len(df),
        value=10,
        step=1,
    )
    st.dataframe(df.head(num_rows), use_container_width=True)


# 사이드바 설정
datafile = st.sidebar.file_uploader("분석할 파일 선택", type=["csv"])
target_col = st.sidebar.text_input("데이터가 있는 컬럼명", value="review")
check_data = st.sidebar.button("데이터 파일 확인")

st.sidebar.header("설정")

with st.sidebar.form("my_form"):
    do_graph = st.checkbox("빈도수 그래프", value=True)
    num_word_graph = st.slider("단어 수", 10, 50, 20, 5, key="graph_slider")

    do_wordcloud = st.checkbox("워드클라우드", value=False)
    num_word_wc = st.slider("단어 수", 20, 500, 50, 10, key="wc_slider")

    submitted = st.form_submit_button("분석 시작")


# 데이터 확인 버튼 클릭 시 모달 창 열기
if check_data:
    if datafile is None:
        st.sidebar.error("먼저 CSV 파일을 업로드하세요.")
    else:
        df_preview = ta.load_corpus(datafile)
        show_data_dialog(df_preview)


# 메인 화면
st.title("단어 빈도수 시각화")
status = st.info("분석 방법을 설정하세요")

if submitted:
    if not do_graph and not do_wordcloud:
        status.error("분석 방법을 설정하세요.")
        st.stop()

    if datafile is None:
        status.error("분석할 CSV 파일을 업로드하세요.")
        st.stop()

    status.info("데이터를 분석 중입니다.")

    # 데이터 로딩
    corpus = ta.load_corpus(datafile)
    status.info("데이터를 로딩했습니다.")

    # 빈도수 산출
    if target_col not in corpus.columns:
        status.error(f"'{target_col}' 컬럼을 찾을 수 없습니다.")
        st.stop()

    counter = ta.get_freq_word(corpus, target_col)
    status.info(f"분석이 완료되었습니다 ({len(corpus):,}개의 리뷰, {sum(counter.values()):,}개의 단어)")

    # 사용자 설정에 따른 시각화
    if do_graph and do_wordcloud:
        col1, col2 = st.columns(2)
        with col1:
            sv.visualize_barchart(counter, num_word_graph)
        with col2:
            sv.visualize_wordcloud(counter, num_word_wc)
    elif do_graph:
        sv.visualize_barchart(counter, num_word_graph)
    elif do_wordcloud:
        sv.visualize_wordcloud(counter, num_word_wc)