
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import uuid

st.set_page_config(page_title="Spectre", layout="wide", page_icon="◉")

# ---------------------------------------------------
# Styling
# ---------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 20% 20%, rgba(59,130,246,0.10), transparent 28%),
        radial-gradient(circle at 80% 0%, rgba(56,189,248,0.08), transparent 24%),
        linear-gradient(135deg,#020617,#07111f 55%,#030712);
    color: #dbe7f5;
}

h1,h2,h3 {
    font-family: 'Rajdhani', sans-serif !important;
    letter-spacing: 0.04em;
}

.metric-card {
    background: rgba(15,23,42,.72);
    border: 1px solid rgba(59,130,246,.14);
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 0 24px rgba(59,130,246,.08);
}

.metric-title {
    color:#94a3b8;
    font-size:12px;
    text-transform:uppercase;
    letter-spacing:0.08em;
}

.metric-value {
    font-size:32px;
    font-weight:700;
    color:white;
    margin-top:6px;
}

.metric-sub {
    color:#94a3b8;
    font-size:13px;
    margin-top:8px;
}

.hero {
    padding:28px;
    border-radius:24px;
    background: rgba(15,23,42,.72);
    border:1px solid rgba(56,189,248,.18);
    box-shadow: 0 0 36px rgba(56,189,248,.10);
    margin-bottom:18px;
}

.hero-kicker {
    color:#67e8f9;
    font-size:12px;
    text-transform:uppercase;
    letter-spacing:0.25em;
    font-weight:700;
}

.hero-title {
    font-size:48px;
    color:white;
    font-weight:700;
}

.hero-sub {
    color:#94a3b8;
    font-size:16px;
    max-width:900px;
}

.status-pill {
    display:inline-block;
    padding:4px 10px;
    border-radius:999px;
    font-size:12px;
    font-weight:700;
}

.red {
    background:rgba(239,68,68,.16);
    border:1px solid rgba(239,68,68,.35);
    color:#fecaca;
}

.amber {
    background:rgba(245,158,11,.14);
    border:1px solid rgba(245,158,11,.35);
    color:#fde68a;
}

.inform {
    background:rgba(59,130,246,.14);
    border:1px solid rgba(59,130,246,.35);
    color:#bfdbfe;
}

.small-note {
    color:#94a3b8;
    font-size:13px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Session state
# ---------------------------------------------------

if "events" not in st.session_state:
    now = datetime.utcnow()

    st.session_state.events = [
        {
            "id":"EVT-2402",
            "title":"Airport disruption following security incident",
            "country":"Türkiye",
            "city":"Istanbul",
            "lat":41.2753,
            "lon":28.7519,
            "classification":"Amber",
            "origin":"Dataminr",
            "summary":"Airport disruption affecting monitored staff movements.",
            "published":False,
            "created":now.isoformat(),
            "status":"Workflow"
        },
        {
            "id":"INT-1001",
            "title":"Staff alert triggered",
            "country":"Singapore",
            "city":"Singapore",
            "lat":1.3521,
            "lon":103.8198,
            "classification":"Red",
            "origin":"Internal staff alert",
            "summary":"Staff member activated emergency alert.",
            "published":True,
            "created":now.isoformat(),
            "status":"Published"
        },
        {
            "id":"OP-2001",
            "title":"Office report: access disruption",
            "country":"UAE",
            "city":"Dubai",
            "lat":25.2048,
            "lon":55.2708,
            "classification":"Amber",
            "origin":"Operator report",
            "summary":"Access road disruption near office.",
            "published":True,
            "created":(now - timedelta(hours=3)).isoformat(),
            "status":"Published"
        },
        {
            "id":"INF-1101",
            "title":"Planned demonstration announced",
            "country":"Germany",
            "city":"Berlin",
            "lat":52.52,
            "lon":13.40,
            "classification":"Inform",
            "origin":"Open media",
            "summary":"Awareness item. No direct exposure identified.",
            "published":True,
            "created":(now - timedelta(hours=6)).isoformat(),
            "status":"Published"
        }
    ]

# ---------------------------------------------------
# Data
# ---------------------------------------------------

offices = pd.DataFrame([
    {"name":"London Office","lat":51.5072,"lon":-0.1276},
    {"name":"Singapore Office","lat":1.3521,"lon":103.8198},
    {"name":"Nairobi Office","lat":-1.2864,"lon":36.8172},
])

temporary_locations = pd.DataFrame([
    {"name":"Manila Project Site","status":"Active","country":"Philippines"},
    {"name":"Lima Field Team","status":"Active","country":"Peru"},
    {"name":"Lagos Election Team","status":"Archived","country":"Nigeria"},
])

moves = pd.DataFrame([
    {"name":"Traveller A","route":"LHR → IST → NBO"},
    {"name":"Traveller B","route":"DXB → SIN"},
])

events_df = pd.DataFrame(st.session_state.events)

# Inform expiry
now = datetime.utcnow()
display_events = []

for _, row in events_df.iterrows():
    created = datetime.fromisoformat(row["created"])

    if row["classification"] == "Inform":
        if now - created < timedelta(hours=12):
            display_events.append(row)
    else:
        display_events.append(row)

display_df = pd.DataFrame(display_events)

published = display_df[display_df["published"] == True]
workflow = display_df[display_df["published"] == False]

# ---------------------------------------------------
# Helpers
# ---------------------------------------------------

def metric(title, value, sub):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

def pill(level):
    return f'<span class="status-pill {level.lower()}">{level}</span>'

def build_map():
    fig = go.Figure()

    colours = {
        "Red":"#ef4444",
        "Amber":"#f59e0b",
        "Inform":"#60a5fa"
    }

    for level in ["Red","Amber","Inform"]:
        subset = published[published["classification"] == level]
        if len(subset) > 0:
            fig.add_trace(go.Scattergeo(
                lon=subset["lon"],
                lat=subset["lat"],
                mode="markers",
                name=level,
                marker=dict(
                    size=20 if level=="Red" else 16,
                    color=colours[level],
                    opacity=0.92,
                    line=dict(width=1,color="white")
                ),
                hovertext=subset["title"],
                hovertemplate="%{hovertext}<extra></extra>"
            ))

    fig.add_trace(go.Scattergeo(
        lon=offices["lat"]*0 + offices["lat"]*0 + [-0.1276,103.8198,36.8172],
        lat=[51.5072,1.3521,-1.2864],
        mode="markers",
        name="Offices",
        marker=dict(
            size=9,
            color="#38bdf8",
            symbol="square"
        )
    ))

    fig.update_geos(
        projection_type="natural earth",
        showland=True,
        landcolor="#0f172a",
        showocean=True,
        oceancolor="#020617",
        showcountries=True,
        countrycolor="#334155",
        coastlinecolor="#334155",
        bgcolor="rgba(0,0,0,0)"
    )

    fig.update_layout(
        height=520,
        margin=dict(l=0,r=0,t=0,b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dbe7f5"),
    )

    return fig

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

st.sidebar.title("Spectre")

page = st.sidebar.radio(
    "Workspace",
    [
        "Common Picture",
        "Monitor",
        "Risk"
    ]
)

# ---------------------------------------------------
# Common Picture
# ---------------------------------------------------

if page == "Common Picture":

    st.markdown("""
    <div class="hero">
        <div class="hero-kicker">Spectre</div>
        <div class="hero-title">Live Common Intelligence Picture</div>
        <div class="hero-sub">
        Validated operational picture displaying published risks, monitored moves and situational awareness updates.
        </div>
    </div>
    """, unsafe_allow_html=True)

    red_count = len(published[published["classification"] == "Red"])
    amber_count = len(published[published["classification"] == "Amber"])
    inform_count = len(published[published["classification"] == "Inform"])

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        metric("Active Red Risks", red_count, "Immediate action required")
    with c2:
        metric("Active Amber Risks", amber_count, "Monitoring and assessment")
    with c3:
        metric("Informs", inform_count, "Awareness only")
    with c4:
        metric("Monitored Moves", len(moves), "Journeys being monitored")

    st.plotly_chart(build_map(), use_container_width=True)

# ---------------------------------------------------
# Monitor
# ---------------------------------------------------

elif page == "Monitor":

    left_title, right_title = st.columns([0.7,0.3])

    with left_title:
        st.title("Monitor")

    with right_title:
        with st.popover("Create Internal Event"):
            with st.form("internal_event_form"):
                title = st.text_input("Event Title")
                country = st.text_input("Country")
                city = st.text_input("City")
                classification = st.selectbox(
                    "Classification",
                    ["Red","Amber","Inform"]
                )

                summary = st.text_area("Summary")

                submitted = st.form_submit_button("Create Event")

                if submitted:
                    new_event = {
                        "id":"INT-" + str(uuid.uuid4())[:6].upper(),
                        "title":title,
                        "country":country,
                        "city":city,
                        "lat":0,
                        "lon":0,
                        "classification":classification,
                        "origin":"Operator created",
                        "summary":summary,
                        "published":True,
                        "created":datetime.utcnow().isoformat(),
                        "status":"Published"
                    }

                    st.session_state.events.append(new_event)
                    st.success("Internal event created and published.")

    st.caption("Operational event workflow and triage")

    left, centre, right = st.columns([1,1.5,0.9])

    workflow = pd.DataFrame([
        e for e in st.session_state.events if e["published"] == False
    ])

    if len(workflow) == 0:
        workflow = pd.DataFrame([st.session_state.events[0]])

    with left:

        st.subheader("Workflow Events")

        selected = st.radio(
            "Events",
            workflow["id"].tolist(),
            label_visibility="collapsed"
        )

        selected_event = workflow[workflow["id"] == selected].iloc[0]

        st.divider()

        st.subheader("Selected Event")

        st.markdown(
            pill(selected_event["classification"]),
            unsafe_allow_html=True
        )

        st.markdown(f"### {selected_event['title']}")

        st.write(f"**Origin:** {selected_event['origin']}")
        st.write(f"**Location:** {selected_event['city']}, {selected_event['country']}")

        st.markdown(
            f'<div class="small-note">{selected_event["summary"]}</div>',
            unsafe_allow_html=True
        )

    with centre:

        st.subheader("Operational Map")
        st.plotly_chart(build_map(), use_container_width=True)

        t1,t2,t3 = st.tabs([
            "All Events",
            "Locations",
            "Monitored Moves"
        ])

        with t1:
            st.dataframe(
                pd.DataFrame(st.session_state.events)[[
                    "id",
                    "origin",
                    "title",
                    "country",
                    "classification",
                    "status"
                ]],
                use_container_width=True,
                hide_index=True
            )

        with t2:

            st.markdown("##### Offices")

            st.dataframe(
                offices,
                use_container_width=True,
                hide_index=True
            )

            st.markdown("##### Temporary Locations")

            st.dataframe(
                temporary_locations,
                use_container_width=True,
                hide_index=True
            )

        with t3:
            st.dataframe(
                moves,
                use_container_width=True,
                hide_index=True
            )

    with right:

        st.subheader("Operator Decision")

        classification = st.selectbox(
            "Final Classification",
            ["Red","Amber","Inform","Discard"]
        )

        notes = st.text_area(
            "Operator Notes",
            placeholder="Add context or escalation notes..."
        )

        if st.button("Publish", use_container_width=True):

            for e in st.session_state.events:
                if e["id"] == selected_event["id"]:
                    e["published"] = True
                    e["classification"] = classification
                    e["status"] = "Published"

            st.success("Event published to Common Picture.")

        if st.button("Monitor", use_container_width=True):

            for e in st.session_state.events:
                if e["id"] == selected_event["id"]:
                    e["status"] = "Monitoring"

            st.success("Event retained in monitoring workflow.")

        if st.button("Discard", use_container_width=True):

            for e in st.session_state.events:
                if e["id"] == selected_event["id"]:
                    e["status"] = "Discarded"
                    e["published"] = False

            st.success("Event discarded.")

# ---------------------------------------------------
# Risk
# ---------------------------------------------------

else:

    st.title("Risk")

    c1,c2,c3 = st.columns(3)

    with c1:
        metric("Reviews Due","3","Next 30 days")

    with c2:
        metric("Open Mitigations","14","Outstanding recommendations")

    with c3:
        metric("Recurring Hotspots","8","Persistent exposure locations")

    st.divider()

    st.subheader("Published Event Archive")

    archive = pd.DataFrame([
        e for e in st.session_state.events
        if e["published"] == True
    ])

    st.dataframe(
        archive[[
            "id",
            "title",
            "country",
            "origin",
            "classification",
            "created",
            "summary"
        ]],
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Published events automatically populate the archive to support long-term risk analysis, trends and mitigation planning."
    )
