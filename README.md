# 🩺 村医AI — 基于 MiniCPM-V 的离线多模态医疗助手

> MiniCPM-V 视觉语言模型 Android 端部署，支持离线图像理解、文字对话与摄像头实时分析。

## ✨ 功能特性

- **🖼️ 图像理解** — 上传图片进行 AI 分析识别
- **📷 摄像头拍照** — 直接拍照分析，无需从相册选取
- **💬 智能对话** — 基于多模态模型的文字对话能力
- **🔌 完全离线** — 所有推理在设备本地运行，无需网络
- **🩺 医疗辅助** — 专为基层医疗场景优化

## 📱 支持的模型

| 模型 | 参数量 | 推荐量化 | 模型文件大小 | 推荐设备内存 |
| --- | --- | --- | --- | --- |
| MiniCPM-V 2.6 | 80亿 | Q4_K_M | ~5.4 GB | ≥ 8 GB |
| MiniCPM-V 4.0 | 41亿 | Q4_K_M | ~2.9 GB | ≥ 6 GB |
| MiniCPM-V 4.6 | 13亿 | Q4_K_M | ~1.6 GB | ≥ 6 GB |

## 🛠️ 环境要求

- **Android Studio** (Giraffe 或更新版本)
- **Android SDK + NDK** (NDK 28.2 / CMake 3.22.1)
- **物理设备**: 64位 ARM 处理器 (`arm64-v8a`)
- **设备内存**: 见上表，推荐 8GB+

## 🚀 快速安装

### 方式一：直接安装 APK

下载预构建的 `app-debug.apk`（18MB），传输到 Android 设备后直接安装。

> ⚠️ 需要开启「允许未知来源」安装权限。

### 方式二：从源码构建

```bash
cd MiniCPM-V-demo-Android
./gradlew assembleDebug
```

构建产物位于 `app/build/outputs/apk/debug/app-debug.apk`。

## 📖 使用说明

1. **安装应用** — 安装 APK 到 Android 设备
2. **下载模型** — 首次打开应用，通过「模型管理」下载 GGUF 模型文件
3. **开始使用**:
   - 点击 📷 按钮拍照分析
   - 点击 🖼️ 按钮从相册选取图片
   - 输入文字进行对话

## 📂 模型文件下载

推荐从 ModelScope 下载（国内访问更快）：

- **MiniCPM-V 2.6**: [ModelScope](https://modelscope.cn/models/OpenBMB/MiniCPM-V-2_6-gguf)
- **MiniCPM-V 4.0**: [ModelScope](https://modelscope.cn/models/OpenBMB/MiniCPM-V-4-gguf)
- **MiniCPM-V 4.6**: [ModelScope](https://modelscope.cn/models/OpenBMB/MiniCPM-V-4.6-gguf)

需要下载两个文件：
- 语言模型文件（如 `ggml-model-Q4_K_M.gguf`）
- 视觉投影文件（`mmproj-model-f16.gguf`）

也可通过 HuggingFace 下载：[MiniCPM-V-2.6](https://huggingface.co/openbmb/MiniCPM-V-2_6-gguf) | [MiniCPM-V-4.0](https://huggingface.co/openbmb/MiniCPM-V-4-gguf) | [MiniCPM-V-4.6](https://huggingface.co/openbmb/MiniCPM-V-4.6-gguf)

## 🏗️ 项目结构

```
MiniCPM-V-demo-Android/
├── app/
│   ├── src/main/
│   │   ├── java/.../         # Kotlin 源码
│   │   ├── cpp/              # JNI / CMake 原生代码
│   │   └── res/              # 资源文件（布局、图标等）
│   └── build.gradle.kts      # 应用构建配置
├── gradle/                   # Gradle 配置
├── build.gradle.kts          # 项目构建配置
└── settings.gradle.kts       # 项目设置
```

## 📝 版本历史

- **v2.1** — 新增摄像头拍照功能、🩺听诊器图标、修复构建配置
- **v2.0** — AI 辅助诊疗助手基础版本

## 📄 许可证

本项目基于 [MiniCPM-V](https://github.com/OpenBMB/MiniCPM-V) 开源项目构建。

---

> 🇨🇳 **村医AI** — 让基层医疗更智能
