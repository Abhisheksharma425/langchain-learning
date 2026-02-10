from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4.1-2025-04-14", temperature=0)

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

graph_builder = StateGraph(State)

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break
        response = graph.invoke({"messages": [{"role": "user", "content": user_input}]})
        print("Bot:", response["messages"][-1].content)