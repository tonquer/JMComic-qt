import os
import subprocess

for root, dirs, filenames in os.walk("../ui/"):
    for name in filenames:
        if name[-2:] != "ui":
            continue
        outName = name[:-3]
        subprocess.run([
            "pyside6-uic.exe",
            os.path.join(root, outName + ".ui"),
            "-o",
            os.path.join("../src/interface/", outName + ".py")
        ], check=True)

print('Finished!')
