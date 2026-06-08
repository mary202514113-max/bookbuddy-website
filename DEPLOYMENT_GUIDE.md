# BookBuddy Website - GitHub Pages 部署指南

## 第一步：在GitHub上创建仓库

1. 访问 https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `bookbuddy-website`（或者你喜欢的名字）
   - **Description**: `BookBuddy - 双语儿童绘本馆`
   - **Public/Private**: 选择 Public（GitHub Pages免费版需要公开仓库）
   - **不要**勾选 "Add a README file"（我们已经有README了）
   - **不要**勾选 "Add .gitignore"（我们已经有了）
3. 点击 "Create repository"

创建成功后，GitHub会显示一个快速设置页面，复制仓库URL（类似 `https://github.com/你的用户名/bookbuddy-website.git`）

---

## 第二步：配置Git用户信息（重要！）

⚠️ **当前commit使用的邮箱是 `mary@example.com`（占位符），你需要改成你的真实GitHub邮箱，否则贡献统计不会算到你名下。**

执行以下命令（把 `你的邮箱` 和 `你的名字` 替换成真实信息）：

```bash
cd C:/Users/Mary/WorkBuddy/2026-05-17-task-4/bookbuddy-website

# 修改commit的作者信息
git commit --amend --author="你的名字 <你的邮箱>" --no-edit

# 配置全局git信息（避免以后再次出错）
git config --global user.email "你的邮箱"
git config --global user.name "你的名字"
```

> **如何查看你的GitHub邮箱？**
> 1. 登录 GitHub
> 2. 点击右上角头像 > Settings
> 3. 左侧菜单选择 "Emails"
> 4. 看到 "Primary email address" — 就是这个！

---

## 第三步：推送代码到GitHub

执行以下命令（把 `你的用户名` 和 `仓库名` 替换成真实信息）：

```bash
cd C:/Users/Mary/WorkBuddy/2026-05-17-task-4/bookbuddy-website

# 添加remote（只需要执行一次）
git remote add origin https://github.com/你的用户名/仓库名.git

# 推送代码
git push -u origin main
```

> **如果提示需要登录**：
> - 浏览器会自动打开GitHub登录页面
> - 登录后，GitHub会要求授权
> - 点击 "Authorize" 即可
>
> **如果使用SSH**：
> 如果你配置了SSH key，可以用SSH URL：
> ```bash
> git remote add origin git@github.com:你的用户名/仓库名.git
> ```

---

## 第四步：启用GitHub Pages

1. 推送成功后，访问你的GitHub仓库页面
2. 点击顶部菜单 "Settings"
3. 左侧菜单选择 "Pages"（在 "Code and automation" 分类下）
4. **Build and deployment** 部分：
   - **Source**: 选择 "Deploy from a branch"
   - **Branch**: 选择 `main` 和 `/ (root)`
   - 点击 "Save"
5. 等待2-5分钟，GitHub会显示绿色提示：
   ```
   Your site is live at https://你的用户名.github.io/仓库名/
   ```

---

## 第五步：验证网站

访问 `https://你的用户名.github.io/仓库名/`，检查：

- [ ] 首页正常加载（显示30本书）
- [ ] 点击任意一本书，进入详情页
- [ ] 点击"开始阅读"，视频能正常播放
- [ ] 手机访问也正常（响应式设计）

---

## 常见问题

### Q1: push时提示 "remote: Repository not found"

**原因**: 仓库还没创建，或者仓库名写错了。

**解决**: 先在GitHub上创建仓库，再执行push命令。

---

### Q2: push时提示 "Authentication failed"

**原因**: GitHub认证失败。

**解决**:
- 确保你用浏览器登录了正确的GitHub账号
- 如果使用SSH，确保SSH key已配置
- 或者生成Personal Access Token：
  1. GitHub > Settings > Developer settings > Personal access tokens > Tokens (classic)
  2. Generate new token (classic)
  3. 勾选 `repo` 权限
  4. 复制token，push时用token作为密码

---

### Q3: GitHub Pages部署后访问404

**原因**: 可能是以下之一：
- 仓库是Private（免费版GitHub Pages不支持私有仓库）
- Branch选错了（应该选 `main` / `root`）
- HTML文件名不对（应该是 `index.html`）

**解决**:
- 检查仓库是否为Public
- 检查Settings > Pages的配置
- 等待5-10分钟（GitHub Pages部署需要时间）

---

### Q4: 视频无法播放

**原因**: 视频文件路径错误，或视频文件太大（GitHub限制100MB）。

**解决**:
- 检查 `books/book-001/video.mp4` 是否存在
- 如果视频太大，考虑放到其他平台（腾讯云COS、阿里云OSS等），然后修改 `reader.html` 中的视频路径

---

## 高级：自定义域名（可选）

如果你想用自定义域名（比如 `www.bookbuddy.com`），而不是 `用户名.github.io/仓库名`：

1. 在域名服务商添加CNAME记录：
   ```
   类型: CNAME
   名称: www
   值: 你的用户名.github.io.
   ```

2. 在GitHub仓库创建 `CNAME` 文件：
   ```bash
   echo "www.yourdomain.com" > C:/Users/Mary/WorkBuddy/2026-05-17-task-4/bookbuddy-website/CNAME
   git add CNAME
   git commit -m "Add custom domain"
   git push
   ```

3. 在GitHub Settings > Pages 中填写自定义域名并保存。

---

## 完成检查清单

- [ ] GitHub仓库已创建
- [ ] Git用户信息已修改为真实邮箱
- [ ] 代码已推送到GitHub
- [ ] GitHub Pages已启用
- [ ] 网站可以通过 `https://用户名.github.io/仓库名/` 访问
- [ ] 所有功能正常（首页、详情页、视频播放）

---

## 需要帮助？

如果遇到问题，可以：
1. 查看 [GitHub Pages 官方文档](https://docs.github.com/en/pages)
2. 检查仓库的 "Actions" 标签页，看部署日志
3. 联系我（AI助手）寻求帮助

---

**祝部署顺利！** 🚀
