import json
import os
import time
import logging
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List, Union, Tuple, Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

from config import Config

# from src.interaction_agent.context import Context
from src.utils import extract_uri, parse_apis
from src.interaction_agent.tool_context import ToolContext
from src.log import logger
from src.interaction_agent.classes import GetOutgoingRequestsInput, GetOutgoingRequestsOutput


class GetOutgoingRequests(BaseTool):
    cf: Config
    context: ToolContext

    name: str = "get_outgoing_requests"
    description: str = (
        "Function: Get the outgoing requests.\n"
        "Args:\n"
        "  - filtered: bool Whether the outgoing requests should be filtered. (optional, default: True)\n"
        "Returns:\n"
        "  - success: bool Whether the outgoing requests were retrieved successfully.\n"
        "  - message: str The message indicating the result of the operation.\n"
        "  - outgoing_requests: str The outgoing requests.\n"
        "  - error: str The error message if the operation failed.\n"
    )
    args_schema: Type[BaseModel] = GetOutgoingRequestsInput

    def _run(self, filtered: bool = True) -> GetOutgoingRequestsOutput:
        """Use the tool."""
        input = GetOutgoingRequestsInput(filtered=filtered)
        try:
            logger.debug(f"Getting outgoing requests with filtered: {filtered}")
            p_reqs = parse_apis(
                driver=self.cf.driver,
                target=self.cf.target,
                uri=self.context.initial_uri,
                filtered=filtered,
            )
            p_reqs_str = json.dumps(p_reqs, indent=4)
            output = GetOutgoingRequestsOutput(
                success=True, message=f"Got outgoing requests with filtered: {filtered}.", outgoing_requests=p_reqs_str
            )
            self.context.tool_history.append((self.name, input, output))
            self.context.add_observed_uri(extract_uri(self.cf.driver.current_url))
            return output
        except Exception as e:
            logging.debug("Error: Failed to get outgoing requests.")
            output = GetOutgoingRequestsOutput(success=False, message="Failed to get outgoing requests.", error=str(e))
            self.context.tool_history.append((self.name, input, output))
            return output
