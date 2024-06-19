import os
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_groq import ChatGroq

# 設定 Tavily 的 API 金鑰
os.environ["TAVILY_API_KEY"] = "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"

# 定義工具，這裡使用 Tavily 的搜索結果工具，限制最多返回一個結果
tools = [TavilySearchResults(max_results=1)]

# 準備使用的提示文本 - 你可以修改這部分！這裡使用從 hub 拉取的 "hwchase17/react" 模型
prompt = hub.pull("hwchase17/react")

# 選擇要使用的 LLM（大型語言模型）
llm = ChatGroq(api_key="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")

# 創建 ReAct（反應）代理
agent = create_react_agent(llm, tools, prompt)

# 通過傳入代理和工具來創建代理執行器
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 提示用戶輸入問題
question = input("請輸入問題: ")

# 調用代理執行器來發出問題
agent_executor.invoke({"input": question})