# 🚀 AI 视频字幕提取工具 - Railway 部署指南

## 📝 前提条件

在开始之前，请确保你有：
- GitHub 账号（免费）https://github.com/signup
- Railway 账号（免费）https://railway.app/

---

## 步骤 1️⃣：创建 GitHub 仓库

### 1.1 在 GitHub 网站创建仓库

1. 打开浏览器，访问：https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `ai-subtitle-extractor` （或你喜欢的名字）
   - **Description**: AI 视频字幕提取工具
   - **Privacy**: 选择 Public（公开）或 Private（私密）
   - **⚠️ 重要**：不要勾选 "Add a README file"、".gitignore" 或 "license"
3. 点击 **"Create repository"** 按钮
4. **保持这个页面打开**，稍后会用到

### 1.2 获取仓库地址

创建完成后，你会看到类似这样的地址：
```
https://github.com/你的用户名/ai-subtitle-extractor.git
```

**复制这个地址**，稍后会用到。

---

## 步骤 2️⃣：初始化本地 Git 仓库并推送

### 2.1 初始化后端仓库

在终端运行以下命令（我已经帮你准备好了）：

```bash
cd /Users/xixi/subtitle-backend

# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: AI subtitle extractor backend"

# 连接到你的 GitHub 仓库（替换成你的仓库地址）
git remote add origin https://github.com/你的用户名/ai-subtitle-extractor.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

**⚠️ 重要提示：**
- 将上面的 `https://github.com/你的用户名/ai-subtitle-extractor.git` 替换成你在步骤 1.2 复制的地址
- 如果要求输入用户名和密码，使用 GitHub 的 Personal Access Token（不是密码）

### 2.2 如何创建 GitHub Personal Access Token

如果推送时要求登录：

1. 访问：https://github.com/settings/tokens
2. 点击 **"Generate new token"** → **"Generate new token (classic)"**
3. 设置：
   - Note: `Railway Deployment`
   - Expiration: `No expiration`
   - 勾选：`repo` (所有选项)
4. 点击 **"Generate token"**
5. **复制生成的 token**（只显示一次！）
6. 在终端提示输入密码时，粘贴这个 token

---

## 步骤 3️⃣：部署到 Railway

### 3.1 注册/登录 Railway

1. 访问：https://railway.app/
2. 点击 **"Login"** 或 **"Start a New Project"**
3. 使用 GitHub 账号登录（推荐）

### 3.2 创建新项目

1. 在 Railway 控制台，点击 **"New Project"**
2. 选择 **"Deploy from GitHub repo"**
3. 点击 **"Configure GitHub App"**
4. 授权 Railway 访问你的 GitHub 仓库
5. 选择你刚才创建的仓库：`ai-subtitle-extractor`
6. 点击 **"Deploy Now"**

### 3.3 配置环境变量（可选）

Railway 会自动检测 Python 项目并安装依赖。

如果需要，可以在 **Variables** 标签页添加环境变量：
- `PORT`: 8000（Railway 会自动设置，通常不需要手动配置）

### 3.4 查看部署状态

1. 在 Railway 控制台，点击你的项目
2. 查看 **Deployments** 标签页
3. 等待部署完成（通常需要 5-10 分钟，因为要下载 Whisper 模型）
4. 部署成功后，会显示绿色的 ✓

### 3.5 获取公网地址

1. 在项目页面，点击 **Settings** 标签页
2. 找到 **Domains** 部分
3. 点击 **"Generate Domain"** 按钮
4. Railway 会生成一个域名，类似：
   ```
   https://ai-subtitle-extractor-production.up.railway.app
   ```
5. **复制这个地址**

---

## 步骤 4️⃣：配置前端连接到 Railway 后端

### 4.1 更新前端配置

修改前端的 API 地址，指向 Railway 后端：

1. 打开文件：`/Users/xixi/ai-video-subtitle-extractor/vite.config.ts`
2. 修改 proxy 配置：

```typescript
proxy: {
  '/api': {
    target: 'https://你的railway域名.up.railway.app',  // 改成你的 Railway 域名
    changeOrigin: true,
  }
}
```

3. 保存文件

### 4.2 重启前端

```bash
cd /Users/xixi/ai-video-subtitle-extractor
npm run dev
```

---

## 步骤 5️⃣：部署前端（可选）

如果你也想把前端部署到网上，可以使用 Vercel：

### 5.1 前端推送到 GitHub

创建另一个 GitHub 仓库用于前端：

```bash
cd /Users/xixi/ai-video-subtitle-extractor

git init
git add .
git commit -m "Initial commit: frontend"
git remote add origin https://github.com/你的用户名/ai-subtitle-frontend.git
git branch -M main
git push -u origin main
```

### 5.2 部署到 Vercel

1. 访问：https://vercel.com/
2. 使用 GitHub 登录
3. 点击 **"New Project"**
4. 选择 `ai-subtitle-frontend` 仓库
5. 保持默认设置，点击 **"Deploy"**
6. 等待部署完成
7. Vercel 会给你一个域名，如：`https://ai-subtitle-frontend.vercel.app`

### 5.3 更新前端 API 地址（生产环境）

在 Vercel 项目设置中添加环境变量：
- 名称：`VITE_API_URL`
- 值：`https://你的railway域名.up.railway.app`

重新部署即可。

---

## 🎉 完成！

现在你有：
- ✅ 后端部署在 Railway：`https://xxx.railway.app`
- ✅ 前端可以本地运行，或部署在 Vercel
- ✅ 永久固定的网址
- ✅ 不需要电脑一直开着

---

## 📞 常见问题

### Q: Railway 部署失败？
**A:** 检查日志：
1. 在 Railway 控制台点击项目
2. 点击 **Deployments**
3. 点击最新的部署
4. 查看日志找出错误原因

常见原因：
- 依赖安装失败 → 检查 `requirements.txt`
- 内存不足 → Whisper 模型很大，可能需要升级 Railway 套餐
- 端口配置错误 → 确保 server.py 使用环境变量 `PORT`

### Q: Whisper 模型下载很慢？
**A:** 首次部署时，Railway 需要下载 Whisper small 模型（约 500MB），可能需要 10-15 分钟，请耐心等待。

### Q: Railway 免费额度够用吗？
**A:** Railway 免费套餐提供：
- 每月 $5 的免费额度
- 约 500 小时运行时间
- 如果使用频繁，可能需要升级到付费套餐（$5/月起）

### Q: 如何查看 Railway 日志？
**A:**
1. 在 Railway 控制台点击项目
2. 点击 **Deployments** 标签页
3. 点击最新的部署查看实时日志

### Q: 如何更新代码？
**A:**
```bash
cd /Users/xixi/subtitle-backend
git add .
git commit -m "更新说明"
git push
```
Railway 会自动检测并重新部署。

---

## 💡 提示

- Railway 会在每次 Git 推送时自动部署
- 建议在 Railway 项目中设置通知，接收部署状态
- 第一次部署需要较长时间（下载模型），后续更新会快很多
- 可以在 Railway 控制台查看应用的 CPU、内存使用情况

---

## 🔗 有用的链接

- GitHub 文档：https://docs.github.com/
- Railway 文档：https://docs.railway.app/
- Vercel 文档：https://vercel.com/docs
- 项目问题反馈：创建 GitHub Issue
