import streamlit as st

st.set_page_config(
    page_title="전기요금 지킴이",
    layout="wide"
)

# 전기요금 단가
ELECTRICITY_RATE = 150

# 전자제품별 기본 소비전력(W)
POWER_DATA = {
    "공기청정기": 50,
    "노트북": 60,
    "데스크톱 컴퓨터": 300,
    "냉장고": 150,
    "김치냉장고": 100,
    "세탁기": 500,
    "선풍기": 50,
    "식기세척기": 1500,
    "에어컨": 1000,
    "에어프라이어": 1500,
    "의류건조기": 2500,
    "인덕션": 1500,
    "전기다리미": 1000,
    "전기밥솥": 700,
    "전기장판": 100,
    "전기포트": 1500,
    "전자레인지": 1000,
    "제습기": 400,
    "청소기": 1000,
    "TV": 120,
    "헤어드라이어": 1500,
    "전기히터": 1500
}

PRODUCTS = sorted(POWER_DATA.keys())

# 세션 상태
if "page" not in st.session_state:
    st.session_state.page = 1

if "selected_product" not in st.session_state:
    st.session_state.selected_product = None

if "default_power_kw" not in st.session_state:
    st.session_state.default_power_kw = None

if "estimated_cost" not in st.session_state:
    st.session_state.estimated_cost = None


# CSS
st.markdown(
    """
    <style>
    .stApp {
        font-family: Arial, sans-serif;
    }

    div.stButton > button {
        background-color: #28A745;
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        min-height: 45px;
    }

    div.stButton > button:hover {
        background-color: #218838;
        color: white;
    }

    div[data-testid="stNumberInput"] input {
        background-color: #D9ECFF;
        border: 2px solid #4DA3FF;
        color: black;
    }

    div[data-baseweb="select"] {
        background-color: #D9ECFF;
    }

    .page1-title {
        text-align: center;
        color: black;
        font-size: 42px;
        font-weight: bold;
        margin-top: 60px;
        margin-bottom: 70px;
    }

    .selected-product {
        text-align: center;
        color: black;
        font-size: 30px;
        font-weight: bold;
        margin-bottom: 40px;
    }

    .result-title {
        text-align: center;
        color: black;
        font-size: 35px;
        font-weight: bold;
        margin-top: 150px;
    }

    .result-cost {
        text-align: center;
        color: black;
        font-size: 60px;
        font-weight: bold;
        margin-top: 40px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# 1번 페이지
def page_one():

    st.markdown(
        '<div class="page1-title">전기 요금을 확인하세요!</div>',
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1, 2, 1])

    with center:

        selected = st.selectbox(
            "당신이 사용할 전자제품은?",
            ["당신이 사용할 전자제품은?"] + PRODUCTS,
            index=0,
            key="product_select"
        )

        if selected != "당신이 사용할 전자제품은?":

            st.session_state.selected_product = selected
            st.session_state.default_power_kw = None
            st.session_state.estimated_cost = None
            st.session_state.page = 2

            st.rerun()


# 2번 페이지
def page_two():

    st.markdown(
        """
        <style>
        .stApp {
            background-color: #FFF200;
        }

        [data-testid="stHeader"] {
            background-color: #FFF200;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="selected-product">'
        f'{st.session_state.selected_product}'
        f'</div>',
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1, 1, 1])

    with left:

        st.subheader("소비전력 입력하기(kW)")

        power = st.number_input(
            "소비전력 입력하기(kW)",
            min_value=0.0,
            step=0.01,
            format="%.2f",
            value=0.0,
            label_visibility="collapsed",
            key="power_input"
        )

        if st.button("몰라요", key="unknown_power"):

            default_power_w = POWER_DATA[
                st.session_state.selected_product
            ]

            st.session_state.default_power_kw = (
                default_power_w / 1000
            )

    with center:

        st.subheader("예상 사용시간 입력하기(h)")

        usage_time = st.number_input(
            "예상 사용시간 입력하기(h)",
            min_value=0.0,
            max_value=24.0,
            step=0.01,
            format="%.2f",
            value=0.0,
            label_visibility="collapsed",
            key="usage_time_input"
        )

    with right:

        st.write("")
        st.write("")
        st.write("")

        if st.button("완료", key="complete_button"):

            has_power = (
                power > 0
                or st.session_state.default_power_kw is not None
            )

            has_valid_time = (
                usage_time >= 0.01
                and usage_time <= 24.00
            )

            if has_power and has_valid_time:

                if st.session_state.default_power_kw is not None:
                    final_power_kw = (
                        st.session_state.default_power_kw
                    )
                else:
                    final_power_kw = power

                electricity_usage = (
                    final_power_kw * usage_time
                )

                estimated_cost = (
                    electricity_usage * ELECTRICITY_RATE
                )

                st.session_state.estimated_cost = estimated_cost
                st.session_state.page = 3

                st.rerun()

    st.write("")
    st.write("")
    st.write("")
    st.write("")

    empty1, empty2, empty3, bottom = st.columns(
        [1, 1, 1, 1]
    )

    with bottom:

        if st.button(
            "잘못 선택했나요?",
            key="wrong_product"
        ):

            st.session_state.page = 1
            st.session_state.selected_product = None
            st.session_state.default_power_kw = None
            st.session_state.estimated_cost = None

            st.rerun()


# 3번 페이지
def page_three():

    st.markdown(
        """
        <style>
        .stApp {
            background-color: white;
        }

        [data-testid="stHeader"] {
            background-color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="result-title">예상 전기요금</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="result-cost">'
        f'{st.session_state.estimated_cost:,.0f}원'
        f'</div>',
        unsafe_allow_html=True
    )


# 페이지 실행
if st.session_state.page == 1:
    page_one()

elif st.session_state.page == 2:
    page_two()

elif st.session_state.page == 3:
    page_three()
