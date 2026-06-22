version=v1.3.2
#source src/venv/bin/activate
if [ ! -d src ]; then 
    echo "src目录不存在"; 
    exit
fi

if [ ! command -v appimagetool-x86_64.AppImage >/dev/null 2>&1 ]; then
    echo "appimagetool-x86_64.AppImage 命令不存在"
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
rm -rf jmcomic.AppRun
mkdir -p jmcomic.AppRun/usr/bin
cp -r ../../res/appimage/* jmcomic.AppRun/
cp -r ../../res/icon/logo_round.png jmcomic.AppRun/JMComic.png
cp -r start/* jmcomic.AppRun/usr/bin/

chmod +x jmcomic.AppRun/AppRun
chmod +x jmcomic.AppRun/usr/bin/JMComic
appimagetool-x86_64.AppImage jmcomic.AppRun
cd ..
mv dist/JMComic-x86_64.AppImage jmcomic_${version}_linux_nosr_glibc2.42.AppImage

# build
pip3 install -r requirements.txt
pyinstaller --hidden-import=_cffi_backend --collect-data curl_cffi --add-data "../lib/linux/*:."  -w start.py
cd dist
rm -rf jmcomic.AppRun
mkdir -p jmcomic.AppRun/usr/bin
cp -r ../../res/appimage/* jmcomic.AppRun/
cp -r ../../res/icon/logo_round.png jmcomic.AppRun/JMComic.png
cp -r start/* jmcomic.AppRun/usr/bin/

chmod +x jmcomic.AppRun/AppRun
chmod +x jmcomic.AppRun/usr/bin/JMComic
appimagetool-x86_64.AppImage jmcomic.AppRun
cd ..
mv dist/JMComic-x86_64.AppImage jmcomic_${version}_linux_glibc2.42.AppImage
