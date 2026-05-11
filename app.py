
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
INCIDENTS = [
    {
        "id": "EVT-2401",
        "title": "Civil unrest reported near business district",
        "city": "Nairobi",
        "country": "Kenya",
        "lat": -1.286389,
        "lon": 36.817223,
        "type": "Security",
        "rag": "Red",
        "confidence": "High",
        "status": "Under Investigation",
        "source": "Dataminr + local office report",
        "exposure": "Office and 3 monitored movements",
        "distance": "650m from office",
        "summary": "Multiple reports indicate escalating protest activity near a commercial district. One office location and three monitored staff movements are within the likely impact area.",
        "ai": "Recommend Red. Contact local office, confirm staff accountability, advise travellers to avoid CBD access routes, and prepare customer advisory.",
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
        "rag": "Amber",
        "confidence": "Medium",
        "status": "AI Triaged",
        "source": "Aviation feed",
        "exposure": "2 traveller notifications",
        "distance": "Airport-level impact",
        "summary": "Departures are delayed following a security screening disruption. Two staff travellers are scheduled to transit through IST within the next 18 hours.",
        "ai": "Recommend Amber. Monitor airline updates, notify affected travellers, and review onward connections.",
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
        "rag": "Amber",
        "confidence": "High",
        "status": "Monitoring",
        "source": "Government meteorological agency",
        "exposure": "Temporary location",
        "distance": "Regional impact",
        "summary": "A severe storm warning has been issued for the region. One temporary project location may experience travel disruption and localised flooding.",
        "ai": "Recommend Amber. Confirm site readiness, advise local team to review transport options, and monitor escalation to Red if landfall projection worsens.",
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
        "rag": "Green",
        "confidence": "Medium",
        "status": "Closed",
        "source": "Open media reporting",
        "exposure": "No active exposure identified",
        "distance": "No direct exposure",
        "summary": "A planned demonstration has been announced. No offices, staff accommodation, temporary locations or monitored movements are currently assessed as exposed.",
        "ai": "Recommend Green. No action required beyond passive monitoring.",
        "time": "1 hr ago",
    },
]

OFFICES = [
    {"name": "Nairobi Office", "kind": "Office", "lat": -1.2833, "lon": 36.8172, "country": "Kenya"},
    {"name": "Berlin Office", "kind": "Office", "lat": 52.5200, "lon": 13.4050, "country": "Germany"},
    {"name": "Manila Temporary Project Site", "kind": "Temporary location", "lat": 14.6000, "lon": 120.9840, "country": "Philippines"},
    {"name": "Istanbul Staff Accommodation", "kind": "Staff accommodation", "lat": 41.0082, "lon": 28.9784, "country": "Türkiye"},
]

TRAVELLERS = [
    {"traveller": "Traveller A", "country": "Kenya", "airport": "NBO", "date_range": "12-14 May", "status": "Monitored movement", "lat": -1.3192, "lon": 36.9278},
    {"traveller": "Traveller B", "country": "Kenya", "airport": "NBO", "date_range": "12 May", "status": "Traveller notification", "lat": -1.3192, "lon": 36.9278},
    {"traveller": "Traveller C", "country": "Türkiye", "airport": "IST", "date_range": "11-12 May", "status": "Traveller notification", "lat": 41.2753, "lon": 28.7519},
    {"traveller": "Traveller D", "country": "Türkiye", "airport": "IST", "date_range": "12 May", "status": "Traveller notification", "lat": 41.2753, "lon": 28.7519},
]

RISK_REPORTS = [
    {"title": "Kenya Six-Month Security Review", "status": "Due in 12 days", "detail": "Civil unrest, transport disruption and office proximity events trending upwards."},
    {"title": "Türkiye Travel Resilience Assessment", "status": "Draft", "detail": "Airport disruption and transit exposure remain the primary traveller risk drivers."},
    {"title": "Philippines Severe Weather Mitigation Plan", "status": "In Review", "detail": "Temporary location readiness and flooding procedures require validation."},
]

df_incidents = pd.DataFrame(INCIDENTS)
df_offices = pd.DataFrame(OFFICES)
df_travellers = pd.DataFrame(TRAVELLERS)

RAG_COLOURS = {
    "Red": [239, 68, 68],
    "Amber": [245, 158, 11],
    "Green": [34, 197, 94],
}

df_incidents["colour"] = df_incidents["rag"].map(RAG_COLOURS)
df_incidents["radius"] = df_incidents["rag"].map({"Red": 45000, "Amber": 30000, "Green": 18000})

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
    .main {
        background: #020617;
    }
    .block-container {
        padding-top: 1.2rem;
    }
    .metric-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 18px;
        padding: 18px;
        min-height: 120px;
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
        font-weight: 700;
        margin-top: 6px;
    }
    .metric-sub {
        color: #94a3b8;
        font-size: 13px;
        margin-top: 8px;
    }
    .panel {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 18px;
        padding: 18px;
    }
    .rag-red {
        color: #fecaca;
        background: rgba(239, 68, 68, .18);
        border: 1px solid rgba(239, 68, 68, .4);
        border-radius: 999px;
        padding: 4px 10px;
        font-size: 12px;
        font-weight: 700;
    }
    .rag-amber {
        color: #fde68a;
        background: rgba(245, 158, 11, .18);
        border: 1px solid rgba(245, 158, 11, .4);
        border-radius: 999px;
        padding: 4px 10px;
        font-size: 12px;
        font-weight: 700;
    }
    .rag-green {
        color: #bbf7d0;
        background: rgba(34, 197, 94, .18);
        border: 1px solid rgba(34, 197, 94, .4);
        border-radius: 999px;
        padding: 4px 10px;
        font-size: 12px;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def rag_badge(rag):
    css = {"Red": "rag-red", "Amber": "rag-amber", "Green": "rag-green"}[rag]
    return f"<span class='{css}'>{rag}</span>"

def metric_card(label, value, sub):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def map_view(show_offices=True, show_travellers=True):
    layers = [
        pdk.Layer(
            "ScatterplotLayer",
            data=df_incidents,
            get_position="[lon, lat]",
            get_fill_color="colour",
            get_radius="radius",
            pickable=True,
            opacity=0.8,
            stroked=True,
            get_line_color=[255, 255, 255],
            line_width_min_pixels=1,
        )
    ]

    if show_offices:
        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data=df_offices,
                get_position="[lon, lat]",
                get_fill_color=[56, 189, 248],
                get_radius=18000,
                pickable=True,
                opacity=0.9,
            )
        )

    if show_travellers:
        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data=df_travellers,
                get_position="[lon, lat]",
                get_fill_color=[168, 85, 247],
                get_radius=14000,
                pickable=True,
                opacity=0.9,
            )
        )

    deck = pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v10",
        initial_view_state=pdk.ViewState(latitude=18, longitude=30, zoom=1.15, pitch=0),
        layers=layers,
        tooltip={
            "html": "<b>{title}</b><br/>{city}, {country}<br/>{rag}<br/>{exposure}",
            "style": {"backgroundColor": "#0f172a", "color": "white"},
        },
    )
    st.pydeck_chart(deck, use_container_width=True)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🛡️ Overwatch")
st.sidebar.caption("Prototype v1: dummy data only")

page = st.sidebar.radio(
    "Select environment",
    ["Overwatch Pulse", "Overwatch Monitor", "Overwatch Risk"],
)

st.sidebar.divider()
st.sidebar.caption("Prototype navigation")
st.sidebar.write("Pulse: customer-facing view")
st.sidebar.write("Monitor: operator workspace")
st.sidebar.write("Risk: strategic risk and mitigation")

# -----------------------------
# Page: Pulse
# -----------------------------
if page == "Overwatch Pulse":
    st.title("Overwatch Pulse")
    st.caption("Customer-facing global operational picture")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Active advisories", "4", "1 Red, 2 Amber, 1 Green")
    with c2:
        metric_card("Potentially impacted", "5", "Across Kenya and Türkiye")
    with c3:
        metric_card("Traveller notices", "7", "Issued or pending review")
    with c4:
        metric_card("Published updates", "12", "Last 24 hours")

    st.subheader("Global threat map")
    map_view(show_offices=True, show_travellers=True)

    st.subheader("Current published advisories")
    for item in INCIDENTS:
        with st.container(border=True):
            cols = st.columns([0.7, 0.15, 0.15])
            with cols[0]:
                st.markdown(f"### {item['title']}")
                st.write(f"{item['city']}, {item['country']} · {item['time']}")
                st.write(item["summary"])
            with cols[1]:
                st.markdown(rag_badge(item["rag"]), unsafe_allow_html=True)
            with cols[2]:
                st.write(item["status"])

# -----------------------------
# Page: Monitor
# -----------------------------
elif page == "Overwatch Monitor":
    st.title("Overwatch Monitor")
    st.caption("Operator dashboard for live triage, exposure correlation and dissemination")

    left, centre, right = st.columns([0.85, 1.45, 0.9])

    with left:
        st.subheader("AI triage queue")
        selected_id = st.radio(
            "Select event",
            [i["id"] for i in INCIDENTS],
            format_func=lambda x: f"{x} · {next(i for i in INCIDENTS if i['id'] == x)['rag']} · {next(i for i in INCIDENTS if i['id'] == x)['city']}",
            label_visibility="collapsed",
        )
        selected = next(i for i in INCIDENTS if i["id"] == selected_id)

        st.divider()
        st.caption("Queue controls")
        st.selectbox("Filter by RAG", ["All", "Red", "Amber", "Green"])
        st.selectbox("Filter by status", ["All", "AI Triaged", "Under Investigation", "Monitoring", "Closed"])

    with centre:
        st.subheader("Operational map")
        map_view(show_offices=True, show_travellers=True)

        st.subheader("Selected incident")
        st.markdown(f"### {selected['title']}")
        st.markdown(rag_badge(selected["rag"]), unsafe_allow_html=True)
        st.write(f"**Location:** {selected['city']}, {selected['country']}")
        st.write(f"**Source:** {selected['source']}")
        st.write(f"**Confidence:** {selected['confidence']}")
        st.write(f"**Exposure:** {selected['exposure']}")
        st.write(f"**Distance / impact area:** {selected['distance']}")
        st.write(selected["summary"])

    with right:
        st.subheader("AI assessment")
        with st.container(border=True):
            st.write(selected["ai"])

        st.subheader("Operator decision")
        final_rag = st.selectbox("Final RAG", ["Green", "Amber", "Red"], index=["Green", "Amber", "Red"].index(selected["rag"]))
        status = st.selectbox("Workflow status", ["New", "AI Triaged", "Under Investigation", "Analyst Assessed", "Published", "Monitoring", "Closed", "Archived"])
        notes = st.text_area("Analyst notes", placeholder="Add operational context, source validation or override rationale...")
        st.button("Save analyst assessment", type="primary")

        st.subheader("Dissemination")
        st.selectbox("Suggested distribution list", [f"{selected['country']} security distribution", "Regional leadership", "Global crisis team", "Traveller-only notification"])
        st.button("Draft email advisory")
        st.button("Publish to Overwatch Pulse")

# -----------------------------
# Page: Risk
# -----------------------------
else:
    st.title("Overwatch Risk")
    st.caption("Strategic risk, reporting and mitigation workspace")

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Reviews due", "3", "Next 30 days")
    with c2:
        metric_card("Hotspots", "8", "Recurring exposure locations")
    with c3:
        metric_card("Open mitigations", "14", "Recommendations requiring action")

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
        df_incidents[["id", "country", "city", "type", "rag", "confidence", "status", "exposure"]],
        use_container_width=True,
        hide_index=True,
    )
