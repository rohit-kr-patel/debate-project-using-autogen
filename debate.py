import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage
from autogen_agentchat.agents import AssistantAgent
from dotenv import load_dotenv
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
import os

async def teamConfig(topic):
    model = OpenAIChatCompletionClient(
    base_url="https://openrouter.ai/api/v1",
    model="deepseek/deepseek-chat-v3-0324:free",
    api_key = open_router_api_key,
    model_info={
        "family":'deepseek',
        "vision" :True,
        "function_calling":True,
        "json_output": False,
        "structured_output": False, 
    }
)
    topic="shall US government ban tiktok?"

    host= AssistantAgent(
       name="Jane",
       model_client=model,
         system_message=(
            'You are Jane, the host of a debate between John , a supporter agent,'
            'and Jack, a critic agent. You will moderate the debate.'
            f'The topic of the debate is {topic}.'
            'At the beginning of each round, announce the round number.'
            'At the beginning of third round, declare that it wil be '
            'the last round. After the last round, thank the audience and exactly'
            'say "Terminate".' 
    

          )
    )

    supporter = AssistantAgent( 
      name='John',
      system_message=(f"You are supporter in a debate for the topic {topic}. You will be debating against jack, a critic agent"),
       model_client=model,)

    critic = AssistantAgent(
        name='Jack',
        system_message=(f"You are critic in a debate for the topic {topic}. You will be debating against john, a supporter agent"),
        model_client=model,)

#start the debate

    team =RoundRobinGroupChat(
    participants=[host,supporter, critic],
    max_turns=10,
    termination_condition=TextMentionTermination(text="Terminate")
    )   

    return team

# Load API key from .env
load_dotenv()
open_router_api_key = os.getenv("OPENROUTER_API_KEY")

async def debate(team):
   
    
#start the debate
    
    async for message in team.run_stream(task="start the debate!"):
   
     if isinstance(message, TaskResult):
        message=f'Stopping reason: {message.stop_reason}'
        yield message
     else:
        message=f'{message.source}: {message.content}'
        yield message

    # res = await team.run(task="start the debate!")
    # for message in res.messages:
    #     print('-'*20)
    #     print(f'{message.source}: {message.content}')

async def main():
   topic="Shall US government ban tiktok?"
   team= await teamConfig(topic)
   async for message in debate(team):
       print('_' *20)
       print(message)
      
     
if __name__ == "__main__": 
    topic="Shall US government ban tiktok?"
    asyncio.run(main())
