
# Overwatch Streamlit Prototype v8

## Changes

- Removed MIDB points counter from Monitor.
- Removed temporary locations counter from Monitor.
- Moved Selected Event beneath Events Workflow in the left column.
- Improved map markers using icon-style labels:
  - ✈ Airports
  - ⚓ Ports
  - ▣ Diplomatic outposts
  - ◇ Border crossings
  - ✚ Hospitals
  - 🏢 Offices
  - ▲ Travelling staff
  - ◆ Temporary locations
- Added operational records tabs below the map:
  - All events
  - Temporary locations
  - Monitored moves
- Added operator-generated event example.
- Kept draft distribution email.

## Note on map zoom from table clicks

Streamlit table row selection is included. Depending on Streamlit version, selecting a row may require a rerun to reflect map focus. This is enough for prototype discussion, but a production version would use a proper stateful map component.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```
