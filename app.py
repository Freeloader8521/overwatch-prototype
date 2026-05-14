
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import uuid
import re

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

.discard {
    background:rgba(100,116,139,.14);
    border:1px solid rgba(100,116,139,.35);
    color:#cbd5e1;
}

.small-note {
    color:#94a3b8;
    font-size:13px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Session State
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
            "status":"Workflow",
            "location_records":"Istanbul Airport | 41.2753, 28.7519"
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
            "status":"Published",
            "location_records":"Singapore | 1.3521, 103.8198"
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
            "status":"Published",
            "location_records":"Berlin | 52.5200, 13.4000"
        }
    ]

if "moves" not in st.session_state:
    st.session_state.moves = [
        {
            "id":"MOV-001",
            "traveller":"Traveller A",
            "origin":"London Heathrow",
            "destination":"Nairobi",
            "start_dtg":"2026-05-14 0800Z",
            "end_dtg":"2026-05-15 1800Z",
            "return_trip":"Yes",
            "poc":"Regional Security Manager EMEA",
            "status":"Active",
            "mode":"Air",
            "route_points":[
                {"label":"London Heathrow","lat":51.4700,"lon":-0.4543},
                {"label":"Istanbul Airport","lat":41.2753,"lon":28.7519},
                {"label":"Nairobi Airport","lat":-1.3192,"lon":36.9278},
            ]
        },
        {
            "id":"MOV-002",
            "traveller":"Traveller B",
            "origin":"Dubai",
            "destination":"Singapore",
            "start_dtg":"2026-05-14 2200Z",
            "end_dtg":"2026-05-15 0900Z",
            "return_trip":"No",
            "poc":"APAC Duty Manager",
            "status":"Active",
            "mode":"Air",
            "route_points":[
                {"label":"Dubai","lat":25.2048,"lon":55.2708},
                {"label":"Changi Airport","lat":1.3644,"lon":103.9915},
            ]
        }
    ]

if "staged_route_points" not in st.session_state:
    st.session_state.staged_route_points = []

if "staged_locations" not in st.session_state:
    st.session_state.staged_locations = []

# ---------------------------------------------------
# Reference lookups
# ---------------------------------------------------

KNOWN_LOCATIONS = {
    "london": {"label":"London", "lat":51.5072, "lon":-0.1276},
    "heathrow": {"label":"London Heathrow", "lat":51.4700, "lon":-0.4543},
    "istanbul airport": {"label":"Istanbul Airport", "lat":41.2753, "lon":28.7519},
    "nairobi": {"label":"Nairobi", "lat":-1.2864, "lon":36.8172},
    "nairobi airport": {"label":"Nairobi Airport", "lat":-1.3192, "lon":36.9278},
    "singapore": {"label":"Singapore", "lat":1.3521, "lon":103.8198},
    "changi": {"label":"Changi Airport", "lat":1.3644, "lon":103.9915},
    "dubai": {"label":"Dubai", "lat":25.2048, "lon":55.2708},
    "manila": {"label":"Manila", "lat":14.5995, "lon":120.9842},
    "berlin": {"label":"Berlin", "lat":52.5200, "lon":13.4050},
    "madrid": {"label":"Madrid Barajas Airport", "lat":40.4983, "lon":-3.5676},
}

offices = pd.DataFrame([
    {"name":"London Office","lat":51.5072,"lon":-0.1276},
    {"name":"Singapore Office","lat":1.3521,"lon":103.8198},
    {"name":"Nairobi Office","lat":-1.2864,"lon":36.8172},
])

temporary_locations = pd.DataFrame([
    {"name":"Manila Project Site","status":"Active","country":"Philippines","start":"2026-05-01","end":"2026-06-30"},
    {"name":"Lima Field Team","status":"Active","country":"Peru","start":"2026-05-10","end":"2026-05-19"},
    {"name":"Lagos Election Team","status":"Archived","country":"Nigeria","start":"2026-02-10","end":"2026-03-02"},
])

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

def parse_latlon(text):
    nums = re.findall(r"-?\d+(?:\.\d+)?", text)
    if len(nums) >= 2:
        lat = float(nums[0])
        lon = float(nums[1])
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return lat, lon
    return None

def resolve_point(raw_text, label="Route point"):
    raw = raw_text.strip()
    if not raw:
        return None, "No location entered."

    latlon = parse_latlon(raw)
    if latlon:
        lat, lon = latlon
        return {"label":label, "lat":lat, "lon":lon, "source":raw}, None

    match = KNOWN_LOCATIONS.get(raw.lower())
    if match:
        return {"label":match["label"], "lat":match["lat"], "lon":match["lon"], "source":raw}, None

    return None, "Could not resolve. Try lat/long or known dummy places like Heathrow, Istanbul Airport, Nairobi Airport, Changi, Dubai, Berlin."

def parse_bulk_route(text):
    points = []
    errors = []

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for idx, line in enumerate(lines, start=1):
        parts = [p.strip() for p in line.split(",")]
        if len(parts) >= 3:
            label = parts[0]
            candidate = f"{parts[1]}, {parts[2]}"
        elif len(parts) == 2:
            label = f"Point {idx}"
            candidate = f"{parts[0]}, {parts[1]}"
        else:
            label = f"Point {idx}"
            candidate = parts[0]

        point, err = resolve_point(candidate, label=label)
        if point:
            if len(parts) >= 3:
                point["label"] = label
            points.append(point)
        else:
            errors.append({"line":idx, "input":line, "error":err})
    return points, errors

def event_display_df():
    df = pd.DataFrame(st.session_state.events)
    now = datetime.utcnow()
    rows = []

    for _, row in df.iterrows():
        created = datetime.fromisoformat(row["created"])
        if row["classification"] == "Inform":
            if now - created < timedelta(hours=12):
                rows.append(row)
        else:
            rows.append(row)
    return pd.DataFrame(rows)

def moves_df():
    rows = []
    for move in st.session_state.moves:
        rows.append({
            "Move ID":move["id"],
            "Traveller / Team":move["traveller"],
            "Origin":move["origin"],
            "Destination":move["destination"],
            "Start DTG":move["start_dtg"],
            "End DTG":move["end_dtg"],
            "Return Trip":move["return_trip"],
            "Mode":move["mode"],
            "Status":move["status"],
            "Point of Contact":move["poc"],
        })
    return pd.DataFrame(rows)

def build_map(selected_move_id=None, extra_route=None):
    fig = go.Figure()

    df = event_display_df()
    published = df[df["published"] == True]

    colours = {"Red":"#ef4444", "Amber":"#f59e0b", "Inform":"#60a5fa"}

    for level in ["Red","Amber","Inform"]:
        subset = published[published["classification"] == level]
        if len(subset) > 0:
            fig.add_trace(go.Scattergeo(
                lon=subset["lon"],
                lat=subset["lat"],
                mode="markers",
                name=f"{level} risks",
                marker=dict(
                    size=10 if level == "Inform" else 12,
                    color=colours[level],
                    opacity=0.96,
                    line=dict(width=1,color="white")
                ),
                hovertext=subset["title"],
                hovertemplate="%{hovertext}<extra></extra>"
            ))

    # Offices
    fig.add_trace(go.Scattergeo(
        lon=offices["lon"],
        lat=offices["lat"],
        mode="markers",
        name="Offices",
        marker=dict(size=8,color="#38bdf8",symbol="square",opacity=.72),
        hovertext=offices["name"],
        hovertemplate="%{hovertext}<extra></extra>"
    ))

    # Move routes
    for move in st.session_state.moves:
        points = move["route_points"]
        selected = selected_move_id == move["id"]
        width = 3 if selected else 1.4
        opacity = 0.95 if selected else 0.42
        colour = "#a78bfa" if selected else "#64748b"

        fig.add_trace(go.Scattergeo(
            lon=[p["lon"] for p in points],
            lat=[p["lat"] for p in points],
            mode="lines+markers",
            name=f"Move {move['id']}",
            line=dict(width=width,color=colour),
            marker=dict(size=7 if selected else 5,color=colour),
            opacity=opacity,
            hovertext=[p["label"] for p in points],
            hovertemplate="%{hovertext}<extra></extra>"
        ))

    if extra_route:
        fig.add_trace(go.Scattergeo(
            lon=[p["lon"] for p in extra_route],
            lat=[p["lat"] for p in extra_route],
            mode="lines+markers",
            name="Staged route",
            line=dict(width=3,color="#67e8f9",dash="dot"),
            marker=dict(size=9,color="#e0f2fe",symbol="circle-open"),
            hovertext=[p["label"] for p in extra_route],
            hovertemplate="%{hovertext}<extra></extra>"
        ))

    center = dict(lat=18, lon=20)
    scale = 1

    if selected_move_id:
        move = next((m for m in st.session_state.moves if m["id"] == selected_move_id), None)
        if move:
            lats = [p["lat"] for p in move["route_points"]]
            lons = [p["lon"] for p in move["route_points"]]
            center = dict(lat=sum(lats)/len(lats), lon=sum(lons)/len(lons))
            scale = 2.4

    fig.update_geos(
        projection_type="natural earth",
        center=center,
        projection_scale=scale,
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
        height=540,
        margin=dict(l=0,r=0,t=0,b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dbe7f5"),
        legend=dict(orientation="h",y=-0.06,x=0.5,xanchor="center")
    )

    return fig

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

st.sidebar.title("Spectre")

page = st.sidebar.radio(
    "Workspace",
    ["COP", "Monitor", "Risk"]
)

# ---------------------------------------------------
# COP
# ---------------------------------------------------

if page == "COP":
    df = event_display_df()
    published = df[df["published"] == True]

    red_count = len(published[published["classification"] == "Red"])
    amber_count = len(published[published["classification"] == "Amber"])
    inform_count = len(published[published["classification"] == "Inform"])

    st.markdown("""
    <div class="hero">
        <div class="hero-kicker">Spectre COP</div>
        <div class="hero-title">Common Operations Picture</div>
        <div class="hero-sub">
        Validated operational picture displaying published risks and monitored moves.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)
    with c1:
        metric("Active Red Risks", red_count, "Immediate action required")
    with c2:
        metric("Active Amber Risks", amber_count, "Monitoring and assessment")
    with c3:
        metric("Informs", inform_count, "Awareness only")

    st.divider()

    st.subheader("Operational Map")

    move_table = moves_df()
    selected_move = None

    with st.expander("Focus map on monitored move"):
        selected_move = st.selectbox(
            "Select move",
            ["None"] + move_table["Move ID"].tolist()
        )
        if selected_move == "None":
            selected_move = None

    st.plotly_chart(build_map(selected_move_id=selected_move), use_container_width=True)

    st.subheader("Monitored Moves")
    st.caption("Read-only view of active monitored journeys. Managed in Monitor.")
    st.dataframe(move_table, use_container_width=True, hide_index=True)

# ---------------------------------------------------
# Monitor
# ---------------------------------------------------

elif page == "Monitor":
    st.title("Monitor")
    st.caption("Operational event workflow, location management and monitored move management.")

    top_left, top_right = st.columns([0.7, 0.3])
    with top_right:
        create_internal = st.popover("Create Internal Event")
        with create_internal:
            st.write("Internal event creation remains available here. Use the move-management section below for monitored travel.")

    workflow = pd.DataFrame([e for e in st.session_state.events if e["published"] == False])
    if len(workflow) == 0:
        workflow = pd.DataFrame([st.session_state.events[0]])

    left, centre, right = st.columns([1,1.5,0.9])

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
        st.markdown(pill(selected_event["classification"]), unsafe_allow_html=True)
        st.markdown(f"### {selected_event['title']}")
        st.write(f"**Origin:** {selected_event['origin']}")
        st.write(f"**Location:** {selected_event['city']}, {selected_event['country']}")
        st.markdown(f'<div class="small-note">{selected_event["summary"]}</div>', unsafe_allow_html=True)

    with centre:
        st.subheader("Operational Map")
        st.plotly_chart(build_map(extra_route=st.session_state.staged_route_points), use_container_width=True)

        t1,t2,t3 = st.tabs(["All Events","Locations","Monitored Moves"])

        with t1:
            st.dataframe(pd.DataFrame(st.session_state.events)[["id","origin","title","country","classification","status","published"]], use_container_width=True, hide_index=True)

        with t2:
            st.markdown("##### Offices")
            st.dataframe(offices, use_container_width=True, hide_index=True)
            st.markdown("##### Temporary Locations")
            st.dataframe(temporary_locations, use_container_width=True, hide_index=True)

        with t3:
            st.dataframe(moves_df(), use_container_width=True, hide_index=True)

            st.divider()
            st.markdown("### Add / Edit Monitored Move")

            with st.form("move_details"):
                traveller = st.text_input("Traveller / Team")
                origin = st.text_input("Origin")
                destination = st.text_input("Destination")
                c1,c2 = st.columns(2)
                with c1:
                    start_dtg = st.text_input("Start DTG", placeholder="2026-05-14 0800Z")
                    return_trip = st.selectbox("Return Trip", ["No","Yes"])
                    mode = st.selectbox("Mode", ["Air","Road","Rail","Maritime","Mixed"])
                with c2:
                    end_dtg = st.text_input("End DTG", placeholder="2026-05-15 1800Z")
                    poc = st.text_input("Point of Contact")
                    status = st.selectbox("Status", ["Planned","Active","Completed","Cancelled"])
                saved_move_details = st.form_submit_button("Stage move details")
                if saved_move_details:
                    st.session_state.pending_move = {
                        "traveller":traveller,
                        "origin":origin,
                        "destination":destination,
                        "start_dtg":start_dtg,
                        "end_dtg":end_dtg,
                        "return_trip":return_trip,
                        "poc":poc,
                        "status":status,
                        "mode":mode,
                    }
                    st.success("Move details staged. Add route points below.")

            st.markdown("#### Route Coordinates")
            route_input_mode = st.radio("Input method", ["Single point", "Bulk route paste"], horizontal=True)

            if route_input_mode == "Single point":
                label = st.text_input("Point label", value="Route point")
                point_input = st.text_input("Point coordinate or known place", placeholder="e.g. Heathrow or 51.4700, -0.4543")
                if st.button("Add route point"):
                    point, err = resolve_point(point_input, label=label)
                    if point:
                        st.session_state.staged_route_points.append(point)
                        st.success("Route point added.")
                    else:
                        st.error(err)

            else:
                bulk = st.text_area(
                    "Bulk route paste",
                    placeholder="Origin, 51.4700, -0.4543\nTransit, 41.2753, 28.7519\nDestination, -1.3192, 36.9278\n\nOr use known places:\nHeathrow\nIstanbul Airport\nNairobi Airport",
                    height=150
                )
                if st.button("Resolve bulk route"):
                    points, errors = parse_bulk_route(bulk)
                    st.session_state.staged_route_points.extend(points)
                    if points:
                        st.success(f"{len(points)} route point(s) added.")
                    if errors:
                        st.warning("Some lines could not be resolved.")
                        st.dataframe(pd.DataFrame(errors), use_container_width=True, hide_index=True)

            if st.session_state.staged_route_points:
                st.markdown("#### Staged Route Points")
                st.dataframe(pd.DataFrame(st.session_state.staged_route_points), use_container_width=True, hide_index=True)

                c1,c2 = st.columns(2)
                with c1:
                    if st.button("Clear staged route"):
                        st.session_state.staged_route_points = []
                        st.rerun()
                with c2:
                    if st.button("Create monitored move", type="primary"):
                        pending = st.session_state.get("pending_move")
                        if not pending:
                            st.error("Stage move details first.")
                        elif len(st.session_state.staged_route_points) < 2:
                            st.error("Add at least an origin and destination point.")
                        else:
                            st.session_state.moves.append({
                                "id":"MOV-" + str(uuid.uuid4())[:6].upper(),
                                "traveller":pending["traveller"],
                                "origin":pending["origin"],
                                "destination":pending["destination"],
                                "start_dtg":pending["start_dtg"],
                                "end_dtg":pending["end_dtg"],
                                "return_trip":pending["return_trip"],
                                "poc":pending["poc"],
                                "status":pending["status"],
                                "mode":pending["mode"],
                                "route_points":st.session_state.staged_route_points.copy()
                            })
                            st.session_state.staged_route_points = []
                            st.session_state.pending_move = None
                            st.success("Monitored move created.")
                            st.rerun()

    with right:
        st.subheader("Operator Decision")
        classification = st.selectbox("Final Classification", ["Red","Amber","Inform","Discard"])
        notes = st.text_area("Operator Notes", placeholder="Add context or escalation notes...")

        if st.button("Publish", use_container_width=True):
            for e in st.session_state.events:
                if e["id"] == selected_event["id"]:
                    e["published"] = True
                    e["classification"] = classification
                    e["status"] = "Published"
            st.success("Event published to COP.")

        if st.button("Monitor", use_container_width=True):
            for e in st.session_state.events:
                if e["id"] == selected_event["id"]:
                    e["status"] = "Monitoring"
            st.success("Event retained in workflow.")

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
    archive = pd.DataFrame([e for e in st.session_state.events if e["published"] == True])
    if len(archive) > 0:
        st.dataframe(archive[["id","title","country","origin","classification","created","summary"]], use_container_width=True, hide_index=True)
    else:
        st.info("No published events archived yet.")

    st.subheader("Monitored Move Archive")
    st.dataframe(moves_df(), use_container_width=True, hide_index=True)
