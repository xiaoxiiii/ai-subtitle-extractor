# 🚀 快速开始 - AI 视频字幕提取工具

## 一键启动

```bash
/Users/xixi/subtitle-backend/start_all.sh
```

看到 "🎉 所有服务器启动成功！" 后，在浏览器打开：

**http://localhost:5173/**

---

## 使用步骤

1. ✅ **启动服务器**（如上）
2. 🌐 **打开浏览器**访问 http://localhost:5173/
3. 📋 **粘贴 B 站视频链接**（例如：https://www.bilibili.com/video/BV1xx411c7mD）
4. 🎬 **点击"开始提取字幕"**
5. ⏳ **等待 3-8 分钟**
6. 📝 **查看字幕和 AI 摘要**

---

## 停止服务器

```bash
/Users/xixi/subtitle-backend/stop_all.sh
```

---

## 遇到问题？

### 无法连接服务器
```bash
# 重新启动
/Users/xixi/subtitle-backend/start_all.sh
```

### 测试连接
访问：**http://localhost:5173/test.html**

### 查看详细故障排除
```bash
cat /Users/xixi/subtitle-backend/TROUBLESHOOTING.md
```

---

## 📂 重要文件

- **启动脚本**：`/Users/xixi/subtitle-backend/start_all.sh`
- **停止脚本**：`/Users/xixi/subtitle-backend/stop_all.sh`
- **故障排除**：`/Users/xixi/subtitle-backend/TROUBLESHOOTING.md`
- **经验总结**：`/Users/xixi/subtitle-backend/LESSONS_LEARNED.md`
- **后端日志**：`/Users/xixi/subtitle-backend/backend.log`
- **前端日志**：`/Users/xixi/ai-video-subtitle-extractor/frontend.log`

---

**就这么简单！** 🎉
