from typing import Dict, List, TypedDict, Union
from langgraph.graph import StateGraph, START, END
from langchain.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv


load_dotenv()

class AgentState(TypedDict):
    message: List[Union[HumanMessage, AIMessage]]

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7, max_tokens=2048, max_retries=0)

def process_node(state: AgentState) -> AgentState:
    reply = llm.invoke(state['message'])
    state['message'].append(AIMessage(content=reply.content))
    return state

graph = StateGraph(AgentState)
graph.add_node("process_node", process_node)
graph.add_edge(START, "process_node")
graph.add_edge("process_node", END)
agent = graph.compile()


input_message = input("Enter your message: ")
while(input_message.lower() != "exit"):
    reply = agent.invoke({"message": [HumanMessage(content= input_message)]})
    print("AI:", reply['message'][-1].content)
    input_message = input("Enter your message: ")


