import asyncio
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from agentagency import AgentAgency


async def main():
    model_client = OpenAIChatCompletionClient(model='gpt-5-mini')
    agency = AgentAgency(model_client)

    database_agent = agency.create_database_agent("Database Expert")
    restapi_agent = agency.create_api_agent("REST API Expert")
    excel_agent = agency.create_excel_agent("Excel Expert")

    participants = [database_agent, restapi_agent, excel_agent]

    termination_condition = TextMentionTermination("registration process complete")

    team = RoundRobinGroupChat(participants=participants, termination_condition=termination_condition)

    task = "Read the user data from the database, register each user via the API, verify login for each, and write the results to Excel."

    result = await Console(team.run_stream(task=task))
    print(result)


asyncio.run(main())