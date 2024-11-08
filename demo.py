from config import Config
from src.interaction_agent.agent import InteractionAgent
from src.llm.api_parser import LLM_ApiParser

target = "https://demoqa.com/webtables"

print()
print("Starting interaction agent demo...")
print()
config = Config(target)
agent = InteractionAgent(cf=config, llm_page_request_parser=LLM_ApiParser(config))

agent.interact(uri="/webtables", interaction="Coworker Table", limit="1")
