
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
from urllib.parse import quote

st.set_page_config(
    page_title="Overwatch Prototype v8",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Dummy data
# -----------------------------
OFFICES = [
    {"id": "OFF-001", "name": "London Office", "city": "London", "country": "United Kingdom", "lat": 51.5072, "lon": -0.1276, "record_type": "Office"},
    {"id": "OFF-002", "name": "Nairobi Office", "city": "Nairobi", "country": "Kenya", "lat": -1.2864, "lon": 36.8172, "record_type": "Office"},
    {"id": "OFF-003", "name": "Singapore Office", "city": "Singapore", "country": "Singapore", "lat": 1.3521, "lon": 103.8198, "record_type": "Office"},
    {"id": "OFF-004", "name": "Washington DC Office", "city": "Washington DC", "country": "United States", "lat": 38.9072, "lon": -77.0369, "record_type": "Office"},
    {"id": "OFF-005", "name": "Dubai Office", "city": "Dubai", "country": "United Arab Emirates", "lat": 25.2048, "lon": 55.2708, "record_type": "Office"},
]

TEMPORARY_LOCATIONS = [
    {"id": "TMP-001", "name": "Manila Project Site", "city": "Manila", "country": "Philippines", "lat": 14.5995, "lon": 120.9842, "status": "Active", "start_date": "2026-05-01", "end_date": "2026-06-30", "record_type": "Temporary Location"},
    {"id": "TMP-002", "name": "Lagos Election Support Team", "city": "Lagos", "country": "Nigeria", "lat": 6.5244, "lon": 3.3792, "status": "Archived", "start_date": "2026-02-10", "end_date": "2026-03-02", "record_type": "Temporary Location"},
    {"id": "TMP-003", "name": "Lima Field Visit", "city": "Lima", "country": "Peru", "lat": -12.0464, "lon": -77.0428, "status": "Active", "start_date": "2026-05-10", "end_date": "2026-05-19", "record_type": "Temporary Location"},
]

TRAVELLING_STAFF = [
    {"id": "MOV-001", "name": "Traveller A", "route": "LHR → IST → NBO", "airport": "NBO", "city": "Nairobi", "country": "Kenya", "lat": -1.3192, "lon": 36.9278, "date_range": "12-14 May", "status": "Active", "record_type": "Monitored Move"},
    {"id": "MOV-002", "name": "Traveller B", "route": "JFK → LHR", "airport": "LHR", "city": "London", "country": "United Kingdom", "lat": 51.4700, "lon": -0.4543, "date_range": "13 May", "status": "Active", "record_type": "Monitored Move"},
    {"id": "MOV-003", "name": "Traveller C", "route": "DXB → SIN", "airport": "SIN", "city": "Singapore", "country": "Singapore", "lat": 1.3644, "lon": 103.9915, "date_range": "13-15 May", "status": "Active", "record_type": "Monitored Move"},
    {"id": "MOV-004", "name": "Traveller D", "route": "LHR → MAD", "airport": "MAD", "city": "Madrid", "country": "Spain", "lat": 40.4983, "lon": -3.5676, "date_range": "13 May", "status": "Active", "record_type": "Monitored Move"},
]

MIDB_POINTS = [
    {"id": "MIDB-AIR-001", "name": "✈ Heathrow Airport", "type": "Airport", "city": "London", "country": "United Kingdom", "lat": 51.4700, "lon": -0.4543},
    {"id": "MIDB-AIR-002", "name": "✈ Istanbul Airport", "type": "Airport", "city": "Istanbul", "country": "Türkiye", "lat": 41.2753, "lon": 28.7519},
    {"id": "MIDB-AIR-003", "name": "✈ Jomo Kenyatta International Airport", "type": "Airport", "city": "Nairobi", "country": "Kenya", "lat": -1.3192, "lon": 36.9278},
    {"id": "MIDB-AIR-004", "name": "✈ Changi Airport", "type": "Airport", "city": "Singapore", "country": "Singapore", "lat": 1.3644, "lon": 103.9915},
    {"id": "MIDB-AIR-005", "name": "✈ Madrid Barajas Airport", "type": "Airport", "city": "Madrid", "country": "Spain", "lat": 40.4983, "lon": -3.5676},
    {"id": "MIDB-DIP-001", "name": "▣ British Embassy Nairobi", "type": "Diplomatic Outpost", "city": "Nairobi", "country": "Kenya", "lat": -1.2304, "lon": 36.8135},
    {"id": "MIDB-DIP-002", "name": "▣ US Embassy London", "type": "Diplomatic Outpost", "city": "London", "country": "United Kingdom", "lat": 51.4816, "lon": -0.1271},
    {"id": "MIDB-PORT-001", "name": "⚓ Port of Singapore", "type": "Port", "city": "Singapore", "country": "Singapore", "lat": 1.2644, "lon": 103.8222},
    {"id": "MIDB-PORT-002", "name": "⚓ Port of Mombasa", "type": "Port", "city": "Mombasa", "country": "Kenya", "lat": -4.0435, "lon": 39.6682},
    {"id": "MIDB-PORT-003", "name": "⚓ Dover Port", "type": "Port", "city": "Dover", "country": "United Kingdom", "lat": 51.1251, "lon": 1.3338},
    {"id": "MIDB-BDR-001", "name": "◇ Turkey-Bulgaria Border Crossing", "type": "Border Crossing", "city": "Kapıkule", "country": "Türkiye", "lat": 41.7167, "lon": 26.3500},
    {"id": "MIDB-BDR-002", "name": "◇ Kenya-Tanzania Border Crossing", "type": "Border Crossing", "city": "Namanga", "country": "Kenya", "lat": -2.5439, "lon": 36.7906},
    {"id": "MIDB-HOS-001", "name": "✚ St Thomas' Hospital", "type": "Hospital", "city": "London", "country": "United Kingdom", "lat": 51.4980, "lon": -0.1187},
    {"id": "MIDB-HOS-002", "name": "✚ Aga Khan University Hospital", "type": "Hospital", "city": "Nairobi", "country": "Kenya", "lat": -1.2625, "lon": 36.8172},
]

EVENTS = [
    {"id": "EVT-2401", "title": "Civil unrest reported near business district", "city": "Nairobi", "country": "Kenya", "lat": -1.286389, "lon": 36.817223, "type": "Security", "origin": "Dataminr", "ai_classification": "Red", "operator_classification": "Red", "operator_status": "Published", "confidence": "High", "exposure": "Nairobi Office 650m away and 3 monitored moves in-country", "summary": "Multiple reports indicate escalating protest activity near a commercial district. One office location and monitored staff movements are within the likely impact area.", "ai_reason": "Security event within 1000m of a fixed office location and overlapping with monitored movement. AI recommends Red.", "published": True, "published_hours_ago": 1, "time": "11 mins ago", "record_type": "AI Event"},
    {"id": "EVT-2402", "title": "Airport disruption following security incident", "city": "Istanbul", "country": "Türkiye", "lat": 41.275278, "lon": 28.751944, "type": "Travel", "origin": "Dataminr", "ai_classification": "Amber", "operator_classification": None, "operator_status": "Awaiting operator review", "confidence": "Medium", "exposure": "2 travelling staff due through IST within affected window", "summary": "Departures are delayed following a security screening disruption. Two staff travellers are scheduled to transit through IST within the next 18 hours.", "ai_reason": "Travel disruption at an airport with travelling staff during the affected time window. AI recommends Amber.", "published": False, "published_hours_ago": None, "time": "24 mins ago", "record_type": "AI Event"},
    {"id": "EVT-2403", "title": "Severe weather warning issued", "city": "Manila", "country": "Philippines", "lat": 14.599512, "lon": 120.984222, "type": "Environmental", "origin": "Government weather alert", "ai_classification": "Amber", "operator_classification": None, "operator_status": "Awaiting operator review", "confidence": "High", "exposure": "Active temporary location in warning area", "summary": "A severe storm warning has been issued for the region. One temporary project location may experience travel disruption and localised flooding.", "ai_reason": "Environmental event overlaps with an active temporary location. AI recommends Amber pending operator validation.", "published": False, "published_hours_ago": None, "time": "48 mins ago", "record_type": "AI Event"},
    {"id": "EVT-2404", "title": "Large public gathering announced", "city": "Berlin", "country": "Germany", "lat": 52.520008, "lon": 13.404954, "type": "Civil Unrest", "origin": "Open media", "ai_classification": "Inform", "operator_classification": "Inform", "operator_status": "Published", "confidence": "Medium", "exposure": "No active corporate exposure identified", "summary": "A planned demonstration has been announced. No offices, temporary locations or travelling staff are currently assessed as exposed.", "ai_reason": "Relevant regional awareness but no current corporate exposure. AI recommends Inform.", "published": True, "published_hours_ago": 9, "time": "1 hr ago", "record_type": "AI Event"},
    {"id": "OP-2001", "title": "Office report: access road blocked", "city": "Dubai", "country": "United Arab Emirates", "lat": 25.2048, "lon": 55.2708, "type": "Operator Generated", "origin": "Office phone report", "ai_classification": "Amber", "operator_classification": None, "operator_status": "Awaiting operator review", "confidence": "Medium", "exposure": "Dubai Office access road reportedly blocked", "summary": "Local office has reported access disruption near the site entrance. Cause currently unconfirmed.", "ai_reason": "Internal office-originated report is relevant to fixed exposure and requires operator assessment.", "published": False, "published_hours_ago": None, "time": "16 mins ago", "record_type": "Operator Event"},
    {"id": "INT-1001", "title": "Staff alert triggered", "city": "Singapore", "country": "Singapore", "lat": 1.3521, "lon": 103.8198, "type": "Staff Alert", "origin": "Internal staff alert", "ai_classification": "Red", "operator_classification": None, "operator_status": "Immediate operator action", "confidence": "High", "exposure": "Internal alert from travelling staff near Singapore Office", "summary": "A travelling staff member has activated an emergency alert. Location places them near the Singapore office district.", "ai_reason": "Internal staff alert is inherently relevant and should be treated as immediate action pending operator contact.", "published": False, "published_hours_ago": None, "time": "3 mins ago", "record_type": "Operator Event"},
]

df_events = pd.DataFrame(EVENTS)
df_offices = pd.DataFrame(OFFICES)
df_temp = pd.DataFrame(TEMPORARY_LOCATIONS)
df_travel = pd.DataFrame(TRAVELLING_STAFF)
df_midb = pd.DataFrame(MIDB_POINTS)

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 16% 12%, rgba(56,189,248,.18), transparent 28%),
        radial-gradient(circle at 84% 8%, rgba(59,130,246,.12), transparent 28%),
        linear-gradient(135deg, #020617, #061326 60%, #000814);
    color: #e2e8f0;
}
.block-container { padding-top: 1.1rem; }
.hero {
    border: 1px solid rgba(56,189,248,.26);
    border-radius: 28px;
    padding: 26px;
    background: linear-gradient(135deg, rgba(15,23,42,.92), rgba(2,6,23,.86));
    box-shadow: 0 0 42px rgba(56,189,248,.25);
    margin-bottom: 18px;
}
.hero-kicker { color: #67e8f9; text-transform: uppercase; letter-spacing: .28em; font-size: 12px; font-weight: 700; }
.hero-title { color: white; font-size: 44px; font-weight: 800; line-height: 1.05; margin-top: 8px; }
.hero-sub { color: #94a3b8; font-size: 17px; margin-top: 10px; max-width: 980px; }
.metric-card {
    background: rgba(15,23,42,.78);
    border: 1px solid rgba(56,189,248,.20);
    border-radius: 18px;
    padding: 18px;
    min-height: 112px;
    transition: all .15s ease;
}
.metric-card:hover { border-color: #67e8f9; box-shadow: 0 0 34px rgba(56,189,248,.26); }
.metric-label { color: #94a3b8; font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; }
.metric-value { color: white; font-size: 30px; font-weight: 800; margin-top: 6px; }
.metric-sub { color: #94a3b8; font-size: 13px; margin-top: 8px; }
.info-dot {
    display: inline-flex; align-items: center; justify-content: center;
    width: 18px; height: 18px; border-radius: 999px;
    border: 1px solid #38bdf8; color: #67e8f9;
    font-size: 11px; margin-left: 6px; cursor: help;
}
.ticker { overflow: hidden; white-space: nowrap; border: 1px solid rgba(56,189,248,.2); background: rgba(2,6,23,.72); border-radius: 18px; margin: 10px 0 18px 0; }
.ticker-track { display: inline-block; padding: 12px 0; animation: ticker 32s linear infinite; }
.ticker span { color: #cbd5e1; margin-right: 42px; font-size: 14px; }
@keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
.status-pill { border-radius: 999px; padding: 4px 10px; font-size: 12px; font-weight: 800; border: 1px solid rgba(255,255,255,.22); }
.red { color: #fecaca; background: rgba(239,68,68,.2); border-color: rgba(239,68,68,.55); }
.amber { color: #fde68a; background: rgba(245,158,11,.2); border-color: rgba(245,158,11,.55); }
.inform { color: #bfdbfe; background: rgba(59,130,246,.22); border-color: rgba(59,130,246,.55); }
.discard { color: #cbd5e1; background: rgba(100,116,139,.2); border-color: rgba(100,116,139,.55); }
.email-box {
    background: rgba(2,6,23,.65);
    border: 1px solid rgba(56,189,248,.22);
    border-radius: 14px;
    padding: 14px;
    color: #cbd5e1;
    font-size: 13px;
    white-space: pre-wrap;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Helpers
# -----------------------------
def metric_card(label, value, sub, help_text=""):
    safe_help = help_text.replace('"', '&quot;')
    info = f"<span class='info-dot' title=\"{safe_help}\">i</span>" if help_text else ""
    st.markdown(f"""
        <div class="metric-card" title="{safe_help}">
            <div class="metric-label">{label}{info}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{sub}</div>
        </div>
    """, unsafe_allow_html=True)

def badge(value):
    css = {"Red": "red", "Amber": "amber", "Inform": "inform", "Discard": "discard", None: "inform"}.get(value, "inform")
    label = value if value else "Pending"
    return f"<span class='status-pill {css}'>{label}</span>"

def add_trace(fig, df, name, colour, marker_symbol, size=12, label_prefix=""):
    if df.empty:
        return
    fig.add_trace(go.Scattergeo(
        lon=df["lon"], lat=df["lat"],
        text=label_prefix + df["name"] + "<br>" + df["city"] + ", " + df["country"],
        mode="markers+text",
        name=name,
        marker=dict(size=size, color=colour, symbol=marker_symbol, line=dict(width=1, color="white"), opacity=0.9),
        textposition="top center",
        textfont=dict(size=11, color=colour),
        hovertemplate="<b>%{text}</b><extra>" + name + "</extra>",
    ))

def make_map(show_active_risks=True, show_offices=True, show_temporary=True, show_travelling=True,
             show_airports=True, show_diplomatic=True, show_borders=True, show_ports=True, show_hospitals=False,
             pulse_risks=False, pulse_moves=False, monitor_only=False, selected_point=None, height=560):
    fig = go.Figure()
    event_df = df_events.copy()

    if monitor_only:
        event_df = event_df[event_df["published"] == False]
    else:
        event_df = event_df[(event_df["published"] == True) & (event_df["operator_classification"] != "Discard")]

    if show_active_risks and not event_df.empty:
        display_class = event_df["operator_classification"].fillna(event_df["ai_classification"])
        colours = display_class.map({"Red": "#ef4444", "Amber": "#f59e0b", "Inform": "#3b82f6", "Discard": "#64748b"})
        sizes = display_class.map({"Red": 24, "Amber": 20, "Inform": 16, "Discard": 12})
        if pulse_risks:
            fig.add_trace(go.Scattergeo(
                lon=event_df["lon"], lat=event_df["lat"], text=event_df["title"], mode="markers", name="Risk pulse",
                marker=dict(size=sizes + 30, color="rgba(0,0,0,0)", line=dict(width=3, color="#67e8f9"), opacity=0.42),
                hoverinfo="skip",
            ))
        fig.add_trace(go.Scattergeo(
            lon=event_df["lon"], lat=event_df["lat"],
            text=event_df["id"] + " · " + event_df["title"] + "<br>" + event_df["city"] + ", " + event_df["country"] + "<br>" + event_df["exposure"],
            mode="markers",
            name="Active / workflow risks",
            marker=dict(size=sizes, color=colours, symbol="circle", line=dict(width=1, color="white"), opacity=0.95),
            hovertemplate="<b>%{text}</b><extra>Risk / Event</extra>",
        ))

    if show_offices:
        add_trace(fig, df_offices, "🏢 Offices", "#38bdf8", "square", size=13, label_prefix="🏢 ")

    if show_temporary:
        active_temp = df_temp[df_temp["status"] == "Active"].copy()
        archived_temp = df_temp[df_temp["status"] == "Archived"].copy()
        add_trace(fig, active_temp, "◆ Temporary locations: active", "#22c55e", "diamond", size=13, label_prefix="◆ ")
        add_trace(fig, archived_temp, "◇ Temporary locations: archived", "#64748b", "diamond-open", size=11, label_prefix="◇ ")

    if show_travelling:
        if pulse_moves:
            fig.add_trace(go.Scattergeo(
                lon=df_travel["lon"], lat=df_travel["lat"], text=df_travel["name"], mode="markers", name="Move pulse",
                marker=dict(size=34, color="rgba(0,0,0,0)", line=dict(width=3, color="#a855f7"), opacity=0.42),
                hoverinfo="skip",
            ))
        add_trace(fig, df_travel, "▲ Travelling staff", "#a855f7", "triangle-up", size=14, label_prefix="▲ ")

    if show_airports:
        add_trace(fig, df_midb[df_midb["type"] == "Airport"], "✈ Airports", "#fb923c", "triangle-right", size=12)
    if show_diplomatic:
        add_trace(fig, df_midb[df_midb["type"] == "Diplomatic Outpost"], "▣ Diplomatic outposts", "#e879f9", "star", size=13)
    if show_borders:
        add_trace(fig, df_midb[df_midb["type"] == "Border Crossing"], "◇ Border crossings", "#facc15", "cross", size=12)
    if show_ports:
        add_trace(fig, df_midb[df_midb["type"] == "Port"], "⚓ Ports", "#06b6d4", "circle-open", size=13)
    if show_hospitals:
        add_trace(fig, df_midb[df_midb["type"] == "Hospital"], "✚ Hospitals", "#fb7185", "cross", size=12)

    if selected_point:
        fig.add_trace(go.Scattergeo(
            lon=[selected_point["lon"]], lat=[selected_point["lat"]],
            text=[selected_point.get("label", "Selected point")],
            mode="markers",
            name="Selected record",
            marker=dict(size=34, color="rgba(0,0,0,0)", line=dict(width=4, color="#ffffff"), symbol="circle"),
            hovertemplate="<b>%{text}</b><extra>Selected</extra>",
        ))

    center = dict(lat=18, lon=20)
    projection_scale = 1.05
    if selected_point:
        center = dict(lat=selected_point["lat"], lon=selected_point["lon"])
        projection_scale = 3.8

    fig.update_geos(
        projection_type="natural earth",
        center=center,
        projection_scale=projection_scale,
        showland=True,
        landcolor="#0f172a",
        showocean=True,
        oceancolor="#020617",
        showcountries=True,
        countrycolor="#334155",
        showcoastlines=True,
        coastlinecolor="#475569",
        bgcolor="rgba(0,0,0,0)"
    )
    fig.update_layout(
        height=height,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=-0.03, xanchor="center", x=0.5, font=dict(color="#cbd5e1")),
        font=dict(color="#e2e8f0"),
    )
    st.plotly_chart(fig, use_container_width=True)

def google_maps_link(lat, lon):
    return f"https://www.google.com/maps?q={lat},{lon}"

def build_email(selected, final_classification, notes):
    map_link = google_maps_link(selected["lat"], selected["lon"])
    subject = f"Overwatch Advisory: {final_classification} - {selected['title']} - {selected['country']}"
    body = f"""Overwatch Advisory

Classification: {final_classification}
Event: {selected['title']}
Location: {selected['city']}, {selected['country']}
Time: {selected['time']}
Origin: {selected['origin']}
Confidence: {selected['confidence']}

Risk summary:
{selected['summary']}

Exposure assessment:
{selected['exposure']}

Operator notes:
{notes if notes else 'No additional operator notes added.'}

Map:
{map_link}

Recommended handling:
Review local exposure, contact affected staff or office leads where appropriate, and continue monitoring for updates.

Generated from Overwatch Monitor prototype.
"""
    mailto = f"mailto:dom-lowe@live.com?subject={quote(subject)}&body={quote(body)}"
    return subject, body, mailto, map_link

def selectable_table(label, df, columns):
    selection = st.dataframe(
        df[columns],
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        key=label,
    )
    try:
        rows = selection.selection.rows
        if rows:
            return df.iloc[rows[0]].to_dict()
    except Exception:
        return None
    return None

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🛡️ Overwatch")
st.sidebar.caption("Prototype v8: Monitor layout + selectable records")

page = st.sidebar.radio("Environment", ["Overwatch Pulse", "Overwatch Monitor", "Overwatch Risk"])

st.sidebar.divider()
with st.sidebar.expander("Corporate exposure layers", expanded=True):
    show_offices = st.checkbox("Show office locations", value=True)
    show_temporary = st.checkbox("Show temporary locations", value=True)
    show_travelling = st.checkbox("Show travelling staff locations", value=True)

with st.sidebar.expander("MIDB reference layers", expanded=True):
    show_airports = st.checkbox("Show airports", value=True)
    show_diplomatic = st.checkbox("Show diplomatic outposts", value=True)
    show_borders = st.checkbox("Show border crossings", value=True)
    show_ports = st.checkbox("Show ports", value=True)
    show_hospitals = st.checkbox("Show hospitals", value=False)

with st.sidebar.popover("Classification key"):
    st.write("🔴 **Red**: action required")
    st.write("🟠 **Amber**: monitor / assess")
    st.write("🔵 **Inform**: awareness only")
    st.write("⚫ **Discard**: no operational relevance")

published_df = df_events[(df_events["published"] == True) & (df_events["operator_classification"] != "Discard")].copy()
monitor_df = df_events[df_events["published"] == False].copy()
last_72_df = published_df[published_df["published_hours_ago"] <= 72].copy()

# -----------------------------
# Pulse
# -----------------------------
if page == "Overwatch Pulse":
    st.markdown("""
        <div class="hero">
            <div class="hero-kicker">Overwatch Pulse</div>
            <div class="hero-title">Live Common Intelligence Picture</div>
            <div class="hero-sub">Operator-approved risks, monitored moves and validated updates for customer, executive and traveller awareness.</div>
        </div>
    """, unsafe_allow_html=True)

    ticker_items = [f"{item['operator_classification']} · {item['country']} · {item['title']}" for item in last_72_df.to_dict("records")]
    ticker_html = "<span>LIVE RISKS</span>" + "".join([f"<span>{x}</span>" for x in ticker_items])
    st.markdown(f"<div class='ticker'><div class='ticker-track'>{ticker_html}</div></div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Active risks", str(len(published_df)), "Published operator-approved risks", "Operator-approved live risks currently displayed on Overwatch Pulse.")
    with c2:
        metric_card("Monitored moves", str(len(df_travel)), "Journeys being monitored", "Travelling staff locations and monitored journeys being checked against the live risk picture.")
    with c3:
        red_count = (last_72_df["operator_classification"] == "Red").sum()
        amber_count = (last_72_df["operator_classification"] == "Amber").sum()
        inform_count = (last_72_df["operator_classification"] == "Inform").sum()
        metric_card("Published updates", str(len(last_72_df)), f"72 hrs: {red_count} Red · {amber_count} Amber · {inform_count} Inform", "Operator-approved updates published in the last 72 hours, excluding discarded items.")

    p1, p2 = st.columns([0.5, 0.5])
    with p1:
        pulse_risks = st.toggle("Pulse active risks", value=True)
    with p2:
        pulse_moves = st.toggle("Pulse monitored moves", value=False)

    st.subheader("Global operational map")
    make_map(True, show_offices, show_temporary, show_travelling, show_airports, show_diplomatic, show_borders, show_ports, show_hospitals, pulse_risks, pulse_moves)

    st.subheader("Published updates: last 72 hours")
    tab_red, tab_amber, tab_inform = st.tabs(["Red", "Amber", "Inform"])

    def render_updates(classification):
        data = last_72_df[last_72_df["operator_classification"] == classification]
        if data.empty:
            st.info(f"No {classification} updates in the last 72 hours.")
        for item in data.to_dict("records"):
            with st.container(border=True):
                c1, c2 = st.columns([0.78, 0.22])
                with c1:
                    st.markdown(f"### {item['title']}")
                    st.write(f"{item['city']}, {item['country']} · {item['time']}")
                    st.write(item["summary"])
                with c2:
                    st.markdown(badge(item["operator_classification"]), unsafe_allow_html=True)
                    st.write(item["operator_status"])

    with tab_red:
        render_updates("Red")
    with tab_amber:
        render_updates("Amber")
    with tab_inform:
        render_updates("Inform")

# -----------------------------
# Monitor
# -----------------------------
elif page == "Overwatch Monitor":
    st.title("Overwatch Monitor")
    st.caption("Operator workflow for AI-generated external events and internally generated reports.")

    top1, top2 = st.columns(2)
    with top1:
        metric_card("Workflow events", str(len(monitor_df)), "Awaiting decision", "AI-generated and operator-generated events awaiting operator review.")
    with top2:
        metric_card("Internal alerts", str((monitor_df["origin"] == "Internal staff alert").sum()), "Immediate action", "Staff alerts or internal corporate incidents.")

    left, centre, right = st.columns([1.0, 1.45, 0.85])

    with left:
        st.subheader("Events workflow")
        selected_id = st.radio(
            "Select event",
            monitor_df["id"].tolist(),
            format_func=lambda x: f"{x} · {monitor_df.loc[monitor_df['id'] == x, 'ai_classification'].iloc[0]} · {monitor_df.loc[monitor_df['id'] == x, 'city'].iloc[0]}",
            label_visibility="collapsed",
        )
        selected = df_events[df_events["id"] == selected_id].iloc[0].to_dict()

        st.divider()
        st.subheader("Selected event")
        st.markdown(f"### {selected['title']}")
        st.markdown(badge(selected["ai_classification"]), unsafe_allow_html=True)
        st.write(f"**Origin:** {selected['origin']}")
        st.write(f"**Location:** {selected['city']}, {selected['country']}")
        st.write(f"**Confidence:** {selected['confidence']}")
        st.write(f"**Exposure match:** {selected['exposure']}")
        st.write(selected["summary"])

        with st.expander("Internal AI rationale", expanded=True):
            st.write(selected["ai_reason"])

    selected_point = {
        "lat": selected["lat"],
        "lon": selected["lon"],
        "label": f"{selected['id']} · {selected['title']}"
    }

    with centre:
        st.subheader("Operational map")
        make_map(
            True,
            show_offices,
            show_temporary,
            show_travelling,
            show_airports,
            show_diplomatic,
            show_borders,
            show_ports,
            show_hospitals,
            pulse_risks=False,
            pulse_moves=False,
            monitor_only=True,
            selected_point=selected_point,
        )

        st.subheader("Operational records")
        t_all, t_temp, t_moves = st.tabs(["All events", "Temporary locations", "Monitored moves"])

        table_selected = None

        with t_all:
            st.caption("AI-generated events and operator-generated events.")
            table_selected = selectable_table(
                "all_events_table",
                df_events,
                ["id", "record_type", "time", "origin", "title", "country", "ai_classification", "operator_status", "exposure"],
            )

        with t_temp:
            st.caption("Active and archived temporary locations.")
            temp_selected = selectable_table(
                "temp_locations_table",
                df_temp,
                ["id", "name", "status", "city", "country", "start_date", "end_date", "lat", "lon"],
            )
            if temp_selected:
                table_selected = {"lat": temp_selected["lat"], "lon": temp_selected["lon"], "label": temp_selected["name"]}

        with t_moves:
            st.caption("Travelling staff and monitored journeys.")
            move_selected = selectable_table(
                "monitored_moves_table",
                df_travel,
                ["id", "name", "route", "airport", "city", "country", "date_range", "status", "lat", "lon"],
            )
            if move_selected:
                table_selected = {"lat": move_selected["lat"], "lon": move_selected["lon"], "label": move_selected["name"]}

        if table_selected:
            st.info("Record selected. The map will centre on the selected point after the next rerun. Use the row selection again if needed.")

    with right:
        st.subheader("Operator decision")
        final_classification = st.selectbox("Final classification", ["Red", "Amber", "Inform", "Discard"], index=["Red", "Amber", "Inform", "Discard"].index(selected["ai_classification"]))
        notes = st.text_area("Operator notes", placeholder="Add source validation, context or override rationale...")

        b1, b2, b3 = st.columns(3)
        with b1:
            st.button("Publish", type="primary")
        with b2:
            st.button("Monitor")
        with b3:
            st.button("Discard")

        st.subheader("Draft distribution email")
        subject, body, mailto, map_link = build_email(selected, final_classification, notes)

        st.write("To: **dom-lowe@live.com**")
        st.write(f"Subject: `{subject}`")
        st.markdown(f"[Open small event map]({map_link})")
        st.markdown(f"[Open draft email in mail app]({mailto})")

        with st.expander("Preview email body"):
            st.markdown(f"<div class='email-box'>{body}</div>", unsafe_allow_html=True)

        st.caption("Prototype note: this creates a mailto draft. A live system would use Microsoft Graph or an internal email service.")

    st.divider()
    st.subheader("Temporary location management")
    temp_tab1, temp_tab2, temp_tab3 = st.tabs(["Active", "Archived", "Add / Edit"])
    with temp_tab1:
        st.dataframe(df_temp[df_temp["status"] == "Active"][["id", "name", "city", "country", "start_date", "end_date", "lat", "lon"]], use_container_width=True, hide_index=True)
    with temp_tab2:
        st.dataframe(df_temp[df_temp["status"] == "Archived"][["id", "name", "city", "country", "start_date", "end_date", "lat", "lon"]], use_container_width=True, hide_index=True)
    with temp_tab3:
        with st.form("temporary_location_form"):
            st.write("Dummy form. In production this would update the corporate exposure database.")
            loc_name = st.text_input("Temporary location name")
            city = st.text_input("City")
            country = st.text_input("Country")
            c1, c2 = st.columns(2)
            with c1:
                start = st.date_input("Start date", value=date.today())
                lat = st.number_input("Latitude", value=0.0, format="%.6f")
            with c2:
                end = st.date_input("End date", value=date.today())
                lon = st.number_input("Longitude", value=0.0, format="%.6f")
            status = st.selectbox("Status", ["Active", "Archived"])
            if st.form_submit_button("Save temporary location"):
                st.success("Temporary location saved to dummy model.")

# -----------------------------
# Risk
# -----------------------------
else:
    st.title("Overwatch Risk")
    st.caption("Strategic risk, trend and mitigation workspace.")

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Reviews due", "3", "Next 30 days", "Scheduled country, office or route reviews due.")
    with c2:
        metric_card("Hotspots", "8", "Recurring exposure locations", "Places where incidents repeatedly overlap with corporate exposure.")
    with c3:
        metric_card("Open mitigations", "14", "Outstanding recommendations", "Risk reduction actions not yet completed.")

    st.subheader("Operational data feeding risk")
    st.dataframe(df_events[["id", "country", "city", "type", "origin", "ai_classification", "operator_classification", "confidence", "operator_status", "exposure"]], use_container_width=True, hide_index=True)

    st.subheader("MIDB reference coverage")
    st.dataframe(df_midb[["id", "name", "type", "city", "country", "lat", "lon"]], use_container_width=True, hide_index=True)
