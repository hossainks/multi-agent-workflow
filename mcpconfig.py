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

    def get_restapi_workbench(self):
        restapi_params = StdioServerParams(
            command="npx",
            args=[
                "-y",
                "dkmaker-mcp-rest-api"
            ],
            env={
                "REST_BASE_URL": "https://rahulshettyacademy.com",
                "HEADER_Accept": "application/json"
            }
        )
        return McpWorkbench(server_params= restapi_params)

    def get_excel_workbench(self):
        excel_params = StdioServerParams(
            command="npx",
            args=[
                "--yes",
                "@negokaz/excel-mcp-server"
            ],
            env={
                "EXCEL_MCP_PAGING_CELLS_LIMIT": "4000"
            }
        )
        return McpWorkbench(server_params= excel_params)

    def get_filesystem_workbench(self):
        filesystem_params = StdioServerParams(
            command="npx",
            args=[
                "-y",
                "@modelcontextprotocol/server-filesystem",
                "C:\\Users\\FXDCIU\\Desktop\\Claude-Test\\Json-Files"
            ]
        )
        return McpWorkbench(server_params= filesystem_params)