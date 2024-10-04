#Import necessary lirbaries
import os
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient
from pathlib import Path
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
from azure.search.documents.indexes.models import (
    AzureOpenAIEmbeddingSkill,
    AzureOpenAIVectorizer,
    AzureOpenAIVectorizerParameters,
    BlobIndexerImageAction,
    CorsOptions,
    HnswAlgorithmConfiguration,
    IndexingParameters,
    IndexingParametersConfiguration,
    IndexProjectionMode,
    InputFieldMappingEntry,
    OutputFieldMappingEntry,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SearchIndexer,
    SearchIndexerDataContainer,
    SearchIndexerDataSourceConnection,
    SearchIndexerIndexProjection,
    SearchIndexerIndexProjectionSelector,
    SearchIndexerIndexProjectionsParameters,
    SearchIndexerSkillset,
    SimpleField,
    SplitSkill,
    VectorSearch,
    VectorSearchProfile
)

# Azure OpenAI Service details
openai_type = os.environ["openai_api_type"]
openai_api_base = os.environ['openai_api_base']
openai_api_version = os.environ['openai_api_version']
openai_deployment_completion = os.environ["openai_deployment_completion"]
openai_model_completion = os.environ["openai_model_completion"]
openai_deployment_embedding = os.environ["openai_deployment_embedding"]
openai_model_embedding = os.environ["openai_model_embedding"]
EMBEDDING_LENGTH = 1536

# Storage Account Service details
blob_conn_string = os.environ["BLOB_CONNECTION_STRING_MSI"]
blob_url = os.environ["STORAGE_URL"]
blob_container = SearchIndexerDataContainer(name=os.environ["BLOB_CONTAINER_NAME"])
storage_name = os.environ["STORAGE_ACCOUNT_NAME"]
current_dir = Path(os.getcwd())
filepath = current_dir.parent / "data" / "Woodgrove Asset Management  - Prospective of Asset Management Funds.pdf"
blob_name = os.path.basename(filepath)

# Azure AI Search Service details
aisearch_endpoint = os.environ["aisearch_endpoint"]
index_name = os.environ["aisearch_index_name"] # Desired name of index -- does not need to exist already
skillset_name = f"{index_name}-skillset"
indexer_name = f"{index_name}-indexer"  
vectorConfigName = "contentVector_config"
data_source_name = f"{storage_name}-storageblob-connection"

# Identity
uami_id = os.environ["UAMI_RESOURCE_ID"]


def uploadToBlob(blob_client):
    try:
        with open(filepath, "rb") as data:  
            blob_client.upload_blob(data, overwrite=True)
    except error as e:
        print("An error occurred when upoloading the file to the storage account:", e)

    print(f"File {filepath} uploaded to {blob_container}/{blob_name} successfully.")

def createDataSourceConnection(ds_client):

    data_source_connection = SearchIndexerDataSourceConnection(
        name=data_source_name,
        type="azureblob",
        connection_string=blob_conn_string,
        container=blob_container
    )

    data_source = ds_client.create_or_update_data_source_connection(data_source_connection)

    print(f"Data source '{data_source.name}' created or updated")

def createIndex(index_client):

    fields = [
        SearchableField(name="chunk_id", type=SearchFieldDataType.String, filterable=True, key=True, retrievable=True, sortable=True, analyzer_name="keyword"),
        SearchableField(name="parent_id", type=SearchFieldDataType.String, retrievable=True, filterable=True, sortable=True, facetable=True),
        SearchableField(name="content", type=SearchFieldDataType.String, retrievable=True),
        SearchableField(name="title", type=SearchFieldDataType.String, retrievable=True),
        SimpleField(name="url", type=SearchFieldDataType.String, retrievable=True),
        SimpleField(name="filepath", type=SearchFieldDataType.String, retrievable=True),
        SearchField(name="contentVector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single), hidden=False, vector_search_dimensions=1536, vector_search_profile_name="contentVector_config")  
    ]

    vector_search=VectorSearch(
        algorithms=[
            HnswAlgorithmConfiguration(
                name="myHnsw",
                kind="hnsw",
                parameters={
                    "m": 4,
                    "efConstruction":400,
                    "efSearch":500,
                    "metric":"cosine"
                }
            )
        ],
        vectorizers=[
            AzureOpenAIVectorizer(
                vectorizer_name="myOpenAI",
                kind="azureOpenAI",
                parameters=AzureOpenAIVectorizerParameters(
                    resource_url=openai_api_base,
                    deployment_name=openai_deployment_embedding,
                    model_name=openai_model_embedding
                    )
                )
        ],
        profiles=[
            VectorSearchProfile(
                name="contentVector_config",
                algorithm_configuration_name="myHnsw",
                vectorizer_name="myOpenAI"
            )
        ]  
    )

    cors_options = CorsOptions(allowed_origins=["*"], max_age_in_seconds=60)

    # pass in the name, fields and cors options and create the index
    index = SearchIndex(name=index_name, fields=fields, cors_options=cors_options, vector_search=vector_search)
    index_client.create_or_update_index(index)

def createSkillset(indexer_client):

    split_skill = SplitSkill(
        name="SplitSkill",
        description="Split skill to chunk documents",
        text_split_mode="pages",
        context="/document",
        maximum_page_length=2000,
        page_overlap_length=300,
        inputs=[
            InputFieldMappingEntry(name="text", source="/document/content"),
        ],
        outputs=[
            OutputFieldMappingEntry(name="textItems", target_name="pages")
        ]
    )

    embedding_skill = AzureOpenAIEmbeddingSkill(
        name="EmbeddingSkill",
        description="Skill to generate embeddings via Azure OpenAI",
        context="/document/pages/*",
        resource_url=openai_api_base,
        deployment_name=openai_deployment_embedding,
        model_name=openai_model_embedding,
        dimensions=1536,
        inputs=[
            InputFieldMappingEntry(name="text", source="/document/pages/*"),
        ],
        outputs=[
            OutputFieldMappingEntry(name="embedding", target_name="vector")
        ]
    )

    index_projections = SearchIndexerIndexProjection(
        selectors=[
            SearchIndexerIndexProjectionSelector(
                target_index_name=index_name,
                parent_key_field_name="parent_id",
                source_context="/document/pages/*",
                mappings=[
                    InputFieldMappingEntry(name="content", source="/document/pages/*"),
                    InputFieldMappingEntry(name="contentVector", source="/document/pages/*/vector"),
                    #InputFieldMappingEntry(name="chunk_id", source="/document/pages/*/vector"),
                    #InputFieldMappingEntry(name="parent_id", source="/document/pages/*/vector"),
                    InputFieldMappingEntry(name="title", source="/document/metadata_storage_name"),
                    InputFieldMappingEntry(name="url", source="/document/metadata_storage_path"),
                    InputFieldMappingEntry(name="filepath", source="/document/metadata_storage_path")
                ]
            )
        ],
        parameters=SearchIndexerIndexProjectionsParameters(
            projection_mode=IndexProjectionMode.INCLUDE_INDEXING_PARENT_DOCUMENTS
        )
    )

    skills = [split_skill, embedding_skill]

    skillset = SearchIndexerSkillset(
        name=skillset_name,
        description="Skillset to chunk documents and generating embeddings",
        skills=skills,
        index_projection=index_projections,
    )
    indexer_client.create_or_update_skillset(skillset)
    print(f"{skillset.name} created")

def createIndexer(indexer_client):

    indexer_parameters = IndexingParameters(
        configuration=IndexingParametersConfiguration(
            image_action=BlobIndexerImageAction.GENERATE_NORMALIZED_IMAGE_PER_PAGE,
            query_timeout=None))

    indexer = SearchIndexer(  
        name=indexer_name,  
        description="Indexer to index documents and generate embeddings",  
        skillset_name=skillset_name,  
        target_index_name=index_name,  
        data_source_name=data_source_name,
        parameters=indexer_parameters
    )    
    
    indexer_client.create_or_update_indexer(indexer)
    
    # Run the indexer  
    indexer_client.run_indexer(indexer_name)  
    print(f'{indexer_name} is created and running. If queries return no results, please wait a bit and try again.')

if __name__ == "__main__":
    try:
        credential = DefaultAzureCredential() #Needs to be changed to managed identity credential when running inside the container app
        blob_service_client = BlobServiceClient(account_url=blob_url, credential=credential)  
        container_client = blob_service_client.get_container_client(blob_container)  
        blob_client = container_client.get_blob_client(blob_name)
        index_client = SearchIndexClient(aisearch_endpoint, credential)
        indexer_client = SearchIndexerClient(aisearch_endpoint, credential)

        uploadToBlob(blob_client)
        createDataSourceConnection(indexer_client)
        createIndex(index_client)
        createSkillset(indexer_client)
        createIndexer(indexer_client)

    except Exception as error:
        raise error