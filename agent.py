from typing import List, Literal, TypedDict

from tools.navigate import Navigate
from tools.click import Click
from tools.fill_text_field import FillTextField
from tools.get_page_soup import GetPageSoup

from prompts import high_level_planner_prompt, high_level_replanner_prompt


class State(TypedDict):
    prompt: str
    plan: List[str]
    report: str


class Agent:
    def __inti__(self, cf):
        self.cf = cf
        self.app = self._init_app()

    def _init_tools(self):
        return [
            Navigate(cf=self.cf),
            Click(cf=self.cf),
            FillTextField(cf=self.cf),
            GetPageSoup(cf=self.cf),
        ]
    
    def _init_app(self):
        def should_report(state: State) -> Literal["executer", "reporter"]:
            if "plans" in state and state["plans"] == []:
                return "reporter"
            else:
                return "executer"
            
        high_level_planner = high_level_planner_prompt | self.cf.model.with_structured_output(PlanModel)
        high_level_replanner = high_level_replanner_prompt | self.cf.model.with_structured_output(Act)