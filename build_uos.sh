version=v1.3.2

if [ ! -d src ]; then 
    echo "src目录不存在"; 
    exit
fi

if [ ! command -v pyinstaller >/dev/null 2>&1 ]; then
    echo "pyinstaller 命令不存在"
    exit
fi

cd script/
python build_qrc.py
cd ../src/

# build nosr
rm -rf dist
pip3 uninstall sr-vulkan -y
pip3 uninstall sr-vulkan-model-waifu2x -y
pip3 uninstall sr-vulkan-model-realcugan -y
pip3 uninstall sr-vulkan-model-realesrgan -y
pip3 install -r requirements_nosr.txt
pyinstaller --hidden-import=_cffi_backend --collect-data curl_cffi --add-data "../lib/linux/*:."  -w start.py
cd dist
rm -rf uos
cp -r ../../res/uos .
cp -r start/* uos/opt/apps/org.tonquer.jmcomic/files/
chmod -R 755 uos
sudo dpkg-deb --root-owner-group  -b uos jmcomic.deb
cd ..
mv dist/jmcomic.deb jmcomic_${version}_uos_nosr_amd64.deb

# build
rm -rf dist
pip3 install -r requirements.txt
pyinstaller --hidden-import=_cffi_backend --collect-data curl_cffi --add-data "../lib/linux/*:."  -w start.py
cd dist
rm -rf uos
cp -r ../../res/uos .
cp -r start/* uos/opt/apps/org.tonquer.jmcomic/files/
chmod -R 755 uos
sudo dpkg-deb --root-owner-group  -b uos jmcomic.deb
cd ..
mv dist/jmcomic.deb jmcomic_${version}_uos_amd64.deb
