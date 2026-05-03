import os
from dotenv import load_dotenv
from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench

load_dotenv()


class McpConfig:

    def __init__(self):
        pass

    def get_mysql_workbench(self):
        mysql_params = StdioServerParams(
            command="npx",
            args=[
                "-y",
                "@benborla29/mcp-server-mysql"
            ],
            env= {
                "MYSQL_HOST": os.getenv("MYSQL_HOST"),
                "MYSQL_PORT": os.getenv("MYSQL_PORT"),
                "MYSQL_USER": os.getenv("MYSQL_USER"),
                "MYSQL_PASS": os.getenv("MYSQL_PASS"),
                "MYSQL_DB": os.getenv("MYSQL_DB"),
            }
        )
        return McpWorkbench(server_params= mysql_params)