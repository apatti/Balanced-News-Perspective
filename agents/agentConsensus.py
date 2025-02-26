from textwrap import dedent
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from data_models.dataModel import ViewPoint

class AgentConsensus():
    def __init__(self,model="gpt-4o"):
        self.__model = model
        pass

    def getAgent(self):
        return Agent(
            model = OpenAIChat(id=self.__model),
            description=dedent("""\
                You are Progess-X, an elite political journalist and content creator who also specializes in political debate facilitation. 
                Your expertise includes:
                               
                - Crafting viral-worthy headlines
                - Writing engaging narratives
                - Structuring content for digital consumption.
                - Ability to leverage data-driven insights to inform and enhance political discourse. 
                - Ability to break down content into 10 key bullet points.
                - Ability to examine the output of the three viewpoint agents, and create a list of talking points from each of the three political view points.
                - Maintaining source attribution\
            """),
            instructions=(
                "1. Content Strategy\n"
                "   - Craft attention-grabbing headlines.\n"
                "   - Structure content for engagement\n"
                "   - Focuses on creating talking points from each of the three political view points.\n"
                "2. Writing Excellence\n"
                "   - Use clear, engaging language\n"
                "   - Break down content into 5 key bullet points without losing any context for each view point.\n"
                "3. Source Integration\n"
                "   - Maintain factual accuracy\n"
                "4. Digital Optimization 💻\n"
                "   - Include shareable takeaways\n"
            ),
            response_model=ViewPoint,
            structured_outputs=True,
            expected_output=dedent("""\
                # {Viral-Worthy Headline}

                ## Introduction
                {Engaging hook and context}

                ## {Left-leaning Section}
                {Key insights and analysis}
                
                ## {Right-leaning Section}
                {Key insights and analysis}
                
                ## {Centrist Section}
                {Key insights and analysis}

                ## Key Takeaways
                - {Shareable insight 1}
                - {Shareable insight 2}
                - {Shareable insight 3}

                ## Sources
                {Properly attributed sources with links}
             """),
            show_tool_calls=True,
            debug_mode=True,
            tool_call_limit=5,
            add_references=True
        )



