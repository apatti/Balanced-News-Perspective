from agno.knowledge.website import WebsiteKnowledgeBase
from agno.utils import get_logger
from vectorDB import vector_db

class NewsKnowledgeBase:
    def __init__(self, newsSources):
        self.__logger = get_logger(__name__)
        self.__sources = newsSources

    def getKnowledgeBase(self):
        knowledge_base = WebsiteKnowledgeBase(
            urls=self.__sources,
            vector_db=vector_db,
            max_links=1, #Follow max one link as we are providing news article.
            sources=self.__sources
        )
        return knowledge_base
    