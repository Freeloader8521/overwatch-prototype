
# Overwatch Streamlit Prototype

Prototype v3 for Overwatch.

## Key changes

- Pulse renamed to **Live Common Intelligence Picture**
- Pulse only shows operator-approved/published items
- Monitor now shows AI-generated events in an operator workflow
- Red / Amber / Inform / Discard classification model moved to a small hover key in the sidebar
- Low contrast and high contrast display modes
- Map style no longer depends on a Mapbox token, improving Streamlit deployment reliability
- Dark blue high-tech Pulse styling

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
