

class MessageFormat:
    def __init__(self, st):
        self.st = st

    def formatQueryResults(self, results):
        self.st.markdown("### Retrieved news articles")
        for article in results:
            self.st.markdown(f"- [{article['title']}]({article['url']})")
        pass

    def formatArticleSummaries(self, articleSummaries):
        for article in articleSummaries:
            self.st.markdown(f"- [{article.title}]({article.url})")
            self.st.markdown(f"    - **Summary:** {article.summary}")
        pass

    def formatPerspectiveView(self,view):
        self.st.markdown(f"### {view.title}")
        self.st.markdown(f"**Summary:** {view.summary}")
        self.st.markdown("**Content:**\n")
        for content in view.content:
            self.st.markdown(f"- {content}")
        pass

    def formatConsensusView(self, content):
        self.st.markdown(f"### {content.headline}")
        self.st.markdown("#### Introduction:")
        self.st.markdown(content.introduction)
        self.st.markdown("#### Left-leaning Perspective:")
        self.st.markdown(content.left_section)
        self.st.markdown("#### Right-leaning Perspective:")
        self.st.markdown(content.right_section)
        self.st.markdown("#### Center Perspective:")
        self.st.markdown(content.center_section)
        self.st.markdown("#### Key Takeaways:")
        for key_takeaway in content.key_takeaways:
            self.st.markdown(f"- {key_takeaway}")
        self.st.markdown("#### Sources:")
        for source in content.sources:
            self.st.markdown(f"- {source})")
        
        pass