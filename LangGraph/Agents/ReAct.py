from typing import TypedDict, Dict  
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from dotenv import load_dotenv

load_dotenv()


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def add(a: int, b: int):
    """ This function helps to perform addition operation between two numbers"""
    return a+b

@tool
def sub(a: int, b: int):
    """ This function helps to perform addition operation between two numbers"""
    return a-b

@tool
def multiply(a: int, b: int):
    """ This function helps to perform addition operation between two numbers"""
    return a*b

tools = [add, sub, multiply]

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7, max_tokens=2048, max_retries=0).bind_tools(tools)

def process_node(state: AgentState) -> AgentState:
    system_message = SystemMessage(content= """You are a helpful assistant.
Rules:
1. Use tools ONLY if the query EXACTLY matches the tool capability.
2. If the tool cannot solve the problem, solve it yourself.
3. Do NOT refuse simple commands that can be solved without the tool.""")
    response = llm.invoke([system_message] + state["messages"])
    return {
        "messages": [response]
    }


def should_loop(state: AgentState):
    if not state["messages"][-1].tool_calls:
        return "end"
    return "tool"

graph = StateGraph(AgentState)
graph.add_node("our_agent", process_node)
graph.set_entry_point("our_agent")

tool_node = ToolNode(tools= tools)
graph.add_node("tools", tool_node)

graph.add_conditional_edges(
    "our_agent",
    should_loop,
    {
        "tool": "tools",
        "end": END
    }
)

graph.add_edge("tools", "our_agent")

app = graph.compile()


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

input_message = {"messages": [("user", "Calculate 14 + 23 * 12 and tell me the top trending news in usa")]}
print_stream(app.stream(input=input_message, stream_mode="values"))
