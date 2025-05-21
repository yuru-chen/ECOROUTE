
import streamlit as st

# ✅ 設定頁面樣式
st.set_page_config(page_title="永續小達人測驗", page_icon="🧠")

# ✅ 自訂樣式（視覺優化）
st.markdown(
    """
    <style>
    .question-box {
        background-color: #f1f8e9;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
        border-left: 6px solid #8bc34a;
    }
    .submit-button {
        background-color: #4CAF50 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px !important;
        padding: 0.4em 1.2em !important;
    }
    .result-box {
        background-color: #e8f5e9;
        padding: 20px;
        border-radius: 12px;
        margin-top: 30px;
        border: 2px dashed #66bb6a;
    }
    .download-button {
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🔗 返回首頁連結
st.markdown("[⬅ 回首頁](../)")

quiz_questions = [
    {
        "題目": "以下哪種通勤方式的碳排放量通常最低？",
        "選項": ["開車", "公車", "捷運"],
        "答案": "捷運"
    },
    {
        "題目": "一棵樹一年約可吸收多少公斤二氧化碳？",
        "選項": ["1 公斤", "5 公斤", "16 公斤", "50 公斤"],
        "答案": "16 公斤"
    },
    {
        "題目": "哪一項生活行為最有助於減少碳足跡？",
        "選項": ["天天叫外送", "購買在地食材", "長時間開冷氣", "插頭不拔"],
        "答案": "購買在地食材"
    }
]

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
    st.session_state.quiz_score = 0

if not st.session_state.quiz_submitted:
    st.subheader("🧠 小測驗：你了解碳足跡嗎？")
    for idx, q in enumerate(quiz_questions):
        with st.container():
            st.markdown(f"<div class='question-box'><strong>Q{idx+1}. {q['題目']}</strong></div>", unsafe_allow_html=True)
            user_ans = st.radio("", q["選項"], key=f"quiz_q{idx}")
    if st.button("✅ 提交答案", type="primary"):
        score = 0
        for idx, q in enumerate(quiz_questions):
            if st.session_state.get(f"quiz_q{idx}") == q["答案"]:
                score += 1
        st.session_state.quiz_score = score
        st.session_state.quiz_submitted = True

if st.session_state.quiz_submitted:
    score = st.session_state.quiz_score
    st.markdown("<div class='result-box'>", unsafe_allow_html=True)
    st.subheader("🎉 測驗結果")
    st.markdown(f"你答對了 **{score} / {len(quiz_questions)} 題**")
    if score == len(quiz_questions):
        st.balloons()
        st.success("你是碳足跡小博士！🌱")
    elif score >= 2:
        st.info("不錯唷～你有減碳意識 👏")
    else:
        st.warning("還有進步空間，一起努力學習低碳生活！")

    report_text = f"""【EcoRoute AI 測驗報告】
🧠 小測驗得分：{score} / {len(quiz_questions)} 題

感謝你參與 EcoRoute 測驗，選擇永續，就是最棒的起點 🌿
"""
    st.download_button("📎 下載測驗報告", report_text, file_name="ecoroute_quiz_report.txt", mime="text/plain")
    st.markdown("</div>", unsafe_allow_html=True)
