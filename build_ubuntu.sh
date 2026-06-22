version=v1.3.2
#source src/venv/bin/activate

if [ ! -d src ]; then 
    echo "src目录不存在"; 
    exit
fi

if [ ! command -v pyinstaller >/dev/null 2>&1 ]; then
    echo "pyinstaller 命令不存在"
    exit
fi

cd script/
python3 build_qrc.py
cd ../src/

# build nosr
pip3 uninstall sr-vulkan -y
pip3 uninstall sr-vulkan-model-waifu2x -y
pip3 uninstall sr-vulkan-model-realcugan -y
pip3 uninstall sr-vulkan-model-realesrgan -y
pip3 install -r requirements_nosr.txt
rm -rm dist
pyinstaller --hidden-import=_cffi_backend --collect-data curl_cffi --add-data "../lib/linux/*:."  -w start.py
cd dist
rm -rf uos
cp -r ../../res/ubuntu .
cp -r start/* ubuntu/opt/JMComic/
chmod -R 755 ubuntu
sudo dpkg-deb --root-owner-group  -b ubuntu jmcomic.deb
cd ..
mv dist/jmcomic.deb jmcomic_{$version}_ubuntu_nosr_amd64.deb

# build
pip3 install -r requirements.txt
rm -rf dist
pyinstaller --hidden-import=_cffi_backend --collect-data curl_cffi --add-data "../lib/linux/*:."  -w start.py
cd dist
rm -rf uos
cp -r ../../res/ubuntu .
cp -r start/* ubuntu/opt/JMComic/
chmod -R 755 ubuntu
sudo dpkg-deb --root-owner-group  -b ubuntu jmcomic.deb
cd ..
mv dist/jmcomic.deb jmcomic_{$version}_ubuntu_amd64.deb