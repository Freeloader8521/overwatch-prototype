
import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(
    page_title="Overwatch Prototype",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Dummy data
# -----------------------------
EVENTS = [
    {
        "id": "EVT-2401",
        "title": "Civil unrest reported near business district",
        "city": "Nairobi",
        "country": "Kenya",
        "lat": -1.286389,
        "lon": 36.817223,
        "type": "Security",
        "ai_classification": "Red",
        "operator_classification": "Red",
        "operator_status": "Published",
        "confidence": "High",
        "source": "Dataminr + local office report",
        "exposure": "Office 650m away and 3 monitored movements",
        "summary": "Multiple reports indicate escalating protest activity near a commercial district. One office location and three monitored staff movements are within the likely impact area.",
        "ai_reason": "Security event within 1000m of a fixed exposure and overlapping with monitored movements. AI recommends Red.",
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
        "ai_classification": "Amber",
        "operator_classification": None,
        "operator_status": "Awaiting operator review",
        "confidence": "Medium",
        "source": "Dataminr aviation alert",
        "exposure": "2 traveller notifications through IST within affected window",
        "summary": "Departures are delayed following a security screening disruption. Two staff travellers are scheduled to transit through IST within the next 18 hours.",
        "ai_reason": "Travel disruption at an airport with staff movement during the affected time window. AI recommends Amber.",
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
        "ai_classification": "Amber",
        "operator_classification": None,
        "operator_status": "Awaiting operator review",
        "confidence": "High",
        "source": "Government meteorological agency",
        "exposure": "Temporary project location in warning area",
        "summary": "A severe storm warning has been issued for the region. One temporary project location may experience travel disruption and localised flooding.",
        "ai_reason": "Environmental event overlaps with a temporary location. AI recommends Amber pending operator validation.",
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
        "ai_classification": "Inform",
        "operator_classification": "Inform",
        "operator_status": "Published",
        "confidence": "Medium",
        "source": "Open media reporting",
        "exposure": "No active exposure identified",
        "summary": "A planned demonstration has been announced. No offices, staff accommodation, temporary locations or monitored movements are currently assessed as exposed.",
        "ai_reason": "Relevant regional awareness but no current corporate exposure. AI recommends Inform.",
        "published": True,
        "published_hours_ago": 9,
        "time": "1 hr ago",
    },
    {
        "id": "EVT-2406",
        "title": "Airport strike disruption likely to affect departures",
        "city": "Madrid",
        "country": "Spain",
        "lat": 40.4983,
        "lon": -3.5676,
        "type": "Travel",
        "ai_classification": "Amber",
        "operator_classification": "Amber",
        "operator_status": "Published",
        "confidence": "High",
        "source": "Aviation disruption feed",
        "exposure": "Monitored movement through MAD",
        "summary": "Industrial action is expected to cause delays at Madrid Barajas. One monitored movement may be affected within the next 24 hours.",
        "ai_reason": "Travel disruption overlaps with monitored movement at MAD. AI recommends Amber.",
        "published": True,
        "published_hours_ago": 22,
        "time": "22 hrs ago",
    },
    {
        "id": "EVT-2407",
        "title": "Medical facility disruption reported",
        "city": "Lima",
        "country": "Peru",
        "lat": -12.0464,
        "lon": -77.0428,
        "type": "Medical",
        "ai_classification": "Inform",
        "operator_classification": "Inform",
        "operator_status": "Published",
        "confidence": "Medium",
        "source": "Government health notice",
        "exposure": "No current exposure",
        "summary": "Selected public medical facilities are operating with reduced capacity. No current staff exposure identified.",
        "ai_reason": "Health-related event with no current exposure. AI recommends Inform.",
        "published": True,
        "published_hours_ago": 55,
        "time": "55 hrs ago",
    },
    {
        "id": "EVT-2405",
        "title": "Local traffic accident reported",
        "city": "Lyon",
        "country": "France",
        "lat": 45.764043,
        "lon": 4.835659,
        "type": "Local disruption",
        "ai_classification": "Discard",
        "operator_classification": None,
        "operator_status": "Awaiting discard confirmation",
        "confidence": "High",
        "source": "Open source social media",
        "exposure": "No corporate exposure",
        "summary": "Minor local traffic accident with no assessed security, health, medical or travel relevance to corporate exposure.",
        "ai_reason": "No exposure match and no operational relevance. AI recommends Discard.",
        "published": False,
        "published_hours_ago": None,
        "time": "1 hr 20 mins ago",
    },
]

FIXED_EXPOSURE = [
    {"name": "Nairobi Office", "kind": "Office", "lat": -1.2833, "lon": 36.8172, "country": "Kenya"},
    {"name": "Berlin Office", "kind": "Office", "lat": 52.5200, "lon": 13.4050, "country": "Germany"},
    {"name": "Manila Temporary Project Site", "kind": "Temporary location", "lat": 14.6000, "lon": 120.9840, "country": "Philippines"},
    {"name": "Istanbul Staff Accommodation", "kind": "Staff accommodation", "lat": 41.0082, "lon": 28.9784, "country": "Türkiye"},
]

DYNAMIC_EXPOSURE = [
    {"traveller": "Traveller A", "country": "Kenya", "airport": "NBO", "date_range": "12-14 May", "status": "Monitored move", "lat": -1.3192, "lon": 36.9278},
    {"traveller": "Traveller B", "country": "Kenya", "airport": "NBO", "date_range": "12 May", "status": "Monitored move", "lat": -1.3192, "lon": 36.9278},
    {"traveller": "Traveller C", "country": "Türkiye", "airport": "IST", "date_range": "11-12 May", "status": "Monitored move", "lat": 41.2753, "lon": 28.7519},
    {"traveller": "Traveller D", "country": "Spain", "airport": "MAD", "date_range": "13 May", "status": "Monitored move", "lat": 40.4983, "lon": -3.5676},
]

RISK_REPORTS = [
    {"title": "Kenya Six-Month Security Review", "status": "Due in 12 days", "detail": "Civil unrest, transport disruption and office proximity events trending upwards."},
    {"title": "Türkiye Travel Resilience Assessment", "status": "Draft", "detail": "Airport disruption and transit exposure remain the primary traveller risk drivers."},
    {"title": "Philippines Severe Weather Mitigation Plan", "status": "In Review", "detail": "Temporary location readiness and flooding procedures require validation."},
]

df_events = pd.DataFrame(EVENTS)
df_fixed = pd.DataFrame(FIXED_EXPOSURE)
df_dynamic = pd.DataFrame(DYNAMIC_EXPOSURE)

COLOURS = {
    "Red": [239, 68, 68],
    "Amber": [245, 158, 11],
    "Inform": [59, 130, 246],
    "Discard": [100, 116, 139],
}

df_events["colour"] = df_events["ai_classification"].map(COLOURS)
df_events["display_classification"] = df_events["operator_classification"].fillna(df_events["ai_classification"])
df_events["display_colour"] = df_events["display_classification"].map(COLOURS)
df_events["radius"] = df_events["ai_classification"].map({"Red": 46000, "Amber": 32000, "Inform": 22000, "Discard": 14000})
df_events["pulse_radius"] = df_events["display_classification"].map({"Red": 82000, "Amber": 62000, "Inform": 46000, "Discard": 18000})
df_events["pulse_colour"] = df_events["display_classification"].map(COLOURS)

# -----------------------------
# Sidebar / theme
# -----------------------------
st.sidebar.title("🛡️ Overwatch")
st.sidebar.caption("Prototype v4: dummy data only")

theme_mode = st.sidebar.radio("Display mode", ["Low contrast", "High contrast"], horizontal=False)
page = st.sidebar.radio("Select environment", ["Overwatch Pulse", "Overwatch Monitor", "Overwatch Risk"])

st.sidebar.divider()
st.sidebar.caption("Key")
with st.sidebar.popover("Classification model"):
    st.write("🔴 **Red**: action required")
    st.write("🟠 **Amber**: monitor / assess")
    st.write("🔵 **Inform**: awareness only")
    st.write("⚫ **Discard**: no operational relevance")

high = theme_mode == "High contrast"
bg = "#020617" if not high else "#000814"
panel = "#0f172a" if not high else "#001d3d"
border = "#1e293b" if not high else "#00b4d8"
text = "#e2e8f0" if not high else "#ffffff"
muted = "#94a3b8" if not high else "#caf0f8"
glow = "rgba(56,189,248,.28)" if not high else "rgba(0,180,216,.55)"

st.markdown(
    f"""
    <style>
    .stApp {{
        background:
            radial-gradient(circle at 18% 16%, rgba(56,189,248,.18), transparent 26%),
            radial-gradient(circle at 78% 8%, rgba(59,130,246,.13), transparent 26%),
            linear-gradient(135deg, {bg}, #020617 60%, #000);
        color: {text};
    }}
    .block-container {{ padding-top: 1.1rem; }}
    .hero {{
        border: 1px solid {border};
        background:
            linear-gradient(135deg, rgba(15,23,42,.92), rgba(2,6,23,.86)),
            radial-gradient(circle at 70% 30%, rgba(56,189,248,.22), transparent 35%);
        box-shadow: 0 0 42px {glow};
        border-radius: 28px;
        padding: 26px;
        margin-bottom: 18px;
    }}
    .hero-kicker {{
        color: #67e8f9;
        text-transform: uppercase;
        letter-spacing: .28em;
        font-size: 12px;
        font-weight: 700;
    }}
    .hero-title {{
        color: white;
        font-size: 44px;
        font-weight: 800;
        line-height: 1.05;
        margin-top: 8px;
    }}
    .hero-sub {{
        color: {muted};
        font-size: 17px;
        margin-top: 10px;
        max-width: 980px;
    }}
    .metric-card {{
        background: rgba(15,23,42,.78);
        border: 1px solid {border};
        border-radius: 18px;
        padding: 18px;
        min-height: 118px;
        transition: all .15s ease;
        box-shadow: 0 0 28px rgba(14,165,233,.08);
    }}
    .metric-card:hover {{
        border-color: #67e8f9;
        box-shadow: 0 0 0 1px rgba(103,232,249,.35), 0 0 34px {glow};
    }}
    .metric-label {{
        color: {muted};
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }}
    .metric-value {{
        color: white;
        font-size: 30px;
        font-weight: 800;
        margin-top: 6px;
    }}
    .metric-sub {{
        color: {muted};
        font-size: 13px;
        margin-top: 8px;
    }}
    .info-dot {{
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
    }}
    .ticker {{
        overflow: hidden;
        white-space: nowrap;
        border: 1px solid {border};
        background: rgba(2,6,23,.72);
        border-radius: 18px;
        box-shadow: 0 0 26px rgba(14,165,233,.12);
        margin: 10px 0 18px 0;
    }}
    .ticker-track {{
        display: inline-block;
        padding: 12px 0;
        animation: ticker 32s linear infinite;
    }}
    .ticker span {{
        color: #cbd5e1;
        margin-right: 42px;
        font-size: 14px;
    }}
    @keyframes ticker {{
        0% {{ transform: translateX(100%); }}
        100% {{ transform: translateX(-100%); }}
    }}
    .status-pill {{
        border-radius: 999px;
        padding: 4px 10px;
        font-size: 12px;
        font-weight: 800;
        border: 1px solid rgba(255,255,255,.22);
    }}
    .rag-red {{ color: #fecaca; background: rgba(239,68,68,.2); border-color: rgba(239,68,68,.55); }}
    .rag-amber {{ color: #fde68a; background: rgba(245,158,11,.2); border-color: rgba(245,158,11,.55); }}
    .rag-inform {{ color: #bfdbfe; background: rgba(59,130,246,.22); border-color: rgba(59,130,246,.55); }}
    .rag-discard {{ color: #cbd5e1; background: rgba(100,116,139,.2); border-color: rgba(100,116,139,.55); }}
    </style>
    """,
    unsafe_allow_html=True,
)

def badge(value):
    css = {"Red": "rag-red", "Amber": "rag-amber", "Inform": "rag-inform", "Discard": "rag-discard"}[value]
    return f"<span class='status-pill {css}'>{value}</span>"

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

def map_view(events_df, show_fixed=True, show_dynamic=True, pulse_risks=False, pulse_moves=False):
    layers = []

    if pulse_risks and not events_df.empty:
        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data=events_df,
                get_position="[lon, lat]",
                get_fill_color="[0, 0, 0, 0]",
                get_line_color="pulse_colour",
                get_radius="pulse_radius",
                stroked=True,
                filled=False,
                line_width_min_pixels=3,
                opacity=0.55,
                pickable=False,
            )
        )

    layers.append(
        pdk.Layer(
            "ScatterplotLayer",
            data=events_df,
            get_position="[lon, lat]",
            get_fill_color="display_colour" if "display_colour" in events_df.columns else "colour",
            get_radius="radius",
            pickable=True,
            opacity=0.85,
            stroked=True,
            get_line_color=[255, 255, 255],
            line_width_min_pixels=1,
        )
    )

    if show_fixed:
        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data=df_fixed,
                get_position="[lon, lat]",
                get_fill_color=[56, 189, 248],
                get_radius=19000,
                pickable=True,
                opacity=0.9,
            )
        )

    if show_dynamic and pulse_moves:
        move_df = df_dynamic.copy()
        move_df["ring_radius"] = 44000
        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data=move_df,
                get_position="[lon, lat]",
                get_fill_color=[0, 0, 0, 0],
                get_line_color=[168, 85, 247],
                get_radius="ring_radius",
                stroked=True,
                filled=False,
                line_width_min_pixels=3,
                opacity=0.5,
                pickable=False,
            )
        )

    if show_dynamic:
        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data=df_dynamic,
                get_position="[lon, lat]",
                get_fill_color=[168, 85, 247],
                get_radius=15000,
                pickable=True,
                opacity=0.9,
            )
        )

    deck = pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(latitude=18, longitude=30, zoom=1.1, pitch=0),
        layers=layers,
        tooltip={
            "html": "<b>{title}</b><br/>{city}, {country}<br/>{display_classification}<br/>{exposure}",
            "style": {"backgroundColor": "#0f172a", "color": "white"},
        },
    )
    st.pydeck_chart(deck, use_container_width=True, height=430)

published_df = df_events[df_events["published"] == True].copy()
last_72_df = published_df[published_df["published_hours_ago"] <= 72].copy()
monitor_df = df_events[df_events["published"] == False].copy()

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
        metric_card(
            "Active risks",
            str(len(published_df)),
            "Click/toggle pulse on map",
            "Operator-approved live risks currently displayed on Overwatch Pulse."
        )
    with c2:
        metric_card(
            "Monitored moves",
            str(len(df_dynamic)),
            "Journeys being monitored",
            "Journeys or traveller movements currently being watched against the live risk picture."
        )
    with c3:
        red_count = (last_72_df["operator_classification"] == "Red").sum()
        amber_count = (last_72_df["operator_classification"] == "Amber").sum()
        inform_count = (last_72_df["operator_classification"] == "Inform").sum()
        metric_card(
            "Published updates",
            f"{len(last_72_df)}",
            f"72 hrs: {red_count} Red · {amber_count} Amber · {inform_count} Inform",
            "Operator-approved updates published in the last 72 hours, excluding discarded items."
        )

    pulse_col1, pulse_col2 = st.columns([0.72, 0.28])
    with pulse_col1:
        pulse_risks = st.toggle("Pulse active risks on map", value=True)
    with pulse_col2:
        pulse_moves = st.toggle("Pulse monitored moves", value=False)

    st.subheader("Live common intelligence map")
    map_view(published_df, show_fixed=False, show_dynamic=True, pulse_risks=pulse_risks, pulse_moves=pulse_moves)

    st.subheader("Published updates: last 72 hours")
    tab_red, tab_amber, tab_inform = st.tabs(["Red", "Amber", "Inform"])

    def render_updates(classification):
        data = last_72_df[last_72_df["operator_classification"] == classification]
        if data.empty:
            st.info(f"No {classification} updates in the last 72 hours.")
        for item in data.to_dict("records"):
            with st.container(border=True):
                cols = st.columns([0.78, 0.22])
                with cols[0]:
                    st.markdown(f"### {item['title']}")
                    st.write(f"{item['city']}, {item['country']} · {item['time']}")
                    st.write(item["summary"])
                with cols[1]:
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
    st.caption("Operator workflow for AI-generated events, internal exposure correlation and human decision-making.")

    top1, top2, top3, top4 = st.columns(4)
    with top1:
        metric_card("AI-generated events", str(len(monitor_df)), "Awaiting decision", "Events surfaced to the operator after Dataminr/manual ingestion, standardisation and internal exposure correlation.")
    with top2:
        metric_card("Red candidates", str((monitor_df["ai_classification"] == "Red").sum()), "Action likely", "AI-assessed events where immediate operator review is recommended.")
    with top3:
        metric_card("Amber candidates", str((monitor_df["ai_classification"] == "Amber").sum()), "Monitor / assess", "AI-assessed events that may require operator monitoring, verification or targeted communication.")
    with top4:
        metric_card("Discard candidates", str((monitor_df["ai_classification"] == "Discard").sum()), "Confirm no relevance", "AI-assessed events that appear to have no operational relevance but may still require operator confirmation.")

    left, centre, right = st.columns([0.85, 1.45, 0.9])

    with left:
        st.subheader("Events workflow")
        selected_id = st.radio(
            "Select event",
            [i["id"] for i in EVENTS if not i["published"]],
            format_func=lambda x: f"{x} · {next(i for i in EVENTS if i['id'] == x)['ai_classification']} · {next(i for i in EVENTS if i['id'] == x)['city']}",
            label_visibility="collapsed",
        )
        selected = next(i for i in EVENTS if i["id"] == selected_id)

        st.divider()
        st.caption("Workflow filters")
        st.selectbox("AI classification", ["All", "Red", "Amber", "Inform", "Discard"])
        st.selectbox("Operator status", ["All", "Awaiting operator review", "Awaiting discard confirmation", "Under Investigation", "Published", "Discarded"])

    with centre:
        st.subheader("Operational map")
        show_fixed = st.checkbox("Show fixed exposure", value=True)
        show_dynamic = st.checkbox("Show dynamic exposure", value=True)
        map_view(monitor_df, show_fixed=show_fixed, show_dynamic=show_dynamic, pulse_risks=False, pulse_moves=False)

        st.subheader("AI-generated events table")
        st.dataframe(
            monitor_df[["id", "time", "source", "title", "country", "type", "ai_classification", "confidence", "operator_status", "exposure"]],
            use_container_width=True,
            hide_index=True,
        )

    with right:
        st.subheader("Selected event")
        st.markdown(f"### {selected['title']}")
        st.markdown(badge(selected["ai_classification"]), unsafe_allow_html=True)
        st.write(f"**Location:** {selected['city']}, {selected['country']}")
        st.write(f"**Source:** {selected['source']}")
        st.write(f"**Confidence:** {selected['confidence']}")
        st.write(f"**Exposure match:** {selected['exposure']}")
        st.write(selected["summary"])

        st.subheader("Internal AI rationale")
        with st.container(border=True):
            st.write(selected["ai_reason"])

        st.subheader("Operator decision")
        final_classification = st.selectbox(
            "Final classification",
            ["Red", "Amber", "Inform", "Discard"],
            index=["Red", "Amber", "Inform", "Discard"].index(selected["ai_classification"]),
        )
        status = st.selectbox("Workflow action", ["Publish to Pulse", "Keep monitoring", "Escalate", "Discard", "Request more information"])
        notes = st.text_area("Operator notes", placeholder="Add source validation, context or override rationale...")
        st.button("Save decision", type="primary")
        st.button("Draft distribution email")

# -----------------------------
# Risk
# -----------------------------
else:
    st.title("Overwatch Risk")
    st.caption("Strategic risk, reporting and mitigation workspace.")

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Reviews due", "3", "Next 30 days", "Scheduled country, office or route risk reviews due for update within the next 30 days.")
    with c2:
        metric_card("Hotspots", "8", "Recurring exposure locations", "Countries, cities, airports or areas where incidents repeatedly overlap with corporate exposure or travel activity.")
    with c3:
        metric_card("Open mitigations", "14", "Recommendations requiring action", "Risk reduction actions recommended but not yet completed.")

    st.subheader("Risk products")
    for report in RISK_REPORTS:
        with st.container(border=True):
            st.markdown(f"### {report['title']}")
            st.write(f"**Status:** {report['status']}")
            st.write(report["detail"])

    st.subheader("Operational data feeding risk")
    st.write(
        """
        Overwatch Risk draws on historical incident data, analyst decisions, override rationale, exposure frequency,
        office and accommodation proximity events, monitored movements, mitigation history and recurring country-level disruption.
        """
    )

    st.dataframe(
        df_events[["id", "country", "city", "type", "ai_classification", "operator_classification", "confidence", "operator_status", "exposure"]],
        use_container_width=True,
        hide_index=True,
    )
