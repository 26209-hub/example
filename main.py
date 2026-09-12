import streamlit as st

# ============================================================
# 1. 페이지 기본 설정
# ============================================================

st.set_page_config(
    page_title="전기요금 지킴이",
    page_icon="⚡",
    layout="wide"
)


# ============================================================
# 2. 제품별 평균 소비전력
# 단위: kW
# ============================================================

PRODUCT_POWER = {
    "공기청정기": 0.040,
    "노트북": 0.065,
    "데스크톱 컴퓨터": 0.200,
    "냉장고": 0.100,
    "김치냉장고": 0.100,
    "선풍기": 0.045,
    "세탁기": 0.500,
    "식기세척기": 1.500,
    "에어컨": 1.000,
    "에어프라이어": 1.500,
    "의류건조기": 2.000,
    "인덕션": 2.000,
    "전기다리미": 1.500,
    "전기밥솥": 0.800,
    "전기장판": 0.100,
    "전기포트": 1.500,
    "전자레인지": 1.200,
    "제습기": 0.350,
    "청소기": 1.000,
    "헤어드라이어": 1.500,
    "TV": 0.100
}

PRODUCTS = sorted(PRODUCT_POWER.keys())

ELECTRICITY_RATE = 150


# ============================================================
# 3. 세션 상태 초기화
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = 1

if "selected_product" not in st.session_state:
    st.session_state.selected_product = None

if "power_input" not in st.session_state:
    st.session_state.power_input = 0.0

if "usage_time_input" not in st.session_state:
    st.session_state.usage_time_input = 0.01

if "energy_usage" not in st.session_state:
    st.session_state.energy_usage = 0.0

if "estimated_cost" not in st.session_state:
    st.session_state.estimated_cost = 0.0


# ============================================================
# 4. CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        color: black;
    }

    .main-title {
        text-align: center;
        color: black;
        font-size: 42px;
        font-weight: bold;
        margin-top: 50px;
        margin-bottom: 80px;
    }

    .question-title {
        text-align: center;
        color: black;
        font-size: 30px;
        font-weight: bold;
        margin-bottom: 25px;
    }

    .product-title {
        text-align: center;
        color: black;
        font-size: 38px;
        font-weight: bold;
        margin-top: 30px;
        margin-bottom: 60px;
    }

    .input-title {
        color: black;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    /* 일반 버튼 */
    div.stButton > button {
        background-color: #00A000 !important;
        color: black !important;
        border: none !important;
        border-radius: 5px !important;
        font-weight: bold !important;
        min-height: 50px !important;
    }

    div.stButton > button:hover {
        background-color: #008000 !important;
        color: black !important;
    }

    /* 숫자 입력칸 */
    div[data-testid="stNumberInput"] input {
        background-color: #4DA6FF !important;
        color: black !important;
        border: 2px solid #1976D2 !important;
    }

    /* 제품 선택칸 */
    div[data-baseweb="select"] > div {
        background-color: #4DA6FF !important;
        color: black !important;
    }

    /* 완료 버튼 */
    .complete-button div.stButton > button {
        background-color: red !important;
        color: white !important;
        border-radius: 50% !important;
        width: 115px !important;
        height: 115px !important;
        min-height: 115px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        padding: 0 !important;
    }

    .result-title {
        text-align: center;
        color: black;
        font-size: 40px;
        font-weight: bold;
        margin-top: 100px;
    }

    .result-price {
        text-align: center;
        color: black;
        font-size: 65px;
        font-weight: bold;
        margin-top: 50px;
    }

    .result-info {
        text-align: center;
        color: black;
        font-size: 22px;
        line-height: 2;
        margin-top: 35px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 5. 1페이지
# ============================================================

def page_one():

    st.markdown(
        """
        <style>
        .stApp {
            background-color: #FFFFFF !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-title">전기 요금을 확인하세요!</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="question-title">당신이 사용할 전자제품은?</div>',
        unsafe_allow_html=True
    )

    selected_product = st.selectbox(
        "전자제품",
        PRODUCTS,
        index=None,
        placeholder="전자제품을 선택하세요",
        label_visibility="collapsed",
        key="product_selector"
    )

    if selected_product is not None:

        st.session_state.selected_product = selected_product

        # 제품을 새로 선택하면 소비전력은 0부터 시작
        st.session_state.power_input = 0.0

        st.session_state.usage_time_input = 0.01

        # 2페이지로 이동
        st.session_state.page = 2

        st.rerun()


# ============================================================
# 6. 평균값으로 하기
# ============================================================

def set_average_power():

    product = st.session_state.selected_product

    if product is not None:
        st.session_state.power_input = PRODUCT_POWER[product]


# ============================================================
# 7. 2페이지
# ============================================================

def page_two():

    st.markdown(
        """
        <style>
        .stApp {
            background-color: #FFF200 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    product = st.session_state.selected_product

    if product is None:

        st.session_state.page = 1
        st.rerun()

    st.markdown(
        f'<div class="product-title">{product}</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1.4, 1.4, 1.0])


    # ========================================================
    # 소비전력
    # ========================================================

    with col1:

        st.markdown(
            '<div class="input-title">소비전력 입력하기(kW)</div>',
            unsafe_allow_html=True
        )

        st.number_input(
            "소비전력",
            value=st.session_state.power_input,
            step=0.001,
            format="%.3f",
            key="power_input",
            label_visibility="collapsed"
        )

        st.button(
            "평균값으로 하기",
            key="average_power_button",
            on_click=set_average_power
        )


    # ========================================================
    # 사용시간
    # ========================================================

    with col2:

        st.markdown(
            '<div class="input-title">예상 사용시간 입력하기(h)</div>',
            unsafe_allow_html=True
        )

        st.number_input(
            "예상 사용시간",
            min_value=0.01,
            max_value=24.00,
            value=st.session_state.usage_time_input,
            step=0.01,
            format="%.2f",
            key="usage_time_input",
            label_visibility="collapsed"
        )


    # ========================================================
    # 완료
    # ========================================================

    with col3:

        st.markdown(
            '<div style="height:35px;"></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="complete-button">',
            unsafe_allow_html=True
        )

        if st.button(
            "완료",
            key="complete_button"
        ):

            power_kw = float(st.session_state.power_input)
            usage_hours = float(st.session_state.usage_time_input)

            energy = power_kw * usage_hours

            cost = energy * ELECTRICITY_RATE

            st.session_state.energy_usage = energy
            st.session_state.estimated_cost = cost

            st.session_state.page = 3

            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


    # ========================================================
    # 잘못 선택했나요?
    # ========================================================

    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    left_space, right_button = st.columns([5, 1])

    with right_button:

        if st.button(
            "잘못 선택했나요?",
            key="wrong_product_button"
        ):

            # =================================================
            # 1페이지로 돌아가기 위한 초기화
            # =================================================

            # 페이지 번호를 1로 변경
            st.session_state.page = 1

            # 선택한 제품 삭제
            st.session_state.selected_product = None

            # 소비전력 초기화
            st.session_state.power_input = 0.0

            # 사용시간 초기화
            st.session_state.usage_time_input = 0.01

            # 계산 결과 초기화
            st.session_state.energy_usage = 0.0
            st.session_state.estimated_cost = 0.0

            # -------------------------------------------------
            # 중요:
            # 제품 선택 위젯 자체의 값도 초기화
            # -------------------------------------------------
            if "product_selector" in st.session_state:
                del st.session_state["product_selector"]

            # 즉시 다시 실행하여 1페이지 표시
            st.rerun()


# ============================================================
# 8. 3페이지
# ============================================================

def page_three():

    st.markdown(
        """
        <style>
        .stApp {
            background-color: #FFFFFF !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    energy = st.session_state.energy_usage
    cost = st.session_state.estimated_cost

    st.markdown(
        '<div class="result-title">예상 전기요금</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="result-price">{cost:,.0f}원</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="result-info">
            전력 사용량: {energy:.2f} kWh<br>
            전기요금 단가: {ELECTRICITY_RATE}원/kWh
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    left_space, right_button = st.columns([5, 1])

    with right_button:

        if st.button(
            "이전으로 돌아가기",
            key="back_button"
        ):

            # 1페이지로 이동
            st.session_state.page = 1

            # 모든 값 초기화
            st.session_state.selected_product = None
            st.session_state.power_input = 0.0
            st.session_state.usage_time_input = 0.01
            st.session_state.energy_usage = 0.0
            st.session_state.estimated_cost = 0.0

            # 제품 선택 위젯도 초기화
            if "product_selector" in st.session_state:
                del st.session_state["product_selector"]

            st.rerun()


# ============================================================
# 9. 페이지 실행
# ============================================================

if st.session_state.page == 1:
    page_one()

elif st.session_state.page == 2:
    page_two()

elif st.session_state.page == 3:
    page_three()
