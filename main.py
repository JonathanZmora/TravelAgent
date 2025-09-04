from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.memory import ConversationSummaryBufferMemory
from prompts import make_agent_prompt
from tools import get_weather


load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)

tools = [get_weather]

memory = ConversationSummaryBufferMemory(
    llm=llm,
    memory_key="chat_history",
    return_messages=True,
    max_token_limit=2000,
)

prompt = make_agent_prompt(show_reasoning=True)  # includes system + reasoning instructions + history + scratchpad

agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)


def run():
    print(
        'I’m your travel assistant! Try:\n'
        '• "Suggest fall weekend destinations from Tel Aviv in mid-October."\n'
        '• "Packing list for Kyoto 2025-09-14 to 2025-09-16."\n'
        '• "Kid-friendly attractions in NYC next Saturday."\n'
        'Type "exit" to quit.'
    )

    while True:
        user = input("\nYou: ").strip()
        if user.lower() in {"exit", "quit"}:
            break
        try:
            result = agent_executor.invoke({"input": user})
            print("\nAssistant:\n" + result["output"])
        except Exception as e:
            print(f"\nAssistant (error handler): I hit an unexpected issue: {e}\n"
                  "Try rephrasing or asking for a smaller piece of the task.")


if __name__ == "__main__":
    run()
