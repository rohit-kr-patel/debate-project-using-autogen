import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from dotenv import load_dotenv
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
import os

# Load API key from .env
load_dotenv()
open_router_api_key = os.getenv("OPENROUTER_API_KEY")

async def teamConfig(topic):
    """
    Configure the debate team using the user-provided topic.
    """
    model = OpenAIChatCompletionClient(
        base_url="https://openrouter.ai/api/v1",
        model="deepseek/deepseek-chat-v3-0324:free",
        api_key=open_router_api_key,
        model_info={
            "family": 'deepseek',
            "vision": True,
            "function_calling": True,
            "json_output": False,
            "structured_output": False,
        }
    )

    
    host = AssistantAgent(
        name="Jane",
        model_client=model,
        system_message=(
            'You are Jane, the host of a debate between John, a supporter agent, '
            'and Jack, a critic agent. You will moderate the debate. '
            f'The topic of the debate is {topic}. '
            'At the beginning of each round, announce the round number. '
            'At the beginning of third round, declare that it will be the last round. '
            'After the last round, thank the audience and exactly say "Terminate".'
        )
    )

    supporter = AssistantAgent(
        name='John',
        model_client=model,
        system_message=f"You are a supporter in a debate for the topic '{topic}'. You will debate against Jack, a critic agent."
    )

    critic = AssistantAgent(
        name='Jack',
        model_client=model,
        system_message=f"You are a critic in a debate for the topic '{topic}'. You will debate against John, a supporter agent."
    )

    team = RoundRobinGroupChat(
        participants=[host, supporter, critic],
        max_turns=10,
        termination_condition=TextMentionTermination(text="Terminate")
    )

    return team

async def debate(team):
    """
    Run the debate asynchronously and yield messages.
    """
    async for message in team.run_stream(task="start the debate!"):
        if isinstance(message, TaskResult):
            yield f'Stopping reason: {message.stop_reason}'
        else:
            yield f'{message.source}: {message.content}'


async def main(topic):
    team = await teamConfig(topic)
    async for message in debate(team):
        print('_' * 20)
        print(message)

if __name__ == "__main__":
 
    topic = input("Enter the debate topic: ")
    asyncio.run(main(topic))
