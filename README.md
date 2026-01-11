# AI 视频字幕提取工具 - 使用说明

## 🚀 启动服务器

每次要使用这个工具时，运行以下命令：

```bash
/Users/xixi/subtitle-backend/start_all.sh
```

这个脚本会自动启动前端和后端服务器。

## 🛑 停止服务器

不使用时，可以停止服务器：

```bash
/Users/xixi/subtitle-backend/stop_all.sh
```

## 🌐 访问网站

启动服务器后，在浏览器中打开：

**http://localhost:5173/**

## 📋 常见问题

### 1. 为什么会反复出现"无法连接到服务器"？

**原因：**
- 服务器进程在后台运行时，可能被系统或 shell 自动关闭
- macOS 内存管理可能会终止后台进程
- Terminal 关闭时，后台进程可能被杀死

**解决方案：**
使用 `start_all.sh` 脚本启动服务器，它使用 `nohup` 确保进程持续运行。

### 2. 如何检查服务器是否在运行？

```bash
lsof -ti:5173  # 检查前端
lsof -ti:8000  # 检查后端
```

### 3. 如何查看日志？

```bash
# 查看后端日志
tail -f /Users/xixi/subtitle-backend/backend.log

# 查看前端日志
tail -f /Users/xixi/ai-video-subtitle-extractor/frontend.log
```

### 4. 提取字幕需要多长时间？

通常 3-8 分钟，取决于视频长度。使用的是 Whisper small 模型，准确度较高。

## 🎯 使用步骤

1. 运行 `start_all.sh` 启动服务器
2. 浏览器打开 http://localhost:5173/
3. 粘贴 Bilibili 视频链接
4. 点击"开始提取字幕"
5. 等待 3-8 分钟
6. 查看字幕和 AI 摘要

## 💾 节省空间提示

项目文件占用：
- 前端: ~313MB
- 后端: ~36KB
- Whisper small 模型: ~461MB

如果需要释放空间，可以删除 `~/.cache/whisper/small.pt`，下次使用时会自动重新下载。
