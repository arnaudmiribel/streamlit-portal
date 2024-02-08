import subprocess
from streamlit_kickoff_cli.list.command import get_list
import pandas as pd

def get_apps_metadata() -> pd.DataFrame:

    def get_app_directory(pid: str) -> str:
        lsof = subprocess.check_output(
            f"lsof -p {pid} | grep cwd",
            shell=True,
            stderr=subprocess.STDOUT,
        )

        return lsof.split()[-1].decode("utf-8")

    apps_list: pd.DataFrame = get_list()
    paths = list()
    for _, row in apps_list.iterrows():
        pid = row.T["App ID"]
        paths.append(get_app_directory(pid))
    apps_list["App directory"] = paths

    return apps_list.sort_values(by="App URL", ascending=True).drop_duplicates(
        subset="App URL"
    )
