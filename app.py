import streamlit as st
import pandas as pd
import requests

st.title("GitHub JSON → CSV Converter")

github_url = st.text_input(
    "GitHub Raw JSON URL",
    placeholder="https://raw.githubusercontent.com/user/repo/main/data.json"
)

if st.button("Convert"):
    try:
        response = requests.get(github_url, timeout=30)
        response.raise_for_status()

        data = response.json()

        # Update this path based on your JSON structure
        diamonds = data.get("response", {}).get("body", {}).get("diamonds", [])

        if not diamonds:
            st.error("No data found at response.body.diamonds")
        else:
            df = pd.json_normalize(diamonds)

            st.success(
                f"Loaded {len(df):,} rows and {len(df.columns)} columns"
            )

            csv = df.to_csv(index=False)

            st.download_button(
                "Download CSV",
                csv,
                "diamonds.csv",
                "text/csv"
            )

            st.dataframe(df.head())

    except Exception as e:
        st.error(str(e))
