# 推送到 GitHub 指南

## 当前状态

✅ 代码已修复完成
✅ 已提交到本地 master 分支
⏳ 等待推送到 GitHub

## 推送步骤（3 种方法）

### 方法 1: 通过 GitHub 网页创建（最简单）

#### 步骤 1: 在 GitHub 创建仓库

1. 访问：https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `gemini-image-generator`
   - **Description**: `Dify plugin for generating images using Google Gemini 2.0 Flash via OpenRouter API`
   - 设置为 **Public** (公开)
   - **不要**勾选 "Add a README file"
   - **不要**勾选 "Add .gitignore"
   - **不要**选择 "Choose a license"
3. 点击 **"Create repository"**

#### 步骤 2: 推送代码

在 Git Bash 或命令行中运行：

```bash
cd "d:\OneDrive\4、董娣相关\工作流设计\插件"

# 替换 YOUR_USERNAME 为您的 GitHub 用户名
git remote add origin https://github.com/YOUR_USERNAME/gemini-image-generator.git

# 推送代码
git push -u origin master
```

---

### 方法 2: 使用 GitHub CLI（如果已安装）

```bash
cd "d:\OneDrive\4、董娣相关\工作流设计\插件"

# 如果还未登录，先登录
gh auth login

# 创建仓库并推送
gh repo create gemini-image-generator --public --source=. --remote=origin --push
```

---

### 方法 3: 使用 SSH（如果配置了 SSH 密钥）

```bash
cd "d:\OneDrive\4、董娣相关\工作流设计\插件"

# 替换 YOUR_USERNAME 为您的 GitHub 用户名
git remote add origin git@github.com:YOUR_USERNAME/gemini-image-generator.git

# 推送代码
git push -u origin master
```

---

## 推送成功后

### 在 Dify 中安装插件

1. 登录您的 Dify 实例
2. 进入"插件"管理页面
3. 点击"安装插件" → "通过 GitHub"
4. 输入仓库地址：`YOUR_USERNAME/gemini-image-generator`
5. 配置 OpenRouter API 密钥

### 获取 OpenRouter API 密钥

1. 访问：https://openrouter.ai/
2. 注册并登录
3. 进入 "API Keys" 页面
4. 创建新的 API 密钥（格式：`sk-or-xxxx`）
5. 在 Dify 插件配置中输入密钥

---

## 修复内容总结

### 已完成的修复

1. ✅ **集成 Dify SDK**
   - 创建 `GeminiImageProvider` 类用于凭证验证
   - 重写 `GeminiImageGenerator` 继承自 `Tool`
   - 实现 `_invoke()` 方法返回 Generator

2. ✅ **修复错误处理**
   - 所有错误现在抛出异常而非返回错误值
   - 参数验证失败 → `ValueError`
   - API 错误 → `Exception`
   - 凭证错误 → `ToolProviderCredentialValidationError`

3. ✅ **升级 HTTP 库**
   - 将 `requests` 替换为 `httpx`
   - 更新所有异常处理
   - 更新依赖配置

4. ✅ **符合 Dify 最佳实践**
   - 正确的执行状态机制（SUCCESS/FAILURE）
   - 超时设置（30秒）
   - 重试逻辑（指数退避）
   - 完整的凭证验证

### 代码质量改进

- **结构**: 完全符合 Dify 插件架构
- **错误处理**: 符合 dify-plugin-skill 标准
- **HTTP 客户端**: 使用推荐的 httpx 库
- **文档**: 完整的类型提示和文档字符串

---

## 验证安装

### 测试插件

在 Dify 工作流中配置：

```json
{
  "mode": "text_to_image",
  "prompt": "一只可爱的橘猫坐在窗台上，阳光明媚",
  "size": "1024x1024",
  "num_images": 1
}
```

点击"运行"，几秒钟后应该生成图像！

---

## 需要帮助？

如果遇到问题，请检查：

1. **GitHub 仓库是否设置为 Public**
   - Private 仓库无法通过 GitHub 安装

2. **API 密钥格式**
   - 必须以 `sk-or-` 开头

3. **Dify 日志**
   - 查看 worker 日志：`docker-compose logs -f worker | grep -i gemini`

4. **网络连接**
   - 确保 Dify 可以访问 OpenRouter API

---

**祝使用愉快！** 🎉
