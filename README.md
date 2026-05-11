
# Overwatch Streamlit Prototype

This is a simple dummy-data prototype for the Overwatch concept.

It includes three prototype environments:

- **Overwatch Pulse**: customer-facing global operational picture
- **Overwatch Monitor**: operator dashboard for real-time threat monitoring
- **Overwatch Risk**: strategic risk, mitigation and reporting view

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Create a new GitHub repository.
2. Upload `app.py`, `requirements.txt` and this README.
3. Go to Streamlit Community Cloud.
4. Select the repository.
5. Set the app file to `app.py`.
6. Deploy.

## Notes

This is not connected to live feeds. It uses dummy data only.

Future prototype improvements could include:

- more realistic event lifecycle states
- email advisory preview
- incident clustering
- source reliability scoring
- traveller itinerary upload
- country risk profile pages
- admin configuration for offices and distribution lists
