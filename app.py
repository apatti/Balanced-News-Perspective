
import streamlit as st
from agno.storage.workflow.sqlite import SqliteWorkflowStorage
from BalancedNewsGenerator import BalancedNewsGenerator
from typing import Iterator, Union, Iterable
from agno.workflow import RunResponse
from data_models.dataModel import Consensus
from utils.messageFormat import MessageFormat
import dotenv
dotenv.load_dotenv()

st.title("Balanced News Perpective")
st.write("An innovative tool designed to provide users with diverse perspectives on news headlines.")
st.write(" The app takes a headline as input and delivers three distinct views: right-leaning, left-leaning, and center/unbiased. By presenting these perspectives, the app ensures users gain a well-rounded understanding of the news, fostering critical thinking and informed discussions.")
headLine = st.text_input("Enter a news headline:")
st.write("Please enter a news headline to get started.")
if not headLine:
    st.stop()

generate_news = BalancedNewsGenerator(
    session_id=f"BalancedNewsGenerator-{headLine}",
    storage=SqliteWorkflowStorage(
        db_file="tmp/workflowss.db",
        table_name="balanced_news_workflow"
    )
)

messageFormat = MessageFormat(st)

response : Iterator["RunResponse"] = generate_news.run(
        query=headLine,
        use_search_cache=True,
        use_content_generator_cache=True,
        use_viewpoint_report=True,
        st=st
    )
with(st.spinner('Agents at work...')):
    for resp in response:
        with st.expander("Overall Prespective", expanded=True):
            messageFormat.formatConsensusView(resp.content)

st.success('Analysis complete!')