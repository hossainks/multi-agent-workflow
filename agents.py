import asyncio
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from agentagency import AgentAgency


async def main():
    model_client = OpenAIChatCompletionClient(model='gpt-5-mini')
    agency = AgentAgency(model_client)

    database_agent = agency.create_database_agent(system_message=("""
        You are a database specialist responsible for retrieving user registration data.
        
        Your task:
        1. Connect to the MySQL database 'qaulisher_jcacademy'
        2. Query the 'RegistrationDetails' table to get a random record
        3. Query the 'Usernames' table to get additional user data
        4. Combine the data from both tables to create complete registration information
        5. Ensure the email is unique by adding a timestamp or random number if needed
        6. Prepare all the registration data in a structured format so that another agent can understand
        
        When ready, write: "DATABASE_DATA_READY → APIAgent should proceed next"
        """))
    restapi_agent = agency.create_api_agent(system_message=("""
        You are an API testing specialist with access to both REST API tools and filesystem.
        
        Your task:
        1. FIRST: Extract the EXACT registration data from DatabaseAgent's REGISTRATION_DATA message
        2. Read the Postman collection to understand the API contract
        3. Before making a registration API call - construct its body field with the DatabaseAgent's data
        Email should be unique, add timestamp/random data,
        password should be a format of SecurePass123
        Mobile number format - 1234567890
        
        Once json body field is constructed as per above, then make registration API call with constructed
        
        4. If registration succeeds or fails with "user already exists", proceed with login
        5. Make login API call with userEmail and password from database data
        6. Report the actual API response status and success/failure
        
        CRITICAL: You MUST use the exact data from DatabaseAgent's REGISTRATION_DATA, not the sample data
        
        Base URL: https://qaulisherjtcacademy.com
        Content-Type: application/json
        
        When BOTH Registration attempt and login attempt are complete, write: "API_TESTING_COMPLETE → ExecutionAgent"
        Include the final login status (success/failure) in your response.
        """))
    excel_agent = agency.create_excel_agent("Excel Expert")

    participants = [database_agent, restapi_agent, excel_agent]

    termination_condition = TextMentionTermination("registration process complete")

    team = RoundRobinGroupChat(participants=participants, termination_condition=termination_condition)

    task = "Read the user data from the database, register each user via the API, verify login for each, and write the results to Excel."

    result = await Console(team.run_stream(task=task))
    print(result)


asyncio.run(main())