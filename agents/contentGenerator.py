from textwrap import dedent
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from data_models.dataModel import ArticleContent
from agno.tools.newspaper4k import Newspaper4kTools

class ContentGeneratorAgent():
    def __init__(self,model="gpt-4o-mini"):
        self.__model = model
        pass

    def getAgent(self):
        return Agent(
            model = OpenAIChat(id=self.__model),
            tools = [Newspaper4kTools()],
            description=dedent("""\
                You are ContentBot-X, a specialist in extracting and processing digital content. Your expertise includes:
                               
                - Efficient content extraction
                - Smart formatting and structuring
                - Key information identification
                - Maintaining source attribution\
            """),
            instructions=(
                "1. Content Extraction\n"
                "   - Extract content from the article.\n"
                "   - Preserve important quotes and statistics\n"
                "   - Handle paywalls gracefully\n"
                "   - Avoid loop\n"
                "2. Content Processing\n"
                "   - Extract only text and ignore videos or images\n"
                "   - Format text in clean markdown\n"
                "   - Preserve key information\n"
                "   - Structure content logically\n"
                "3. Quality Control\n"
                "   - Verify content relevance\n"
                "   - Ensure accurate extraction\n"
                "   - Maintain readability\n"
            ),
            response_model=ArticleContent,
            structured_outputs=True,
            show_tool_calls=True,
            debug_mode=False,
            tool_call_limit=5,
            add_references=True
        )



