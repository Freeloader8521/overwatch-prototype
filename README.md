
# Overwatch Streamlit Prototype v6

This version rebuilds the map with Plotly rather than PyDeck to improve reliability on Streamlit.

## Included

- Overwatch Pulse
- Overwatch Monitor
- Overwatch Risk
- Plotly global map
- Office locations
- Temporary locations
- Travelling staff locations
- MIDB-style reference layers:
  - Airports
  - Diplomatic outposts
  - Border crossings
  - Ports
  - Hospitals
- Temporary location management panel
- AI-generated and internal event workflow
- Published Pulse view

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy

Upload these files to GitHub and Streamlit should redeploy automatically:

- app.py
- requirements.txt
- README.md
