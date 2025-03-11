# AI Product Management: Balanced News Perspective App

## Task 1: What problem do you want to solve? Who is it a problem for?

### Problem:
We are predominantly exposed to biased news sources, missing out on diverse perspectives and a comprehensive understanding of events.

### Why this is a problem for our specific user:
In today's highly polarized media landscape, individuals often find themselves trapped in echo chambers, where they are only exposed to news that aligns with their existing beliefs. This lack of diverse perspectives can lead to a skewed understanding of current events, reinforcing biases and limiting critical thinking. For students, educators, journalists, and anyone engaged in debates or discussions about current affairs, this one-sided exposure to news can hinder their ability to form well-rounded opinions and make informed decisions. By not having access to multiple viewpoints, users miss out on the opportunity to understand the full picture and engage in meaningful, balanced discussions.

## Task 2: Propose a Solution

### Proposed Solution:
The Balanced News Perspective App aims to address this issue by providing users with a holistic view of the news. The app takes a headline as input and delivers three distinct perspectives: right-leaning, left-leaning, and center/unbiased. By presenting these diverse viewpoints, the app ensures users gain a well-rounded understanding of the news, fostering critical thinking and informed discussions. The user interface will be intuitive and user-friendly, allowing users to easily input headlines and receive balanced perspectives in a clear and concise format. The app will also feature educational tools to help users compare and contrast different viewpoints, enhancing their critical thinking skills.

### Agentic Reasoning:
The app will utilize agents to gather and analyze news from various sources, categorizing them into right-leaning, left-leaning, and center/unbiased perspectives, the app would then examine the output of the three viewpoint, and create a list of talking points from each of the three political view points. Agentic reasoning will be employed to ensure that the app provides accurate and relevant perspectives for each headline. This will involve using large language models (LLMs) to generate summaries and insights from the gathered news articles, ensuring that users receive comprehensive and balanced information.

### Technical Stack

#### LLM:
- **gpt-4o-mini:** Used for news sources and content retrieval agents. 
  - **Reasoning:** We don't need a powerful GPT model for retrieving and scraping sources.
- **gpt-4:** Used for viewpoint generation.
  - **Reasoning:** Picked a powerful model as we need the LLM to understand and generate different viewpoints.

#### Embedding Model:
- **Not used:** Due to rate limitations imposed by DuckDuckGo and Google search engines, instead, LLMs are used to generate the sources.

#### Orchestration:
- **Agno:** A lightweight library for building multi-modal Agents.
  - **Reasoning:** Agno (previously known as phiData) is lightweight and has 10k performance improvements over langchain/langgraph. Also, it provides an opportunity to learn a new framework.

#### Vector Database:
- **Not used:** Initially used Pinecone vectordb but had to drop it due to rate limitations. Instead, LLMs are used to generate the data and pass it along.

#### Monitoring:
- **Observability:** Used agno provided built-in monitoring capabilities that track session and performance metrics through app.agno.com.
  - **Reasoning:** Buit-in capability provided by Agno. (Attached screenshots)
  - <img width="1469" alt="Screenshot 2025-02-25 at 7 02 11 PM" src="https://github.com/user-attachments/assets/5586c09d-3ce5-400b-8f31-0005e9f54091" />
  - <img width="1465" alt="Screenshot 2025-02-25 at 11 13 06 PM" src="https://github.com/user-attachments/assets/1e92ab1e-69d9-45bd-a0fa-ad9611da7755" />


- **Custom logging:** Using the logging framework provided by Agno.
  - **Reasoning:** Provides comprehensive visibility into agent behavior and system performance.

#### Evaluation:
- **Not used:** Was planning to use RAGAS to evaluate the performance of LLM with use of data sources and kb extraction but with project pivot, didnt had a need to use it.
  - **Reasoning:** Ensures content quality and debate balance throughout the generation process.

#### User Interface:
- **Streamlit:** Used for building and sharing data apps.
  - **Reasoning:** A faster way to build and share data apps, and also Hugging Face has Streamlit-enabled space.

#### Serving and Inference:
- **Hosted on Hugging Face:** The solution is hosted on Hugging Face for serving and inference.

#### Architecture diagram:
![WhatsApp Image 2025-02-26 at 01 19 55](https://github.com/user-attachments/assets/2736b739-69df-4064-96aa-8ca5907d431c)


## Task 3: Dealing with the Data

### Data Sources and External APIs:
Initially, I identified around 30 external APIs (10 each from different perspectives) and planned to extract data from these sites based on user requests. Data extraction was intended to be done through DuckDuckGo and Google search tools (15 each to ensure a distribution of data) and then use Pinecone vectordb with semantic chunking to store the data.
<br/>However, I encountered rate limits imposed by both Google and DuckDuckGo. To avoid getting my IP blacklisted, I pivoted the project to utilize LLMs to generate news articles and then generate the viewpoints.
I have used the external URLs to generate data for three news headlines for fine-tuning embeddings.

The app has 4 agents:
1. **ViewpointRetrieverAgent**: Finds relevant news articles covering different perspectives.
2. **ContentGeneratorAgent**: Extracts the content from the news articles retrieved by the ViewpointRetrieverAgent.
3. **AgentProgress**: Generates left leaning summary
4. **AgentPatriot**: Generates right leaning summary
5. **AgentBalance**: Generates centrist summary
6. **AgentConsensus**: Takes output of three viewpoints and provides the talking points from each of the three political view points.

By integrating these agents, the Balanced News Perspective App will provide users with a comprehensive and balanced understanding of current events, empowering them to break free from biased news bubbles and engage in informed discussions.

## Task 4: Building a Quick End-to-End Prototype
[Balanced News Perpective](https://huggingface.co/spaces/ashwinpatti/Balanced-News-Perspective-App#balanced-news-perpective)

## Task 5: Creating a Golden Test Data Set
1. Identify Sources: Select 30 URLs ([News Sources](https://github.com/apatti/Balanced-News-Perspective/blob/main/fineTuning/newSources.json)) from various news media outlets, ensuring an equal representation of perspectives with 10 URLs each from center, left, and right-leaning sources.
2. Search Topics: Choose three different topics to search across these sites. Extract the relevant data from each URL for these topics.<br/>
     2.1 Topics: ["Musk influence on trump", "Abortion rights",  "Transgender Rights Advocates Condemn State Legislation Targeting Youth"]
3. Label Content: Categorize the extracted content based on its perspective (left, right, center). This will help in maintaining a balanced data set.
4. Compile Records: Combine the labeled content into a single dataset, resulting in 606 labeled records.
5. Fine-Tune Model: Use this dataset to fine-tune your embedding model, ensuring that it accurately represents the different perspectives.

Note: 
1. I initially started with 21 topics but had to cut short to 3 due to rate limit restriction by Google.
2. Topics: [ "Musk influence on trump", 
                 "Abortion rights",
                  "Transgender Rights Advocates Condemn State Legislation Targeting Youth",
                 "Abolition of DEI in federal hiring",
                 "Termination of Department of education",
                 "LA Fires",
                 "Tarrifs",
                 "Russia influence in USA politics",
                 "Oil drilling in USA",
                 "Stopping USAID",
                 "Gaza occupation by Isreal",
                 "Religious Freedom Advocates Challenge LGBTQ+ Anti-Discrimination Laws",
                 "AI would take over our jobs",
                 "Indians are stealing american jobs",
                 "Stock Market Sees Volatile Trading Day",
                 "Global warming",
                 "Support to Urkaine",
                 "Tax Cuts for Wealthy",
                 "Joe Biden presidency",
                 "Zelenskyy visit to white house"
                 "Social security"
                 ]
 

## Task 6: Fine-Tuning Open-Source Embeddings
As mentioned above, I had to drop from using RAG and hence there was no need to fine tune a embedding model

## Task 7:Assessing Performance

## Task 8: Loom video:
[Mid Term demo](https://www.loom.com/share/9eceeb4801bf401b965cd32b12e8ea98?sid=64122305-960e-4e75-b2a0-c016b13f0f38)

## Future enhancements:
1. Ability to share the final report as a pdf.
2. Ability to share the final report as a social media post.
3. Chat feature where users can ask more questions.
4. Fine-tuned embedding model to enhance chatting feature.
5. A validation agent to validate other agents.

