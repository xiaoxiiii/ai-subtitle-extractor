# 🌐 AI 视频字幕提取工具 - 公网部署指南

## 🎉 部署成功！

你的应用已成功部署到公网，朋友可以通过以下网址访问：

**公网访问地址：** https://green-facts-lay.loca.lt

---

## 📋 使用说明

### 给朋友的访问步骤：

1. **打开网址**
   - 在浏览器中访问：https://green-facts-lay.loca.lt

2. **首次访问提示**
   - localtunnel 会显示一个警告页面，提示"This is a localtunnel service"
   - 点击页面上的 **"Click to Continue"** 按钮即可进入应用

3. **使用应用**
   - 粘贴 B 站视频链接
   - 点击"开始提取字幕"
   - 等待 3-8 分钟（AI 处理需要时间）
   - 查看提取的字幕结果

---

## ⚙️ 管理命令

### 启动公网服务
```bash
/Users/xixi/subtitle-backend/deploy_public.sh
```

### 停止所有服务
```bash
/Users/xixi/subtitle-backend/stop_public.sh
```

或者直接按 `Ctrl + C` 停止

### 查看服务状态
```bash
# 检查前端和后端是否运行
lsof -ti:5173 && lsof -ti:8000 && echo "✅ 服务运行正常"

# 查看后端日志
tail -f /Users/xixi/subtitle-backend/backend.log

# 查看前端日志
tail -f /Users/xixi/ai-video-subtitle-extractor/frontend.log
```

---

## ⚠️ 重要提示

### 1. 你的电脑必须保持开启
- 这是内网穿透方案，你的电脑是实际的服务器
- 如果电脑关机或休眠，朋友将无法访问
- 建议：使用时保持电脑开启并连接电源

### 2. 网址会变化
- 每次重启 `deploy_public.sh`，网址会改变
- 如：https://green-facts-lay.loca.lt 下次可能变成 https://blue-tree-run.loca.lt
- 解决方法：每次启动后，查看终端输出的新网址，发送给朋友

### 3. 速度可能较慢
- 流量路径：朋友浏览器 → localtunnel 服务器 → 你的电脑
- 如果朋友距离你较远，可能会有延迟
- AI 处理本身就需要 3-8 分钟，这是正常的

### 4. 安全建议
- 只分享给信任的朋友
- 不要在公开场合发布这个网址
- 使用完毕后记得停止服务

### 5. 首次访问警告页面
- localtunnel 会显示安全警告
- 这是正常的，告诉朋友点击 "Click to Continue" 即可
- 这个警告是 localtunnel 的安全机制

---

## 🔄 如何获取新的网址

每次运行 `deploy_public.sh` 后，终端会显示：

```
your url is: https://xxxxx.loca.lt
```

这就是新的公网访问地址，复制这个网址发送给朋友即可。

---

## 🚀 如果想要固定网址（可选）

如果你希望每次都是同一个网址，可以：

### 方案 1：使用自定义子域名（需要 ngrok 付费版）
- 注册 ngrok 账号
- 购买付费套餐
- 获得固定域名如：https://your-app.ngrok.io

### 方案 2：部署到云服务器（推荐长期使用）
- 使用 Railway、Vercel 或 Render
- 获得永久固定网址
- 无需电脑一直开着
- 我可以帮你配置（请告诉我如果需要）

---

## 📞 常见问题

### Q: 朋友说打不开网址？
**A:**
1. 检查你的电脑是否在运行 `deploy_public.sh`
2. 检查终端是否显示 "your url is: ..."
3. 确认网址复制正确
4. 让朋友点击"Click to Continue"按钮

### Q: 网址突然失效了？
**A:**
1. 可能是你的电脑休眠或网络断开
2. 重新运行 `deploy_public.sh`
3. 会生成新的网址

### Q: 处理速度很慢？
**A:**
这是正常的！AI 处理视频需要时间：
- 短视频（<5分钟）：约 3-5 分钟
- 长视频（5-15分钟）：约 5-8 分钟
- 告诉朋友耐心等待，不要重复点击

### Q: 能同时支持多少个朋友使用？
**A:**
- 理论上可以多人同时访问
- 但 AI 处理是串行的，一次只能处理一个视频
- 建议：同时使用人数不超过 3-5 人

---

## 🎯 下一步

现在你可以：

1. ✅ 把网址发送给朋友：https://green-facts-lay.loca.lt
2. ✅ 告诉他们点击 "Click to Continue" 进入应用
3. ✅ 让他们粘贴 B 站视频链接测试

如果你需要更稳定、更快速的部署方案，我可以帮你部署到云服务器（Railway/Vercel），获得永久固定网址。
