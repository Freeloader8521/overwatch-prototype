
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import uuid
import re
from urllib.parse import quote

st.set_page_config(page_title="Spectre", layout="wide", page_icon="◉")

# ---------------------------------------------------
# Styling
# ---------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

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

.red { background:rgba(239,68,68,.16); border:1px solid rgba(239,68,68,.35); color:#fecaca; }
.amber { background:rgba(245,158,11,.14); border:1px solid rgba(245,158,11,.35); color:#fde68a; }
.inform { background:rgba(59,130,246,.14); border:1px solid rgba(59,130,246,.35); color:#bfdbfe; }
.discard { background:rgba(100,116,139,.14); border:1px solid rgba(100,116,139,.35); color:#cbd5e1; }

.small-note {
    color:#94a3b8;
    font-size:13px;
}

.risk-card {
    border:1px solid rgba(59,130,246,.12);
    background:rgba(15,23,42,.72);
    border-radius:14px;
    padding:12px;
    margin-bottom:10px;
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
            "source_type":"External",
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
            "source_type":"Internal",
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
            "id":"OP-2001",
            "source_type":"Internal",
            "title":"Office report: access disruption",
            "country":"UAE",
            "city":"Dubai",
            "lat":25.2048,
            "lon":55.2708,
            "classification":"Amber",
            "origin":"Office phone report",
            "summary":"Access road disruption near office.",
            "published":True,
            "created":(now - timedelta(hours=3)).isoformat(),
            "status":"Published",
            "location_records":"Dubai Office | 25.2048, 55.2708"
        },
        {
            "id":"INF-1101",
            "source_type":"External",
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

if "temporary_locations" not in st.session_state:
    st.session_state.temporary_locations = [
        {"id":"TMP-001","name":"Manila Project Site","status":"Active","country":"Philippines","city":"Manila","start":"2026-05-01","end":"2026-06-30","lat":14.5995,"lon":120.9842,"notes":"Temporary project location."},
        {"id":"TMP-002","name":"Lima Field Team","status":"Active","country":"Peru","city":"Lima","start":"2026-05-10","end":"2026-05-19","lat":-12.0464,"lon":-77.0428,"notes":"Field visit location."},
        {"id":"TMP-003","name":"Lagos Election Team","status":"Archived","country":"Nigeria","city":"Lagos","start":"2026-02-10","end":"2026-03-02","lat":6.5244,"lon":3.3792,"notes":"Archived election support location."},
    ]

if "staged_route_points" not in st.session_state:
    st.session_state.staged_route_points = []


# ---------------------------------------------------
# Backwards compatibility / data normalisation
# ---------------------------------------------------

for event in st.session_state.events:
    if "source_type" not in event:
        origin = str(event.get("origin", "")).lower()
        if any(term in origin for term in ["internal", "staff", "office", "operator", "email report", "security team"]):
            event["source_type"] = "Internal"
        else:
            event["source_type"] = "External"

    if "published" not in event:
        event["published"] = False

    if "status" not in event:
        event["status"] = "Published" if event.get("published") else "Workflow"

    if "location_records" not in event:
        lat = event.get("lat", 0)
        lon = event.get("lon", 0)
        event["location_records"] = f"{event.get('city', 'Unknown')} | {lat}, {lon}"

for move in st.session_state.moves:
    if "route_points" not in move:
        move["route_points"] = [
            {"label": move.get("origin", "Origin"), "lat": 0, "lon": 0},
            {"label": move.get("destination", "Destination"), "lat": 0, "lon": 0},
        ]

for loc in st.session_state.temporary_locations:
    if "id" not in loc:
        loc["id"] = "TMP-" + str(uuid.uuid4())[:6].upper()
    if "city" not in loc:
        loc["city"] = ""
    if "lat" not in loc:
        loc["lat"] = 0.0
    if "lon" not in loc:
        loc["lon"] = 0.0
    if "notes" not in loc:
        loc["notes"] = ""

# ---------------------------------------------------
# Data
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
    {"name":"Dubai Office","lat":25.2048,"lon":55.2708},
])

midb_points = pd.DataFrame([
    {"name":"Heathrow Airport","type":"Airport","lat":51.4700,"lon":-0.4543},
    {"name":"Istanbul Airport","type":"Airport","lat":41.2753,"lon":28.7519},
    {"name":"Jomo Kenyatta International Airport","type":"Airport","lat":-1.3192,"lon":36.9278},
    {"name":"Changi Airport","type":"Airport","lat":1.3644,"lon":103.9915},
    {"name":"Madrid Barajas Airport","type":"Airport","lat":40.4983,"lon":-3.5676},
    {"name":"Port of Singapore","type":"Port","lat":1.2644,"lon":103.8222},
    {"name":"Port of Mombasa","type":"Port","lat":-4.0435,"lon":39.6682},
    {"name":"Dover Port","type":"Port","lat":51.1251,"lon":1.3338},
    {"name":"British Embassy Nairobi","type":"Diplomatic Outpost","lat":-1.2304,"lon":36.8135},
    {"name":"US Embassy London","type":"Diplomatic Outpost","lat":51.4816,"lon":-0.1271},
    {"name":"Turkey-Bulgaria Border Crossing","type":"Border Crossing","lat":41.7167,"lon":26.3500},
    {"name":"Kenya-Tanzania Border Crossing","type":"Border Crossing","lat":-2.5439,"lon":36.7906},
    {"name":"St Thomas' Hospital","type":"Hospital","lat":51.4980,"lon":-0.1187},
    {"name":"Aga Khan University Hospital","type":"Hospital","lat":-1.2625,"lon":36.8172},
])

# ---------------------------------------------------
# Helpers
# ---------------------------------------------------


def safe_dataframe(df, columns, **kwargs):
    safe = df.copy()
    for col in columns:
        if col not in safe.columns:
            safe[col] = ""
    return st.dataframe(safe[columns], **kwargs)


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

def google_maps_link(lat, lon):
    return f"https://www.google.com/maps?q={lat},{lon}"

def build_notification_email(event, final_classification, notes, recipient):
    subject = f"Spectre Notification: {final_classification} - {event['title']} - {event['country']}"
    map_link = google_maps_link(event["lat"], event["lon"])
    body = f"""Spectre Notification

Classification: {final_classification}
Source Type: {event.get('source_type', 'External')}
Event: {event['title']}
Location: {event['city']}, {event['country']}
Origin: {event['origin']}
Status: {event.get('status', 'N/A')}

Summary:
{event['summary']}

Operator notes:
{notes if notes else 'No additional operator notes added.'}

Map:
{map_link}

This notification was generated from Spectre Monitor.
"""
    mailto = f"mailto:{quote(recipient)}?subject={quote(subject)}&body={quote(body)}"
    return subject, body, mailto, map_link

def add_reference_trace(fig, df, name, colour, symbol, size=7):
    if df is None or len(df) == 0:
        return
    fig.add_trace(go.Scattergeo(
        lon=df["lon"],
        lat=df["lat"],
        mode="markers",
        name=name,
        marker=dict(size=size, color=colour, symbol=symbol, opacity=0.72, line=dict(width=0.8, color="rgba(255,255,255,.65)")),
        hovertext=df["name"],
        hovertemplate="%{hovertext}<extra></extra>"
    ))

def build_map(selected_move_id=None, extra_route=None):
    fig = go.Figure()

    df = event_display_df()
    published = df[df["published"] == True]
    colours = {"Red":"#ef4444", "Amber":"#f59e0b", "Inform":"#60a5fa"}

    # Risks are always visible.
    for level in ["Red","Amber","Inform"]:
        subset = published[published["classification"] == level]
        if len(subset) > 0:
            fig.add_trace(go.Scattergeo(
                lon=subset["lon"],
                lat=subset["lat"],
                mode="markers",
                name=f"{level} risks",
                marker=dict(size=10 if level == "Inform" else 12, color=colours[level], opacity=0.96, line=dict(width=1,color="white")),
                hovertext=subset["title"],
                hovertemplate="%{hovertext}<extra></extra>"
            ))

    # Monitored moves are always visible.
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
            line=dict(width=width, color=colour),
            marker=dict(size=7 if selected else 5, color=colour),
            opacity=opacity,
            hovertext=[p["label"] for p in points],
            hovertemplate="%{hovertext}<extra></extra>"
        ))

    # Toggleable corporate exposure layers.
    if show_offices:
        add_reference_trace(fig, offices, "Office locations", "#38bdf8", "square", size=7)

    tmp = pd.DataFrame(st.session_state.temporary_locations)
    if show_temp_active:
        add_reference_trace(fig, tmp[tmp["status"] == "Active"], "Temporary locations: active", "#14b8a6", "diamond", size=8)
    if show_temp_archived:
        add_reference_trace(fig, tmp[tmp["status"] == "Archived"], "Temporary locations: archived", "#64748b", "diamond-open", size=7)

    # Toggleable MIDB reference layers.
    if show_airports:
        add_reference_trace(fig, midb_points[midb_points["type"] == "Airport"], "Airports", "#94a3b8", "triangle-up", size=7)
    if show_ports:
        add_reference_trace(fig, midb_points[midb_points["type"] == "Port"], "Ports", "#94a3b8", "circle-open", size=7)
    if show_borders:
        add_reference_trace(fig, midb_points[midb_points["type"] == "Border Crossing"], "Border crossings", "#94a3b8", "cross", size=7)
    if show_diplomatic:
        add_reference_trace(fig, midb_points[midb_points["type"] == "Diplomatic Outpost"], "Diplomatic outposts", "#94a3b8", "star", size=8)
    if show_hospitals:
        add_reference_trace(fig, midb_points[midb_points["type"] == "Hospital"], "Hospitals", "#94a3b8", "x", size=7)

    # Staged route is optional but visible when building a move.
    if extra_route:
        fig.add_trace(go.Scattergeo(
            lon=[p["lon"] for p in extra_route],
            lat=[p["lat"] for p in extra_route],
            mode="lines+markers",
            name="Staged route",
            line=dict(width=3, color="#67e8f9", dash="dot"),
            marker=dict(size=9, color="#e0f2fe", symbol="circle-open"),
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

if st.sidebar.button("Reset demo data"):
    for key in ["events", "moves", "temporary_locations", "staged_route_points"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

page = st.sidebar.radio("Workspace", ["COP", "Monitor", "Risk"])

st.sidebar.divider()
with st.sidebar.expander("Map Layers", expanded=True):
    st.caption("Risks and monitored moves are always visible.")

    st.markdown("**Corporate exposure**")
    show_offices = st.checkbox("Office locations", value=True)
    show_temp_active = st.checkbox("Temporary locations: active", value=True)
    show_temp_archived = st.checkbox("Temporary locations: archived", value=False)

    st.markdown("**MIDB reference layers**")
    show_airports = st.checkbox("Airports", value=False)
    show_ports = st.checkbox("Ports", value=False)
    show_borders = st.checkbox("Border crossings", value=False)
    show_diplomatic = st.checkbox("Diplomatic outposts", value=False)
    show_hospitals = st.checkbox("Hospitals", value=False)

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
        <div class="hero-sub">Validated operational picture displaying published risks and monitored moves.</div>
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
        selected_move = st.selectbox("Select move", ["None"] + move_table["Move ID"].tolist())
        if selected_move == "None":
            selected_move = None

    map_col, rail_col = st.columns([0.72, 0.28])

    with map_col:
        st.plotly_chart(build_map(selected_move_id=selected_move), use_container_width=True)

    with rail_col:
        st.subheader("Active Risks")
        if len(published) == 0:
            st.info("No active risks.")
        else:
            for _, risk in published.iterrows():
                colour = {"Red":"#ef4444", "Amber":"#f59e0b", "Inform":"#60a5fa"}.get(risk["classification"], "#94a3b8")
                action_text = {"Red":"Action underway", "Amber":"Monitoring and assessment", "Inform":"Awareness only"}.get(risk["classification"], "Monitoring")
                st.markdown(f"""
                <div class="risk-card" style="border-left:4px solid {colour};">
                    <div style="color:{colour}; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:.08em;">
                        {risk['classification']} · {risk.get('source_type','External')}
                    </div>
                    <div style="color:white; font-weight:700; margin-top:4px;">{risk['city']}, {risk['country']}</div>
                    <div style="color:#cbd5e1; font-size:13px; margin-top:4px;">{risk['title']}</div>
                    <div style="color:#94a3b8; font-size:12px; margin-top:8px;">Action: {action_text}</div>
                </div>
                """, unsafe_allow_html=True)

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
        with st.popover("Create Internal Event"):
            st.markdown("### Create Internal Event")
            st.caption("Create an operator-originated event. It can be published immediately or held in workflow.")

            with st.form("create_internal_event_form"):
                title = st.text_input("Event title", placeholder="e.g. Office report: protest near main entrance")
                country = st.text_input("Country", placeholder="e.g. Kenya")
                city = st.text_input("City", placeholder="e.g. Nairobi")
                classification = st.selectbox("Classification", ["Red", "Amber", "Inform"])
                origin = st.selectbox("Origin", ["Operator report", "Office phone report", "Staff alert", "Email report", "Security team report"])
                summary = st.text_area("Summary", placeholder="Brief operational summary...")
                coord = st.text_input("Primary coordinate or known place", placeholder="e.g. Nairobi or -1.2864, 36.8172")
                publish_now = st.checkbox("Publish immediately to COP", value=True)

                submitted = st.form_submit_button("Create internal event", type="primary")
                if submitted:
                    point, err = resolve_point(coord, label=city if city else "Internal event location")
                    if not title or not country or not city or not summary:
                        st.error("Add title, country, city and summary.")
                    elif not point:
                        st.error(err)
                    else:
                        new_event = {
                            "id": "INT-" + str(uuid.uuid4())[:6].upper(),
                            "source_type": "Internal",
                            "title": title,
                            "country": country,
                            "city": city,
                            "lat": point["lat"],
                            "lon": point["lon"],
                            "classification": classification,
                            "origin": origin,
                            "summary": summary,
                            "published": publish_now,
                            "created": datetime.utcnow().isoformat(),
                            "status": "Published" if publish_now else "Workflow",
                            "location_records": f"{point['label']} | {point['lat']:.6f}, {point['lon']:.6f} | Source: {point['source']}"
                        }
                        st.session_state.events.append(new_event)
                        st.success("Internal event created.")
                        st.rerun()

    workflow = pd.DataFrame([e for e in st.session_state.events if e["published"] == False])
    if len(workflow) == 0:
        workflow = pd.DataFrame([st.session_state.events[0]])

    left, centre, right = st.columns([1,1.5,0.9])

    with left:
        st.subheader("Workflow Events")
        selected = st.radio("Events", workflow["id"].tolist(), label_visibility="collapsed")
        selected_event = workflow[workflow["id"] == selected].iloc[0]

        st.divider()
        st.subheader("Selected Event")
        st.markdown(pill(selected_event["classification"]), unsafe_allow_html=True)
        st.markdown(f"### {selected_event['title']}")
        st.write(f"**Source:** {selected_event.get('source_type','External')} · {selected_event['origin']}")
        st.write(f"**Location:** {selected_event['city']}, {selected_event['country']}")
        st.markdown(f'<div class="small-note">{selected_event["summary"]}</div>', unsafe_allow_html=True)

    with centre:
        st.subheader("Operational Map")
        st.plotly_chart(build_map(extra_route=st.session_state.staged_route_points), use_container_width=True)

        t1,t2,t3 = st.tabs(["All Events","Locations","Monitored Moves"])

        with t1:
            safe_dataframe(
                pd.DataFrame(st.session_state.events),
                ["id","source_type","origin","title","country","classification","status","published"],
                use_container_width=True,
                hide_index=True
            )

        with t2:
            st.markdown("##### Offices")
            st.dataframe(offices, use_container_width=True, hide_index=True)

            st.markdown("##### Temporary Locations")
            loc_tab1, loc_tab2, loc_tab3 = st.tabs(["Active", "Archived", "Add / Edit / Archive"])

            temporary_locations = pd.DataFrame(st.session_state.temporary_locations)

            with loc_tab1:
                st.dataframe(temporary_locations[temporary_locations["status"] == "Active"], use_container_width=True, hide_index=True)

            with loc_tab2:
                st.dataframe(temporary_locations[temporary_locations["status"] == "Archived"], use_container_width=True, hide_index=True)

            with loc_tab3:
                existing_names = ["Create new"] + [x["name"] for x in st.session_state.temporary_locations]
                selected_location_name = st.selectbox("Location record", existing_names)
                existing = None
                if selected_location_name != "Create new":
                    existing = next((x for x in st.session_state.temporary_locations if x["name"] == selected_location_name), None)

                with st.form("temporary_location_management_form"):
                    loc_name = st.text_input("Location name", value=existing["name"] if existing else "")
                    loc_country = st.text_input("Country", value=existing["country"] if existing else "")
                    loc_city = st.text_input("City", value=existing.get("city", "") if existing else "")
                    c1, c2 = st.columns(2)
                    with c1:
                        loc_start = st.text_input("Start date", value=existing["start"] if existing else "2026-05-14")
                        loc_lat = st.number_input("Latitude", value=float(existing["lat"]) if existing else 0.0, format="%.6f")
                    with c2:
                        loc_end = st.text_input("End date", value=existing["end"] if existing else "2026-05-21")
                        loc_lon = st.number_input("Longitude", value=float(existing["lon"]) if existing else 0.0, format="%.6f")
                    loc_status = st.selectbox("Status", ["Active", "Archived"], index=0 if not existing or existing["status"] == "Active" else 1)
                    loc_notes = st.text_area("Notes", value=existing.get("notes", "") if existing else "")
                    save_location = st.form_submit_button("Save location", type="primary")

                    if save_location:
                        if not loc_name or not loc_country or not loc_city:
                            st.error("Add name, country and city.")
                        else:
                            if existing:
                                for x in st.session_state.temporary_locations:
                                    if x["id"] == existing["id"]:
                                        x.update({"name": loc_name, "country": loc_country, "city": loc_city, "start": loc_start, "end": loc_end, "lat": loc_lat, "lon": loc_lon, "status": loc_status, "notes": loc_notes})
                                st.success("Temporary location updated.")
                            else:
                                st.session_state.temporary_locations.append({"id": "TMP-" + str(uuid.uuid4())[:6].upper(), "name": loc_name, "country": loc_country, "city": loc_city, "start": loc_start, "end": loc_end, "lat": loc_lat, "lon": loc_lon, "status": loc_status, "notes": loc_notes})
                                st.success("Temporary location created.")
                            st.rerun()

                if existing:
                    c_archive, c_restore = st.columns(2)
                    with c_archive:
                        if st.button("Archive selected location", use_container_width=True):
                            for x in st.session_state.temporary_locations:
                                if x["id"] == existing["id"]:
                                    x["status"] = "Archived"
                            st.success("Location archived.")
                            st.rerun()
                    with c_restore:
                        if st.button("Restore selected location", use_container_width=True):
                            for x in st.session_state.temporary_locations:
                                if x["id"] == existing["id"]:
                                    x["status"] = "Active"
                            st.success("Location restored.")
                            st.rerun()

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
                    st.session_state.pending_move = {"traveller":traveller, "origin":origin, "destination":destination, "start_dtg":start_dtg, "end_dtg":end_dtg, "return_trip":return_trip, "poc":poc, "status":status, "mode":mode}
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
                bulk = st.text_area("Bulk route paste", placeholder="Origin, 51.4700, -0.4543\nTransit, 41.2753, 28.7519\nDestination, -1.3192, 36.9278\n\nOr use known places:\nHeathrow\nIstanbul Airport\nNairobi Airport", height=150)
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
                            st.session_state.moves.append({"id":"MOV-" + str(uuid.uuid4())[:6].upper(), "traveller":pending["traveller"], "origin":pending["origin"], "destination":pending["destination"], "start_dtg":pending["start_dtg"], "end_dtg":pending["end_dtg"], "return_trip":pending["return_trip"], "poc":pending["poc"], "status":pending["status"], "mode":pending["mode"], "route_points":st.session_state.staged_route_points.copy()})
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

        st.divider()
        st.subheader("Notification Email")
        recipient = st.text_input("Recipient / distribution list", placeholder="e.g. country-security-distribution@example.com")
        if recipient:
            subject, body, mailto, map_link = build_notification_email(selected_event, classification, notes, recipient)
            st.write(f"Subject: `{subject}`")
            st.markdown(f"[Open event map]({map_link})")
            st.markdown(f"[Open email draft]({mailto})")
            with st.expander("Preview notification email"):
                st.text(body)
        else:
            st.caption("Enter a recipient or distribution list to generate a mailto draft.")

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
        safe_dataframe(
            archive,
            ["id","source_type","title","country","origin","classification","created","summary"],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No published events archived yet.")

    st.subheader("Monitored Move Archive")
    st.dataframe(moves_df(), use_container_width=True, hide_index=True)

    st.subheader("MIDB Reference Coverage")
    st.dataframe(midb_points, use_container_width=True, hide_index=True)
