
# Overwatch Streamlit Prototype

Prototype v4.

## Key changes

- Pulse reduced to three main cards:
  - Active Risks
  - Monitored Moves
  - Published Updates
- Pulse map now has toggles for:
  - pulsing active risks
  - pulsing monitored moves
- Monitored moves are distinct from active risks
- Published updates show last 72 hours, split into Red / Amber / Inform
- Discarded items are not shown on Pulse
- Live risks ticker added beneath the hero panel
- Monitor retains AI-generated events workflow

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
