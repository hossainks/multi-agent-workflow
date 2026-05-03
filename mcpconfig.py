import os
from dotenv import load_dotenv
from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench

load_dotenv()


class McpConfig:

    @staticmethod
    def get_mysql_workbench():
        mysql_params = StdioServerParams(
            command="npx",
            args=[
                "-y",
                "@benborla29/mcp-server-mysql"
            ],
            env={k: v for k, v in { # type: ignore[arg-type]
                "MYSQL_HOST": os.getenv("MYSQL_HOST"),
                "MYSQL_PORT": os.getenv("MYSQL_PORT"),
                "MYSQL_USER": os.getenv("MYSQL_USER"),
                "MYSQL_PASS": os.getenv("MYSQL_PASS"),
                "MYSQL_DB": os.getenv("MYSQL_DB"),
            }.items() if v is not None},
            read_timeout_seconds=60
        )
        return McpWorkbench(server_params= mysql_params)

    @staticmethod
    def get_restapi_workbench():
        restapi_params = StdioServerParams(
            command="npx",
            args=[
                "-y",
                "dkmaker-mcp-rest-api"
            ],
            env={ # type: ignore[arg-type]
                "REST_BASE_URL": "https://rahulshettyacademy.com",
                "HEADER_Accept": "application/json"
            },
            read_timeout_seconds=60
        )
        return McpWorkbench(server_params= restapi_params)

    @staticmethod
    def get_excel_workbench():
        excel_params = StdioServerParams(
            command="npx",
            args=[
                "--yes",
                "@negokaz/excel-mcp-server"
            ],
            env={ # type: ignore[arg-type]
                "EXCEL_MCP_PAGING_CELLS_LIMIT": "4000"
            },
            read_timeout_seconds=60
        )
        return McpWorkbench(server_params= excel_params)

    @staticmethod
    def get_filesystem_workbench():
        filesystem_params = StdioServerParams(
            command="npx",
            args=[
                "-y",
                "@modelcontextprotocol/server-filesystem",
                "C:\\Users\\FXDCIU\\Desktop\\Claude-Test\\Json-Files"
            ],
            read_timeout_seconds=60
        )
        return McpWorkbench(server_params= filesystem_params)