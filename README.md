# SYSU 学术报告 Beamer 模板

中山大学绿色风格的 **4:3** 中文学术报告模板，包含封面、自动目录、正文、公式、表格、双栏图片和致谢页。使用 XeLaTeX 编译为 PDF。

## 使用

安装 TeX Live 或 MacTeX，包含 XeLaTeX、latexmk、beamer、ctex、fontspec、tikz、booktabs，以及 Fandol、TeX Gyre 字体。

| 操作 | 命令 |
| --- | --- |
| 下载 | `git clone https://github.com/AmazingUmi/beamerthemeSYSU.git` |
| 进入目录 | `cd beamerthemeSYSU` |
| 编译 | `make` |
| 清理编译文件与 PDF | `make clean` |

生成文件：`output/pdf/SYSU-template.pdf`。PDF 可直接用于跨平台演示。

## 文件

| 文件 | 用途 |
| --- | --- |
| `main.tex` | 报告信息与正文示例 |
| `beamerthemeSYSU.sty` | 配色、字体和页面样式 |
| `assets/` | 校徽、校名和矢量地图 |
| `Makefile` | 编译与清理命令 |
| `build/` | 编译中间文件，自动生成 |
| `output/pdf/` | 生成的 PDF |

## 修改

| 内容 | 位置或写法 |
| --- | --- |
| 题目、姓名、单位、日期 | `main.tex` 中的 `\title`、`\author`、`\institute`、`\date` |
| 指导教师、邮箱、致谢 | `\SYSUsetup{advisor={…},email={…},closing={…}}` |
| 正文与章节 | `frame`、`section`；默认四个章节，目录自动更新 |
| 插图 | 将示例占位框替换为 `\includegraphics[width=\linewidth]{images/result.pdf}`，图片放入自行创建的 `images/` 目录 |
| 逐步展示 | 在正文中加入 `\pause` |
| 合并展示步骤 | 文档类选项加入 `handout` |

支持 PDF、PNG、JPEG 图片；中文使用 Fandol 字体，西文使用 TeX Gyre Termes。
