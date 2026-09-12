import streamlit as st


# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(
    page_title="전기요금 지킴이",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# 제품별 평균 소비전력
# 단위: kW
# =========================================================

PRODUCTS = {
    "공기청정기": 0.04,
    "냉장고": 0.10,
    "김치냉장고": 0.10,
    "노트북": 0.065,
    "데스크톱 컴퓨터": 0.20,
    "세탁기": 0.50,
    "선풍기": 0.045,
    "식기세척기": 1.50,
    "에어컨": 1.00,
    "에어프라이어": 1.50,
    "의류건조기": 2.00,
    "인덕션": 2.00,
    "전기다리미": 1.50,
    "전기밥솥": 0.80,
    "전기장판": 0.10,
    "전자레인지": 1.20,
    "전기포트": 1.50,
    "제습기": 0.35,
    "청소기": 1.00,
    "TV": 0.10,
    "헤어드라이어": 1.50,
}

ELECTRICITY_RATE = 150  # 원/kWh


# =========================================================
# Session State 초기화
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = 1

if "selected_product" not in st.session_state:
    st.session_state.selected_product = None

if "power" not in st.session_state:
    st.session_state.power = None

if "usage_time" not in st.session_state:
    st.session_state.usage_time = 1.00

if "energy_used" not in st.session_state:
    st.session_state.energy_used = None

if "estimated_cost" not in st.session_state:
    st.session_state.estimated_cost = None

if "show_products" not in st.session_state:
    st.session_state.show_products = False


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    /* 전체 앱 기본 */
    .stApp {
        font-family: Arial, sans-serif;
    }

    /* 기본적으로 Streamlit 메뉴/푸터 숨기기 */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* 제목 */
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: #000000;
        margin-top: 40px;
        margin-bottom: 70px;
    }

    /* 선택된 제품 표시 */
    .selected-product {
        text-align: center;
        font-size: 34px;
        font-weight: 800;
        color: #000000;
        margin-top: 30px;
        margin-bottom: 40px;
    }

    /* 결과 */
    .result-title {
        text-align: center;
        font-size: 38px;
        font-weight: 800;
        color: #000000;
        margin-top: 100px;
    }

    .result-cost {
        text-align: center;
        font-size: 64px;
        font-weight: 900;
        color: #000000;
        margin-top: 30px;
    }

    /* 입력창 파란색 */
    div[data-baseweb="input"] > div {
        background-color: #cfe8ff !important;
        border: 2px solid #2589d8 !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #cfe8ff !important;
        border: 2px solid #2589d8 !important;
    }

    /* 숫자 입력 글자 */
    input {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    /* 초록색 버튼 */
    .stButton > button {
        background-color: #19a83a !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 700 !important;
        min-height: 50px;
    }

    .stButton > button:hover {
        background-color: #12852c !important;
        color: white !important;
    }

    /* 큰 제품 선택 버튼 */
    .big-select-button > div > button {
        font-size: 25px !important;
        min-height: 100px !important;
        border-radius: 12px !important;
    }

    /* 완료 버튼 */
    .complete-button > div > button {
        background-color: #e60000 !important;
        border-radius: 50% !important;
        width: 130px !important;
        height: 130px !important;
        font-size: 22px !important;
        font-weight: 800 !important;
        margin: auto !important;
    }

    .complete-button > div > button:hover {
        background-color: #b80000 !important;
    }

    /* 잘못 선택했나요 / 이전으로 */
    .bottom-right {
        margin-top: 120px;
    }

    /* 페이지 2 입력 제목 */
    .input-title {
        color: #000000;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 페이지 1
# =========================================================

def page_one():

    # 흰색 배경
    st.markdown(
        """
        <style>
        .stApp {
            background-color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="main-title">전기 요금을 확인하세요!</div>',
        unsafe_allow_html=True,
    )

    # 선택된 제품이 아직 없을 때
    if st.session_state.selected_product is None:

        st.markdown(
            '<div class="big-select-button">',
            unsafe_allow_html=True,
        )

        if st.button(
            "당신이 사용할 전자제품은?",
            use_container_width=True,
            key="open_product_button",
        ):
            st.session_state.show_products = True
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        # 제품 목록
        if st.session_state.show_products:

            st.markdown(
                "<br><h3 style='text-align:center;'>전자제품을 선택하세요</h3>",
                unsafe_allow_html=True,
            )

            # 가나다순
            product_list = sorted(PRODUCTS.keys())

            # 3열로 제품 표시
            cols = st.columns(3)

            for index, product in enumerate(product_list):

                with cols[index % 3]:

                    if st.button(
                        product,
                        key=f"product_{index}",
                        use_container_width=True,
                    ):
                        st.session_state.selected_product = product
                        st.session_state.power = PRODUCTS[product]
                        st.session_state.show_products = False
                        st.session_state.page = 2
                        st.rerun()


# =========================================================
# 페이지 2
# =========================================================

def page_two():

    # 노란색 배경
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #fff200;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    product = st.session_state.selected_product

    st.markdown(
        f'<div class="selected-product">{product}</div>',
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # 입력 영역
    # -----------------------------------------------------

    left, middle, right = st.columns([1.3, 1.3, 0.8])

    # -----------------------------------------------------
    # 왼쪽: 소비전력
    # -----------------------------------------------------

    with left:

        st.markdown(
            '<div class="input-title">소비전력 입력하기 (kW)</div>',
            unsafe_allow_html=True,
        )

        power = st.number_input(
            "소비전력",
            min_value=0.001,
            max_value=100.0,
            value=float(st.session_state.power),
            step=0.001,
            format="%.3f",
            label_visibility="collapsed",
            key="power_input",
        )

        st.session_state.power = power

        if st.button(
            "몰라요",
            use_container_width=True,
            key="dont_know_power",
        ):
            # 선택된 제품의 평균 소비전력으로 설정
            st.session_state.power = PRODUCTS[product]
            st.rerun()

    # -----------------------------------------------------
    # 가운데: 사용시간
    # -----------------------------------------------------

    with middle:

        st.markdown(
            '<div class="input-title">예상 사용시간 입력하기 (h)</div>',
            unsafe_allow_html=True,
        )

        usage_time = st.number_input(
            "예상 사용시간",
            min_value=0.01,
            max_value=24.00,
            value=float(st.session_state.usage_time),
            step=0.01,
            format="%.2f",
            label_visibility="collapsed",
            key="usage_time_input",
        )

        st.session_state.usage_time = usage_time

    # -----------------------------------------------------
    # 오른쪽: 완료
    # -----------------------------------------------------

    with right:

        st.markdown(
            "<div style='height:30px;'></div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="complete-button">',
            unsafe_allow_html=True,
        )

        if st.button(
            "완료",
            key="complete",
        ):

            power_kw = float(st.session_state.power)
            hours = float(st.session_state.usage_time)

            # 전력 사용량 = 소비전력(kW) × 사용시간(h)
            energy_used = power_kw * hours

            # 예상 전기요금 = 전력 사용량(kWh) × 전기요금 단가
            estimated_cost = energy_used * ELECTRICITY_RATE

            st.session_state.energy_used = energy_used
            st.session_state.estimated_cost = estimated_cost

            st.session_state.page = 3

            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # 오른쪽 아래: 잘못 선택했나요?
    # -----------------------------------------------------

    st.markdown(
        "<div class='bottom-right'></div>",
        unsafe_allow_html=True,
    )

    bottom_left, bottom_middle, bottom_right = st.columns([5, 3, 2])

    with bottom_right:

        if st.button(
            "잘못 선택했나요?",
            key="wrong_product",
            use_container_width=True,
        ):
            st.session_state.page = 1
            st.session_state.selected_product = None
            st.session_state.power = None
            st.session_state.usage_time = 1.00
            st.session_state.energy_used = None
            st.session_state.estimated_cost = None
            st.session_state.show_products = False

            st.rerun()


# =========================================================
# 페이지 3
# =========================================================

def page_three():

    # 흰색 배경
    st.markdown(
        """
        <style>
        .stApp {
            background-color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    cost = st.session_state.estimated_cost

    st.markdown(
        '<div class="result-title">예상 전기 요금</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="result-cost">{cost:,.0f}원</div>',
        unsafe_allow_html=True,
    )

    # 하단 오른쪽 이전으로 버튼
    st.markdown(
        "<div style='margin-top:180px;'></div>",
        unsafe_allow_html=True,
    )

    left, right = st.columns([7, 1.5])

    with right:

        if st.button(
            "이전으로",
            key="go_back",
            use_container_width=True,
        ):
            st.session_state.page = 1
            st.session_state.selected_product = None
            st.session_state.power = None
            st.session_state.usage_time = 1.00
            st.session_state.energy_used = None
            st.session_state.estimated_cost = None
            st.session_state.show_products = False

            st.rerun()


# =========================================================
# 페이지 실행
# =========================================================

if st.session_state.page == 1:
    page_one()

elif st.session_state.page == 2:
    page_two()

elif st.session_state.page == 3:
    page_three()
