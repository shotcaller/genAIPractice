from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, trim_messages
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState,  StateGraph
from typing import Sequence
from typing_extensions import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0.8,
    num_predict=256
)

def basic_test():
    messages = [
        SystemMessage("You are a helpful translator. Translate the user sentence to French."),
        HumanMessage("I love school.")
        
    ]

    for token in llm.stream(messages):
        print(token.content, end="-")

    #rint(llm.invoke(messages))

def basic_prompt_template():
    prompt_template = PromptTemplate.from_template("Who is the director of the movie - {movie}?")

    return prompt_template.invoke({"movie": "Man of Steel"})


def chat_prompt_template():
    sys_template = "Translate the following from English into {language}"

    prompt_template = ChatPromptTemplate.from_messages(
        [("system", sys_template),
         ("human", "{text}")]
    )
    #invoke is not working with ChatPromptTemplate
    prompt = prompt_template.invoke({"language": "Korean", "text": "How are you?"})
    #print(prompt)
    print(prompt.to_messages())
    print(llm.invoke(prompt).content)


def basic_chatbot():
    response = llm.invoke(
        [
            HumanMessage("Hi! My name is Ruturaj"),
            AIMessage("Hello Ruturaj! How can I help you today?"),
            HumanMessage("What's my name?"),
        ]
    )

    print(response.content)

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    field: str

def memory_chatbot():
    #Define a new graph
    #Trim messages
    trimmer = trim_messages(
        max_tokens=65,
        strategy="last",
        token_counter=llm,
        include_system=True,
        allow_partial=False,
        start_on="human"
    )

    prompt_template = ChatPromptTemplate.from_messages(
        [("system", "You are technology expert. Answer the user's questions related to {field}."),
         MessagesPlaceholder(variable_name="messages")]
    )
    workflow = StateGraph(state_schema=State)
    
    def call_model(state: State):
        #Invoke the prompt template in the state
        #This will trim the messages and then invoke the prompt template, pass it in messages in invoke
        #trimmed_messages = trimmer(state["messages"])
        prompt = prompt_template.invoke({"messages": state["messages"], "field": state["field"]})
        #Invoke the model with the messages in the state
        #response = llm.invoke(state["messages"])
        response = llm.invoke(prompt)
        return {"messages": [response]}
    
    #Define the (single) node in the graph
    workflow.add_edge(START, "llm")
    workflow.add_node("llm", call_model)

    #Add memory
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)

    #Run the app
    
    field = input("Enter the field of your query: ")
    while True:
        #Run the app with the query
        
        query = input("Enter your query: ")
        if query.lower() == "exit":
            break
        # response = app.invoke({"messages": [HumanMessage(query)], "field": field}, {"configurable": {"thread_id": "thread-1"}})
        # response["messages"][-1].pretty_print() #output the last message in a pretty format

        #for streaming response
        for chunk, metadata in app.stream(
            {"messages": [HumanMessage(query)], "field": field},
            {"configurable": {"thread_id": "thread-1"}}, stream_mode="messages"
        ):
            if isinstance(chunk, AIMessage): #Filter to AI responses
                print(chunk.content, end="-")
        
memory_chatbot()
#basic_chatbot()
#print(llm.invoke(basic_prompt_template()))
#basic_test()
#chat_prompt_template()


