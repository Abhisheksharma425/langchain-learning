# from typing import TypedDict, Annotated
# from langgraph.graph import StateGraph, START, END
# from langgraph.graph.message import add_messages
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import BaseMessage
# from langchain.chains import create_sql_query_chain
# from langchain.chains import create_sql_query_chain
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.agent_toolkits import create_sql_agent


load_dotenv()


db = SQLDatabase.from_uri("sqlite:///./data/ecommerce.db")

# print(db.get_table_info())

llm = ChatOpenAI(model = 'gpt-4o-mini', temperature = 0)



agent = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)




agent.invoke({"input": "how many customers are there?"})
print(hasattr(agent, "get_graph"))
# write_query = create_sql_query_chain(llm, db)

# print(write_query.invoke({"question": "How many tables are in the database?"}))



# 1. Connect to DB
# db = SQLDatabase.from_uri("sqlite:///your_database_name.db")

# 2. Initialize LLM
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 3. Create a Custom Prompt
# We explicitly tell the LLM: "Here is the schema, write the SQL."
# template = """You are a SQLite expert. Given an input question, create a syntactically correct SQLite query to run.
# Return ONLY the SQL query. Do not wrap it in markdown blocks (like ```sql ... ```).

# Here is the table info:
# {schema}

# Question: {question}
# SQL Query:"""

# prompt = ChatPromptTemplate.from_template(template)

# # 4. Define the Chain
# # The 'schema' variable is filled dynamically by a tiny function (lambda)
# def get_schema(_):
#     return db.get_table_info()

# # The chain: Get Schema -> Format Prompt -> Run LLM -> Clean Output
# sql_chain = (
#     {
#         "schema": get_schema, 
#         "question": lambda x: x["question"]
#     }
#     | prompt
#     | llm
#     | StrOutputParser()
# )

# # 5. Test it
# response = sql_chain.invoke({"question": "How many tables are in the database?"})
# print("Generated SQL:", response)










# llm = ChatOpenAI(model="gpt-4.1-2025-04-14", temperature=0)

# class State(TypedDict):
#     messages: Annotated[list[BaseMessage], add_messages]
#     generated_sql_query: str
#     actual_query: str

# graph_builder = StateGraph(State)

# def chatbot(state: State):
#     return {"messages": [llm.invoke(state["messages"])]}

# graph_builder.add_node("chatbot", chatbot)
# graph_builder.add_edge(START, "chatbot")
# graph_builder.add_edge("chatbot", END)

# graph = graph_builder.compile()

# if __name__ == "__main__":
#     while True:
#         user_input = input("User: ")
#         if user_input.lower() == "exit":
#             break
#         response = graph.invoke({"messages": [{"role": "user", "content": user_input}]})
#         print("Bot:", response["messages"][-1].content)