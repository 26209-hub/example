import streamlit as st

# =========================================================
# 기본 설정
# =========================================================
st.set_page_config(
    page_title="전기요금 지킴이",
    page_icon="⚡",
    layout="wide"
)

# =========================================================
# 전자제품 평균 소비전력
# 단위: kW
# =========================================================
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
    "TV": 0.100,
}

PRODUCTS = sorted(PRODUCT_POWER.keys())

ELECTRICITY_RATE = 150


# =========================================================
# 세션 상태
# =========================================================
if "page" not in st.session_state:
    st.session_state.page = 1

if "selected_product" not in st.session_state:
    st.session_state.selected_product = ""

if "power" not in st.session_state:
    st.session_state.power = 0.0

if "usage_time" not in st.session_state:
    st.session_state.usage_time = 0.01

if "energy_usage" not in st.session_state:
    st.session_state.energy_usage = 0.0

if "estimated_cost" not in st.session_state:
    st.session_state.estimated_cost = 0.0


# =========================================================
# CSS
# =========================================================
st.markdown(
    """
    <style>

    /* 전체 앱 */
    .stApp {
        color: #000000;
    }

    /* 제목 */
    .title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        color: #000000;
        padding-top: 40px;
        padding-bottom: 60px;
    }

    .question {
        text-align: center;
        font-size: 28px;
        font-weight: 700;
        color: #000000;
        padding-bottom: 20px;
    }

    /* 일반 버튼 */
    .stButton > button {
        background-color: #00A000 !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 5px !important;
        font-weight: 700 !important;
        min-height: 50px !important;
    }

    .stButton > button:hover {
        background-color: #008000 !important;
        color: #000000 !important;
    }

    /* 숫자 입력칸 */
    .stNumberInput input {
        background-color: #4DA6FF !important;
        color: #000000 !important;
        font-size: 18px !important;
    }

    /* Selectbox */
    div[data-baseweb="select"] > div {
        background-color: #4DA6FF !important;
        color: #000000 !important;
    }

    /* 완료 버튼 */
    .complete-button .stButton > button {
        background-color: #FF0000 !important;
        color: #FFFFFF !important;
        border-radius: 50% !important;
        width: 110px !important;
        height: 110px !important;
        min-height: 110px !important;
        font-size: 20px !important;
        padding: 0 !important;
    }

    /* 결과 금액 */
    .result-title {
        text-align: center;
        font-size: 40px;
        font-weight: 700;
        color: #000000;
        margin-top: 100px;
    }

    .result-price {
        text-align: center;
        font-size: 65px;
        font-weight: 700;
        color: #000000;
        margin-top: 40px;
    }

    .result-info {
        text-align: center;
        font-size: 22px;
        line-height: 2;
        color: #000000;
        margin-top: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 1페이지
# =========================================================
def page_one():

    # 흰색 배경
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
        '<div class="title">전기 요금을 확인하세요!</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="question">당신이 사용할 전자제품은?</div>',
        unsafe_allow_html=True
    )

    selected = st.selectbox(
        "전자제품 선택",
        PRODUCTS,
        index=None,
        placeholder="전자제품을 선택하세요",
        label_visibility="collapsed"
    )

    if selected:

        st.session_state.selected_product = selected
        st.session_state.power = PRODUCT_POWER[selected]
        st.session_state.usage_time = 0.01

        st.session_state.page = 2

        st.rerun()


# =========================================================
# 2페이지
# =========================================================
def page_two():

    # 노란색 배경
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

    if not product:
        st.session_state.page = 1
        st.rerun()

    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:36px;
            font-weight:700;
            color:black;
            margin-top:30px;
            margin-bottom:60px;
        ">
            {product}
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1.4, 1.4, 1])

    # -----------------------------------------------------
    # 소비전력
    # -----------------------------------------------------
    with col1:

        st.markdown(
            """
            <div style="
                color:black;
                font-size:20px;
                font-weight:700;
                margin-bottom:10px;
            ">
                소비전력 입력하기(kW)
            </div>
            """,
            unsafe_allow_html=True
        )

        power = st.number_input(
            "소비전력",
            min_value=0.000,
            max_value=100.000,
            value=float(st.session_state.power),
            step=0.001,
            format="%.3f",
            key="power_input",
            label_visibility="collapsed"
        )

        st.session_state.power = power

        if st.button("몰라요", key="dont_know"):

            # 기존에 입력한 값이 있어도
            # 선택한 제품의 평균 소비전력으로 덮어씀
            st.session_state.power = PRODUCT_POWER[product]

            # 위젯 값도 함께 변경
            st.session_state.power_input = PRODUCT_POWER[product]

            st.rerun()

    # -----------------------------------------------------
    # 사용시간
    # -----------------------------------------------------
    with col2:

        st.markdown(
            """
            <div style="
                color:black;
                font-size:20px;
                font-weight:700;
                margin-bottom:10px;
            ">
                예상 사용시간 입력하기(h)
            </div>
            """,
            unsafe_allow_html=True
        )

        usage_time = st.number_input(
            "사용시간",
            min_value=0.01,
            max_value=24.00,
            value=float(st.session_state.usage_time),
            step=0.01,
            format="%.2f",
            key="usage_time_input",
            label_visibility="collapsed"
        )

        st.session_state.usage_time = usage_time

    # -----------------------------------------------------
    # 완료
    # -----------------------------------------------------
    with col3:

        st.markdown(
            '<div style="height:35px;"></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="complete-button">',
            unsafe_allow_html=True
        )

        if st.button("완료", key="complete"):

            power_kw = float(st.session_state.power)
            hours = float(st.session_state.usage_time)

            # 전력 사용량
            energy = power_kw * hours

            # 예상 전기요금
            cost = energy * ELECTRICITY_RATE

            st.session_state.energy_usage = energy
            st.session_state.estimated_cost = cost

            st.session_state.page = 3

            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # 하단
    # -----------------------------------------------------
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    left, right = st.columns([5, 1])

    with right:

        if st.button("잘못 선택했나요?", key="wrong_product"):

            st.session_state.page = 1
            st.session_state.selected_product = ""
            st.session_state.power = 0.0
            st.session_state.usage_time = 0.01

            st.rerun()


# =========================================================
# 3페이지
# =========================================================
def page_three():

    # 흰색 배경
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

    cost = st.session_state.estimated_cost
    energy = st.session_state.energy_usage

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

    left, right = st.columns([5, 1])

    with right:

        if st.button("이전으로 돌아가기", key="go_first"):

            st.session_state.page = 1
            st.session_state.selected_product = ""
            st.session_state.power = 0.0
            st.session_state.usage_time = 0.01
            st.session_state.energy_usage = 0.0
            st.session_state.estimated_cost = 0.0

            st.rerun()


# =========================================================
# 현재 페이지 실행
# =========================================================
if st.session_state.page == 1:
    page_one()

elif st.session_state.page == 2:
    page_two()

elif st.session_state.page == 3:
    page_three()
