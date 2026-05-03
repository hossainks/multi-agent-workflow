from autogen_agentchat.agents import AssistantAgent


class AgentAgency:
    def __init__(self,model_client):
        self.model_client = model_client

    def create_database_agent(self,system_message):
            db_expert= AssistantAgent( name='DatabaseExpert', model_client= self.model_client, workbench='', system_message= system_message )