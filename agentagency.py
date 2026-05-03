from autogen_agentchat.agents import AssistantAgent
from mcpconfig import McpConfig


class AgentAgency:
    def __init__(self,model_client):
        self.model_client = model_client
        self.mcpconfig = McpConfig()

    def create_database_agent(self,system_message):
        db_expert= AssistantAgent( name='DatabaseExpert', model_client= self.model_client, workbench=self.mcpconfig.get_mysql_workbench(), system_message= system_message )

        return db_expert

    def create_api_agent(self, system_message):
        restapi_workbench = self.mcpconfig.get_restapi_workbench()
        filesystem_workbench = self.mcpconfig.get_filesystem_workbench()
        api_agent = AssistantAgent(name='ApiAgent', model_client=self.model_client, workbench=[restapi_workbench, filesystem_workbench], system_message=system_message)

        return api_agent

    def create_excel_agent(self, system_message):
        excel_workbench = self.mcpconfig.get_excel_workbench()
        excel_agent = AssistantAgent(name='ExcelAgent', model_client=self.model_client, workbench=excel_workbench, system_message=system_message)

        return excel_agent