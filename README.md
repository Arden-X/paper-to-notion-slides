# Paper to Notion & Slides

把一篇论文转换为两份相互对应的成果：

1. 五段式论文精读笔记：有 Notion 时自动写入，没有时输出 Markdown。
2. 使用原文完整图片、主要元素可编辑的 PowerPoint。

## 快速开始

安装 [`paper-to-notion-slides`](paper-to-notion-slides) 目录后，上传论文 PDF，并使用类似提示：

```text
使用 $paper-to-notion-slides 分析这篇论文，生成论文阅读笔记和可编辑 PPT。
```

也可以提供论文名称，让 Agent 获取官方预印版：

```text
使用 $paper-to-notion-slides 分析 Mooncake。请从官方预印版取材，长论文使用多页 PPT。
```

## 输入与输出

| 项目 | 说明 |
| --- | --- |
| 输入 | 用户上传的论文 PDF，或可准确定位的官方预印版 |
| 阅读笔记 | Notion 页面或 UTF-8 `.md` 文件 |
| 演示文稿 | 可编辑 `.pptx`；短论文单页或少页，长论文多页 |
| 图片 | 直接取自原文，保留完整图体、坐标轴、图例、子图标记和 `Figure N:` 图注 |

阅读笔记固定包含：

1. 论文信息
2. 问题背景与难点
3. 核心思路与创新点
4. 实验数据与结果分析
5. 对该领域的启示

公式推导放在“核心思路与创新点”中，以连续叙述解释符号、推导过程和直观含义，避免过度分点。

## Notion 是可选的

- 已连接 Notion MCP：技能定位 `论文阅读`，读取页面或数据库结构，创建笔记并回读验证。
- 未连接 Notion：技能直接交付结构相同的 `.md` 文件，不影响论文分析与 PPT 生成。

因此，安装和使用此 Skill 不要求必须拥有 Notion。

## PPT 规则

- 中文使用 SimHei，非中文使用 Times New Roman。
- 使用浅绿色背景和高对比深色文字。
- 原文图片必须截图完整，并包含原始图注与安全白边。
- 图片已经包含图号和图注时，幻灯片外部不重复添加 `Fig. N`。
- 文本、形状、表格和图表保持可编辑；原文图片可以是位图。
- 文字必须留在所属背景模块内，底部至少保留 12 px 空隙。

## 安装结构

真正的 Skill 位于子目录：

```text
paper-to-notion-slides/
├── SKILL.md
├── agents/openai.yaml
├── assets/icon.svg
├── references/layout-contract.md
└── scripts/validate_paper_deck_layout.py
```

将这个子目录整体安装到支持 Agent Skills 的环境即可。`SKILL.md` 是入口文件。

## 验证幻灯片

验证器会检查原文截图完整性、图注、来源页码、安全白边，以及文字与背景模块的几何边界：

```bash
python3 paper-to-notion-slides/scripts/validate_paper_deck_layout.py \
  --layout-dir path/to/layout-json \
  --figure-manifest path/to/figure-manifest.json
```

运行仓库测试：

```bash
python3 -m unittest discover -s tests -v
```

## 隐私与许可

仓库只包含通用工作流、版式约束与验证代码，不包含论文 PDF、Notion 页面或生成的 PPT。

使用 [MIT License](LICENSE)。
