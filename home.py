import streamlit as st
st.set_page_config(page_title="EcoRoute AI", page_icon="🌍")

import folium
from streamlit_folium import st_folium
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.font_manager as fm
import random
import cv2
import numpy as np
import os

# ✅ 自訂字型設定（支援中文字）
font_path = "./fonts/NotoSansTC-VariableFont_wght.ttf"
if os.path.exists(font_path):
    st.success(f"✅ 成功讀取字型：{font_path}")
    prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = prop.get_name()
else:
    st.error(f"❌ 找不到字型檔：{font_path}，圖表中文字可能無法顯示")
    rcParams['font.family'] = 'sans-serif'

# ✅ 自訂樣式
st.markdown(
    """
    <style>
    body {
        background-color: #f4f7f9;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.4em 1em;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stDataFrame {
        border-radius: 10px;
        border: 1px solid #ddd;
    }
    .stAlert {
        border-left: 5px solid #4CAF50;
        background-color: #e7f4ec;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌍 EcoRoute：AI永續路線小幫手")
st.subheader("讓你每天少走冤枉路，也少排二氧化碳")
st.caption("輸入起點與目的地，系統將根據天氣與交通影像自動推薦最佳通勤選項")

start = st.text_input("請輸入起點：", value="")
end = st.text_input("請輸入目的地：", value="")
weather = st.selectbox("請選擇今日天氣狀況：", ["", "晴天", "陰天", "雨天"])
if not start or not end or not weather:
    st.warning("請完整輸入起點、目的地與天氣狀況。")
    st.stop()

# 模擬資料庫
if weather == "晴天":
    route_database = {
        ("台北車站", "臺灣科技大學"): {
            "捷運": {"時間": 25, "距離": 4.0, "碳排": 0.033, "說明": "紅線至中正紀念堂轉綠線至公館，步行至台科大"},
            "公車": {"時間": 30, "距離": 4.5, "碳排": 0.1, "說明": "搭羅斯福路幹線至公館站，步行 5 分鐘抵達"},
            "開車": {"時間": 18, "距離": 5.8, "碳排": 0.21, "說明": "經市民大道、中山南路、公館圓環至台科大"},
        }
    }
elif weather == "陰天":
    route_database = {
        ("台北車站", "臺灣科技大學"): {
            "捷運": {"時間": 27, "距離": 4.0, "碳排": 0.033, "說明": "紅線至中正紀念堂轉綠線至公館"},
            "公車": {"時間": 34, "距離": 4.5, "碳排": 0.105, "說明": "搭羅斯福路幹線至公館站"},
            "開車": {"時間": 22, "距離": 5.8, "碳排": 0.21, "說明": "經市民大道至台科大"},
        }
    }
else:
    route_database = {
        ("台北車站", "臺灣科技大學"): {
            "捷運": {"時間": 30, "距離": 4.0, "碳排": 0.033, "說明": "轉乘紅線與綠線後步行"},
            "公車": {"時間": 40, "距離": 4.5, "碳排": 0.12, "說明": "羅斯福路幹線到公館"},
            "開車": {"時間": 28, "距離": 5.8, "碳排": 0.25, "說明": "自駕路線經中山南路與基隆路"},
        }
    }

key = (start.strip(), end.strip())
if key not in route_database:
    st.warning("🔍 正在查找路線資料，請確認輸入是否正確。")
    st.stop()

# 表格整理
selected_routes = route_database[key]
df_data = []
for mode, data in selected_routes.items():
    碳排量 = round(data["距離"] * data["碳排"], 3)
    df_data.append({
        "交通方式": mode,
        "時間（分鐘）": data["時間"],
        "距離（公里）": int(data["距離"]),
        "碳排係數（kg CO₂/km）": data["碳排"],
        "碳排量（kg CO₂）": 碳排量,
        "說明": data["說明"]
    })
df = pd.DataFrame(df_data)

st.subheader("📋 通勤方案比較表（含碳足跡分析）")
st.dataframe(df[["交通方式", "時間（分鐘）", "距離（公里）", "碳排係數（kg CO₂/km）", "碳排量（kg CO₂）"]], use_container_width=True)

# 圖表
st.subheader("📊 Time & Carbon Comparison")
labels = df["交通方式"].tolist()
carbon_values = df["碳排量（kg CO₂）"].tolist()
time_values = df["時間（分鐘）"].tolist()
x = np.arange(len(labels))

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.bar(x, time_values, color='skyblue', width=0.4)
ax2.plot(x, carbon_values, 'ro-', linewidth=2, markersize=8)

ax1.set_xticks(x)
ax1.set_xticklabels(labels)
ax1.set_ylabel("Commute Time (min)")
ax2.set_ylabel("Carbon Emission (kg CO2)")

st.pyplot(fig)

# 地圖
st.subheader("起點與終點地圖")
m = folium.Map(location=[25.04, 121.56], zoom_start=13)
folium.Marker([25.0478, 121.5170], popup="台北車站", icon=folium.Icon(color='blue')).add_to(m)
folium.Marker([25.0130, 121.5414], popup="臺灣科技大學", icon=folium.Icon(color='green')).add_to(m)
st_folium(m, width=700, height=450)

# ✅ 插入縮減空白的間距控制
st.markdown("<div style='margin-top: -30px;'></div>", unsafe_allow_html=True)

# 車流分析
if "car_count" not in st.session_state:
    st.session_state["car_count"] = None

st.subheader("🚦 即時交通影像分析")
if st.button("📸 啟動車流量分析（高公局 33K+800）"):
    cap = cv2.VideoCapture("https://cctvn.freeway.gov.tw/abs2mjpg/bmjpg?camera=13380")
    bg_subtractor = cv2.createBackgroundSubtractorMOG2()
    count = 0
    for _ in range(60):
        ret, frame = cap.read()
        if not ret:
            break
        fg = bg_subtractor.apply(frame)
        contours, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cars = [cnt for cnt in contours if cv2.contourArea(cnt) > 500]
        count = max(count, len(cars))
    cap.release()
    st.session_state["car_count"] = count
    st.success(f"目前偵測約有 {count} 輛車")

# 推薦邏輯
car_flow = st.session_state.get("car_count", None)
recommendation = None
target = None

if car_flow is not None:
    st.subheader("📌 今日通勤推薦總結卡")
    if weather == "雨天":
        if car_flow > 10:
            recommendation = "🚇 建議搭乘捷運避開壅塞與雨天不便"
            target = "捷運"
        else:
            target = df[df["交通方式"].isin(["捷運", "公車"])].sort_values(by="碳排量（kg CO₂）").iloc[0]["交通方式"]
            recommendation = f"🚌 車流順暢，雨天建議使用低碳選項：**{target}**"
    elif car_flow > 10:
        target = df.sort_values(by=["時間（分鐘）", "碳排量（kg CO₂）"]).iloc[0]["交通方式"]
        recommendation = f"🚇 車多易塞，建議選擇快速且低碳的通勤方式：**{target}**"
    else:
        target = df[df["交通方式"].isin(["公車", "開車"])].sort_values(by="碳排量（kg CO₂）").iloc[0]["交通方式"]
        recommendation = f"🚗 車流順暢，推薦通勤方式：**{target}**（兼顧效率與碳排）"

    st.success(recommendation)
    total_carbon = df[df["交通方式"] == target]["碳排量（kg CO₂）"].values[0]
    tree_equivalent = round(total_carbon / 0.016, 1)
    st.info(f"🌳 選擇 {target} 預估碳排為 **{total_carbon} kg CO₂**，約需 **{tree_equivalent} 棵樹** 一年吸收")

    green_quotes_by_context = {
        ("晴天", "捷運"): ["🚇 捨棄油門，搭上捷運，那些微小選擇也能成為光。"],
        ("晴天", "公車"): ["🚌 有些快不是真的快，有些慢才是真的到達。"],
        ("晴天", "開車"): ["🚗 城市的風景，從慢下來的駕駛窗外開始。"],
        ("雨天", "捷運"): ["☔ 雨水落下，也落在穩定前行的捷運軌道上。"],
        ("雨天", "公車"): ["🚌 一起擠上車的時候，也是一種暖和的選擇。"],
        ("陰天", "捷運"): ["🚇 陰天讓人想躲進地下，但心裡依舊明亮。"],
        ("陰天", "公車"): ["🚌 坐在窗邊，讓城市慢慢往後滑走。"],
        ("陰天", "開車"): ["🚗 車窗起霧時，也別忘了我們在選擇更永續的方向。"],
    }
    quotes = green_quotes_by_context.get((weather, target), [])
    if quotes:
        st.subheader("🌱 今日綠色生活提醒")
        st.markdown(random.choice(quotes))

    # ✅ 幸運植物 + 植物語
    st.subheader("🪴 今日幸運綠色植物")

    plant_image_map = {
        "晴天": "image/Monstera.png",
        "雨天": "image/Calathea.png",
        "陰天": "image/Pothos.png"
    }

    plant_language_map = {
        "晴天": "🌿 龜背芋的語言：**堅毅、獨立、自信成長**",
        "雨天": "🌧️ 竹芋的語言：**療癒、安撫、包容溫柔的心**",
        "陰天": "☁️ 黃金葛的語言：**堅韌、順應環境、不畏逆境**"
    }

    plant_image_path = plant_image_map.get(weather)
    if plant_image_path:
        st.image(plant_image_path, caption=f"{weather}日的綠色植物祝福 🌿", use_column_width=True)
        plant_message = plant_language_map.get(weather)
        if plant_message:
            st.markdown(f"<div style='text-align:center; font-size:18px; color:#2e7d32; margin-top:10px;'>{plant_message}</div>", unsafe_allow_html=True)
    else:
        st.info("🌱 今天的綠色植物資料尚未準備完成")

# 測驗連結卡片
st.markdown("""
<div style='
    background-color: #e0f7e9;
    padding: 25px;
    border-radius: 14px;
    border: 2px dashed #4CAF50;
    text-align: center;
    margin-top: 40px;
    margin-bottom: 10px;
'>
    <h4 style='color: #2e7d32; font-size: 24px;'>🎯 想知道你有多懂永續嗎？</h4>
    <p style='font-size:18px;'>點擊下方按鈕挑戰「永續小達人測驗」 🧠</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.page_link("pages/quiz.py", label="➠➠➠前往測驗", use_container_width=True)
