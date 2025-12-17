import os
from typing import List, Dict, Any
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents import create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import Tool
from scholarly import scholarly,ProxyGenerator
from rich.console import Console
from rich.table import Table
from langchain_core.prompts import PromptTemplate
import time

# ======================
# 🔑 替换为你自己的 DashScope API Key
# ======================
os.environ["DASHSCOPE_API_KEY"] = "sk-"

# 初始化通义千问模型（Qwen-Plus）
llm = ChatTongyi(
    model_name="qwen-turbo",
    base_url="https://dashscope.aliyuncs.com/v1",
    temperature=0.2,
    max_tokens=1000
)


# ======================
# 📚 文献检索工具函数
# ======================
def search_literature(input_str: str) -> List[Dict[str, Any]]:
    """
    输入：关键词字符串（如 "machine learning climate"）
    输出：最多5篇文献的列表，每篇含 title, authors, year, abstract, url, citations
    """

    pg = ProxyGenerator()
    # 注意：SingleProxy 接受 host:port 字符串，但需指定协议（http/https）
    # 更推荐显式指定：
    success = pg.SingleProxy("127.0.0.1:8080")
    if not success:
        print("⚠️ 代理设置失败")

    scholarly.use_proxy(pg, ProxyGenerator())

    keywords = input_str.strip().split()
    if not keywords:
        return []

    results = []
    try:
        for keyword in keywords:
            search_query = scholarly.search_pubs(keyword)
            count = 0
            while count < 5 and len(results) < 5:
                try:
                    pub = next(search_query)

                    # 直接按字典访问（适用于 scholarly >= 1.0）
                    bib = pub.get('bib', {})
                    title = bib.get('title', 'N/A')
                    authors = bib.get('author', [])
                    if isinstance(authors, str):
                        authors = [authors]
                    year = bib.get('pub_year', 'N/A')
                    abstract = bib.get('abstract', '无摘要可用') or '无摘要可用'
                    url = pub.get('pub_url', '')
                    citations = pub.get('citedby', 0)

                    results.append({
                        "title": title,
                        "authors": authors,
                        "year": year,
                        "abstract": abstract,
                        "url": url,
                        "citations": citations
                    })
                    count += 1
                    time.sleep(1)
                except StopIteration:
                    break
            if len(results) >= 5:
                break
    except Exception as e:
        print(f"⚠️ 搜索关键词 '{input_str}' 时出错: {e}")
    return results[:5]


# ======================
# 🛠️ 封装为 LangChain 工具
# ======================
literature_tool = Tool(
    name="search_literature",
    func=search_literature,
    description="输入一个或多个关键词（空格分隔的字符串），返回最多5篇相关学术文献信息，包括标题、作者、年份、摘要、URL和引用次数。"
)

# ======================
# 🧠 构造 ReAct Agent Prompt
# ======================
template = "你是一个学术文献检索助手。你可以使用以下工具：{tools}" \
           "使用以下格式进行推理：" \
           "Question: 用户的问题" \
           "Thought: 你应该总是先思考该怎么做" \
           "Action: 要采取的行动，必须是 [{tool_names}] 之一" \
           "Action Input: 行动的输入（关键词字符串）" \
           "Observation: 行动的结果...（可重复多次）" \
           "Thought: 我现在知道最终答案了" \
           "Final Answer: 对用户的最终回答（用中文总结文献）" \
           "Begin!" \
           "Question: {input}" \
           "Thought: {agent_scratchpad}"

prompt = PromptTemplate.from_template(template)

# ======================
# 🤖 创建 Agent 和执行器
# ======================
agent = create_react_agent(llm, [literature_tool], prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=[literature_tool],
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5
)


# ======================
# 🖥️ 结果展示（表格）
# ======================
def display_results(results: List[Dict]):
    if not results:
        print("❌ 未找到相关文献。")
        return

    console = Console()
    table = Table(title="📚 学术文献检索结果", show_header=True, header_style="bold cyan")
    table.add_column("序号", justify="right", style="bold")
    table.add_column("标题", style="bold green")
    table.add_column("作者", style="magenta")
    table.add_column("年份", justify="right", style="bold")
    table.add_column("摘要", style="white")
    table.add_column("引用", justify="right", style="yellow")

    for i, r in enumerate(results, 1):
        authors = ", ".join(r["authors"][:3])
        if len(r["authors"]) > 3:
            authors += "..."
        abstract = (r["abstract"][:120] + "...") if len(r["abstract"]) > 120 else r["abstract"]
        table.add_row(
            str(i),
            r["title"],
            authors,
            str(r["year"]),
            abstract,
            str(r["citations"])
        )
    console.print(table)


# ======================
# ▶️ 主程序
# ======================
def main():
    print("🎓 欢迎使用学术文献智能检索助手！")
    print("请输入您的研究方向（例如：'climate change deep learning'）：")

    while True:
        user_input = input("\n> ").strip()
        if not user_input:
            print("⚠️ 请输入有效的研究方向！")
            continue

        try:
            # 执行 Agent（它会自动调用工具）
            response = agent_executor.invoke({"input": user_input})
            final_answer = response.get("output", "未能生成答案。")
            print(f"\n✅ 最终回答：\n{final_answer}")

            # 💡 如果你想直接展示工具返回的文献（跳过 LLM 总结），可以这样：
            # results = search_literature(user_input)
            # display_results(results)

        except Exception as e:
            print(f"❌ 执行出错: {e}")

        if input("\n继续检索？(y/n): ").lower() != 'y':
            break

    print("👋 再见！")


if __name__ == "__main__":
    main()
