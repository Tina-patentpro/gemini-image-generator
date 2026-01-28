# 🔧 解决"未找到发布版本"问题

## 问题原因

Dify 无法从您的 GitHub 仓库找到发布版本（Release）。

## 解决方案

### 方法 1：创建 GitHub Release（推荐）

#### 步骤 1：访问 GitHub Releases 页面

点击链接打开您的仓库的 Releases 页面：
🔗 https://github.com/Tina-patentpro/gemini-image-generator/releases

#### 步骤 2：创建新 Release

1. 点击 **"Create a new release"** 按钮
2. 填写信息：
   - **Tag**: 选择或输入 `v1.0.0`
   - **Title**: `v1.0.0 - 初始发布`
   - **Description**:
     ```
     # Dify Gemini 图像生成插件 v1.0.0

     ## 功能特性
     - ✅ 支持 4 种图像生成模式
     - ✅ 11 个预设模板
     - ✅ 完全符合 Dify v0.5.2 标准
     - ✅ 生产级代码质量

     ## 安装
     在 Dify 中通过 GitHub 安装：`Tina-patentpro/gemini-image-generator`

     ## 配置
     需要 OpenRouter API 密钥（格式：sk-or-xxxx）
     ```

3. **勾选 "Set as the latest release"**
4. 点击 **"Publish release"** 按钮

---

### 方法 2：检查仓库可见性

#### 确认仓库是公开的

1. 访问：https://github.com/Tina-patentpro/gemini-image-generator/settings
2. 滚动到底部 "Danger Zone"
3. 确保 **"Change repository visibility"** 可以看到
4. 如果是私有的，改为公开：
   - 将仓库设置为 **Public**
   - 点击 **"I understand... change repository visibility"** 确认

**重要**: Dify 无法从私有仓库安装插件！

---

### 方法 3：等待 GitHub 同步（刚推送后）

如果您刚刚推送代码，可能需要等待 1-2 分钟让 GitHub 同步。

**等待后**：
1. 在 Dify 中刷新页面
2. 重新尝试安装

---

## 验证步骤

### 检查 1：确认 Release 已创建

访问：https://github.com/Tina-patentpro/gemini-image-generator/releases

应该能看到 **v1.0.0** 的 release。

### 检查 2：确认仓库可见性

访问：https://github.com/Tina-patentpro/gemini-image-generator

**不登录也能看到** = 仓库是公开的 ✅
**需要登录才能看到** = 仓库是私有的 ❌（需要改为公开）

---

## 快速诊断

请告诉我以下信息：

1. **能否访问这个链接？**
   https://github.com/Tina-patentpro/gemini-image-generator

2. **能否访问这个链接？**
   https://github.com/Tina-patentpro/gemini-image-generator/releases

3. **使用的是 Dify 哪个版本？**
   - 社区版
   - 云端版
   - 自托管

---

## 临时解决方案

如果 GitHub Release 方式有问题，您可以：

### 方案 A：直接本地安装（备用）

```bash
# 1. 将插件复制到 Dify 插件目录
cp -r "d:\OneDrive\4、董娣相关\工作流设计\插件" /path/to/dify/plugins/gemini-image-generator

# 2. 重启 Dify
docker-compose restart worker
```

### 方案 B：检查 Dify 日志

查看详细错误信息：
```bash
docker-compose logs -f worker | grep -i gemini
```

---

需要帮助吗？告诉我您在哪个步骤遇到了问题！
