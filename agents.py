import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url

load_dotenv()

# Safe import across LangChain v1.0 / LangGraph prebuilt
try:
    from langchain.agents import create_agent
except ImportError:
    try:
        from langgraph.prebuilt import create_react_agent as create_agent
    except ImportError:
        from langchain.agents import create_tool_calling_agent, AgentExecutor
        from langchain_core.prompts import MessagesPlaceholder
        def create_agent(model, tools):
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are an intelligent autonomous research assistant."),
                MessagesPlaceholder(variable_name="messages"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ])
            agent = create_tool_calling_agent(model, tools, prompt)
            return AgentExecutor(agent=agent, tools=tools)

# Model setup: Google Gemini
gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
gemini_model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm = ChatGoogleGenerativeAI(
        model=gemini_model,
        google_api_key=gemini_key,
        temperature=0.1
    )
except ImportError:
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0)

# 1st agent: Web Search
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )

# 2nd agent: Deep Reader & Scraper
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url]
    )


#writer chain 

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

#critic_chain 

critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()

