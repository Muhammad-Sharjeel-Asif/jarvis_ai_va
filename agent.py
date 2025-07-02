from agents import Agent,AsyncOpenAI, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from dotenv import load_dotenv
import os

def agent(command):
    load_dotenv()

    gemini_api_key = os.getenv("GEMINI_API_KEY")

    client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    set_tracing_disabled(disabled=True)

    agent = Agent(
        name="Virtual Assistant",
        instructions="You are a virtual assistent. Help people in daily life activities and queries. You are directed to give short and summarized answers.",
        model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    )

    result = Runner.run_sync(
            agent,
            command,
    )

    return result.final_output