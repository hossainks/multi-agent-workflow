from autogen_agentchat.agents import AssistantAgent
from mcpconfig import McpConfig


class AgentAgency:
    def __init__(self,model_client):
        self.model_client = model_client
        self.mcpconfig = McpConfig()

    def create_database_agent(self,system_message):
        db_expert= AssistantAgent( name='DatabaseExpert', model_client= self.model_client, workbench=self.mcpconfig.get_mysql_workbench(), system_message= system_message )

        return db_expert