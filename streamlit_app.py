import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(page_title="Synchrony Dashboard Demo", layout="wide")

st.title("Synchrony Monitor Demo")


np.random.seed(42)

times = np.linspace(0, 120, 200)  

scores = 0.4 * np.sin(times / 8) + 0.1 * np.random.randn(len(times))

threshold = 0.0

col_video, col_status = st.columns([2, 1])


with col_video:
    st.subheader("Counselling Session")
    st.markdown(
        """
        <div style="border-radius:12px;border:2px solid #444;height:360px;
                    display:flex;align-items:center;justify-content:center;
                    color:#777;font-size:20px;">
            Remote counselling video stream
        </div>
        """,
        unsafe_allow_html=True,
    )


with col_status:
    st.subheader("Synchrony Monitor")

    current_time = st.slider(
        "Session time (seconds)",
        float(times[0]),
        float(times[-1]),
        float(times[0]),
        step=float((times[-1] - times[0]) / 200),
    )


    idx = int(np.argmin(np.abs(times - current_time)))
    current_score = float(scores[idx])

    
    st.metric("Current synchrony score", f"{current_score:.3f}")

    
    if current_score < threshold:
        st.error(f"Low synchrony!")
    else:
        st.success("Synchrony within safe range :)")



st.subheader("Synchrony over time")

sync_df = pd.DataFrame({"Time (s)": times, "Synchrony score": scores})

base = alt.Chart(sync_df).mark_line().encode(
    x="Time (s):Q",
    y="Synchrony score:Q"
)

current_line = alt.Chart(
    pd.DataFrame({"Time (s)": [current_time]})
).mark_rule(color="red").encode(x="Time (s):Q")

st.altair_chart(base + current_line, use_container_width=True)
