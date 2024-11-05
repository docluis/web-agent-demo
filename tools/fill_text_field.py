from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field, Optional
from typing import Type

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from config import Config

class FillTextFieldInput(BaseModel):
    xpath_identifier: str = Field(description="The xpath of the text field.")
    value: str = Field(description="The value to be filled in the text field.", default="")


class FillTextFieldOutput(BaseModel):
    success: bool = Field(description="Whether the text field was filled successfully.")
    message: str = Field(description="The message indicating the result of the operation.")
    error: Optional[str] = Field(default=None, description="The error message if the operation failed.")


class FillTextField(BaseTool):
    cf: Config

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
            element = self.cf.driver.find_element(By.XPATH, xpath_identifier)
            # clear the field first
            element.clear()
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(Keys.DELETE)
            element.send_keys(50 * Keys.BACKSPACE)

            element.send_keys(value)
            output = FillTextFieldOutput(
                success=True, message=f"Filled in the text field {xpath_identifier} with {value}."
            )
            return output
        except Exception as e:
            output = FillTextFieldOutput(success=False, message="Failed to fill in the text field.", error=str(e))
            return output
