from typing import Dict, List, TypedDict
from langchain.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7, max_tokens=2048, max_retries=0)

class AgentState(TypedDict):
    message: List[HumanMessage | AIMessage]

def process_node(state: AgentState) -> AgentState:
    reply = llm.invoke(state['message'])
    state['message'].append(AIMessage(content=reply.content))
    print("AI: ", reply.content)
    return state

graph = StateGraph(AgentState)
graph.add_node("process_node", process_node)
graph.add_edge(START, "process_node")
graph.add_edge("process_node", END)
agent = graph.compile()

conversations = []

input_message = input("Enter your message: ")
while(input_message != "exit"):
    conversations.append(HumanMessage(content=input_message))
    reply = agent.invoke({"message": conversations})
    conversations.append(reply['message'][-1])
    input_message = input("Enter your message: ")

with open("conversation_history.txt", "w") as f:
    for message in conversations:
        if isinstance(message, HumanMessage):
            f.write(f"Human: {message.content}\n")
        else:
            f.write(f"AI: {message.content}\n")
