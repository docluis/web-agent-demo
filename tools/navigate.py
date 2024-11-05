import time
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional

from config import Config

class NavigateInput(BaseModel):
    url: str = Field(description="The URL to be navigated to.")


class NavigateOutput(BaseModel):
    success: bool = Field(description="Whether the navigation was successful.")
    message: str = Field(description="The message indicating the result of the operation.")
    error: Optional[str] = Field(default=None, description="The error message if the operation failed.")


class Navigate(BaseTool):
    cf: Config

    name: str = "navigate"
    description: str = (
        "Function: Navigate to a URL.\n"
        "Args:\n"
        "  - url: str The URL to be navigated to. (required)\n"
        "Returns:\n"
        "  - success: bool Whether the URL was navigated to successfully.\n"
        "  - message: str The message indicating the result of the operation.\n"
        "  - error: str The error message if the operation failed.\n"
    )
    args_schema: Type[BaseModel] = NavigateInput

    def _run(self, url: str) -> NavigateOutput:
        """Use the tool."""
        input = NavigateInput(url=url)
        try:
            self.cf.driver.get(url)
            time.sleep(self.cf.selenium_rate)
            url_now = self.cf.driver.current_url

            output = NavigateOutput(success=True, message=f"Navigated to the URL {url}. Actual URL now: {url_now}")
            return output
        except Exception as e:
            output = NavigateOutput(success=False, message="Failed to navigate to the URL.", error=str(e))
            return output
