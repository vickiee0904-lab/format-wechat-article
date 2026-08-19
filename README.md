# 公众号文章排版 Skill

`format-wechat-article` 是一个面向 Codex 的公众号排版技能。它可以分析中文长文结构、推荐视觉风格，并生成适合微信公众号编辑器的内联样式 HTML，同时尽量保持原文内容、顺序和语义不变。

## 主要功能

- 分析标题、导语、章节、列表、引用、案例、警示和结语等内容结构
- 根据文章主题、语气、信息密度和配图推荐三种候选风格
- 将选定风格应用到整篇文章，生成移动端优先的公众号排版
- 输出可粘贴的文章 HTML、浏览器预览和兼容性校验报告
- 检查脚本、外部样式、脆弱 CSS、本地图片路径和移动端图片适配等问题
- 保留原文事实、限定条件、引用和段落顺序，避免静默删改内容

## 内置主题

| 主题 | 适用内容 |
| --- | --- |
| 简约留白 | 随笔、访谈、观点文章和文字密集型内容 |
| 专业报告 | 研究、政策、财经、商业和证据驱动型文章 |
| 知识卡片 | 教程、科普、清单、术语解释和结构化知识 |
| 清透科技杂志 | AI、软件、数字产品和未来科技主题 |
| 温暖生活 | 成长、亲子、健康、旅行和个人故事 |

## 安装

### 使用 GitHub CLI

需要支持 `gh skill` 的新版 GitHub CLI。安装到 Codex 的用户级技能目录：

```bash
gh skill install vickiee0904-lab/format-wechat-article format-wechat-article/SKILL.md --agent codex --scope user
```

安装后重新启动 Codex，或新建一个任务，让 Codex 重新发现技能。

### 手动安装

1. 下载 [format-wechat-article.zip](format-wechat-article.zip)。
2. 解压后得到 `format-wechat-article` 文件夹。
3. 将整个文件夹复制到 `~/.codex/skills/`。
4. 重新启动 Codex，或新建一个任务。

安装后的结构应为：

```text
~/.codex/skills/format-wechat-article/
├── SKILL.md
├── agents/
├── assets/
├── references/
└── scripts/
```

## 使用示例

在 Codex 中上传或粘贴文章，然后提出类似请求：

```text
使用 $format-wechat-article 分析这篇文章，推荐三种合适的公众号排版风格。
```

```text
使用 $format-wechat-article，把这篇 AI 科普文章排成“清透科技杂志”风格，保留全部原文和配图。
```

```text
帮我自主选择最合适的风格，生成可复制到微信公众号编辑器的完整排版和移动端预览。
```

如果没有指定风格，技能会先比较并推荐三种候选方案；如果允许自主决定，则会直接采用匹配度最高的主题。

## 输出内容

一次完整排版通常会生成：

- `article.html`：仅包含文章主体，可用于复制到公众号编辑器
- `preview.html`：带移动端阅读区域和复制按钮的浏览器预览
- `validation.json`：微信公众号 HTML 兼容性检查结果

## 工作流程

1. 读取完整原文和配图，建立文章内容结构。
2. 根据主题、语气、阅读密度和图片风格选择排版主题。
3. 使用内联 CSS 生成公众号文章主体。
4. 运行兼容性校验器并生成独立预览页面。
5. 检查约 375 px 及更窄手机视口下的标题、段落、图片和间距。
6. 交付文章 HTML、预览和校验状态。

## 仓库结构

```text
format-wechat-article/
├── SKILL.md                         # 核心工作流和质量要求
├── agents/openai.yaml              # Codex 界面元数据
├── assets/themes/                  # 五种主题配置
├── references/                     # 内容结构、风格选择和兼容性规则
└── scripts/
    ├── validate_wechat_html.py     # HTML 兼容性检查
    └── wrap_preview.py             # 移动端预览生成器
```

## 注意事项

- `article.html` 使用内联样式，不依赖外部 CSS、字体或 JavaScript。
- 本地图片路径只能用于预览；正式发布前仍需在公众号编辑器中上传图片。
- 微信公众号编辑器可能清理部分样式，正式发布前建议粘贴到测试草稿并再次检查。
- 技能默认只调整结构包装和视觉样式，不会主动改写、总结或补充原文。
