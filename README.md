# 去 AI 腔（no-ai-slop-zh）

把中文文稿里那些"一看就是 AI 写的"套路删掉，同时保住你自己的语气。

这是一个给 AI 编程助手 / Agent 用的 skill。它不会把你的文章改成千篇一律的"标准好文"，而是删掉 AI 腔的痕迹，留下你的用词习惯、句子节奏、幽默和犹疑。

## 它解决什么问题

AI 让写东西变容易了，但写出来的东西越来越像同一个人写的。中文里最常见的几类：

- "这不是 X，而是 Y。"
- "很多人不知道的是……"
- "答案很简单：……"
- "具有里程碑意义"
- "研究表明"（却不说谁研究的）
- "未来已来"
- 一段话拆成"首先、其次、最后"三点

更麻烦的是，用 AI 润色会把你原本的语气磨掉——那些真正像你说话的地方，被"顺"成了标准的、谁都能写的句子。

## 它抓什么

**四类禁用词：** 互联网黑话（赋能、抓手、闭环、护城河、颗粒度、底层逻辑）、浮夸宣传腔（极大地、淋漓尽致、注入新活力、交出答卷）、空洞副词（其实、事实上、进一步、有效地）、空洞短语（值得一提的是、综上所述、归根结底、在当今……的时代）。

**21 类套路：** 二元对比、清嗓子开场（"让我们一起来探讨"）、伪洞见铺垫（"很多人不知道的是"）、冒号揭示、表面分析式的"彰显"结尾、重要性吹捧、模糊引用、同义词轮换、伪深刻结尾、排比对仗堆砌、强行分点、总结复述式结尾、格式滥用、破折号依赖、机器人节奏、修辞式设问、"在……的今天"开头、空话式动宾搭配、假强动词、否定式列举、"不仅……更是……"。

完整的规则和示例见 [`skills/no-ai-slop-zh/SKILL.md`](skills/no-ai-slop-zh/SKILL.md)，改稿后的自检清单见 [`skills/no-ai-slop-zh/eval.md`](skills/no-ai-slop-zh/eval.md)。

## 安装

**方式一：让你的 Agent 自己装。** 把这句话发给 WorkBuddy、Claude Code、Codex 或任意你用的编码 Agent：

```
Install the /no-ai-slop-zh skill globally from https://github.com/lrz8023nolan/no-ai-slop-zh
```

**方式二：npx。**

```bash
npx skills add lrz8023nolan/no-ai-slop-zh --skill no-ai-slop-zh --global --yes
```

**方式三：手动复制。** 把 `skills/no-ai-slop-zh/` 整个目录复制到 Agent 的技能目录：

- WorkBuddy：`C:\Users\<你>\.workbuddy\skills\no-ai-slop-zh\`
- Claude Code：`~/.claude/skills/no-ai-slop-zh/`

## 用法

**改稿（默认）：**

```
/no-ai-slop-zh （你的文稿）
```

它会删掉 AI 腔、保留你的语气，并在末尾附一节「改了什么」，说明动了哪些地方。

**只检测，不改写：**

```
/no-ai-slop-zh 这段有 AI 味吗？（你的文稿）
```

它会列出命中的每一条套路、引用原句、给出简短改法。不改写、不打分、也不猜这段文字是不是 AI 写的——AI 检测靠猜，命名套路才是你能自己核对的证据。

## 与原版的关系

本仓库基于 [Peter Yang 的 no-ai-slop](https://github.com/petergyang/no-ai-slop)（MIT 协议）做中文本地化改造。

| 部分 | 处理方式 |
|------|----------|
| 编辑方法论 | **保留**：最小有效编辑、保护作者声音、便携性测试、展示而非告知、编辑原则 16 条、工作流与自检机制 |
| 禁用词表 | **重写**：英文词表（delve、leverage、robust…）对中文无用，按中文写作语境重建为四类 |
| 套路清单 | **重写**：英文表达（"It's not X. It's Y."）改为中文对应表达，并补上中文特有项 |
| 新增条目 | 排比对仗堆砌、强行分点、四字成语连用、"在……的今天/背景下"开头、假强动词、空话式动宾搭配 |
| 全部示例 | **替换**：例句改为中文实例，如「这个集成把部署时间从 40 分钟压到 4 分钟」 |

原版是英文写作工具，直接翻译过来会有一半条目用不上。这个中文版保留的是它的方法论骨架，规则内容按中文实际写作习惯重建。

## 致谢

- 原版 [no-ai-slop](https://github.com/petergyang/no-ai-slop) 作者 [Peter Yang](https://github.com/petergyang)
- 中文版改造者 [Nolan](https://github.com/lrz8023nolan)

## 许可

MIT License。使用、修改、分发均可，需保留版权声明。详见 [LICENSE](LICENSE)。
