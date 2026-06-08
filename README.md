# BookBuddy - 双语儿童绘本馆

BookBuddy是一个面向3-8岁儿童的双语绘本阅读平台，提供高质量的中英双语绘本视频。

## 项目结构

```
bookbuddy-website/
├── index.html          # 首页 - 绘本列表
├── book.html          # 绘本详情页
├── reader.html        # 视频阅读器
├── books/             # 绘本资源
│   ├── book-001/     # 小舞者的梦想
│   │   ├── cover.png  # 封面图
│   │   └── video.mp4  # 绘本视频
│   ├── book-002/     # 小狐狸的星空之旅
│   └── ...
└── README.md          # 本文件
```

## 功能特性

- 📚 **30+双语绘本**：覆盖3-8岁儿童阅读需求
- 🎥 **视频阅读**：沉浸式绘本视频体验
- 🌍 **双语配音**：美式/英式英语可选
- 📱 **响应式设计**：支持手机、平板、电脑

## 技术栈

- 纯HTML/CSS/JavaScript（无框架依赖）
- GitHub Pages 托管
- 响应式布局

## 本地预览

```bash
# 启动本地服务器
npx serve . -l 8080

# 浏览器访问
http://localhost:8080
```

## 部署到GitHub Pages

1. 创建GitHub仓库（如果还没有）：
   ```bash
   # 在GitHub上创建名为 bookbuddy-website 的仓库
   ```

2. 推送代码：
   ```bash
   cd bookbuddy-website
   git add .
   git commit -m "Initial commit: BookBuddy website"
   git branch -M main
   git remote add origin https://github.com/你的用户名/bookbuddy-website.git
   git push -u origin main
   ```

3. 启用GitHub Pages：
   - 进入仓库 Settings > Pages
   - Source 选择 "main" 分支
   - 点击 Save
   - 等待2-5分钟，网站将发布到 `https://你的用户名.github.io/bookbuddy-website/`

## 版权声明

所有绘本内容版权归BookBuddy团队所有。未经授权，不得转载或使用。

## 联系方式

- 邮箱：[待填写]
- 微信：[待填写]
