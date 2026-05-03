from autogen_ext.models.openai import OpenAIChatCompletionClient

from agentagency import AgentAgency


async def main():
    model_client = OpenAIChatCompletionClient(model='gpt-5-mini')
    agency = AgentAgency(model_client)
    agency.create_database_agent("")