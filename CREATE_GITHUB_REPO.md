# 🚀 创建 GitHub 仓库并推送代码

## 第一步：在 GitHub 创建仓库

### 方法 1：通过浏览器创建（推荐）

1. **访问 GitHub 创建页面**：
   - 点击链接：https://github.com/new

2. **填写仓库信息**：
   ```
   Repository name: gemini-image-generator
   Description: Dify plugin for generating images using Google Gemini 2.0 Flash via OpenRouter API

   ☐ Public  (选择公开仓库)

   ☑️ Add a README file (不勾选)
   ☑️ Add .gitignore (不勾选)
   ☑️ Choose a license (不勾选)
   ```

3. **点击 "Create repository"**

---

## 第二步：推送代码

**创建仓库后**，在 Git Bash 或命令行中运行：

```bash
cd "d:\OneDrive\4、董娣相关\工作流设计\插件"
git push -u origin master
```

---

## 🎯 完成后的下一步

### 在 Dify 中安装插件

1. **登录 Dify** - 访问您的 Dify 实例
2. **进入插件管理** - 点击右上角"插件"图标
3. **安装插件** - 点击"安装插件" → "通过 GitHub"
4. **输入仓库地址** - `Tina-patentpro/gemini-image-generator`
5. **配置 API 密钥** - 输入 OpenRouter API 密钥（格式：`sk-or-xxxx`）

---

## 💡 快速参考

**仓库地址**：`https://github.com/Tina-patentpro/gemini-image-generator`

**插件特点**：
- ✅ 支持 4 种图像生成模式
- ✅ 11 个预设模板
- ✅ 完全符合 Dify v0.5.2 标准
- ✅ 生产级代码质量

**OpenRouter API 密钥获取**：
- 访问：https://openrouter.ai/
- 注册并创建 API 密钥
- 密钥格式：`sk-or-xxxx`

---

需要帮助吗？告诉我您在哪一步遇到了问题！
