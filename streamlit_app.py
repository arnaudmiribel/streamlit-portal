import os
import subprocess
import time

import streamlit as st
from streamlit.components.v1 import html, iframe
from streamlit_kickoff_cli.list.command import get_list

title = "Streamlit Local Portal"
st.set_page_config(page_icon="🖲", page_title=title)


browser_mockup_css = """
<style>
.browser-mockup {
  border-top: 2em solid rgba(230, 230, 230, 0.7);
  box-shadow: 0 0.1em 1em 0 rgba(0, 0, 0, 0.4);
  position: relative;
  border-radius: 3px 3px 0 0
}

.browser-mockup:before {
  display: block;
  position: absolute;
  content: '';
  top: -1.25em;
  left: 1em;
  width: 0.5em;
  height: 0.5em;
  border-radius: 50%;
  background-color: #f44;
  box-shadow: 0 0 0 2px #f44, 1.5em 0 0 2px #9b3, 3em 0 0 2px #fb5;
}

.browser-mockup.with-tab:after {
  display: block;
  position: absolute;
  content: '';
  top: -2em;
  left: 5.5em;
  width: 20%;
  height: 0em;
  border-bottom: 2em solid white;
  border-left: 0.8em solid transparent;
  border-right: 0.8em solid transparent;
}

.browser-mockup.with-url:after {
  display: block;
  position: absolute;
  content: '';
  top: -1.6em;
  left: 5.5em;
  width: calc(100% - 6em);
  height: 1.2em;
  border-radius: 2px;
  background-color: white;
}

.browser-mockup > * {
  display: block;
}

</style>
"""


def get_app_directory(pid: str) -> str:

    lsof = subprocess.check_output(
        f"lsof -p {pid} | grep cwd",
        shell=True,
        stderr=subprocess.STDOUT,
    )

    return lsof.split()[-1].decode("utf-8")


def get_apps_metadata():
    apps_list = get_list()
    paths = list()
    for _, row in apps_list.iterrows():
        pid = row.T["App ID"]
        paths.append(get_app_directory(pid))
    apps_list["App directory"] = paths
    return apps_list.sort_values(by="App URL", ascending=True)


st.title("🖲 " + title)

st.write("### 🟢 Running apps")
apps_list = get_apps_metadata().drop_duplicates(subset="App URL")

num_apps = len(apps_list)
st.markdown(
    f"""Running **{num_apps}** Streamlit app{'s' if num_apps > 1 else ''} locally."""
)

for _, row in apps_list.iterrows():
    url = row.T["App URL"]
    port = int(url.split(":")[-1])
    pid = row.T["App ID"]
    directory = row.T["App directory"]
    if port == 8500:
        expander_title = f"{directory.split('/')[-1]} **[this app]** - {url} - {pid}"
    else:
        expander_title = f"{directory.split('/')[-1]} - {url} - {pid}"

    with st.expander(expander_title, expanded=False):
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"[Open in browser]({url})")
        open_code = col2.button("Open code", key=f"code_{pid}")
        kill = col3.button("Kill app", key=f"kill_{pid}")
        kill_status = col3.empty()
        st.caption("Preview app:")
        left, middle, right = st.columns((1, 4, 1))
        with middle:
            html(
                browser_mockup_css
                + '<div class="browser-mockup"><iframe src="{}" style="width:100%; border:none; height:300px;"> </iframe></div>'.format(
                    url
                ),
                height=300,
            )
        # iframe(url, height=300)
        if open_code:
            os.system(f"code {directory} --new-window")
        if kill:
            kill_status.text("Killing app...")
            time.sleep(2)
            os.system(f"kill -9 {pid}")
            kill_status.text("Killed app! Restarting...")
            time.sleep(2)
            st.experimental_rerun()
