import streamlit as st

# ==========================================
# 기본 설정
# ==========================================

st.set_page_config(
    page_title="전기요금 지킴이",
    layout="wide"
)

# 전기요금 단가
ELECTRICITY_RATE = 150  # 원/kWh


# ==========================================
# 전자제품별 기본 소비전력
# 단위: W
# ==========================================

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


# ==========================================
# 전자제품 가나다순 정렬
# ==========================================

PRODUCTS = sorted(POWER_DATA.keys())


# ==========================================
# 세션 상태
# ==========================================

if "page" not in st.session_state:
    st.session_state.page = 1

if "selected_product" not in st.session_state:
    st.session_state.selected_product = None

if "selected_power" not in st.session_state:
    st.session_state.selected_power = None

if "estimated_cost" not in st.session_state:
    st.session_state.estimated_cost = None


# ==========================================
# CSS
# ==========================================

st.markdown(
    """
    <style>

    /* 전체 앱 */
    .stApp {
        font-family: Arial, sans-serif;
    }

    /* 모든 일반 버튼 - 초록색 */
    div.stButton > button {
        background-color: #28A745;
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: bold;
    }

    div.stButton > button:hover {
        background-color: #218838;
        color: white;
    }

    /* 숫자 입력 칸 - 파란색 */
    div[data-testid="stNumberInput"] input {
        background-color: #D9ECFF;
        border: 2px solid #4DA3FF;
        color: black;
    }

    /* 제품 선택 칸 - 파란색 */
    div[data-baseweb="select"] {
        background-color: #D9ECFF;
    }

    /* 1번 페이지 제목 */
    .page1-title {
        text-align: center;
        color: black;
        font-size: 42px;
        font-weight: bold;
        margin-top: 50px;
        margin-bottom: 80px;
    }

    /* 3번 페이지 결과 */
    .result-cost {
        text-align: center;
        color: black;
        font-size: 60px;
        font-weight: bold;
        margin-top: 180px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# 1번 페이지
# ==========================================

def page_one():

    st.markdown(
        '<div class="page1-title">전기 요금을 확인하세요!</div>',
        unsafe_allow_html=True
    )

    # 화면 가운데 배치
    left, center, right = st.columns([1, 2, 1])

    with center:

        selected = st.selectbox(
            "당신이 사용할 전자제품은?",
            ["당신이 사용할 전자제품은?"] + PRODUCTS,
            index=0
        )

        # 제품을 선택하면 바로 2번 페이지로 이동
        if selected != "당신이 사용할 전자제품은?":

            st.session_state.selected_product = selected

            # 이전에 입력했던 소비전력 초기화
            st.session_state.selected_power = None

            # 2번 페이지로 이동
            st.session_state.page = 2

            st.rerun()


# ==========================================
# 2번 페이지
# ==========================================

def page_two():

    # 노란색 배경
    st.markdown(
        """
        <div style="
            background-color: #FFF200;
            min-height: 85vh;
            padding: 40px;
            border-radius: 10px;
        ">
        """,
        unsafe_allow_html=True
    )

    # 선택한 제품 이름
    st.markdown(
        f"""
        <div style="
            text-align: center;
            color: black;
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 50px;
        ">
            {st.session_state.selected_product}
        </div>
        """,
        unsafe_allow_html=True
    )

    # 화면을 왼쪽 / 가운데 / 오른쪽으로 나눔
    left, center, right = st.columns([1, 1, 1])


    # ======================================
    # 왼쪽 - 소비전력
    # ======================================

    with left:

        st.subheader("소비전력 입력하기(kW)")

        power = st.number_input(
            "소비전력 입력하기(kW)",
            min_value=0.0,
            step=0.01,
            format="%.2f",
            value=0.0,
            label_visibility="collapsed"
        )

        # 몰라요 버튼
        if st.button("몰라요"):

            # 기본 소비전력(W)을 kW로 변환
            default_power_kw = (
                POWER_DATA[st.session_state.selected_product] / 1000
            )

            st.session_state.selected_power = default_power_kw


    # ======================================
    # 가운데 - 예상 사용시간
    # ======================================

    with center:

        st.subheader("예상 사용시간 입력하기(h)")

        usage_time = st.number_input(
            "예상 사용시간 입력하기(h)",
            min_value=0.0,
            max_value=24.0,
            step=0.01,
            format="%.2f",
            value=0.0,
            label_visibility="collapsed"
        )


    # ======================================
    # 오른쪽 - 완료
    # ======================================

    with right:

        st.write("")
        st.write("")
        st.write("")

        if st.button("완료"):

            # --------------------------------
            # 소비전력을 입력하지 않은 경우
            # --------------------------------

            if power <= 0 and st.session_state.selected_power is None:

                # 아무것도 하지 않음
                pass

            # --------------------------------
            # 사용시간이 범위를 벗어난 경우
            # --------------------------------

            elif usage_time < 0.01 or usage_time > 24.00:

                # 아무것도 하지 않음
                pass

            # --------------------------------
            # 정상적으로 입력한 경우
            # --------------------------------

            else:

                # 소비전력 결정
                if st.session_state.selected_power is not None:
                    final_power_kw = st.session_state.selected_power
                else:
                    final_power_kw = power

                # ==================================
                # 전력 사용량 계산
                # ==================================
                #
                # 전력 사용량(kWh)
                # = 소비전력(kW) × 사용시간(h)
                #

                electricity_usage = (
                    final_power_kw * usage_time
                )

                # ==================================
                # 예상 전기요금 계산
                # ==================================
                #
                # 예상 전기요금(원)
                # = 전력 사용량(kWh) × 150원
                #

                estimated_cost = (
                    electricity_usage * ELECTRICITY_RATE
                )

                # 계산 결과 저장
                st.session_state.estimated_cost = estimated_cost

                # 3번 페이지로 이동
                st.session_state.page = 3

                st.rerun()


    # ======================================
    # 우측 하단 - 잘못 선택했나요?
    # ======================================

    st.write("")
    st.write("")
    st.write("")

    empty_space, bottom_right = st.columns([5, 1])

    with bottom_right:

        if st.button("잘못 선택했나요?"):

            # 1번 페이지로 이동
            st.session_state.page = 1

            # 선택 정보 초기화
            st.session_state.selected_product = None
            st.session_state.selected_power = None
            st.session_state.estimated_cost = None

            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# 3번 페이지
# ==========================================

def page_three():

    st.markdown(
        f"""
        <div style="
            background-color: white;
            min-height: 85vh;
            display: flex;
            justify-content: center;
            align-items: center;
        ">
            <div style="
                color: black;
                font-size: 60px;
                font-weight: bold;
                text-align: center;
            ">
                {st.session_state.estimated_cost:,.0f}원
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# 현재 페이지 실행
# ==========================================

if st.session_state.page == 1:

    page_one()

elif st.session_state.page == 2:

    page_two()

elif st.session_state.page == 3:

    page_three()

