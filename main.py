import streamlit as st

# =========================================================
# 기본 설정
# =========================================================
st.set_page_config(
    page_title="전기요금 지킴이",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
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
    "컴퓨터": 0.200,
    "헤어드라이어": 1.500,
    "TV": 0.100,
}

# 사용자가 제공한 제품만 사용
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

# 가나다순 정렬
PRODUCTS = sorted(PRODUCT_POWER.keys())

# 전기요금 단가
ELECTRICITY_RATE = 150


# =========================================================
# 세션 상태
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

    /* 전체 여백 */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    /* 페이지별 배경 */
    .page-white {
        background-color: white;
        min-height: 80vh;
        color: black;
        padding: 30px;
        border-radius: 10px;
    }

    .page-yellow {
        background-color: #FFF200;
        min-height: 80vh;
        color: black;
        padding: 30px;
        border-radius: 10px;
    }

    /* 제목 */
    .main-title {
        text-align: center;
        color: black;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 80px;
    }

    /* 선택된 제품 */
    .selected-product {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        color: black;
        margin-top: 25px;
    }

    /* 일반 버튼 */
    div.stButton > button {
        background-color: #00A000;
        color: black;
        border: none;
        border-radius: 5px;
        font-size: 18px;
        font-weight: bold;
        min-height: 50px;
    }

    div.stButton > button:hover {
        background-color: #008000;
        color: black;
    }

    /* 입력칸 */
    div[data-baseweb="input"] {
        background-color: #4DA6FF;
        border-radius: 5px;
    }

    div[data-baseweb="input"] input {
        color: black !important;
        background-color: #4DA6FF !important;
        font-size: 18px;
    }

    /* 숫자 입력 위젯 */
    div[data-testid="stNumberInput"] input {
        background-color: #4DA6FF !important;
        color: black !important;
    }

    /* 선택 상자 */
    div[data-baseweb="select"] > div {
        background-color: #4DA6FF;
        color: black;
    }

    /* 완료 버튼 */
    .complete-button div.stButton > button {
        background-color: red !important;
        color: white !important;
        border-radius: 50% !important;
        width: 120px !important;
        height: 120px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        padding: 0 !important;
    }

    /* 결과 */
    .result-title {
        text-align: center;
        color: black;
        font-size: 38px;
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
        margin-top: 30px;
    }

    /* 우측 하단 버튼 */
    .bottom-right {
        margin-top: 150px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 페이지 1
# =========================================================
def page_one():

    st.markdown(
        '<div class="page-white">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-title">전기 요금을 확인하세요!</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            text-align:center;
            color:black;
            font-size:25px;
            font-weight:bold;
            margin-bottom:20px;
        ">
            당신이 사용할 전자제품은?
        </div>
        """,
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

    if selected:
        st.session_state.selected_product = selected

        st.markdown(
            f'<div class="selected-product">{selected}</div>',
            unsafe_allow_html=True
        )

        # 선택 즉시 2페이지로 이동
        st.session_state.power = PRODUCT_POWER[selected]
        st.session_state.usage_time = 0.01
        st.session_state.page = 2
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# 페이지 2
# =========================================================
def page_two():

    st.markdown(
        '<div class="page-yellow">',
        unsafe_allow_html=True
    )

    product = st.session_state.selected_product

    if product is None:
        st.session_state.page = 1
        st.rerun()

    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:32px;
            font-weight:bold;
            color:black;
            margin-bottom:60px;
        ">
            {product}
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1.2, 1.2, 0.8])

    # -----------------------------------------------------
    # 소비전력
    # -----------------------------------------------------
    with col1:

        st.markdown(
            """
            <div style="
                color:black;
                font-size:20px;
                font-weight:bold;
                margin-bottom:10px;
            ">
                소비전력 입력하기(kW)
            </div>
            """,
            unsafe_allow_html=True
        )

        power = st.number_input(
            "소비전력",
            min_value=0.0,
            max_value=100.0,
            value=float(st.session_state.power),
            step=0.001,
            format="%.3f",
            key="power_input",
            label_visibility="collapsed"
        )

        st.session_state.power = power

        if st.button("몰라요", key="unknown_power"):
            # 사용자가 기존에 입력했던 값과 관계없이
            # 해당 제품의 평균 소비전력으로 강제 변경
            st.session_state.power = PRODUCT_POWER[product]
            st.rerun()

    # -----------------------------------------------------
    # 사용 시간
    # -----------------------------------------------------
    with col2:

        st.markdown(
            """
            <div style="
                color:black;
                font-size:20px;
                font-weight:bold;
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
    # 완료 버튼
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

            # 전력 사용량(kWh)
            energy = power_kw * hours

            # 예상 전기요금(원)
            cost = energy * ELECTRICITY_RATE

            st.session_state.energy_usage = energy
            st.session_state.estimated_cost = cost

            st.session_state.page = 3
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # 잘못 선택했나요?
    # -----------------------------------------------------
    st.markdown('<div class="bottom-right">', unsafe_allow_html=True)

    col_left, col_right = st.columns([5, 1])

    with col_right:
        if st.button("잘못 선택했나요?", key="wrong_product"):
            st.session_state.page = 1
            st.session_state.selected_product = None
            st.session_state.power = 0.0
            st.session_state.usage_time = 0.01
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# 페이지 3
# =========================================================
def page_three():

    st.markdown(
        '<div class="page-white">',
        unsafe_allow_html=True
    )

    cost = st.session_state.estimated_cost
    energy = st.session_state.energy_usage

    st.markdown(
        '<div class="result-title">예상 전기요금</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="result-price">
            {cost:,.0f}원
        </div>
        """,
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

    # 우측 하단 이전으로 돌아가기
    st.markdown('<div class="bottom-right">', unsafe_allow_html=True)

    col_left, col_right = st.columns([5, 1])

    with col_right:
        if st.button("이전으로 돌아가기", key="back_to_first"):
            st.session_state.page = 1
            st.session_state.selected_product = None
            st.session_state.power = 0.0
            st.session_state.usage_time = 0.01
            st.session_state.energy_usage = 0.0
            st.session_state.estimated_cost = 0.0
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# 페이지 실행
# =========================================================
if st.session_state.page == 1:
    page_one()

elif st.session_state.page == 2:
    page_two()

elif st.session_state.page == 3:
    page_three()

실행 방법
위 코드를 app.py라는 이름으로 저장합니다.
터미널에서 해당 파일이 있는 폴더로 이동합니다.
다음 명령을 실행합니다.
pip install streamlit
streamlit run app.py


별도의 로그인이나 데이터베이스는 필요하지 않습니다.

참고로 Streamlit의 기본 selectbox는 웹앱에서 마우스를 가까이 가져갔을 때 목록이 뜨는 방식이 아니라 클릭하면 목록이 열리는 방식입니다. 따라서 요청하신 1페이지의 전자제품 선택 기능은 Streamlit에 맞게 selectbox로 구현했습니다.
