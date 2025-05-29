from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

@tool
def calculator(a:float,b:float) -> str:
    """
    A simple calculator that can perform addition, subtraction, multiplication, and division.
    Usage: calculator(a: float, b: float) -> str
    Example: calculator(2, 3) will return "5.0"
    """
    print("Calulator tool is working!")
    return f"The sum of {a} and {b} is {a + b}"

def main():
    model = ChatOpenAI(temperature=0.0)
    tools = [calculator]
    agent_executor = create_react_agent(model, tools=tools, verbose=True)

    print("This is you AI assistant.")
    print("You can MATH, and I will try to help you.")
    print("Type 'quit' to quit the program.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input == "quit":
            break
        
        print("\nAssistant: ", end="")
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")

        print("\n")  # New line after the assistant's response

if __name__ == "__main__":
    main()