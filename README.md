# SYSU（中山大学）学术报告 LaTeX 模板

从 PPT 模板提取并重构，使用 XeLaTeX 编译。仓库包含编译所需的全部素材，
不依赖原始 PPT 或其他项目目录。

```bash
git clone https://github.com/AmazingUmi/latex-template.git
cd latex-template
make
```

生成文件为 `output/pdf/SYSU-template.pdf`，中间文件保存在 `build/`。
首次构建会自动编译多轮，更新目录和交叉引用。
也可以在支持 XeLaTeX 的编辑器中打开 `main.tex`；所有素材路径均相对项目目录。

## 文件

- `main.tex`：报告信息和正文，包含七种原稿页面的使用示例。
- `beamerthemeSYSU.sty`：配色、字体、封面、目录、页眉、章节标记和致谢页。
- `assets/`：原始校徽、白色校名，以及从 PPT 自由曲线路径提取的矢量地图。
- `tools/extract_assets.py`：重新提取素材的脚本，日常编译不需要运行。

原始 PPT 未包含在此仓库。如需从同一原稿重新提取素材，执行
`python3 tools/extract_assets.py /path/to/ppt模版.pptx`，该脚本需要 Pillow。

在 `main.tex` 中修改 `\title`、`\author`、`\institute`、`\date` 和
`\SYSUsetup`。正文使用标准 `frame`、`section`、`columns`、公式和表格环境。
每个 `\section` 对应原稿的一个章节标记，当前主题保持原稿的四章节结构。
目录自动读取章节名称，不需要重复输入。

插入结果图时，将 `\SYSUfigureplaceholder{...}` 换成：

```latex
\includegraphics[width=\linewidth,height=31mm,keepaspectratio]{images/result.pdf}
```

`images/` 用于保存自己的图片。PDF 矢量图可直接使用，PNG/JPEG 也受支持。
取消示例中的 `\pause` 注释即可逐步展示；每个步骤会生成一页 PDF。
需要合并所有步骤时，将文档类选项改为 `[aspectratio=43,11pt,t,handout]`。

## 提取范围与排版

保持原稿 **4:3** 页面、`#005825` 深绿页眉、`#008E3D` 章节标记、
封面和致谢的地图、侧边色块，以及右上角校徽。七张原稿实际使用的版式
对应封面、目录、Introduction、Method、Analysis、Conclusion 和致谢。
文字、公式、表格和页眉均由 LaTeX 排版，没有将原页截图铺成背景。

原稿使用华文楷体、宋体和 Times New Roman。本模板统一采用 TeX Live
提供的 **Fandol 楷体/宋体 + TeX Gyre Termes**，字体笔形与原稿略有差别，
无需安装 Office 或特定操作系统字体。PPT 字号按原画布比例换算，
如原稿 32 pt 的页眉约对应本模板 16.2 pt。

原稿中的个人信息改为集中配置，重复目录占位符改为自动目录。
此目录只包含模板及示例，未迁移已有报告正文。

编译环境需要 TeX Live 或 MacTeX 中的 `beamer`、`ctex`、`fontspec`、
`tikz`、`booktabs`、Fandol 和 TeX Gyre 字体，以及 `latexmk`。
编译后的 PDF 可独立播放；换机器修改源码时，需要相应的 TeX 环境。
