from bs4 import BeautifulSoup
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional


from config import Config

class GetPageSoupInput(BaseModel):
    pass

class GetPageSoupOutput(BaseModel):
    success: bool = Field(description="Whether the page source was retrieved successfully.")
    page_source: Optional[str] = Field(description="The page source.")
    error: Optional[str] = Field(default=None, description="The error message if the operation failed.")


class GetPageSoup(BaseTool):
    cf: Config

    name: str = "get_page_soup"
    description: str = (
        "Function: Get the page source.\n"
        "Returns:\n"
        "  - success: bool Whether the page source was retrieved successfully.\n"
        "  - page_source: str The page source.\n"
        "  - error: str The error message if the operation failed.\n"
    )
    args_schema: Type[BaseModel] = GetPageSoupInput

    def _run(self) -> GetPageSoupOutput:
        """Use the tool."""
        input = GetPageSoupInput()
        try:
            res = BeautifulSoup(self.cf.driver.page_source, "html.parser")
            output = GetPageSoupOutput(
                success=True,
                page_source=res.prettify(),
            )
            return output
        except Exception as e:
            output = GetPageSoupOutput(
                success=False, error=str(e), page_source=None
            )
            return output
