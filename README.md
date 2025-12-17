# LangChain Literature Agent / 基于 LangChain 的学术文献智能检索代理

> An intelligent academic literature search assistant powered by LangChain and Google Scholar.  
> 一个基于 LangChain 与 Google Scholar 的智能学术文献检索助手。

## 🌐 中文介绍

本项目利用 **LangChain 的 ReAct Agent 架构**，结合 **通义千问（Qwen）大模型** 和 **Google Scholar 学术搜索引擎**，实现自然语言驱动的文献检索与总结。

用户只需输入研究关键词（如 `climate change deep learning`），Agent 会自动：
- 调用 Scholar 检索最多 5 篇相关论文
- 提取标题、作者、年份、摘要、引用数等信息
- 使用 Qwen 模型生成中文总结
- 以美观表格形式展示结果

支持本地 HTTP 代理（默认 `127.0.0.1:8080`），适用于需要科学上网的环境。

---

## 🌍 English Description

This project implements an intelligent academic literature search agent using **LangChain’s ReAct agent framework**, integrated with the **Tongyi Qianwen (Qwen) large language model** and **Google Scholar**.

Users simply input research keywords (e.g., `climate change deep learning`), and the agent will:
- Automatically query Google Scholar for up to 5 relevant papers
- Extract title, authors, publication year, abstract, citation count, and URL
- Use Qwen to generate a concise Chinese summary of the findings
- Display results in a clean, formatted table via Rich

Supports local HTTP proxy (default: `127.0.0.1:8080`) for reliable access to Google Scholar in restricted networks.

---

## 🛠️ 快速开始 / Quick Start

### 1. 克隆仓库 / Clone the repo
```bash
git clone https://github.com/dremmanuel2/langchain-literature-agent.git
cd langchain-literature-agent
2. 安装依赖 / Install dependencies
Bash
编辑
pip install -r requirements.txt
3. 设置 API 密钥 / Set your API key
⚠️ 切勿将密钥写入代码！

⚠️ Never hardcode your API key!

在终端中设置环境变量（Linux/macOS）：

Bash
编辑
export DASHSCOPE_API_KEY="sk-your-api-key-here"
Windows (PowerShell):

Powershell
编辑
$env:DASHSCOPE_API_KEY="sk-your-api-key-here"
4. 启动代理 / Start your proxy
确保本地代理运行在 127.0.0.1:8080（如 Clash、v2ray 等）。

5. 运行程序 / Run the agent
Bash
编辑
python literature_agent.py
⚠️ 注意事项 / Notes
本项目使用 scholarly 库访问 Google Scholar，请遵守其 使用条款。
频繁请求可能导致 IP 被临时限制，程序已内置 time.sleep(1) 缓冲。
若无需 LLM 总结，可直接调用 search_literature() 函数获取原始结果。
📜 许可证 / License
本项目采用 MIT 许可证。

This project is licensed under the MIT License.

🙌 贡献 / Contributions
欢迎提交 Issue 或 Pull Request！

Issues and PRs are welcome!
