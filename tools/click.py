import time
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional

from selenium.webdriver.common.by import By

from config import Config

class ClickInput(BaseModel):
    xpath_identifier: str = Field(description="The xpath of the element to be clicked.")
    using_javascript: bool = Field(default=False, description="Whether to use JavaScript to click.")


class ClickOutput(BaseModel):
    success: bool = Field(description="Whether the element was clicked successfully.")
    message: str = Field(description="The message indicating the result of the operation.")
    page_diff: Optional[str] = Field(description="The diff of the page before and after clicking.")
    error: Optional[str] = Field(default=None, description="The error message if the operation failed.")


class Click(BaseTool):
    cf: Config

    name: str = "click"
    description: str = (
        "Function: Click on an element.\n"
        "Args:\n"
        "  - xpath_identifier: str The xpath of the element to be clicked. (required)\n"
        "  - using_javascript: bool Whether to use JavaScript to click. (optional, default: True)\n"
        "Returns:\n"
        "  - success: bool Whether the element was clicked successfully.\n"
        "  - message: str The message indicating the result of the operation.\n"
        "  - error: str The error message if the operation failed.\n"
    )
    args_schema: Type[BaseModel] = ClickInput

    def _run(self, xpath_identifier: str, using_javascript: bool = True) -> ClickOutput:
        """Use the tool."""
        try:
            time.sleep(self.cf.selenium_rate)
            element = self.cf.driver.find_element(By.XPATH, xpath_identifier)
            if using_javascript:
                self.cf.driver.execute_script("arguments[0].click();", element)
            else:
                element.click()

            time.sleep(self.cf.selenium_rate)
            message = f"Clicked element with name: {xpath_identifier}. Current URL: {self.cf.driver.current_url}"

            output = ClickOutput(success=True, message=message)
            return output
        except Exception as e:
            output = ClickOutput(
                success=False,
                message=f"Failed to click element. Current URL: {self.cf.driver.current_url}",
                error=str(e),
            )
            return output
