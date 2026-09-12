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
    "TV": 0.100
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

# 소비전력 기본값은 0
if "power_value" not in st.session_state:
    st.session_state.power_value = 0.0

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

    /* 제목 */
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        color: black;
        padding-top: 50px;
        margin-bottom: 70px;
    }

    /* 질문 */
    .question {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        color: black;
        margin-bottom: 25px;
    }

    /* 제품 이름 */
    .product-name {
        text-align: center;
        font-size: 38px;
        font-weight: bold;
        color: black;
        margin-top: 30px;
        margin-bottom: 70px;
    }

    /* 입력칸 제목 */
    .input-label {
        color: black;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    /* 일반 버튼 */
    .stButton > button {
        background-color: #00A000 !important;
        color: black !important;
        border: none !important;
        border-radius: 5px !important;
        font-weight: bold !important;
        min-height: 50px !important;
    }

    .stButton > button:hover {
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
    .complete-area .stButton > button {
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

    /* 결과 제목 */
    .result-title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: black;
        margin-top: 100px;
    }

    /* 결과 금액 */
    .result-price {
        text-align: center;
        font-size: 65px;
        font-weight: bold;
        color: black;
        margin-top: 50px;
    }

    /* 결과 상세 */
    .result-info {
        text-align: center;
        font-size: 22px;
        line-height: 2;
        color: black;
        margin-top: 35px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 1페이지
# =========================================================

def show_page_one():

    # 흰색 배경
    st.markdown(
        """
        <style>
        .stApp {
            background-color: white !important;
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
        '<div class="question">당신이 사용할 전자제품은?</div>',
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

    # 제품 선택
    if selected is not None:

        # 선택한 제품 저장
        st.session_state.selected_product = selected

        # 중요:
        # 제품을 선택해도 소비전력은 0으로 시작
        # 평균값은 '몰라요'를 눌렀을 때만 사용
        st.session_state.power_value = 0.0

        # 사용시간 초기값
        st.session_state.usage_time = 0.01

        # 2페이지 이동
        st.session_state.page = 2

        st.rerun()


# =========================================================
# 몰라요 버튼
# =========================================================

def use_average_power():

    product = st.session_state.selected_product

    if product is not None:

        # 선택한 제품의 평균 소비전력으로 변경
        st.session_state.power_value = PRODUCT_POWER[product]


# =========================================================
# 2페이지
# =========================================================

def show_page_two():

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

    # 제품이 없으면 1페이지
    if product is None:

        st.session_state.page = 1
        st.rerun()

    # 제품 이름
    st.markdown(
        f'<div class="product-name">{product}</div>',
        unsafe_allow_html=True
    )

    # 화면을 3개 영역으로 나눔
    col1, col2, col3 = st.columns([1.4, 1.4, 1])


    # =====================================================
    # 소비전력 입력
    # =====================================================

    with col1:

        st.markdown(
            '<div class="input-label">소비전력 입력하기(kW)</div>',
            unsafe_allow_html=True
        )

        power = st.number_input(
            "소비전력",
            min_value=0.0,
            max_value=100.0,

            # 기본값 0
            value=float(st.session_state.power_value),

            # 0.001 kW 단위
            step=0.001,

            format="%.3f",

            key="power_input_box",

            label_visibility="collapsed"
        )

        # 사용자가 직접 입력한 값을 저장
        st.session_state.power_value = power

        # 몰라요 버튼
        st.button(
            "몰라요",
            key="average_power_button",
            on_click=use_average_power
        )


    # =====================================================
    # 사용시간 입력
    # =====================================================

    with col2:

        st.markdown(
            '<div class="input-label">예상 사용시간 입력하기(h)</div>',
            unsafe_allow_html=True
        )

        usage_time = st.number_input(
            "사용시간",

            # 최소 0.01
            min_value=0.01,

            # 최대 24.00
            max_value=24.00,

            # 0.01 단위
            step=0.01,

            value=float(st.session_state.usage_time),

            format="%.2f",

            key="usage_time_box",

            label_visibility="collapsed"
        )

        st.session_state.usage_time = usage_time


    # =====================================================
    # 완료 버튼
    # =====================================================

    with col3:

        st.markdown(
            '<div style="height:35px;"></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="complete-area">',
            unsafe_allow_html=True
        )

        if st.button(
            "완료",
            key="complete_button"
        ):

            # 소비전력
            power_kw = float(st.session_state.power_value)

            # 사용시간
            hours = float(st.session_state.usage_time)

            # ---------------------------------------------
            # 전력 사용량 계산
            # kWh = kW × h
            # ---------------------------------------------

            energy = power_kw * hours

            # ---------------------------------------------
            # 전기요금 계산
            # 원 = kWh × 150원
            # ---------------------------------------------

            cost = energy * ELECTRICITY_RATE

            # 계산 결과 저장
            st.session_state.energy_usage = energy
            st.session_state.estimated_cost = cost

            # 3페이지로 이동
            st.session_state.page = 3

            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


    # =====================================================
    # 잘못 선택했나요?
    # =====================================================

    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    left, right = st.columns([5, 1])

    with right:

        if st.button(
            "잘못 선택했나요?",
            key="wrong_product_button"
        ):

            # 1페이지로 이동
            st.session_state.page = 1

            # 데이터 초기화
            st.session_state.selected_product = None
            st.session_state.power_value = 0.0
            st.session_state.usage_time = 0.01

            st.rerun()


# =========================================================
# 3페이지
# =========================================================

def show_page_three():

    # 흰색 배경
    st.markdown(
        """
        <style>
        .stApp {
            background-color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 계산 결과
    cost = st.session_state.estimated_cost
    energy = st.session_state.energy_usage

    # 제목
    st.markdown(
        '<div class="result-title">예상 전기요금</div>',
        unsafe_allow_html=True
    )

    # 전기요금
    st.markdown(
        f'<div class="result-price">{cost:,.0f}원</div>',
        unsafe_allow_html=True
    )

    # 상세 정보
    st.markdown(
        f"""
        <div class="result-info">
            전력 사용량: {energy:.2f} kWh<br>
            전기요금 단가: {ELECTRICITY_RATE}원/kWh
        </div>
        """,
        unsafe_allow_html=True
    )

    # 화면 아래쪽
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    left, right = st.columns([5, 1])

    with right:

        if st.button(
            "이전으로 돌아가기",
            key="back_to_first_button"
        ):

            # 1페이지로 이동
            st.session_state.page = 1

            # 모든 값 초기화
            st.session_state.selected_product = None
            st.session_state.power_value = 0.0
            st.session_state.usage_time = 0.01
            st.session_state.energy_usage = 0.0
            st.session_state.estimated_cost = 0.0

            st.rerun()


# =========================================================
# 페이지 실행
# =========================================================

if st.session_state.page == 1:

    show_page_one()

elif st.session_state.page == 2:

    show_page_two()

elif st.session_state.page == 3:

    show_page_three()
