# src/interface/__main__.py
import multiprocessing
import os
import sys

import streamlit.web.cli as stcli

from importlib.resources import files, as_file


def _get_main_path() -> str:
    res = files("ui").joinpath("main.py")
    with as_file(res) as real_path:
        return str(real_path)


def main():
    if getattr(sys, "frozen", False):
        multiprocessing.freeze_support()
        try:
            multiprocessing.set_start_method("spawn", force=True)
        except RuntimeError:
            pass

        streamlit_args = [
            "--server.fileWatcherType=none",
            "--global.developmentMode=false",
            "--browser.gatherUsageStats=false",
            "--client.toolbarMode=viewer",
            "--ui.hideTopBar=true",
        ]
    else:
        streamlit_args = [
            "--server.fileWatcherType=auto",
            "--global.developmentMode=false",
            "--browser.gatherUsageStats=true",
            "--client.toolbarMode=viewer",
            "--ui.hideTopBar=true",
        ]

    sys.argv = [
        "streamlit",
        "run",
        _get_main_path(),
        "--server.headless=false",
        "--server.address=localhost",
        f"--server.port={os.getenv("STREAMLIT_SERVER_PORT", "8501")}",
        "--secrets.files=./.streamlit/secrets.toml",
        "--global.developmentMode=false",
    ] + streamlit_args
    stcli.main()


if __name__ == "__main__":
    main()
