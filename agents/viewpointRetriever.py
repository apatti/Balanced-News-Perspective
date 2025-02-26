from textwrap import dedent
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from data_models.dataModel import QueryResults
from agno.tools.duckduckgo import DuckDuckGoTools

class ViewpointRetrieverAgent():
    def __init__(self,model="gpt-4o-mini"):
        self.__model = model
        pass

    def getAgent(self):
        return Agent(
            model = OpenAIChat(id=self.__model),
            tools = [DuckDuckGoTools()],
            description=dedent("""\
                You are experienced journalist and editor specializing in political news articles. Your expertise includes:
                               
                - Finding relavant and tending news articles
                - Summarizing news articles
                - Evaluating content credibility, bias and relevance
                - Identifying diverse viewpoints on a topic
                - Identifying diverse prespecives and expert opinions
                - Retrieving news articles from different media biases i.e. left learning, right leaning, center, etc.
                - Identifying fake news and misinformation
                - Discovering unique angles and insights
                - Ensuring comphrensive coverage of a topic\
            """),
            instructions=(
                "1. Search Strategy: Use the search tool to find news articles on a specific topic.\n"
                "   - Find 15 relevant sources and select the 10 best ones.\n"
                "   - Prioritize recent, authoritative content\n"
                "   - Look for uniqu angles and insights\n"
                "2. Source Evaluation - Evaluate the credibility, bias and relevance of the sources.\n"
                "   - Assess content depth and uniqueness\n"
                "   - Identify click baits\n"
                "   - Identify fake news and misinformation\n"
                "3. Diversity of Perspectives - Find articles from different viewpoints.\n"
                "   - Identify left-leaning, right-leaning, and center sources\n"
                "   - Find expert opinions and diverse perspectives\n"
                "   - Include different viewpoints\n"
                "   - Gather both mainstream and expert opinions\n"
                "   - Gather opinions from different political affiliations\n"
                "   - Gather social media reactions and public opinions\n"
            ),
            response_model=QueryResults,
            structured_outputs=True
        )



