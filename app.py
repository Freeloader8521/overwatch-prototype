
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date

st.set_page_config(
    page_title="Overwatch Prototype v6",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Dummy Data
# -----------------------------
OFFICES = [
    {"name": "London Office", "city": "London", "country": "United Kingdom", "lat": 51.5072, "lon": -0.1276, "layer": "Office"},
    {"name": "Nairobi Office", "city": "Nairobi", "country": "Kenya", "lat": -1.2864, "lon": 36.8172, "layer": "Office"},
    {"name": "Singapore Office", "city": "Singapore", "country": "Singapore", "lat": 1.3521, "lon": 103.8198, "layer": "Office"},
    {"name": "Washington DC Office", "city": "Washington DC", "country": "United States", "lat": 38.9072, "lon": -77.0369, "layer": "Office"},
    {"name": "Dubai Office", "city": "Dubai", "country": "United Arab Emirates", "lat": 25.2048, "lon": 55.2708, "layer": "Office"},
]

TEMPORARY_LOCATIONS = [
    {
        "name": "Manila Project Site",
        "city": "Manila",
        "country": "Philippines",
        "lat": 14.5995,
        "lon": 120.9842,
        "status": "Active",
        "start_date": "2026-05-01",
        "end_date": "2026-06-30",
        "layer": "Temporary Location",
    },
    {
        "name": "Lagos Election Support Team",
        "city": "Lagos",
        "country": "Nigeria",
        "lat": 6.5244,
        "lon": 3.3792,
        "status": "Archived",
        "start_date": "2026-02-10",
        "end_date": "2026-03-02",
        "layer": "Temporary Location",
    },
    {
        "name": "Lima Field Visit",
        "city": "Lima",
        "country": "Peru",
        "lat": -12.0464,
        "lon": -77.0428,
        "status": "Active",
        "start_date": "2026-05-10",
        "end_date": "2026-05-19",
        "layer": "Temporary Location",
    },
]

TRAVELLING_STAFF = [
    {"name": "Traveller A", "route": "LHR → IST → NBO", "airport": "NBO", "city": "Nairobi", "country": "Kenya", "lat": -1.3192, "lon": 36.9278, "date_range": "12-14 May", "layer": "Travelling Staff"},
    {"name": "Traveller B", "route": "JFK → LHR", "airport": "LHR", "city": "London", "country": "United Kingdom", "lat": 51.4700, "lon": -0.4543, "date_range": "13 May", "layer": "Travelling Staff"},
    {"name": "Traveller C", "route": "DXB → SIN", "airport": "SIN", "city": "Singapore", "country": "Singapore", "lat": 1.3644, "lon": 103.9915, "date_range": "13-15 May", "layer": "Travelling Staff"},
    {"name": "Traveller D", "route": "LHR → MAD", "airport": "MAD", "city": "Madrid", "country": "Spain", "lat": 40.4983, "lon": -3.5676, "date_range": "13 May", "layer": "Travelling Staff"},
]

MIDB_POINTS = [
    {"name": "Heathrow Airport", "type": "Airport", "city": "London", "country": "United Kingdom", "lat": 51.4700, "lon": -0.4543},
    {"name": "Istanbul Airport", "type": "Airport", "city": "Istanbul", "country": "Türkiye", "lat": 41.2753, "lon": 28.7519},
    {"name": "Jomo Kenyatta International Airport", "type": "Airport", "city": "Nairobi", "country": "Kenya", "lat": -1.3192, "lon": 36.9278},
    {"name": "Changi Airport", "type": "Airport", "city": "Singapore", "country": "Singapore", "lat": 1.3644, "lon": 103.9915},
    {"name": "Madrid Barajas Airport", "type": "Airport", "city": "Madrid", "country": "Spain", "lat": 40.4983, "lon": -3.5676},
    {"name": "British Embassy Nairobi", "type": "Diplomatic Outpost", "city": "Nairobi", "country": "Kenya", "lat": -1.2304, "lon": 36.8135},
    {"name": "US Embassy London", "type": "Diplomatic Outpost", "city": "London", "country": "United Kingdom", "lat": 51.4816, "lon": -0.1271},
    {"name": "Port of Singapore", "type": "Port", "city": "Singapore", "country": "Singapore", "lat": 1.2644, "lon": 103.8222},
    {"name": "Port of Mombasa", "type": "Port", "city": "Mombasa", "country": "Kenya", "lat": -4.0435, "lon": 39.6682},
    {"name": "Dover Port", "type": "Port", "city": "Dover", "country": "United Kingdom", "lat": 51.1251, "lon": 1.3338},
    {"name": "Turkey-Bulgaria Border Crossing", "type": "Border Crossing", "city": "Kapıkule", "country": "Türkiye", "lat": 41.7167, "lon": 26.3500},
    {"name": "Kenya-Tanzania Border Crossing", "type": "Border Crossing", "city": "Namanga", "country": "Kenya", "lat": -2.5439, "lon": 36.7906},
    {"name": "St Thomas' Hospital", "type": "Hospital", "city": "London", "country": "United Kingdom", "lat": 51.4980, "lon": -0.1187},
    {"name": "Aga Khan University Hospital", "type": "Hospital", "city": "Nairobi", "country": "Kenya", "lat": -1.2625, "lon": 36.8172},
]

EVENTS = [
    {
        "id": "EVT-2401",
        "title": "Civil unrest reported near business district",
        "city": "Nairobi",
        "country": "Kenya",
        "lat": -1.286389,
        "lon": 36.817223,
        "type": "Security",
        "origin": "Dataminr",
        "ai_classification": "Red",
        "operator_classification": "Red",
        "operator_status": "Published",
        "confidence": "High",
        "exposure": "Nairobi Office 650m away and 3 monitored moves in-country",
        "summary": "Multiple reports indicate escalating protest activity near a commercial district. One office location and monitored staff movements are within the likely impact area.",
        "ai_reason": "Security event within 1000m of a fixed office location and overlapping with monitored movement. AI recommends Red.",
        "published": True,
        "published_hours_ago": 1,
        "time": "11 mins ago",
    },
    {
        "id": "EVT-2402",
        "title": "Airport disruption following security incident",
        "city": "Istanbul",
        "country": "Türkiye",
        "lat": 41.275278,
        "lon": 28.751944,
        "type": "Travel",
        "origin": "Dataminr",
        "ai_classification": "Amber",
        "operator_classification": None,
        "operator_status": "Awaiting operator review",
        "confidence": "Medium",
        "exposure": "2 travelling staff due through IST within affected window",
        "summary": "Departures are delayed following a security screening disruption. Two staff travellers are scheduled to transit through IST within the next 18 hours.",
        "ai_reason": "Travel disruption at an airport with travelling staff during the affected time window. AI recommends Amber.",
        "published": False,
        "published_hours_ago": None,
        "time": "24 mins ago",
    },
    {
        "id": "EVT-2403",
        "title": "Severe weather warning issued",
        "city": "Manila",
        "country": "Philippines",
        "lat": 14.599512,
        "lon": 120.984222,
        "type": "Environmental",
        "origin": "Government weather alert",
        "ai_classification": "Amber",
        "operator_classification": None,
        "operator_status": "Awaiting operator review",
        "confidence": "High",
        "exposure": "Active temporary location in warning area",
        "summary": "A severe storm warning has been issued for the region. One temporary project location may experience travel disruption and localised flooding.",
        "ai_reason": "Environmental event overlaps with an active temporary location. AI recommends Amber pending operator validation.",
        "published": False,
        "published_hours_ago": None,
        "time": "48 mins ago",
    },
    {
        "id": "EVT-2404",
        "title": "Large public gathering announced",
        "city": "Berlin",
        "country": "Germany",
        "lat": 52.520008,
        "lon": 13.404954,
        "type": "Civil Unrest",
        "origin": "Open media",
        "ai_classification": "Inform",
        "operator_classification": "Inform",
        "operator_status": "Published",
        "confidence": "Medium",
        "exposure": "No active corporate exposure identified",
        "summary": "A planned demonstration has been announced. No offices, temporary locations or travelling staff are currently assessed as exposed.",
        "ai_reason": "Relevant regional awareness but no current corporate exposure. AI recommends Inform.",
        "published": True,
        "published_hours_ago": 9,
        "time": "1 hr ago",
    },
    {
        "id": "INT-1001",
        "title": "Staff alert triggered",
        "city": "Singapore",
        "country": "Singapore",
        "lat": 1.3521,
        "lon": 103.8198,
        "type": "Staff Alert",
        "origin": "Internal staff alert",
        "ai_classification": "Red",
        "operator_classification": None,
        "operator_status": "Immediate operator action",
        "confidence": "High",
        "exposure": "Internal alert from travelling staff near Singapore Office",
        "summary": "A travelling staff member has activated an emergency alert. Location places them near the Singapore office district.",
        "ai_reason": "Internal staff alert is inherently relevant and should be treated as immediate action pending operator contact.",
        "published": False,
        "published_hours_ago": None,
        "time": "3 mins ago",
    },
]

RISK_REPORTS = [
    {"title": "Kenya Six-Month Security Review", "status": "Due in 12 days", "detail": "Civil unrest, transport disruption and office proximity events trending upwards."},
    {"title": "Türkiye Travel Resilience Assessment", "status": "Draft", "detail": "Airport disruption and transit exposure remain the primary traveller risk drivers."},
    {"title": "Philippines Severe Weather Mitigation Plan", "status": "In Review", "detail": "Temporary location readiness and flooding procedures require validation."},
]

df_events = pd.DataFrame(EVENTS)
df_offices = pd.DataFrame(OFFICES)
df_temp = pd.DataFrame(TEMPORARY_LOCATIONS)
df_travel = pd.DataFrame(TRAVELLING_STAFF)
df_midb = pd.DataFrame(MIDB_POINTS)

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
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
        background:
            linear-gradient(135deg, rgba(15,23,42,.92), rgba(2,6,23,.86)),
            radial-gradient(circle at 70% 30%, rgba(56,189,248,.22), transparent 35%);
        box-shadow: 0 0 42px rgba(56,189,248,.25);
        margin-bottom: 18px;
    }
    .hero-kicker {
        color: #67e8f9;
        text-transform: uppercase;
        letter-spacing: .28em;
        font-size: 12px;
        font-weight: 700;
    }
    .hero-title {
        color: white;
        font-size: 44px;
        font-weight: 800;
        line-height: 1.05;
        margin-top: 8px;
    }
    .hero-sub {
        color: #94a3b8;
        font-size: 17px;
        margin-top: 10px;
        max-width: 980px;
    }
    .metric-card {
        background: rgba(15,23,42,.78);
        border: 1px solid rgba(56,189,248,.20);
        border-radius: 18px;
        padding: 18px;
        min-height: 118px;
        transition: all .15s ease;
        box-shadow: 0 0 28px rgba(14,165,233,.08);
    }
    .metric-card:hover {
        border-color: #67e8f9;
        box-shadow: 0 0 0 1px rgba(103,232,249,.35), 0 0 34px rgba(56,189,248,.26);
    }
    .metric-label {
        color: #94a3b8;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .metric-value {
        color: white;
        font-size: 30px;
        font-weight: 800;
        margin-top: 6px;
    }
    .metric-sub {
        color: #94a3b8;
        font-size: 13px;
        margin-top: 8px;
    }
    .info-dot {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 18px;
        height: 18px;
        border-radius: 999px;
        border: 1px solid #38bdf8;
        color: #67e8f9;
        font-size: 11px;
        margin-left: 6px;
        cursor: help;
    }
    .ticker {
        overflow: hidden;
        white-space: nowrap;
        border: 1px solid rgba(56,189,248,.2);
        background: rgba(2,6,23,.72);
        border-radius: 18px;
        box-shadow: 0 0 26px rgba(14,165,233,.12);
        margin: 10px 0 18px 0;
    }
    .ticker-track {
        display: inline-block;
        padding: 12px 0;
        animation: ticker 32s linear infinite;
    }
    .ticker span {
        color: #cbd5e1;
        margin-right: 42px;
        font-size: 14px;
    }
    @keyframes ticker {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    .status-pill {
        border-radius: 999px;
        padding: 4px 10px;
        font-size: 12px;
        font-weight: 800;
        border: 1px solid rgba(255,255,255,.22);
    }
    .red { color: #fecaca; background: rgba(239,68,68,.2); border-color: rgba(239,68,68,.55); }
    .amber { color: #fde68a; background: rgba(245,158,11,.2); border-color: rgba(245,158,11,.55); }
    .inform { color: #bfdbfe; background: rgba(59,130,246,.22); border-color: rgba(59,130,246,.55); }
    .discard { color: #cbd5e1; background: rgba(100,116,139,.2); border-color: rgba(100,116,139,.55); }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Helpers
# -----------------------------
def metric_card(label, value, sub, help_text=""):
    safe_help = help_text.replace('"', '&quot;')
    info = f"<span class='info-dot' title=\"{safe_help}\">i</span>" if help_text else ""
    st.markdown(
        f"""
        <div class="metric-card" title="{safe_help}">
            <div class="metric-label">{label}{info}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def badge(value):
    css = {
        "Red": "red",
        "Amber": "amber",
        "Inform": "inform",
        "Discard": "discard",
        None: "inform",
    }.get(value, "inform")
    label = value if value else "Pending"
    return f"<span class='status-pill {css}'>{label}</span>"

def add_trace(fig, df, name, colour, symbol, size=11, text_field="name"):
    if df.empty:
        return
    fig.add_trace(
        go.Scattergeo(
            lon=df["lon"],
            lat=df["lat"],
            text=df[text_field] + "<br>" + df["city"] + ", " + df["country"],
            mode="markers",
            name=name,
            marker=dict(
                size=size,
                color=colour,
                symbol=symbol,
                line=dict(width=1, color="white"),
                opacity=0.9,
            ),
            hovertemplate="<b>%{text}</b><extra>" + name + "</extra>",
        )
    )

def make_map(
    show_active_risks=True,
    show_offices=True,
    show_temporary=True,
    show_travelling=True,
    show_airports=True,
    show_diplomatic=True,
    show_borders=True,
    show_ports=True,
    show_hospitals=False,
    pulse_risks=False,
    pulse_moves=False,
    monitor_only=False,
):
    fig = go.Figure()

    event_df = df_events.copy()
    if monitor_only:
        event_df = event_df[event_df["published"] == False]
    else:
        event_df = event_df[(event_df["published"] == True) & (event_df["operator_classification"] != "Discard")]

    if show_active_risks and not event_df.empty:
        colours = event_df["operator_classification"].fillna(event_df["ai_classification"]).map({
            "Red": "#ef4444",
            "Amber": "#f59e0b",
            "Inform": "#3b82f6",
            "Discard": "#64748b",
        })
        sizes = event_df["operator_classification"].fillna(event_df["ai_classification"]).map({
            "Red": 22,
            "Amber": 18,
            "Inform": 14,
            "Discard": 10,
        })

        if pulse_risks:
            fig.add_trace(
                go.Scattergeo(
                    lon=event_df["lon"],
                    lat=event_df["lat"],
                    text=event_df["title"],
                    mode="markers",
                    name="Risk pulse",
                    marker=dict(
                        size=sizes + 28,
                        color="rgba(0,0,0,0)",
                        line=dict(width=3, color="#67e8f9"),
                        opacity=0.42,
                    ),
                    hoverinfo="skip",
                )
            )

        fig.add_trace(
            go.Scattergeo(
                lon=event_df["lon"],
                lat=event_df["lat"],
                text=event_df["title"] + "<br>" + event_df["city"] + ", " + event_df["country"] + "<br>" + event_df["exposure"],
                mode="markers",
                name="Active risks",
                marker=dict(
                    size=sizes,
                    color=colours,
                    symbol="circle",
                    line=dict(width=1, color="white"),
                    opacity=0.95,
                ),
                hovertemplate="<b>%{text}</b><extra>Active Risk</extra>",
            )
        )

    if show_offices:
        add_trace(fig, df_offices, "Office locations", "#38bdf8", "square", size=13)

    if show_temporary:
        temp = df_temp.copy()
        active = temp[temp["status"] == "Active"]
        archived = temp[temp["status"] == "Archived"]
        add_trace(fig, active, "Temporary locations: active", "#22c55e", "diamond", size=13)
        add_trace(fig, archived, "Temporary locations: archived", "#64748b", "diamond", size=10)

    if show_travelling:
        if pulse_moves:
            fig.add_trace(
                go.Scattergeo(
                    lon=df_travel["lon"],
                    lat=df_travel["lat"],
                    text=df_travel["name"],
                    mode="markers",
                    name="Monitored move pulse",
                    marker=dict(
                        size=34,
                        color="rgba(0,0,0,0)",
                        line=dict(width=3, color="#a855f7"),
                        opacity=0.42,
                    ),
                    hoverinfo="skip",
                )
            )
        add_trace(fig, df_travel, "Travelling staff locations", "#a855f7", "triangle-up", size=13, text_field="name")

    if not df_midb.empty:
        if show_airports:
            add_trace(fig, df_midb[df_midb["type"] == "Airport"], "MIDB: airports", "#f97316", "x", size=11)
        if show_diplomatic:
            add_trace(fig, df_midb[df_midb["type"] == "Diplomatic Outpost"], "MIDB: diplomatic outposts", "#e879f9", "star", size=12)
        if show_borders:
            add_trace(fig, df_midb[df_midb["type"] == "Border Crossing"], "MIDB: border crossings", "#facc15", "cross", size=11)
        if show_ports:
            add_trace(fig, df_midb[df_midb["type"] == "Port"], "MIDB: ports", "#06b6d4", "circle-open", size=11)
        if show_hospitals:
            add_trace(fig, df_midb[df_midb["type"] == "Hospital"], "MIDB: hospitals", "#fb7185", "cross", size=11)

    fig.update_geos(
        projection_type="natural earth",
        showland=True,
        landcolor="#0f172a",
        showocean=True,
        oceancolor="#020617",
        showcountries=True,
        countrycolor="#334155",
        showcoastlines=True,
        coastlinecolor="#475569",
        bgcolor="rgba(0,0,0,0)",
    )
    fig.update_layout(
        height=560,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.02,
            xanchor="center",
            x=0.5,
            font=dict(color="#cbd5e1"),
        ),
        font=dict(color="#e2e8f0"),
    )
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.title("🛡️ Overwatch")
st.sidebar.caption("Prototype v6: Plotly map + MIDB layers")

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
    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">Overwatch Pulse</div>
            <div class="hero-title">Live Common Intelligence Picture</div>
            <div class="hero-sub">
                Operator-approved risks, monitored moves and validated updates for customer, executive and traveller awareness.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    ticker_items = []
    for item in last_72_df.to_dict("records"):
        ticker_items.append(f"{item['operator_classification']} · {item['country']} · {item['title']}")
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
    make_map(
        show_active_risks=True,
        show_offices=show_offices,
        show_temporary=show_temporary,
        show_travelling=show_travelling,
        show_airports=show_airports,
        show_diplomatic=show_diplomatic,
        show_borders=show_borders,
        show_ports=show_ports,
        show_hospitals=show_hospitals,
        pulse_risks=pulse_risks,
        pulse_moves=pulse_moves,
    )

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
    st.caption("Operator workflow for AI-generated external events, internal incidents and temporary location management.")

    top1, top2, top3, top4 = st.columns(4)
    with top1:
        metric_card("Workflow events", str(len(monitor_df)), "Awaiting decision", "Events and internal incidents awaiting operator review.")
    with top2:
        metric_card("Internal alerts", str((monitor_df["origin"] == "Internal staff alert").sum()), "Immediate action", "Staff alerts or internal corporate incidents that bypass normal external relevance filtering.")
    with top3:
        metric_card("Temporary locations", str((df_temp["status"] == "Active").sum()), "Active", "Temporary locations currently active and included in exposure correlation.")
    with top4:
        metric_card("MIDB points", str(len(df_midb)), "Reference layer", "Airports, diplomatic outposts, border crossings, ports and hospitals available as contextual map layers.")

    left, centre, right = st.columns([0.85, 1.45, 0.9])

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
        st.caption("Workflow filters")
        st.selectbox("AI classification", ["All", "Red", "Amber", "Inform", "Discard"])
        st.selectbox("Origin", ["All", "Dataminr", "Government weather alert", "Open media", "Internal staff alert", "Manual operator entry"])

    with centre:
        st.subheader("Operational map")
        make_map(
            show_active_risks=True,
            show_offices=show_offices,
            show_temporary=show_temporary,
            show_travelling=show_travelling,
            show_airports=show_airports,
            show_diplomatic=show_diplomatic,
            show_borders=show_borders,
            show_ports=show_ports,
            show_hospitals=show_hospitals,
            pulse_risks=False,
            pulse_moves=False,
            monitor_only=True,
        )

        st.subheader("AI-generated and internal events table")
        st.dataframe(
            monitor_df[["id", "time", "origin", "title", "country", "type", "ai_classification", "confidence", "operator_status", "exposure"]],
            use_container_width=True,
            hide_index=True,
        )

    with right:
        st.subheader("Selected event")
        st.markdown(f"### {selected['title']}")
        st.markdown(badge(selected["ai_classification"]), unsafe_allow_html=True)
        st.write(f"**Origin:** {selected['origin']}")
        st.write(f"**Location:** {selected['city']}, {selected['country']}")
        st.write(f"**Confidence:** {selected['confidence']}")
        st.write(f"**Exposure match:** {selected['exposure']}")
        st.write(selected["summary"])

        st.subheader("Internal AI rationale")
        with st.container(border=True):
            st.write(selected["ai_reason"])

        st.subheader("Operator decision")
        st.selectbox("Final classification", ["Red", "Amber", "Inform", "Discard"], index=["Red", "Amber", "Inform", "Discard"].index(selected["ai_classification"]))
        st.selectbox("Workflow action", ["Publish to Pulse", "Keep monitoring", "Escalate", "Discard", "Request more information"])
        st.text_area("Operator notes", placeholder="Add source validation, context or override rationale...")
        st.button("Save decision", type="primary")
        st.button("Draft distribution email")

    st.divider()
    st.subheader("Temporary location management")

    temp_tab1, temp_tab2, temp_tab3 = st.tabs(["Active", "Archived", "Add / Edit"])

    with temp_tab1:
        active = df_temp[df_temp["status"] == "Active"]
        st.dataframe(active[["name", "city", "country", "start_date", "end_date", "lat", "lon"]], use_container_width=True, hide_index=True)

    with temp_tab2:
        archived = df_temp[df_temp["status"] == "Archived"]
        st.dataframe(archived[["name", "city", "country", "start_date", "end_date", "lat", "lon"]], use_container_width=True, hide_index=True)

    with temp_tab3:
        with st.form("temporary_location_form"):
            st.write("This is a dummy form. In a live system, saving would write to the corporate exposure database.")
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
            submit = st.form_submit_button("Save temporary location")
            if submit:
                st.success("Temporary location saved to dummy model. In production this would update the corporate exposure database.")

# -----------------------------
# Risk
# -----------------------------
else:
    st.title("Overwatch Risk")
    st.caption("Strategic risk, trend and mitigation workspace.")

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Reviews due", "3", "Next 30 days", "Scheduled country, office or route risk reviews due for update within the next 30 days.")
    with c2:
        metric_card("Hotspots", "8", "Recurring exposure locations", "Countries, cities, airports or areas where incidents repeatedly overlap with corporate exposure or travel activity.")
    with c3:
        metric_card("Open mitigations", "14", "Outstanding recommendations", "Risk reduction actions recommended but not yet completed.")

    st.subheader("Risk products")
    for report in RISK_REPORTS:
        with st.container(border=True):
            st.markdown(f"### {report['title']}")
            st.write(f"**Status:** {report['status']}")
            st.write(report["detail"])

    st.subheader("Operational data feeding risk")
    st.dataframe(
        df_events[["id", "country", "city", "type", "origin", "ai_classification", "operator_classification", "confidence", "operator_status", "exposure"]],
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("MIDB reference coverage")
    st.dataframe(df_midb[["name", "type", "city", "country", "lat", "lon"]], use_container_width=True, hide_index=True)
