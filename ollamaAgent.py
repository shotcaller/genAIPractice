from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

TAVILY_API_KEY = "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"


llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0.8,
    num_predict=256
)

#Define tools
search_tool = TavilySearch(
    tavily_api_key=TAVILY_API_KEY,
    max_results=2)
# search_results = search_tool.invoke("What is the weather in Fredericton?")
# print("Search Results:", search_results)

#List the tools
tools = [search_tool]

#Create a memory saver
memory_saver = MemorySaver()

#Create a chatbot with tools
def agent_chatbot():
    #agent = llm.bind_tools(tools)
    agent_executor = create_react_agent(model=llm, tools=tools, checkpointer=memory_saver)
    # response = agent_executor.invoke(
    #     {"messages": [{"role": "user", "content": "Hi. My name is Ruturaj."}]}, 
    #     {"configurable": {"thread_id": "thread-1"}}
    # )
#########################################################################################################
    #Streaming tokens
    # for step, metadata in agent_executor.stream(
    #     {"messages":[{"role": "user", "content": "Hi. My name is Ruturaj. What is the weather in Fredericton?"}]},
    #     {"configurable": {"thread_id": "thread-1"}},
    #     stream_mode="messages"
    # ):
    #     if metadata["langgraph_node"] == "agent" and (text := step.text()):
    #         print(text, end="-")

    #########################################################################3
    #Printing the response
    # for message in response["messages"]:
    #     message.pretty_print()

    ###################################################################################################
    #Streaming messages
    while True:
        query = input("Enter your query: ")
        if query.lower() == "exit":
            break
        for step in agent_executor.stream({"messages": [{"role": "user", "content": query}]},
                                          {"configurable": {"thread_id": "thread-1"}},
                                        stream_mode="values"):
            step["messages"][-1].pretty_print()  # Output the last message in a pretty format

agent_chatbot()