import subprocess
import sys
import os
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.langconv import Converter


QT_LINGUIST_DIR = os.environ.get("QT_LINGUIST_DIR")
LINGUIST_DIR = Path(QT_LINGUIST_DIR) if QT_LINGUIST_DIR else None


def find_tool(env_name, names):
    env_value = os.environ.get(env_name)
    if env_value:
        return env_value

    if LINGUIST_DIR and LINGUIST_DIR.exists():
        for name in names:
            tool = LINGUIST_DIR / name
            if tool.exists():
                return str(tool)

    for name in names:
        tool = shutil.which(name)
        if tool:
            return tool

    raise FileNotFoundError(
        "Could not find {}. Set {}, QT_LINGUIST_DIR, or install PySide6 command line tools.".format(names[0], env_name)
    )


LUPDATE = find_tool("LUPDATE", ("lupdate", "lupdate.exe", "pyside6-lupdate", "pyside6-lupdate.exe"))
LRELEASE = find_tool("LRELEASE", ("lrelease", "lrelease.exe", "pyside6-lrelease", "pyside6-lrelease.exe"))


def run(*args):
    subprocess.run(args, check=True)


def fill_hk_translations(*paths):
    converter = Converter("zh-hant")
    for path in paths:
        current_source = ""
        output = []
        for line in path.read_text(encoding="utf-8").splitlines(keepends=True):
            stripped = line.strip()
            if stripped.startswith("<source>") and stripped.endswith("</source>"):
                current_source = stripped[len("<source>"):-len("</source>")]

            if stripped.startswith('<translation type="unfinished">') and stripped.endswith("</translation>"):
                indent = line[:len(line) - len(line.lstrip())]
                newline = "\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""
                output.append(f"{indent}<translation>{converter.convert(current_source)}</translation>{newline}")
            else:
                output.append(line)

        path.write_text("".join(output), encoding="utf-8")


run(str(LUPDATE), "-no-obsolete", "-source-language", "zh_CN", "-target-language", "zh_HK",
    str(ROOT / "src" / "tools" / "str.py"), "-ts", str(ROOT / "translate" / "str_hk.ts"))
run(str(LUPDATE), "-no-obsolete", "-source-language", "zh_CN", "-target-language", "en_US",
    str(ROOT / "src" / "tools" / "str.py"), "-ts", str(ROOT / "translate" / "str_en.ts"))

run(str(LUPDATE), "-no-obsolete", "-source-language", "zh_CN", "-target-language", "zh_HK",
    str(ROOT / "ui"), "-ts", str(ROOT / "translate" / "ui_hk.ts"))
run(str(LUPDATE), "-no-obsolete", "-source-language", "zh_CN", "-target-language", "en_US",
    str(ROOT / "ui"), "-ts", str(ROOT / "translate" / "ui_en.ts"))

fill_hk_translations(ROOT / "translate" / "str_hk.ts", ROOT / "translate" / "ui_hk.ts")

run(str(LRELEASE), str(ROOT / "translate" / "str_en.ts"), str(ROOT / "translate" / "ui_en.ts"),
    "-qm", str(ROOT / "res" / "tr" / "tr_en.qm"))
run(str(LRELEASE), str(ROOT / "translate" / "str_hk.ts"), str(ROOT / "translate" / "ui_hk.ts"),
    "-qm", str(ROOT / "res" / "tr" / "tr_hk.qm"))

run(sys.executable, str(ROOT / "script" / "build_qrc.py"))
