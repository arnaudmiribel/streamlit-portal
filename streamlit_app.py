import os

import time

import streamlit as st
from utils.ui import open_vs_code, show_app_in_browser
from utils.metadata import get_apps_metadata

title = "Streamlit Local Portal"
st.set_page_config(page_icon="🖲", page_title=title)

st.title("🖲 " + title)

st.write("#### 🟢 Running apps")
apps_df = get_apps_metadata()

num_apps = len(apps_df)
st.caption(
    f"""Found **{num_apps}** Streamlit app{'s' if num_apps > 1 else ''} running locally."""
)

for _, row in apps_df.iterrows():
    row_dict = row.to_dict()
    url = row_dict.get("App URL").strip()
    port = int(row_dict.get("PORT").strip())
    process_id = row_dict.get("App ID")
    directory_path = row_dict.get("App directory")
    directory_name = directory_path.split("/")[-1]

    if directory_name == "streamlit-portal" and port == 8500:
        expander_title = f"{directory_name} **[this app]** - {url} - {process_id}"
    else:
        expander_title = f"{directory_name} - {url} - {process_id}"

    with st.expander(expander_title, expanded=False):

        col1, col2, col3 = st.columns(3)
        col1.link_button(
            "Open in browser 🌐",
            url,
            use_container_width=True,
        )
        code_button = col2.button(
            "Open code 👨‍💻",
            key=f"code_{process_id}",
            use_container_width=True,
        )
        kill_button = col3.button(
            "Kill 🔫",
            key=f"kill_{process_id}",
            use_container_width=True,
        )

        kill_status = col3.empty()

        show_app_in_browser(url)

        if code_button:
            open_vs_code(directory_path)

        if kill_button:
            kill_status.text("Killing app...")
            time.sleep(1)
            os.system(f"kill -9 {process_id}")
            kill_status.text("Killed app! Restarting...")
            time.sleep(1)
            st.rerun()
