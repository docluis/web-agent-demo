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
from src.utils import extract_uri
from src.interaction_agent.tool_context import ToolContext
from src.log import logger
from src.interaction_agent.classes import FillTextFieldInput, FillTextFieldOutput


class FillTextField(BaseTool):
    cf: Config
    context: ToolContext

    name: str = "fill_text_field"
    description: str = (
        "Function: Fill in a text field.\n"
        "Args:\n"
        "  - xpath_identifier: str The xpath of the element to be clicked. (required)\n"
        "  - value: str The value to be filled in the text field. (optional, default: '')\n"
        "Returns:\n"
        "  - success: bool Whether the text field was filled successfully.\n"
        "  - message: str The message indicating the result of the operation.\n"
        "  - error: str The error message if the operation failed.\n"
    )
    args_schema: Type[BaseModel] = FillTextFieldInput

    def _run(self, xpath_identifier: str, value: str = "") -> FillTextFieldOutput:
        """Use the tool."""
        input = FillTextFieldInput(xpath_identifier=xpath_identifier, value=value)
        try:
            logger.debug(f"Filling in the text field {xpath_identifier} with {value}")
            element = self.cf.driver.find_element(By.XPATH, xpath_identifier)
            # clear the field first
            element.clear()
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(Keys.DELETE)
            element.send_keys(50 * Keys.BACKSPACE)

            element.send_keys(value)
            actual_value = element.get_attribute("value")

            # self.context.note_uri(self.cf)
            output = FillTextFieldOutput(
                success=True, message=f"Filled in the text field {xpath_identifier} with {value}."
            )
            self.context.tool_history.append((self.name, input, output))
            self.context.add_observed_uri(extract_uri(self.cf.driver.current_url))
            return output
        except Exception as e:
            # logging.error(str(e))
            logging.debug("Error: Failed to fill in the text field.")
            output = FillTextFieldOutput(success=False, message="Failed to fill in the text field.", error=str(e))
            self.context.tool_history.append((self.name, input, output))
            return output
