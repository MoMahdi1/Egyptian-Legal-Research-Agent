## Project Structure

```
Egyptian-Legal-Research-Agent/
│
├── app/
│   │
│   ├── agents/
│   │   ├── orchestrator_agent.py   # Coordinates the multi-agent workflow
│   │   ├── retriever_agent.py      # Retrieves relevant legal documents
│   │   ├── critic_agent.py         # Reviews and validates generated answers
│   │   ├── writer_agent.py         # Generates the final legal response
│   │   └── reranker.py             # Re-ranks retrieved documents by relevance
│   │
│   ├── llms/
│   │   └── provider.py             # LLM provider abstraction layer
│   │
│   ├── tools/
│   │   ├── search.py               # Tavily web search integration
│   │   └── retriever.py            # Retrieval utilities
│   │
│   ├── graph.py                    # LangGraph workflow definition
│   ├── state.py                    # Shared state management
│   └── main.py                     # FastAPI application entry point
│
├── frontend/                       # User interface
├── data/                           # Egyptian legal documents and datasets
├── tests/                          # Unit and integration tests
├── .env                            # Environment variables
├── requirements.txt                # Project dependencies
├── Dockerfile                      # Docker image configuration
├── docker-compose.yml              # Container orchestration
└── README.md                       # Project documentation
```
