from agno.workflow import RunEvent, RunResponse, Workflow
from textwrap import dedent
from agno.agent import Agent
from agents.agentBalance import AgentBalance
from agents.agentConsensus import AgentConsensus
from agents.contentGenerator import ContentGeneratorAgent
from agents.viewpointRetriever import ViewpointRetrieverAgent
from agents.agentPatriot import AgentPatriot
from agents.agentProgress import AgentProgress
from typing import Dict, Iterator, Optional
from data_models.dataModel import ViewPoint, ArticleContent, QueryResults,Consensus
from agno.utils.log import logger
from utils.messageFormat import MessageFormat
import json


class BalancedNewsGenerator(Workflow):
    """Advanced workflow that intelligently dissects news headlines and provides diverse viewpoints."""

    description: str = dedent("""\
        An intelligent news generator that helps to generate balanced news articles by providing diverse viewpoints on a topic. 
        This workflow orchestrates multiple AI agent to analyze news articles, summarize content, evaluate credibility and bias, 
        and identify diverse perspectives. The workflow is ideal for journalists, editors, and anyone looking to gain a comprehensive 
        understanding of a news topic by exploring multiple viewpoints. The system excels at creating content that is both informative and optimized for
        digital consumption.
    """)

    # News Retriver Agent: Handles intelligent web searching and source gathering
    newsRetriever: Agent = (ViewpointRetrieverAgent()).getAgent()

    # Content Generator: Extracts and processes article content
    newsContentGenerator: Agent = (ContentGeneratorAgent()).getAgent()

    # Agent Progress: Takes the retrieved information and generates a left-leaning interpretation.
    progress: Agent = (AgentProgress()).getAgent()

    # Agent Progress: Takes the retrieved information and generates a right-leaning interpretation.
    patriot: Agent = (AgentPatriot()).getAgent()

    # Agent Progress: Takes the retrieved information and generates a centerist interpretation.
    balance: Agent = (AgentBalance()).getAgent()

    # Agent Consensus: Examine the output of the three viewpoint agents, and create a list of talking points from each of the three political view points
    consensus: Agent = (AgentConsensus()).getAgent()

    def run(
        self,
        query: str,
        use_search_cache: bool = True,
        use_content_generator_cache: bool = True,
        use_viewpoint_report: bool = True,
        st = None
    ) -> Iterator[RunResponse]:
        messageFormat = MessageFormat(st)
    
        # Use the cached if use_cache is True
        if use_viewpoint_report:
            cached_left_view = self.get_cached_left_view(query)
            cached_right_view = self.get_cached_right_viewt(query)
            cached_center_view = self.get_cached_center_view(query)
            cached_final_view = self.get_cached_final_view(query)
            if cached_final_view:
                yield RunResponse(
                    content=[cached_left_view,cached_right_view,cached_center_view,cached_final_view], event=RunEvent.workflow_completed
                )
                return
        with(st.spinner('Retrieving latest news articles...')):
            query_results: Optional[QueryResults] = self.get_query_results(query, use_search_cache)
            with st.expander("Retrieved news articles", expanded=False):
                messageFormat.formatQueryResults(query_results["articles"])
                
        logger.debug(f"Query results: {query_results}")
        # If no query_results are found for the topic, end the workflow
        if query_results is None or len(query_results['articles']) == 0:
            yield RunResponse(
                event=RunEvent.workflow_completed,
                content=f"Sorry, could not find any articles on the topic: {query}",
            )
            return
        
        logger.debug(f"Extracting content from the news articles for: {query}")
        # Extract content from the articles
        with(st.spinner('Extracting content from the news articles...')):
            article_contents: Dict[str, ArticleContent] = self.extract_article_contents(query,query_results, use_content_generator_cache)
            with st.expander("Retrieved article summaries", expanded=False):
                messageFormat.formatArticleSummaries(article_contents.values())

        logger.debug(
            'Extracted the article content!!'
        )
        # Generate viewpoints
        with(st.spinner('Retrieving left prespective...')):
            left_view=self.write_view_point(query, article_contents, "left")
            #logger.debug(f"Left View:\n{left_view}")
            with st.expander("Left View", expanded=True):
                messageFormat.formatPerspectiveView(left_view)
                
        with(st.spinner('Retrieving right prespective...')):
            right_view=self.write_view_point(query, article_contents, "right")
            with st.expander("Right View", expanded=True):
                messageFormat.formatPerspectiveView(right_view)

        with(st.spinner('Retrieving center prespective...')):
            center_view=self.write_view_point(query, article_contents, "center")
            with st.expander("Center View", expanded=True):
                messageFormat.formatPerspectiveView(center_view)
        
        
        # Generate final view
        with(st.spinner('Consulting experts...')):
            consensus_report = self.write_final_view(query,left_view,right_view,center_view)
            #st.markdown(consensus_report)
            yield RunResponse(
                content=consensus_report,
                event=RunEvent.workflow_completed
            )

    def write_final_view(
            self,
            query: str,
            leftView: str,
            rightView: str,
            centerView: str
    ) -> Consensus:
        
        viewpoint_input = dedent(f"""
            <headline>
                {query}
            </headline>
            <viewPoints>
                <left>
                    <title>{leftView.title}</title>
                    <summary>{leftView.summary}</summary>
                    <content>
                        {"\n".join(leftView.content)}
                    </content>
                    <sources>
                        {"\n".join(leftView.urls)}
                    </sources>
                </left>
                <right>
                    <title>{rightView.title}</title>
                    <summary>{rightView.summary}</summary>
                    <content>
                        {"\n".join(rightView.content)}
                    </content>
                    <sources>
                        {"\n".join(rightView.urls)}
                    </sources>
                </right>
                <center>
                    <title>{centerView.title}</title>
                    <summary>{centerView.summary}</summary>
                    <content>
                        {"\n".join(centerView.content)}
                    </content>
                    <sources>
                        {"\n".join(centerView.urls)}
                    </sources>
                </center>
            </viewPoints>
        """)

        #yield self.consensus.run(json.dumps(viewpoint_input, indent=4), stream=True)
        consensus_response = self.consensus.run(viewpoint_input)
        if(
                consensus_response is not None
                and consensus_response.content is not None
                and isinstance(consensus_response.content, Consensus)
            ):
            #self.add_final_view_to_cache(query, consensus_response.content)
            return consensus_response.content


    def write_view_point(
            self,
            query: str,
            articleContents: Dict[str, ArticleContent],
            viewPoint: str
    ) -> ViewPoint:
        
        viewpoint_input = dedent(f"""
            <headline> 
                {query}
            </headline>
                                 
            <articles> 
                {"\n".join([v.content for v in articleContents.values()])}
            </articles>
        """)

        logger.debug(f"Generating viewpoint for {viewpoint_input}")
        if viewPoint == "left":
            left_response:RunResponse = self.progress.run(viewpoint_input)
            if(
                left_response is not None
                and left_response.content is not None
                and isinstance(left_response.content, ViewPoint)
            ):
                self.add_left_view_to_cache(query, left_response.content)
                #logger.debug(f"Left View:\n{left_response.content}")
                #self.st.markdown(left_response.content)
                return left_response.content
        elif viewPoint == "right":
            right_response:RunResponse = self.patriot.run(viewpoint_input)
            if(
                right_response is not None
                and right_response.content is not None
                and isinstance(right_response.content, ViewPoint)
            ):
                self.add_right_view_to_cache(query, right_response.content)
                #self.st.markdown(right_response.content)
                return right_response.content
        elif viewPoint == "center": 
            center_response:RunResponse = self.balance.run(viewpoint_input)
            if(
                center_response is not None
                and center_response.content is not None
                and isinstance(center_response.content, ViewPoint)
            ):
                self.add_center_view_to_cache(query, center_response.content)
                #self.st.markdown(center_response.content)
                return center_response.content

        #return viewpoint_response
            

    def get_cached_left_view(self, query: str) -> Optional[ViewPoint]:
        logger.debug("Checking if cached left view exist")
        return self.session_state.get("left_view", {}).get(query)
    def add_left_view_to_cache(self, query: str,view: str):
        logger.debug(f"Saving left view results for: {query}")
        self.session_state.setdefault("left_view", {})
        self.session_state["left_view"][query] = view.model_dump()
        self.write_to_storage()
    
    def get_cached_right_viewt(self, query: str) -> Optional[ViewPoint]:
        logger.debug("Checking if cached search results exist")
        return self.session_state.get("right_view", {}).get(query)
    def add_right_view_to_cache(self, query: str,view: str):
        logger.debug(f"Saving right view results for: {query}")
        self.session_state.setdefault("right_view", {})
        self.session_state["right_view"][query] = view.model_dump()
        self.write_to_storage()
    
    def get_cached_center_view(self, query: str) -> Optional[ViewPoint]:
        logger.debug("Checking if cached search results exist")
        return self.session_state.get("center_view", {}).get(query)
    def add_center_view_to_cache(self, query: str,view: str):
        logger.debug(f"Saving center view results for: {query}")
        self.session_state.setdefault("center_view", {})
        self.session_state["center_view"][query] = view.model_dump()
        self.write_to_storage()

    def get_cached_final_view(self, query: str) -> Optional[ViewPoint]:
        logger.debug("Checking if cached search results exist")
        return self.session_state.get("final_view", {}).get(query)
    def add_final_view_to_cache(self, query: str,view: str):
        logger.debug(f"Saving final view results for: {query}")
        self.session_state.setdefault("final_view", {})
        logger.debug(f"Final View:\n {view}")
        self.session_state["final_view"][query] = view.model_dump()
        self.write_to_storage()
        logger.debug(f"Saved final view results for: {query}")

    def get_cached_search_results(self, query: str) -> Optional[QueryResults]:
        logger.debug("Checking if cached search results exist")
        return self.session_state.get("query_results", {}).get(query)

    def add_search_results_to_cache(self, query: str, query_results: QueryResults):
        logger.debug(f"Saving query results for: {query}")
        self.session_state.setdefault("query_results", {})
        self.session_state["query_results"][query] = query_results.model_dump()
        self.write_to_storage()
    

    def get_cached_article_contents(self, query: str) -> Optional[QueryResults]:
        logger.debug(f"Checking if cached article contents exist for: {query}")
        return self.session_state.get("extracted_article_contents_results", {}).get(query)
    
    def add_article_contents_to_cache(self, query: str, article_contents: Dict[str, ArticleContent]):
        logger.debug(f"Saving extract article contents for: {query}")
        self.session_state.setdefault("extracted_article_contents_results", {})
        self.session_state["extracted_article_contents_results"][query] = article_contents
        self.write_to_storage()

    def get_query_results(
            self, query: str, use_search_cache: bool = True
    ) -> Optional[QueryResults]:
        """Retrieve news articles based on the given query."""
        if use_search_cache:
            query_results_from_cache = self.get_cached_search_results(query)
            if query_results_from_cache:
                return query_results_from_cache
            
        query_response: RunResponse = self.newsRetriever.run(query)
        if (
            query_response is not None 
            and query_response.content is not None 
            and isinstance(query_response.content, QueryResults)
           ):
            logger.debug("Saving query results to cache")
            self.add_search_results_to_cache(query, query_response.content)
            return query_response.content.model_dump() 

        return None

    def extract_article_contents(self, query: str, query_results: QueryResults, use_content_generator_cache: bool = True) -> Dict[str, ArticleContent]:
        article_contents: Dict[str,ArticleContent] = {}

        if use_content_generator_cache:
            logger.debug(f"Checking if cached article contents exist for: {query}")
            article_contents_from_cache = self.get_cached_article_contents(query)
            if article_contents_from_cache:
                logger.debug(f"Found: {len(article_contents_from_cache)}")
                return article_contents_from_cache
            
        logger.debug(f"Extracting content from the news articles for: {len(query_results['articles'])}")
        for article in query_results['articles']:
            logger.debug(f"Extracting content for: {article['url']}")
            if article['url'] in article_contents:
                continue
            content_response: RunResponse = self.newsContentGenerator.run(article['url'])
            if (
                content_response is not None 
                and content_response.content is not None 
                and isinstance(content_response.content, ArticleContent)
            ):
                article_contents[content_response.content.url] = (content_response.content)
            
        self.add_article_contents_to_cache(query, article_contents)
        return article_contents
