import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import datetime
from gtts import gTTS
import pygame
import tempfile
import os

def speak(text):
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
            tmp_path = f.name
        tts.save(tmp_path)
        pygame.mixer.init()
        pygame.mixer.music.load(tmp_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()
        os.unlink(tmp_path)
    except Exception as e:
        st.error(f"Voice error: {e}")
import plotly.graph_objects as go
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# ---- AUTO REFRESH HAR 10 SEC ----
st_autorefresh(interval=10000, key="autorefresh")

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="🅿️ Smart Parking AI",
    page_icon="🅿️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- ULTRA CSS ----
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600&display=swap');

* { font-family: 'Rajdhani', sans-serif; }

.main { background: #000000; }

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #000000 0%, #0a0015 50%, #000a1a 100%);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0015, #000a1a) !important;
    border-right: 1px solid #7b2ff7;
}

.title-main {
    font-family: 'Orbitron', monospace !important;
    font-size: 52px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #00f5ff, #7b2ff7, #ff006e, #00f5ff);
    background-size: 300% 300%;
    animation: gradientShift 3s ease infinite;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding: 10px;
    text-shadow: none;
    letter-spacing: 3px;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.subtitle {
    text-align: center;
    color: #00f5ff;
    font-size: 16px;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 10px;
    opacity: 0.8;
}

.metric-card {
    background: linear-gradient(135deg, #0a001a, #001a2e);
    border-radius: 20px;
    padding: 25px 15px;
    text-align: center;
    border: 1px solid rgba(123, 47, 247, 0.4);
    box-shadow: 0 0 20px rgba(0, 245, 255, 0.1);
    transition: all 0.3s;
    margin: 5px;
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #00f5ff, #7b2ff7);
}

.metric-card:hover {
    border-color: #00f5ff;
    box-shadow: 0 0 30px rgba(0, 245, 255, 0.3);
    transform: translateY(-3px);
}

.zone-name { color: #aaaacc; font-size: 13px; letter-spacing: 1px; margin-bottom: 8px; }
.occ-free  { color: #00ff88; font-size: 38px; font-weight: 900; font-family: 'Orbitron', monospace; }
.occ-busy  { color: #ffd700; font-size: 38px; font-weight: 900; font-family: 'Orbitron', monospace; }
.occ-full  { color: #ff4444; font-size: 38px; font-weight: 900; font-family: 'Orbitron', monospace; animation: pulse 1s infinite; }

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
}

.status-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 2px;
    margin-top: 5px;
}

.badge-free { background: rgba(0,255,136,0.2); color: #00ff88; border: 1px solid #00ff88; }
.badge-busy { background: rgba(255,215,0,0.2); color: #ffd700; border: 1px solid #ffd700; }
.badge-full { background: rgba(255,68,68,0.2); color: #ff4444; border: 1px solid #ff4444; }

.ai-box {
    background: linear-gradient(135deg, #050010, #001020);
    border: 1px solid rgba(0, 245, 255, 0.3);
    border-radius: 20px;
    padding: 25px;
    margin: 10px 0;
    position: relative;
    overflow: hidden;
}

.ai-box::after {
    content: '🤖';
    position: absolute;
    right: 20px;
    top: 20px;
    font-size: 40px;
    opacity: 0.15;
}

.live-badge {
    display: inline-block;
    background: #ff0040;
    color: white;
    padding: 3px 10px;
    border-radius: 10px;
    font-size: 12px;
    font-weight: bold;
    animation: livePulse 1.5s infinite;
    letter-spacing: 2px;
}

@keyframes livePulse {
    0% { box-shadow: 0 0 0 0 rgba(255,0,64,0.7); }
    70% { box-shadow: 0 0 0 8px rgba(255,0,64,0); }
    100% { box-shadow: 0 0 0 0 rgba(255,0,64,0); }
}

.section-title {
    font-family: 'Orbitron', monospace;
    color: #00f5ff;
    font-size: 18px;
    letter-spacing: 3px;
    border-bottom: 1px solid rgba(0,245,255,0.3);
    padding-bottom: 10px;
    margin: 20px 0 15px 0;
}

.stat-row {
    background: rgba(0,245,255,0.05);
    border-radius: 10px;
    padding: 15px;
    margin: 5px 0;
    border-left: 3px solid #7b2ff7;
}

div[data-testid="stMetric"] {
    background: rgba(123,47,247,0.1);
    border-radius: 10px;
    padding: 10px;
    border: 1px solid rgba(123,47,247,0.3);
}
</style>
""", unsafe_allow_html=True)

# ---- LOAD MODEL ----
@st.cache_resource
def load_model():
    df = pd.read_csv('dataset.csv')
    df.dropna(inplace=True)
    df['LastUpdated'] = pd.to_datetime(df['LastUpdated'])
    df['Hour']    = df['LastUpdated'].dt.hour
    df['Minute']  = df['LastUpdated'].dt.minute
    df['Day']     = df['LastUpdated'].dt.dayofweek
    df['OccupancyRate'] = df['Occupancy'] / df['Capacity']
    le = LabelEncoder()
    df['Location_enc'] = le.fit_transform(df['SystemCodeNumber'])
    X = df[['Hour','Minute','Day','Capacity','Location_enc']]
    y = df['OccupancyRate']
    model = LinearRegression()
    model.fit(X, y)
    return model, df, le

model, df, le = load_model()

# ---- ZONES ----
zones = {
    "BHMBCCMKT01": {"name": "Bull Ring Market",  "lat": 52.4774, "lon": -1.8934, "capacity": 577},
    "BHMBCCPST01": {"name": "Paradise Street",   "lat": 52.4797, "lon": -1.9036, "capacity": 1632},
    "BHMBCCSNH01": {"name": "Snow Hill",         "lat": 52.4850, "lon": -1.8998, "capacity": 388},
    "BHMBCCTHL01": {"name": "Town Hall",         "lat": 52.4808, "lon": -1.9000, "capacity": 348},
    "BHMBRCBRG01": {"name": "Broad Street",      "lat": 52.4778, "lon": -1.9108, "capacity": 1100},
    "BHMBRCBRG02": {"name": "Brindleyplace",     "lat": 52.4765, "lon": -1.9122, "capacity": 900},
    "BHMBRCBRG03": {"name": "Gas Street Basin",  "lat": 52.4751, "lon": -1.9098, "capacity": 750},
    "BHMMBMMBX01": {"name": "Mailbox",           "lat": 52.4733, "lon": -1.9016, "capacity": 500},
}

def predict_occ(code, hour, minute, day):
    try:    loc_enc = le.transform([code])[0]
    except: loc_enc = 0
    cap = zones[code]['capacity']
    noise = np.random.uniform(-0.05, 0.05)
    pred = model.predict(pd.DataFrame({
        'Hour':[hour],'Minute':[minute],
        'Day':[day],'Capacity':[cap],
        'Location_enc':[loc_enc]
    }))[0]
    return max(0.05, min(0.99, pred + noise))

def get_css(occ):
    if occ > 0.8: return "occ-full",  "badge-full",  "🔴 CRITICAL"
    if occ > 0.5: return "occ-busy",  "badge-busy",  "🟡 BUSY"
    return              "occ-free",  "badge-free",  "🟢 AVAILABLE"

# ---- SIDEBAR ----
with st.sidebar:
    st.markdown('<p style="font-family:Orbitron; color:#00f5ff; font-size:16px; letter-spacing:3px;">⚙️ CONTROLS</p>', unsafe_allow_html=True)
    st.markdown("---")
    use_live = st.toggle("⚡ LIVE MODE", value=True)
    now = datetime.datetime.now()

    if use_live:
        hour, minute, day = now.hour, now.minute, now.weekday()
        st.markdown(f'<div class="live-badge">● LIVE</div>', unsafe_allow_html=True)
        st.markdown(f"<p style='color:#aaa; margin-top:10px;'>🕐 {now.strftime('%H:%M:%S')}<br>📅 {now.strftime('%A, %d %b %Y')}</p>", unsafe_allow_html=True)
    else:
        hour   = st.slider("🕐 Hour", 0, 23, 9)
        minute = st.slider("⏱ Minute", 0, 59, 0)
        day    = st.selectbox("📅 Day", ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])
        day    = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"].index(day)

    st.markdown("---")
    st.markdown('<p style="font-family:Orbitron; color:#7b2ff7; font-size:13px;">📊 DATASET STATS</p>', unsafe_allow_html=True)
    st.markdown(f"<p style='color:#aaa; font-size:13px;'>Total Records: {len(df):,}<br>Zones: {len(zones)}<br>Model: Linear Regression<br>Metric: RMSE</p>", unsafe_allow_html=True)

    st.markdown("---")
    selected_zone = st.selectbox("🔍 Zone Detail", [zones[z]['name'] for z in zones])

# ---- HEADER ----
st.markdown('<div class="title-main">🅿️ SMART PARKING AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Real-Time Occupancy Prediction System — Birmingham City</div>', unsafe_allow_html=True)

col_live, col_time, col_refresh = st.columns([1,2,1])
with col_live:
    if use_live:
        st.markdown('<div class="live-badge">● LIVE FEED</div>', unsafe_allow_html=True)
with col_time:
    st.markdown(f"<p style='text-align:center; color:#7b2ff7; font-family:Orbitron; font-size:14px;'>⏰ {now.strftime('%H:%M:%S')} | {now.strftime('%A').upper()}</p>", unsafe_allow_html=True)
with col_refresh:
    st.markdown("<p style='color:#555; font-size:11px; text-align:right;'>🔄 Auto-refresh: 10s</p>", unsafe_allow_html=True)

# ---- PREDICT ALL ----
predictions = {code: predict_occ(code, hour, minute, day) for code in zones}

# ---- TOP STATS ----
st.markdown("---")
s1, s2, s3, s4 = st.columns(4)
total_cap   = sum(z['capacity'] for z in zones.values())
total_occ   = sum(predictions[c] * zones[c]['capacity'] for c in zones)
avg_occ     = np.mean(list(predictions.values()))
free_zones  = sum(1 for v in predictions.values() if v < 0.5)
full_zones  = sum(1 for v in predictions.values() if v > 0.8)

s1.metric("🏙️ Total Capacity",  f"{total_cap:,} slots")
s2.metric("🚗 Currently Occupied", f"{int(total_occ):,}", f"{avg_occ*100:.1f}% full")
s3.metric("🟢 Free Zones",  f"{free_zones} / {len(zones)}")
s4.metric("🔴 Critical Zones", f"{full_zones} / {len(zones)}")

# ---- ZONE CARDS ----
st.markdown('<div class="section-title">📡 LIVE ZONE STATUS</div>', unsafe_allow_html=True)

cols1 = st.columns(4)
cols2 = st.columns(4)
all_cols = cols1 + cols2
zone_list = list(zones.keys())

for i, col in enumerate(all_cols):
    code = zone_list[i]
    info = zones[code]
    occ  = predictions[code]
    occ_cls, badge_cls, status = get_css(occ)
    slots_free = int(info['capacity'] * (1 - occ))

    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="zone-name">{info['name'].upper()}</div>
            <div class="{occ_cls}">{occ*100:.0f}%</div>
            <div class="status-badge {badge_cls}">{status}</div>
            <div style="color:#555; font-size:11px; margin-top:8px;">
                {slots_free} slots free<br>
                Cap: {info['capacity']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---- MAP ----
st.markdown('<div class="section-title">🗺️ LIVE CITY MAP</div>', unsafe_allow_html=True)

m = folium.Map(
    location=[52.4800, -1.9000],
    zoom_start=14,
    tiles='CartoDB dark_matter'
)

for code, info in zones.items():
    occ   = predictions[code]
    color = '#ff4444' if occ > 0.8 else '#ffd700' if occ > 0.5 else '#00ff88'
    radius = 15 + (occ * 20)

    folium.CircleMarker(
        location=[info['lat'], info['lon']],
        radius=radius,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.6,
        popup=folium.Popup(f"""
            <div style='font-family:monospace; background:#000; color:#0ff; padding:10px; border-radius:8px;'>
                <b style='color:#fff'>{info['name']}</b><br>
                <span style='color:#0f0'>Occupancy: {occ*100:.1f}%</span><br>
                Free Slots: {int(info['capacity']*(1-occ))}<br>
                Capacity: {info['capacity']}
            </div>
        """, max_width=220)
    ).add_to(m)

    folium.Marker(
        location=[info['lat'], info['lon']],
        icon=folium.DivIcon(html=f"""
            <div style='font-family:monospace; font-size:12px; font-weight:900;
                        color:{color}; text-shadow: 0 0 10px {color};
                        text-align:center; white-space:nowrap;'>
                {occ*100:.0f}%
            </div>
        """)
    ).add_to(m)

st_folium(m, width=1400, height=500, returned_objects=[])

# ---- AI ADVISOR ----
st.markdown('<div class="section-title">🤖 AI ADVISOR</div>', unsafe_allow_html=True)

best  = min(predictions, key=predictions.get)
worst = max(predictions, key=predictions.get)

adv1, adv2 = st.columns(2)
# ---- VOICE BUTTON ----
v1, v2, v3 = st.columns([1,1,2])
with v1:
    if st.button("🔊 Speak Best Zone"):
        b_occ = predictions[best]
        msg = f"Best parking zone is {zones[best]['name']}. Currently {int(b_occ*100)} percent full. {int(zones[best]['capacity']*(1-b_occ))} slots available. Go now!"
        speak(msg)

with v2:
    if st.button("📢 Speak All Zones"):
        full_msg = "Smart Parking Status Report. "
        for code in zone_list:
            occ_val = predictions[code]
            status_word = "critical" if occ_val > 0.8 else "busy" if occ_val > 0.5 else "available"
            full_msg += f"{zones[code]['name']}, {int(occ_val*100)} percent, {status_word}. "
        speak(full_msg)

with v3:
    if st.button("🚨 Alert Critical Zones"):
        critical = [c for c in predictions if predictions[c] > 0.8]
        if critical:
            alert_msg = f"Warning! {len(critical)} critical zones detected. "
            for c in critical:
                alert_msg += f"{zones[c]['name']} is almost full. "
            alert_msg += "Please redirect to available zones immediately!"
            speak(alert_msg)
        else:
            speak("All zones are operating normally. No critical zones at this time.")

with adv1:
    b_occ = predictions[best]
    st.markdown(f"""
    <div class="ai-box">
        <p style='color:#00ff88; font-family:Orbitron; font-size:13px; letter-spacing:2px;'>✅ BEST ZONE NOW</p>
        <h2 style='color:white; margin:5px 0;'>{zones[best]['name']}</h2>
        <p style='color:#00f5ff; font-size:36px; font-family:Orbitron; font-weight:900; margin:0;'>{b_occ*100:.0f}%</p>
        <p style='color:#aaa;'>Only {int(zones[best]['capacity']*(1-b_occ))} slots remaining — Go NOW!</p>
        <div style='background:rgba(0,255,136,0.1); border-radius:8px; padding:10px; margin-top:10px;'>
            <p style='color:#00ff88; margin:0;'>🤖 AI says: Estimated wait time <b>0 min</b>. Best option in city!</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with adv2:
    w_occ = predictions[worst]
    wait  = int(w_occ * 30)
    st.markdown(f"""
    <div class="ai-box" style='border-color:rgba(255,68,68,0.4);'>
        <p style='color:#ff4444; font-family:Orbitron; font-size:13px; letter-spacing:2px;'>⚠️ AVOID THIS ZONE</p>
        <h2 style='color:white; margin:5px 0;'>{zones[worst]['name']}</h2>
        <p style='color:#ff4444; font-size:36px; font-family:Orbitron; font-weight:900; margin:0;'>{w_occ*100:.0f}%</p>
        <p style='color:#aaa;'>Almost full — only {int(zones[worst]['capacity']*(1-w_occ))} slots left!</p>
        <div style='background:rgba(255,68,68,0.1); border-radius:8px; padding:10px; margin-top:10px;'>
            <p style='color:#ff4444; margin:0;'>🤖 AI says: Expected wait ~{wait} min. Avoid if possible!</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---- CHARTS ----
st.markdown('<div class="section-title">📈 HOURLY PREDICTION ANALYSIS</div>', unsafe_allow_html=True)

ch1, ch2 = st.columns(2)

with ch1:
    hours = list(range(24))
    fig = go.Figure()
    colors_line = ['#00f5ff','#7b2ff7','#ff006e','#00ff88','#ffd700','#ff8c00','#00bfff','#ff69b4']
    for i, code in enumerate(zone_list):
        preds = [predict_occ(code, h, 0, day)*100 for h in hours]
        fig.add_trace(go.Scatter(
            x=hours, y=preds,
            name=zones[code]['name'],
            line=dict(color=colors_line[i], width=2),
            fill='tozeroy',
            fillcolor=f"rgba{tuple(list(bytes.fromhex(colors_line[i][1:])) + [20])}",
        ))
    fig.add_vline(x=hour, line_dash="dash", line_color="white", opacity=0.5)
    fig.update_layout(
        title="24-Hour Occupancy Forecast",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,20,0.8)',
        font=dict(color='white'),
        legend=dict(bgcolor='rgba(0,0,0,0.5)'),
        xaxis=dict(title="Hour", gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title="Occupancy %", gridcolor='rgba(255,255,255,0.1)'),
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

with ch2:
    zone_names = [zones[c]['name'] for c in zone_list]
    occ_vals   = [predictions[c]*100 for c in zone_list]
    bar_colors = ['#ff4444' if v>80 else '#ffd700' if v>50 else '#00ff88' for v in occ_vals]

    fig2 = go.Figure(go.Bar(
        x=occ_vals,
        y=zone_names,
        orientation='h',
        marker=dict(color=bar_colors, line=dict(color='rgba(255,255,255,0.2)', width=1)),
        text=[f"{v:.1f}%" for v in occ_vals],
        textposition='outside',
        textfont=dict(color='white')
    ))
    fig2.add_vline(x=50, line_dash="dot", line_color="#ffd700", opacity=0.5)
    fig2.add_vline(x=80, line_dash="dot", line_color="#ff4444", opacity=0.5)
    fig2.update_layout(
        title="Current Zone Comparison",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,20,0.8)',
        font=dict(color='white'),
        xaxis=dict(title="Occupancy %", range=[0,110], gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        height=400
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---- ZONE DETAIL ----
st.markdown('<div class="section-title">🔍 ZONE DEEP DIVE</div>', unsafe_allow_html=True)

sel_code = [c for c in zones if zones[c]['name'] == selected_zone][0]
sel_occ  = predictions[sel_code]
sel_info = zones[sel_code]
_, badge_cls, status = get_css(sel_occ)

d1, d2, d3, d4 = st.columns(4)
d1.metric("📍 Zone",        sel_info['name'])
d2.metric("📊 Occupancy",   f"{sel_occ*100:.1f}%")
d3.metric("🚗 Slots Used",  f"{int(sel_info['capacity']*sel_occ)}")
d4.metric("✅ Slots Free",  f"{int(sel_info['capacity']*(1-sel_occ))}")

gauge = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=sel_occ * 100,
    title={'text': f"{sel_info['name']}", 'font': {'color': 'white', 'size': 16}},
    number={'suffix': "%", 'font': {'color': 'white', 'size': 40}},
    delta={'reference': 50, 'font': {'color': 'white'}},
    gauge={
        'axis': {'range': [0, 100], 'tickcolor': 'white', 'tickfont': {'color': 'white'}},
        'bar': {'color': '#ff4444' if sel_occ>0.8 else '#ffd700' if sel_occ>0.5 else '#00ff88'},
        'bgcolor': 'rgba(0,0,0,0)',
        'bordercolor': '#333',
        'steps': [
            {'range': [0, 50],  'color': 'rgba(0,255,136,0.1)'},
            {'range': [50, 80], 'color': 'rgba(255,215,0,0.1)'},
            {'range': [80, 100],'color': 'rgba(255,68,68,0.1)'},
        ],
        'threshold': {'line': {'color': "white", 'width': 3}, 'thickness': 0.75, 'value': sel_occ*100}
    }
))
gauge.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    height=300
)
st.plotly_chart(gauge, use_container_width=True)
# ---- SLOT BOOKING SYSTEM ----
st.markdown('<div class="section-title">🎫 SLOT BOOKING SYSTEM</div>', unsafe_allow_html=True)

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import io

# Session state for bookings
if 'bookings' not in st.session_state:
    st.session_state.bookings = []

bk1, bk2 = st.columns([1, 1])

with bk1:
    st.markdown("""
    <div class="ai-box">
        <p style='color:#00f5ff; font-family:Orbitron; font-size:13px; letter-spacing:2px;'>📝 BOOK YOUR SLOT</p>
    </div>
    """, unsafe_allow_html=True)

    user_name    = st.text_input("👤 Your Name")
    user_phone   = st.text_input("📱 Phone Number")
    user_vehicle = st.text_input("🚗 Vehicle Number")
    book_zone    = st.selectbox("📍 Select Zone", [zones[z]['name'] for z in zones])
    book_hours   = st.slider("⏱ Hours to Park", 1, 8, 2)

    book_zone_code = [c for c in zones if zones[c]['name'] == book_zone][0]
    zone_occ       = predictions[book_zone_code]
    slots_free     = int(zones[book_zone_code]['capacity'] * (1 - zone_occ))
    price_per_hour = 50
    total_price    = book_hours * price_per_hour

    st.markdown(f"""
    <div style='background:rgba(0,245,255,0.05); border-radius:10px; padding:15px; margin:10px 0; border:1px solid rgba(0,245,255,0.2);'>
        <p style='color:#aaa; margin:3px 0;'>📊 Zone Occupancy: <span style='color:#00f5ff;'>{zone_occ*100:.0f}%</span></p>
        <p style='color:#aaa; margin:3px 0;'>🅿️ Free Slots: <span style='color:#00ff88;'>{slots_free}</span></p>
        <p style='color:#aaa; margin:3px 0;'>💰 Rate: <span style='color:#ffd700;'>Rs. {price_per_hour}/hour</span></p>
        <p style='color:#aaa; margin:3px 0;'>💵 Total: <span style='color:#ffd700; font-size:20px; font-weight:bold;'>Rs. {total_price}</span></p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("✅ CONFIRM BOOKING", use_container_width=True):
        if user_name and user_phone and user_vehicle:
            if slots_free > 0:
                booking_id = f"PK{datetime.datetime.now().strftime('%d%m%H%M%S')}"
                slot_num   = f"{book_zone_code[-2:]}-{np.random.randint(10,99)}"
                booking = {
                    'id':       booking_id,
                    'name':     user_name,
                    'phone':    user_phone,
                    'vehicle':  user_vehicle,
                    'zone':     book_zone,
                    'slot':     slot_num,
                    'hours':    book_hours,
                    'price':    total_price,
                    'time':     datetime.datetime.now().strftime('%d %b %Y, %H:%M'),
                    'status':   'CONFIRMED'
                }
                st.session_state.bookings.append(booking)

                # ---- GENERATE PDF TICKET ----
                def generate_ticket(b):
                    buf = io.BytesIO()
                    c = canvas.Canvas(buf, pagesize=A4)
                    w, h = A4

                    # Background
                    c.setFillColorRGB(0.04, 0.0, 0.1)
                    c.rect(0, 0, w, h, fill=1, stroke=0)

                    # Header bar
                    c.setFillColorRGB(0.0, 0.96, 1.0)
                    c.rect(0, h-100, w, 100, fill=1, stroke=0)

                    c.setFillColorRGB(0, 0, 0)
                    c.setFont("Helvetica-Bold", 28)
                    c.drawCentredString(w/2, h-55, "SMART PARKING AI")
                    c.setFont("Helvetica", 14)
                    c.drawCentredString(w/2, h-80, "BOOKING CONFIRMATION TICKET")

                    # Ticket box
                    c.setFillColorRGB(0.08, 0.0, 0.18)
                    c.setStrokeColorRGB(0.0, 0.96, 1.0)
                    c.setLineWidth(2)
                    c.roundRect(40, h-380, w-80, 260, 15, fill=1, stroke=1)

                    # Booking ID big
                    c.setFillColorRGB(0.0, 0.96, 1.0)
                    c.setFont("Helvetica-Bold", 22)
                    c.drawCentredString(w/2, h-145, f"BOOKING ID: {b['id']}")

                    # Divider
                    c.setStrokeColorRGB(0.48, 0.18, 0.97)
                    c.setLineWidth(1)
                    c.line(60, h-160, w-60, h-160)

                    # Details
                    details = [
                        ("👤 Passenger",  b['name']),
                        ("📱 Phone",      b['phone']),
                        ("🚗 Vehicle",    b['vehicle']),
                        ("📍 Zone",       b['zone']),
                        ("🅿️ Slot No.",   b['slot']),
                        ("⏱ Duration",   f"{b['hours']} Hours"),
                        ("💰 Amount",     f"Rs. {b['price']}"),
                        ("🕐 Booked At",  b['time']),
                    ]

                    y_pos = h - 190
                    for label, value in details:
                        c.setFillColorRGB(0.6, 0.6, 0.8)
                        c.setFont("Helvetica", 11)
                        c.drawString(70, y_pos, label)
                        c.setFillColorRGB(1.0, 1.0, 1.0)
                        c.setFont("Helvetica-Bold", 12)
                        c.drawString(250, y_pos, str(value))
                        y_pos -= 25

                    # Status badge
                    c.setFillColorRGB(0.0, 1.0, 0.53)
                    c.roundRect(w/2-70, h-400, 140, 35, 8, fill=1, stroke=0)
                    c.setFillColorRGB(0, 0, 0)
                    c.setFont("Helvetica-Bold", 16)
                    c.drawCentredString(w/2, h-378, "✓ CONFIRMED")

                    # Barcode simulation
                    c.setFillColorRGB(1,1,1)
                    c.setFont("Helvetica", 7)
                    bar_x = 60
                    for i in range(80):
                        bw = np.random.choice([1,2,3])
                        if np.random.random() > 0.4:
                            c.setFillColorRGB(1,1,1)
                        else:
                            c.setFillColorRGB(0.04,0,0.1)
                        c.rect(bar_x, h-470, bw, 50, fill=1, stroke=0)
                        bar_x += bw + 1

                    c.setFillColorRGB(0.6,0.6,0.8)
                    c.setFont("Helvetica", 9)
                    c.drawCentredString(w/2, h-490, b['id'])

                    # Footer
                    c.setFillColorRGB(0.3, 0.3, 0.5)
                    c.setFont("Helvetica", 10)
                    c.drawCentredString(w/2, 40, "AI Applications Lab | Project 72 | Smart Parking System")
                    c.drawCentredString(w/2, 25, "This is a computer generated ticket. No signature required.")

                    c.save()
                    buf.seek(0)
                    return buf

                pdf_buf = generate_ticket(booking)

                st.success(f"✅ Booking Confirmed! ID: {booking_id}")
                st.balloons()

                st.download_button(
                    label="🎫 DOWNLOAD YOUR TICKET (PDF)",
                    data=pdf_buf,
                    file_name=f"parking_ticket_{booking_id}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            else:
                st.error("❌ No slots available in this zone!")
        else:
            st.warning("⚠️ Please fill all fields!")

with bk2:
    st.markdown("""
    <div class="ai-box">
        <p style='color:#7b2ff7; font-family:Orbitron; font-size:13px; letter-spacing:2px;'>📋 RECENT BOOKINGS</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.bookings:
        for b in reversed(st.session_state.bookings[-5:]):
            st.markdown(f"""
            <div style='background:rgba(123,47,247,0.1); border-radius:10px;
                        padding:12px; margin:8px 0; border-left:3px solid #7b2ff7;'>
                <p style='color:#00f5ff; font-weight:bold; margin:0;'>#{b['id']}</p>
                <p style='color:#fff; margin:3px 0;'>{b['name']} — {b['vehicle']}</p>
                <p style='color:#aaa; font-size:12px; margin:0;'>
                    📍 {b['zone']} | 🅿️ {b['slot']} | ⏱ {b['hours']}h | 💰 Rs.{b['price']}
                </p>
                <p style='color:#555; font-size:11px; margin:3px 0;'>{b['time']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='text-align:center; padding:50px; color:#333;'>
            <p style='font-size:40px;'>🅿️</p>
            <p>No bookings yet!</p>
        </div>
        """, unsafe_allow_html=True)

        # ---- AI CHATBOT (No API needed) ----
st.markdown('<div class="section-title">🤖 AI PARKING CHATBOT</div>', unsafe_allow_html=True)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def smart_reply(user_msg):
    msg = user_msg.lower()
    
    best  = min(predictions, key=predictions.get)
    worst = max(predictions, key=predictions.get)
    b_occ = predictions[best]
    w_occ = predictions[worst]
    free_slots = {c: int(zones[c]['capacity'] * (1 - predictions[c])) for c in zones}
    most_free  = max(free_slots, key=free_slots.get)

    # Best zone
    if any(w in msg for w in ['best', 'accha', 'achha', 'sahi', 'recommend', 'kahan jaun', 'suggest']):
        return f"🟢 Best zone abhi **{zones[best]['name']}** hai!\n\n📊 Sirf **{b_occ*100:.0f}% full** hai\n🅿️ **{free_slots[best]} slots** available\n💰 Rs. 50/hour\n\n✅ Abhi jao — best time hai!"

    # Avoid
    elif any(w in msg for w in ['avoid', 'mat ja', 'full', 'busy', 'bheed']):
        return f"🔴 **{zones[worst]['name']}** avoid karo!\n\n😬 **{w_occ*100:.0f}% full** hai abhi\n😰 Sirf **{free_slots[worst]} slots** bache hain\n\n➡️ Instead jao: **{zones[best]['name']}** — {b_occ*100:.0f}% full"

    # Free slots
    elif any(w in msg for w in ['free', 'khali', 'space', 'slot', 'jagah']):
        return f"🅿️ Sabse zyada jagah **{zones[most_free]['name']}** mein hai!\n\n✅ **{free_slots[most_free]} slots** available\n📊 {predictions[most_free]*100:.0f}% full\n💰 Rs. 50/hour"

    # Price
    elif any(w in msg for w in ['price', 'rate', 'cost', 'kitna', 'paisa', 'charge', 'fee']):
        return f"💰 Pricing bilkul simple hai!\n\n🕐 Rs. **50 per hour** — sabhi zones mein same rate\n📋 2 ghante = Rs. 100\n📋 4 ghante = Rs. 200\n📋 8 ghante = Rs. 400\n\n💳 Booking system se reserve karo!"

    # Status all
    elif any(w in msg for w in ['status', 'sab', 'all', 'sabhi', 'sara', 'report']):
        reply = "📊 **Live Parking Status:**\n\n"
        for code in zone_list:
            occ = predictions[code]
            emoji = "🔴" if occ > 0.8 else "🟡" if occ > 0.5 else "🟢"
            reply += f"{emoji} **{zones[code]['name']}** — {occ*100:.0f}% full ({free_slots[code]} slots free)\n"
        return reply

    # Time / when
    elif any(w in msg for w in ['time', 'kab', 'when', 'subah', 'morning', 'evening', 'sham']):
        return f"⏰ **Best time to park:**\n\n🌅 Early morning (6-8 AM) — sabse kam bheed\n☀️ Midday (12-2 PM) — moderate\n🌆 Evening (5-8 PM) — sabse zyada bheed\n\n💡 Abhi **{now.strftime('%H:%M')}** hai — {zones[best]['name']} best option!"

    # Book
    elif any(w in msg for w in ['book', 'reserve', 'booking', 'kaise']):
        return f"💳 **Booking kaise karein:**\n\n1️⃣ Neeche 'Slot Booking System' mein jao\n2️⃣ Apna naam, phone, vehicle number dalo\n3️⃣ Zone select karo\n4️⃣ Hours choose karo\n5️⃣ **Confirm Booking** dabao\n6️⃣ PDF ticket download karo! 🎫\n\n✅ Rs. 50/hour — simple aur fast!"

    # Hello / hi
    elif any(w in msg for w in ['hello', 'hi', 'hey', 'helo', 'salam', 'assalam', 'namaste']):
        return f"👋 **Assalam o Alaikum / Hello!**\n\nMain hoon aapka **Smart Parking AI Assistant** 🤖\n\nMain in chezon mein help kar sakta hoon:\n🟢 Best zone dhundna\n🔴 Busy zones avoid karna\n💰 Pricing info\n📊 Live status\n💳 Booking guide\n\nPoochho kuch bhi! 😊"

    # Thanks
    elif any(w in msg for w in ['thanks', 'shukriya', 'thank', 'shukria', 'theek']):
        return "😊 **Khushi hui madad karke!**\n\nSafe parking karo bhai! 🚗✨\nKoi aur sawaal ho toh zaroor poochho!"

    # Default
    else:
        return f"🤖 Samajh nahi aaya — try karo:\n\n💬 'Best zone kaunsa hai?'\n💬 'Kahan avoid karun?'\n💬 'Kitne slots free hain?'\n💬 'Price kya hai?'\n💬 'Sab zones ka status bata'\n💬 'Booking kaise karun?'\n\n❓ Ya neeche quick buttons use karo!"

# Chat display
for msg in st.session_state.chat_history:
    if msg['role'] == 'user':
        st.markdown(f"""
        <div style='display:flex; justify-content:flex-end; margin:8px 0;'>
            <div style='background:linear-gradient(135deg, #7b2ff7, #00f5ff);
                        padding:12px 18px; border-radius:20px 20px 5px 20px;
                        max-width:70%; color:white; font-size:14px;'>
                {msg['content']}
            </div>
            <span style='margin-left:8px; font-size:20px;'>👤</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='display:flex; justify-content:flex-start; margin:8px 0;'>
            <span style='margin-right:8px; font-size:20px;'>🤖</span>
            <div style='background:linear-gradient(135deg, #0a0015, #001020);
                        padding:12px 18px; border-radius:20px 20px 20px 5px;
                        max-width:70%; color:#00f5ff; font-size:14px;
                        border:1px solid rgba(0,245,255,0.2);'>
                {msg['content']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Quick buttons
st.markdown("<p style='color:#555; font-size:12px; margin:5px 0;'>⚡ Quick Questions:</p>", unsafe_allow_html=True)
qc1, qc2, qc3, qc4 = st.columns(4)
quick_q = None
with qc1:
    if st.button("🟢 Best zone?"): quick_q = "Best zone kaunsa hai?"
with qc2:
    if st.button("🔴 Avoid kahan?"): quick_q = "Kahan avoid karun?"
with qc3:
    if st.button("💰 Price kya hai?"): quick_q = "Price kya hai?"
with qc4:
    if st.button("📊 Full status?"): quick_q = "Sab zones ka status bata"

user_input = st.chat_input("Poochho kuch bhi... 'Best zone kaunsa hai?'")
if quick_q:
    user_input = quick_q

if user_input:
    st.session_state.chat_history.append({'role': 'user', 'content': user_input})
    reply = smart_reply(user_input)
    st.session_state.chat_history.append({'role': 'assistant', 'content': reply})
    st.rerun()

if st.session_state.chat_history:
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# ---- FOOTER ----
st.markdown("---")
st.markdown("""
<div style='text-align:center; padding:20px;'>
    <p style='font-family:Orbitron; color:#333; font-size:11px; letter-spacing:3px;'>
        AI APPLICATIONS LAB | PROJECT 72 | SMART PARKING SYSTEM<br>
        <span style='color:#7b2ff7;'>POWERED BY MACHINE LEARNING</span>
    </p>
</div>
""", unsafe_allow_html=True)