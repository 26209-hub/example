import streamlit as st

# =========================================================
# 페이지 설정
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

# 가나다순
PRODUCTS = sorted(PRODUCT_POWER.keys())

# 전기요금 단가
ELECTRICITY_RATE = 150


# =========================================================
# 세션 상태 초기화
# =========================================================
if "page" not in st.session_state:
    st.session_state.page = 1

if "selected_product" not in st.session_state:
    st.session_state.selected_product = None

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
        color: black;
    }

    /* 기본 버튼 */
    div.stButton > button {
        background-color: #00A000;
        color: black;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        min-height: 50px;
    }

    div.stButton > button:hover {
        background-color: #008000;
        color: black;
    }

    /* 입력칸 */
    div[data-testid="stNumberInput"] input {
        background-color: #4DA6FF !important;
        color: black !important;
        border: 2px solid #1976D2 !important;
    }

    /* Selectbox */
    div[data-baseweb="select"] > div {
        background-color: #4DA6FF !important;
        color: black !important;
    }

    /* 첫 페이지 제목 */
    .main-title {
        text-align: center;
        color: black;
        font-size: 42px;
        font-weight: bold;
        margin-top: 40px;
        margin-bottom: 80px;
    }

    /* 제품 선택 제목 */
    .select-title {
        text-align: center;
        color: black;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    /* 2페이지 제품 이름 */
    .product-name {
        text-align: center;
        color: black;
        font-size: 35px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 60px;
    }

    /* 2페이지 라벨 */
    .input-title {
        color: black;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    /* 완료 버튼 */
    .complete-button div.stButton > button {
        background-color: red !important;
        color: white !important;
        border-radius: 50% !important;
        width: 110px !important;
        height: 110px !important;
        min-height: 110px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        padding: 0 !important;
    }

    /* 결과 페이지 */
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
        font-size: 64px;
        font-weight: bold;
        margin-top: 50px;
    }

    .result-detail {
        text-align: center;
        color: black;
        font-size: 22px;
        line-height: 2;
        margin-top: 40px;
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
        <div style="
            background-color: white;
            min-height: 85vh;
            padding: 20px;
        ">
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-title">전기 요금을 확인하세요!</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="select-title">당신이 사용할 전자제품은?</div>',
        unsafe_allow_html=True
    )

    # 전자제품 선택
    selected = st.selectbox(
        "전자제품",
        PRODUCTS,
        index=None,
        placeholder="전자제품을 선택하세요",
        label_visibility="collapsed"
    )

    # 제품을 선택하면 즉시 2페이지
    if selected is not None:

        st.session_state.selected_product = selected

        # 평균 소비전력으로 초기 설정
        st.session_state.power = PRODUCT_POWER[selected]

        # 사용시간 초기값
        st.session_state.usage_time = 0.01

        st.session_state.page = 2

        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# 2페이지
# =========================================================
def page_two():

    # 노란색 배경
    st.markdown(
        """
        <div style="
            background-color: #FFF200;
            min-height: 85vh;
            padding: 30px;
        ">
        """,
        unsafe_allow_html=True
    )

    product = st.session_state.selected_product

    if product is None:
        st.session_state.page = 1
        st.rerun()

    st.markdown(
        f'<div class="product-name">{product}</div>',
        unsafe_allow_html=True
    )

    # 3개의 영역
    col1, col2, col3 = st.columns([1.4, 1.4, 1])

    # -----------------------------------------------------
    # 소비전력
    # -----------------------------------------------------
    with col1:

        st.markdown(
            '<div class="input-title">소비전력 입력하기(kW)</div>',
            unsafe_allow_html=True
        )

        power = st.number_input(
            "소비전력",
            min_value=0.0,
            max_value=100.0,
            value=float(st.session_state.power),
            step=0.001,
            format="%.3f",
            key="power_box",
            label_visibility="collapsed"
        )

        st.session_state.power = power

        # 몰라요
        if st.button("몰라요", key="unknown_button"):

            # 사용자가 기존에 입력한 값이 있더라도
            # 반드시 평균 소비전력으로 변경
            st.session_state.power = PRODUCT_POWER[product]

            st.rerun()

    # -----------------------------------------------------
    # 사용시간
    # -----------------------------------------------------
    with col2:

        st.markdown(
            '<div class="input-title">예상 사용시간 입력하기(h)</div>',
            unsafe_allow_html=True
        )

        usage_time = st.number_input(
            "예상 사용시간",
            min_value=0.01,
            max_value=24.00,
            value=float(st.session_state.usage_time),
            step=0.01,
            format="%.2f",
            key="time_box",
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

        if st.button("완료", key="complete_button"):

            # 소비전력 kW
            power_kw = float(st.session_state.power)

            # 사용시간 h
            hours = float(st.session_state.usage_time)

            # 전력 사용량(kWh)
            energy = power_kw * hours

            # 예상 전기요금
            cost = energy * ELECTRICITY_RATE

            st.session_state.energy_usage = energy
            st.session_state.estimated_cost = cost

            # 3페이지 이동
            st.session_state.page = 3

            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # 잘못 선택했나요?
    # -----------------------------------------------------
    st.markdown(
        '<div style="height:180px;"></div>',
        unsafe_allow_html=True
    )

    left, right = st.columns([5, 1])

    with right:

        if st.button("잘못 선택했나요?", key="wrong_button"):

            st.session_state.page = 1
            st.session_state.selected_product = None
            st.session_state.power = 0.0
            st.session_state.usage_time = 0.01

            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# 3페이지
# =========================================================
def page_three():

    # 흰색 배경
    st.markdown(
        """
        <div style="
            background-color: white;
            min-height: 85vh;
            padding: 30px;
        ">
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
        <div class="result-detail">
            전력 사용량: {energy:.2f} kWh<br>
            전기요금 단가: {ELECTRICITY_RATE}원/kWh
        </div>
        """,
        unsafe_allow_html=True
    )

    # 우측 하단
    st.markdown(
        '<div style="height:180px;"></div>',
        unsafe_allow_html=True
    )

    left, right = st.columns([5, 1])

    with right:

        if st.button("이전으로 돌아가기", key="back_button"):

            st.session_state.page = 1
            st.session_state.selected_product = None
            st.session_state.power = 0.0
            st.session_state.usage_time = 0.01
            st.session_state.energy_usage = 0.0
            st.session_state.estimated_cost = 0.0

            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# 페이지 표시
# =========================================================
if st.session_state.page == 1:
    page_one()

elif st.session_state.page == 2:
    page_two()

elif st.session_state.page == 3:
    page_three()
