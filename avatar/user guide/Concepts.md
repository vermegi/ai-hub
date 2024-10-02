# Key Concepts

## Generative AI

Artificial Intelligence (AI) imitates human behavior by using machine learning to interact with the environment and execute tasks without explicit directions on what to output. Generative AI describes a category of capabilities within AI that create original content. People typically interact with generative AI that has been built into chat applications.

## Vector Database

A **vector database** is a database designed to store and manage vector embeddings, which are mathematical representations of data in a high-dimensional space. In this space, each dimension corresponds to a feature of the data, and tens of thousands of dimensions might be used to represent sophisticated data. A vector's position in this space represents its characteristics. Words, phrases, or entire documents, and images, audio, and other types of data can all be vectorized.A vector database that is **integrated** in a highly performant NoSQL or relational database provides additional capabilities. The **integrated vector database** in a NoSQL or relational database can store, index, and query embeddings alongside the corresponding original data. In this repo we help you understand via working example how vectors are generated when data is inserted into Azure AI Search from Azure Cosmos DB and is used for vector searches.

<img src='/media/00_RAGwithAISearch.png' width='650' height='280'>

Users then ask natural language questions using the web-based search bar user interface (User Prompts). These prompts are then changed search query with vectorized data and used to search in Azure AI Search. The results are then sent back to the user. All of the User Search History are stored in a Cosmos DB container along with the number of tokens consumed by each user prompt. In a production environment users would only be able to see their own sessions but this solution shows all sessions from all users.

## Azure Search


## Promptflow


## Indexes


# References

* [Generative AI Fundamentals: Explore Fundamentals Of Generative AI (1 of 3)](https://learn.microsoft.com/shows/on-demand-instructor-led-training-series/generative-ai-module-1/)
