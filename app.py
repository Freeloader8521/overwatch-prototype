
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Spectre",
    layout="wide",
    page_icon="◉"
)

# -------------------------------------------------
# Styling
# -------------------------------------------------

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

.section-box {
    background: rgba(15,23,42,.52);
    border-radius:18px;
    border:1px solid rgba(59,130,246,.10);
    padding:18px;
}

.small-note {
    color:#94a3b8;
    font-size:13px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Dummy Data
# -------------------------------------------------

events = pd.DataFrame([
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
        "published":False
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
        "published":True
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
        "published":True
    }
])

offices = pd.DataFrame([
    {"name":"London Office","lat":51.5072,"lon":-0.1276},
    {"name":"Singapore Office","lat":1.3521,"lon":103.8198},
    {"name":"Nairobi Office","lat":-1.2864,"lon":36.8172},
])

moves = pd.DataFrame([
    {"name":"Traveller A","lat":41.2753,"lon":28.7519},
    {"name":"Traveller B","lat":1.3644,"lon":103.9915},
])

airports = pd.DataFrame([
    {"name":"Heathrow","lat":51.4700,"lon":-0.4543},
    {"name":"Istanbul Airport","lat":41.2753,"lon":28.7519},
])

ports = pd.DataFrame([
    {"name":"Singapore Port","lat":1.2644,"lon":103.8222},
])

# -------------------------------------------------
# Helpers
# -------------------------------------------------

def metric(title, value, sub):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

def pill(level):
    cls = level.lower()
    return f'<span class="status-pill {cls}">{level}</span>'

def add_points(fig, df, colour, symbol, name, size):
    fig.add_trace(go.Scattergeo(
        lon=df["lon"],
        lat=df["lat"],
        mode="markers",
        name=name,
        marker=dict(
            size=size,
            color=colour,
            symbol=symbol,
            opacity=0.9,
            line=dict(width=1,color="white")
        ),
        hovertext=df["name"],
        hovertemplate="%{hovertext}<extra></extra>"
    ))

def build_map():
    fig = go.Figure()

    published = events[events["published"] == True]

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
                name=f"{level} Risks",
                marker=dict(
                    size=20 if level=="Red" else 16,
                    color=colours[level],
                    opacity=0.92,
                    line=dict(width=1,color="white")
                ),
                hovertext=subset["title"],
                hovertemplate="%{hovertext}<extra></extra>"
            ))

    add_points(fig, offices, "#38bdf8", "square", "Offices", 9)
    add_points(fig, moves, "#8b5cf6", "circle", "Monitored Moves", 7)
    add_points(fig, airports, "#94a3b8", "triangle-up", "Airports", 6)
    add_points(fig, ports, "#94a3b8", "diamond", "Ports", 6)

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
        legend=dict(
            orientation="h",
            y=-0.08,
            x=0.5,
            xanchor="center"
        )
    )

    return fig

# -------------------------------------------------
# Sidebar
# -------------------------------------------------

st.sidebar.title("Spectre")

page = st.sidebar.radio(
    "Environment",
    [
        "Atlas",
        "Spectre Monitor",
        "Risk"
    ]
)

st.sidebar.divider()

with st.sidebar.expander("Map Layers", expanded=True):
    st.checkbox("Office Locations", value=True)
    st.checkbox("Temporary Locations", value=True)
    st.checkbox("Travelling Staff", value=True)
    st.checkbox("Airports", value=True)
    st.checkbox("Ports", value=True)

# -------------------------------------------------
# Atlas
# -------------------------------------------------

if page == "Atlas":

    st.markdown("""
    <div class="hero">
        <div class="hero-kicker">Spectre Atlas</div>
        <div class="hero-title">Live Common Intelligence Picture</div>
        <div class="hero-sub">
        Operator-approved global operational picture showing validated risks, monitored staff movements and situational awareness updates.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        metric("Active Red Risks","1","Immediate action required")
    with c2:
        metric("Active Amber Risks","1","Monitoring and assessment")
    with c3:
        metric("Informs","0","Awareness only")
    with c4:
        metric("Monitored Moves","2","Journeys being monitored")

    st.plotly_chart(build_map(), use_container_width=True)

# -------------------------------------------------
# Monitor
# -------------------------------------------------

elif page == "Spectre Monitor":

    top_left, top_right = st.columns([0.7,0.3])

    with top_left:
        st.title("Spectre Monitor")

    with top_right:
        st.button("Create Internal Event", use_container_width=True)

    st.caption("Operational monitoring and event workflow")

    left, centre, right = st.columns([1,1.5,0.9])

    workflow = events.copy()

    with left:
        st.subheader("Workflow Events")

        selected = st.radio(
            "Events",
            workflow["id"].tolist(),
            format_func=lambda x: f"{x} · {workflow.loc[workflow['id']==x,'classification'].iloc[0]} · {workflow.loc[workflow['id']==x,'city'].iloc[0]}",
            label_visibility="collapsed"
        )

        selected_event = workflow[workflow["id"] == selected].iloc[0]

        st.divider()

        st.subheader("Selected Event")

        st.markdown(pill(selected_event["classification"]), unsafe_allow_html=True)

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
                workflow[[
                    "id",
                    "origin",
                    "title",
                    "country",
                    "classification"
                ]],
                use_container_width=True,
                hide_index=True
            )

        with t2:
            st.dataframe(
                offices,
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

        st.selectbox(
            "Final Classification",
            ["Red","Amber","Inform","Discard"]
        )

        st.text_area(
            "Operator Notes",
            placeholder="Add context, validation or escalation notes..."
        )

        b1,b2,b3 = st.columns(3)

        with b1:
            st.button("Publish", use_container_width=True)

        with b2:
            st.button("Monitor", use_container_width=True)

        with b3:
            st.button("Discard", use_container_width=True)

        st.divider()

        st.subheader("Distribution")

        st.markdown(
            '<div class="small-note">Distribution drafting intentionally disabled in public prototype.</div>',
            unsafe_allow_html=True
        )

# -------------------------------------------------
# Risk
# -------------------------------------------------

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

    st.subheader("Strategic Risk Data")

    st.dataframe(
        events[[
            "id",
            "country",
            "origin",
            "classification",
            "summary"
        ]],
        use_container_width=True,
        hide_index=True
    )
