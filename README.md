# 禁漫天堂

[![GitHub](https://img.shields.io/github/license/tonquer/JMComic-qt)](https://raw.githubusercontent.com/tonquer/picacg-windows/master/LICENSE.txt)
![Relese](https://img.shields.io/badge/Python-3.7.9%2B-brightgreen)
[![Relese](https://img.shields.io/github/v/release/tonquer/JMComic-qt)](https://github.com/tonquer/JMComic-qt/releases)
[![Relese](https://img.shields.io/github/downloads/tonquer/JMComic-qt/total.svg)](https://github.com/tonquer/JMComic-qt/releases)

- 禁漫天堂PC客户端（支持window、Linux和macOS），界面使用QT
- 该项目仅供技术研究使用，请勿用于其他用途
- 如果觉得本项目对你有所帮助，请点个star关注，感谢支持
- 如有使用中遇到问题，欢迎提ISSUE

## 功能
- 已实现禁漫天堂大部分功能
- 支持看图和下载

## 如何使用
  ### Windows (测试使用win10)
  1. 下载 [最新的版本](https://github.com/tonquer/JMComic-qt/releases)
  2. 解压zip
  3. 打开start.exe
  4. 后续有更新，只需要下载最新版本覆盖原目录即可
  5. 如果无法初始化Waifu2x, DLL错误, 请安装 [Vs运行库](https://download.visualstudio.microsoft.com/download/pr/366c0fb9-fe05-4b58-949a-5bc36e50e370/015EDD4E5D36E053B23A01ADB77A2B12444D3FB6ECCEFE23E3A8CD6388616A16/VC_redist.x64.exe), [Vulkan运行库](https://sdk.lunarg.com/sdk/download/1.2.162.0/windows/VulkanRT-1.2.162.0-Installer.exe)

  ### macOS (测试使用 macOS 10.15.7)
  1. 下载 [最新的版本](https://github.com/tonquer/JMComic-qt/releases)
  2. 加载dmg文件
  3. 将 JMComic 拖入访达 (Finder) 左侧侧栏的应用程序 (Applications) 文件夹中
  4. 从启动台 (Launchpad) 中找到并打开 JMComic
  5. 如果出现文件损坏提示，请在控制台运行 
  ```
  sudo xattr -r -d com.apple.quarantine /Applications/JMComic.app
  ```
  
  ### Linux (测试使用deepin 20.2)
  1. Deepin或Uos系统请下载安装qt依赖， 
  ```
  wget http://ftp.br.debian.org/debian/pool/main/x/xcb-util/libxcb-util1_0.4.0-1+b1_amd64.deb
  sudo dpkg -i ./libxcb-util1_0.4.0-1+b1_amd64.deb
  ```
  2. 下载 [最新的版本](https://github.com/tonquer/JMComic-qt/releases)
  3. 运行

## 如何编译
  ### 使用Git Actions编译
  1. 查看编译结果[Git Actions编译](https://github.com/tonquer/JMComic-qt/actions) 
 
## 界面

* 登录

* 搜索

* 漫画详情

* 下载

* 看图

## 我的其他项目
 [![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=tonquer&repo=picacg-qt)](https://github.com/tonquer/picacg-qt)  
 [![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=tonquer&repo=ehentai-qt)](https://github.com/tonquer/ehentai-qt) 
 
## 感谢以下项目
  ### 禁漫
   [![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=Sexypanda8888&repo=18comic-)](https://github.com/Sexypanda8888/18comic-)  
  ### waifu2x功能
   [![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=nihui&repo=waifu2x-ncnn-vulkan)](https://github.com/nagadomi/waifu2x-ncnn-vulkan)  
   [![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=tonquer&repo=waifu2x-vulkan)](https://github.com/tonquer/waifu2x-vulkan)  
