from typing import List


from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, ToolMessage
from langchain.tools import tool, BaseTool
from langchain_groq import ChatGroq

load_dotenv()

@tool
def get_text_length(text: str) -> int:
    """Returns the length of the input text."""
    print(f"Received text: {text}")
    #str = str.strip("'\n").strip('"')
    return len(text)


def find_tool_by_mame(tools: List[BaseTool], name: str) -> BaseTool:
    for tool in tools:
        if tool.name == name:
            return tool
    raise ValueError(f"Tool with name {name} not found.")

if __name__ == "__main__":
    print(f"chat client using langchain tool (function call) capability")

    # define tools
    tools = [get_text_length]

    # define LLM with tool capability
    llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
    llm_with_tools = llm.bind_tools(tools)

    # start conversation
    messages = [HumanMessage(content="What is the length of the text 'Hello, LangChain Tools!'?")]

    # conversation loop
    while True:
        # get AI message
        ai_message = llm_with_tools.invoke(messages)
        print(f"AI Message: {ai_message}")

        # if the model decides to call a tool
        tool_calls = getattr(ai_message, "tool_calls", None) or []
        if len(tool_calls) > 0:
            # append AI message to the conversation (context) 
            messages.append(ai_message)
            
            for tool_call in tool_calls:
                tool_name = tool_call.get("name")
                tool_arg = tool_call.get("args", {})
                tool_call_id = tool_call.get("id")
                tool_to_use = find_tool_by_mame(tools, tool_name)
                
                # invoke the tool
                observation = tool_to_use.invoke(tool_arg)
                print(f"Observation from tool {tool_name}: {observation}")           
                # Observation from tool get_text_length: 23
                
                # append tool observation to the conversation (context)
                messages.append(ToolMessage(content=str(observation), tool_call_id=tool_call_id))
        else: 
            print(f"AI Response: {ai_message.content}")
            break

### command line - uv run chat-client-function-tool.py

### run output ###
# chat client using langchain tool (function call) capability
# AI Message:
# content=''
# additional_kwargs={
#     'reasoning_content': 'We need to call the function get_text_length with text "Hello, LangChain Tools!". The function returns length. Let\'s compute manually: "Hello, LangChain Tools!" Count characters: H(1)e2l3l4o5,6 space7 L8a9n10g11C12h13a14i15n16 space17 T18o19o20l21s22 !23. So length 23. But we should use function.',
#     'tool_calls': [
#         {
#             'id': 'fc_09a90837-5102-4397-b96f-5d92be040b79',
#             'function': {
#                 'arguments': '{"text":"Hello, LangChain Tools!"}',
#                 'name': 'get_text_length'
#             },
#             'type': 'function'
#         }
#     ]
# }
# response_metadata={
#     'token_usage': {
#         'completion_tokens': 126,
#         'prompt_tokens': 137,
#         'total_tokens': 263,
#         'completion_time': 0.123811946,
#         'prompt_time': 0.011557079,
#         'queue_time': 0.048788411,
#         'total_time': 0.135369025
#     },
#     'model_name': 'openai/gpt-oss-20b',
#     'system_fingerprint': 'fp_e99e93f2ac',
#     'service_tier': 'on_demand',
#     'finish_reason': 'tool_calls',
#     'logprobs': None,
#     'model_provider': 'groq'
# }
# id='lc_run--147d6527-30e6-4b83-b96b-824a191401a4-0'
# tool_calls=[
#     {
#         'name': 'get_text_length',
#         'args': {'text': 'Hello, LangChain Tools!'},
#         'id': 'fc_09a90837-5102-4397-b96f-5d92be040b79',
#         'type': 'tool_call'
#     }
# ]
# usage_metadata={
#     'input_tokens': 137,
#     'output_tokens': 126,
#     'total_tokens': 263

# Received text: Hello, LangChain Tools!
# Observation from tool get_text_length: 23

# AI Message:
# content='The length of the text "Hello, LangChain Tools!" is **23** characters.'
# additional_kwargs={
#     'reasoning_content': 'We need to respond with the length. The tool returned 23. So answer: 23.'
# }
# response_metadata={
#     'token_usage': {
#         'completion_tokens': 48,
#         'prompt_tokens': 170,
#         'total_tokens': 218,
#         'completion_time': 0.047242279,
#         'prompt_time': 0.009522264,
#         'queue_time': 0.049114042,
#         'total_time': 0.056764543
#     },
#     'model_name': 'openai/gpt-oss-20b',
#     'system_fingerprint': 'fp_e99e93f2ac',
#     'service_tier': 'on_demand',
#     'finish_reason': 'stop',
#     'logprobs': None,
#     'model_provider': 'groq'
# }
# id='lc_run--4975de29-3574-47eb-9540-122504d2c8e2-0'
# usage_metadata={
#     'input_tokens': 170,
#     'output_tokens': 48,
#     'total_tokens': 218
# }
# AI Response:
# The length of the text "Hello, LangChain Tools!" is **23** characters.
