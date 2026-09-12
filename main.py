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

# 가나다순
PRODUCTS = sorted(PRODUCT_POWER.keys())

# 전기요금 단가
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
# 4. 공통 CSS
# ============================================================

st.markdown(
    """
    <style>

    /* 전체 앱 */
    .stApp {
        color: black;
    }

    /* 1페이지 제목 */
    .main-title {
        text-align: center;
        color: black;
        font-size: 42px;
        font-weight: bold;
        margin-top: 50px;
        margin-bottom: 80px;
    }

    /* 질문 */
    .question-title {
        text-align: center;
        color: black;
        font-size: 30px;
        font-weight: bold;
        margin-bottom: 25px;
    }

    /* 선택 제품명 */
    .product-title {
        text-align: center;
        color: black;
        font-size: 38px;
        font-weight: bold;
        margin-top: 30px;
        margin-bottom: 60px;
    }

    /* 입력 제목 */
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

    /* 결과 제목 */
    .result-title {
        text-align: center;
        color: black;
        font-size: 40px;
        font-weight: bold;
        margin-top: 100px;
    }

    /* 결과 금액 */
    .result-price {
        text-align: center;
        color: black;
        font-size: 65px;
        font-weight: bold;
        margin-top: 50px;
    }

    /* 결과 상세 */
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
# 5. 페이지 1
# ============================================================

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

    # 제목
    st.markdown(
        '<div class="main-title">전기 요금을 확인하세요!</div>',
        unsafe_allow_html=True
    )

    # 질문
    st.markdown(
        '<div class="question-title">당신이 사용할 전자제품은?</div>',
        unsafe_allow_html=True
    )

    # 제품 선택
    selected_product = st.selectbox(
        "전자제품",
        PRODUCTS,
        index=None,
        placeholder="전자제품을 선택하세요",
        label_visibility="collapsed",
        key="product_selector"
    )

    # 제품을 선택한 경우
    if selected_product is not None:

        # 선택한 제품 저장
        st.session_state.selected_product = selected_product

        # 제품 선택 시 소비전력은 0으로 시작
        st.session_state.power_input = 0.0

        # 사용시간도 초기화
        st.session_state.usage_time_input = 0.01

        # 2페이지로 이동
        st.session_state.page = 2

        st.rerun()


# ============================================================
# 6. 평균 소비전력 적용 함수
# ============================================================

def set_average_power():

    product = st.session_state.selected_product

    if product is not None:

        # 제품별 정확한 평균값을 가져옴
        average_power = PRODUCT_POWER[product]

        # 소비전력 입력칸에 평균값 적용
        st.session_state.power_input = average_power


# ============================================================
# 7. 페이지 2
# ============================================================

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

    # 선택된 제품
    product = st.session_state.selected_product

    # 제품이 없는 경우 1페이지로
    if product is None:

        st.session_state.page = 1
        st.rerun()

    # 제품 이름 표시
    st.markdown(
        f'<div class="product-title">{product}</div>',
        unsafe_allow_html=True
    )

    # 화면 3분할
    col1, col2, col3 = st.columns([1.4, 1.4, 1.0])


    # ========================================================
    # 소비전력
    # ========================================================

    with col1:

        st.markdown(
            '<div class="input-title">소비전력 입력하기(kW)</div>',
            unsafe_allow_html=True
        )

        # 중요:
        # min_value / max_value를 지정하지 않음
        # 따라서 소비전력 입력에는 최대/최소 제한이 없음
        st.number_input(
            "소비전력",
            value=st.session_state.power_input,
            step=0.001,
            format="%.3f",
            key="power_input",
            label_visibility="collapsed"
        )

        # 평균값으로 하기
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

        # 사용시간은 0.01 ~ 24.00
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

            # 현재 소비전력
            power_kw = float(st.session_state.power_input)

            # 현재 사용시간
            usage_hours = float(st.session_state.usage_time_input)

            # -----------------------------------------------
            # 전력 사용량
            # 소비전력(kW) × 사용시간(h)
            # -----------------------------------------------

            energy = power_kw * usage_hours

            # -----------------------------------------------
            # 예상 전기요금
            # 전력 사용량(kWh) × 150원
            # -----------------------------------------------

            cost = energy * ELECTRICITY_RATE

            # 결과 저장
            st.session_state.energy_usage = energy
            st.session_state.estimated_cost = cost

            # 3페이지 이동
            st.session_state.page = 3

            st.rerun()

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


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

            # 1페이지로 이동
            st.session_state.page = 1

            # 선택 정보 초기화
            st.session_state.selected_product = None

            # 소비전력 초기화
            st.session_state.power_input = 0.0

            # 사용시간 초기화
            st.session_state.usage_time_input = 0.01

            st.rerun()


# ============================================================
# 8. 페이지 3
# ============================================================

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

    # 계산 결과 가져오기
    energy = st.session_state.energy_usage
    cost = st.session_state.estimated_cost

    # 제목
    st.markdown(
        '<div class="result-title">예상 전기요금</div>',
        unsafe_allow_html=True
    )

    # 금액
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

    # 하단 공간
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

            st.rerun()


# ============================================================
# 9. 현재 페이지 실행
# ============================================================

if st.session_state.page == 1:

    page_one()

elif st.session_state.page == 2:

    page_two()

elif st.session_state.page == 3:

    page_three()
