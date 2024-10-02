# FSI Industry - Custom support virtual agent - Avatar based

## Introduction

Customer facing support and assistance is essential to any business that relies on B2C engagement. Through digital or physical means, assistance is carried out to either fix a customer issue or help them navigate the multiple options that the business has to offer. 

The Banking industry has been relying on GenerativeAI to simplify this process, adding a chatbot component to their public facing websites that leverages internal data to be able to answer the customer’s questions. Usually, this GenAI use case will be divided into 3 main scenarios: 

-  External Customer facing web application for support on specific issues or assistance in acquiring services 

- Internal Employee facing web application to accelerate productivity 

- Video production for marketing material leveraging image based LLMs 

## Solution Architecture


TODO: INSERT ARCHTECTURE PICTURE

| <img src='/media/00_Solution_Architecture.png' width='790' height='500'> |
| ---- |

## Key Components

Components of the solution are as follows:

- **Azure AI Studio** is a PaaS based platform for chatbot creation. The comprehensive platform accelerates the development of production-ready copilots to support enterprise chat, content generation, data analysis, and more. It integrates with the other platforms of Azure AI Services, such as Speech, AI Search, etc, while also maintaining tools for productivity and operationalization of the development, such as PromptFlow, the model catalog, content filtering and safety. 
    - **Promptflow** is a development tool designed to streamline the entire development cycle of AI applications powered by Large Language Models (LLMs). Prompt flow provides a comprehensive solution that simplifies the process of prototyping, experimenting, iterating, and deploying your AI applications.Prompt flow is available independently as an open-source project on GitHub, with its own SDK and VS Code extension. 
- **Azure Speech to Text** enables real-time and batch transcription of audio 		streams into text. With additional reference text input, it also enables real-time 	pronunciation assessment and gives speakers feedback on the accuracy and 	fluency of spoken audio. 
- **Azure Text to Speech** to speech enables applications, tools, or devices to convert text into human like synthesized speech. The text to speech capability is also known as speech synthesis. Use human like prebuilt neural voices out of the box, or create a custom neural voice that's unique to your product or brand 
- **AI Search** - A cloud solution that provides a rich search experience with key word and vector store capabilities over private, heterogeneous content in web, mobile, and enterprise applications. This will be used for vector search functionality.
- **Azure OpenAI Service** provides REST API access to OpenAI's powerful language models including Embeddings model series. Users can access the service through REST APIs, Python SDK, or our web-based interface in the Azure OpenAI Studio.  This will be used for embedding functionality.
- **Azure Content Safety** is a service that helps you detect and filter harmful user-generated and AI-generated content in your applications and services. Content Safety includes text and image detection to find content that is offensive, risky, or undesirable, such as profanity, adult content, gore, violence, hate speech, and more. This will be used to implement responsible generative AI measures.

## Getting Started

This repo assumes you are familiar with the basics of Generative AI 

### Prerequisites

You need the following to be able to deploy the solution:

- Azure Subscription : Ideally use a dedicated Azure subscription, where you have submitted the subscription ID into the form for [requesting access to Azure OpenAI](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR7en2Ais5pxKtso_Pz4b1_xUOFA5Qk1UWDRBMjg0WFhPMkIzTzhKQ1dWNyQlQCN0PWcu). This will ensure that the subscription is enabled for Azure OpenAI, including GTP-4.
- The user who's deploying the reference implementation must be Owner of the subscription, as the deployment will be making role assignments for the managed identities that are created for the Azure services.
- [Azure PowerShell](https://docs.microsoft.com/powershell/azure/install-az-ps)
- Bash shell
- [Git](https://git-scm.com/downloads)
- [Azure CLI](https://docs.microsoft.com/cli/azure/install-azure-cli)
- [VS Code](https://code.visualstudio.com/download)



The solution is based on the Azure OpenAI Enterprise Hub, as well as the Azure Speech Services samples that enables Speech Services Avatar



## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.


