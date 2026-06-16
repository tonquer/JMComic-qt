import os
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def find_tool(env_name, names):
    env_value = os.environ.get(env_name)
    if env_value:
        return env_value

    for name in names:
        tool = shutil.which(name)
        if tool:
            return tool

    raise FileNotFoundError(
        "Could not find {}. Set {} or install PySide6 command line tools.".format(names[0], env_name)
    )


RCC = find_tool("PYSIDE6_RCC", ("pyside6-rcc", "pyside6-rcc.exe"))

subprocess.run(
    [RCC, "-o", str(ROOT / "src" / "images_rc.py"), str(ROOT / "res" / "images.qrc")],
    check=True,
)
