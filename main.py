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

    # 첫 페이지로 돌아가기 버튼
    st.write("")
    st.write("")

    left, center, right = st.columns([1, 1, 1])

    with center:

        if st.button(
            "첫페이지로 돌아가기",
            key="go_first_page"
        ):

            st.session_state.page = 1
            st.session_state.selected_product = None
            st.session_state.default_power_kw = None
            st.session_state.estimated_cost = None

            st.rerun()

