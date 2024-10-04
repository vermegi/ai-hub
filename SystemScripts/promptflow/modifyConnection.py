import yaml
import os
from io import StringIO
from ruamel.yaml import YAML

AISTUDIO_AOAI_CONN_NAME = os.environ["AIS_AOAI_CONN_NAME"]
AISTUDIO_AOAI_CONN_RESOURCEID = os.environ["AIS_AOAI_CONN_RESOURCEID"] # has to be something like: /subscriptions/[subscription_id]/resourceGroups/[resource_group_name]/providers/Microsoft.MachineLearningServices/workspaces/[ai_studio_project_name]/connections/[aistudio_aoai_conn_name]
AISTUDIO_SEARCH_CONN_RESOURCEID = os.environ["AIS_SEARCH_CONN_RESOURCEID"]

openai_type = os.environ["openai_api_type"]
openai_api_base = os.environ['openai_api_base']
openai_api_version = os.environ['openai_api_version']
openai_deployment_completion = os.environ["openai_deployment_completion"]
openai_model_completion = os.environ["openai_model_completion"]
openai_deployment_embedding = os.environ["openai_deployment_embedding"]
openai_model_embedding = os.environ["openai_model_embedding"]

aisearch_endpoint = os.environ["aisearch_endpoint"]
index_name = os.environ["aisearch_index_name"]

yaml = YAML()

# Load the YAML file
with open('sampleflow.dag.yaml', 'r') as file:
    data = yaml.load(file)

# Update the connection fields
for node in data['nodes']:
    if node['name'] == 'classifier':
        node['connection'] = AISTUDIO_AOAI_CONN_NAME
        node['inputs']['deployment_name'] = openai_deployment_completion
    elif node['name'] == 'history_parser':
        node['connection'] = AISTUDIO_AOAI_CONN_NAME
        node['inputs']['deployment_name'] = openai_deployment_completion
    elif node['name'] == 'chat':
        node['connection'] = AISTUDIO_AOAI_CONN_NAME
        node['inputs']['deployment_name'] = openai_deployment_completion
    elif node['name'] == 'fsi_doc_lookup':
        # Parse the mlindex_content as YAML (otherwise the mlindex won't be recognized as a string and will be treated as an int)
        mlindex_content = yaml.load(node['inputs']['mlindex_content'])

        #Update the values
        mlindex_content['embeddings']['api_type'] = openai_type
        mlindex_content['embeddings']['api_base'] = openai_api_base
        mlindex_content['embeddings']['api_version'] = openai_api_version
        mlindex_content['embeddings']['connection']['id'] = AISTUDIO_AOAI_CONN_RESOURCEID
        mlindex_content['embeddings']['deployment'] = openai_deployment_embedding
        mlindex_content['embeddings']['model'] = openai_model_embedding
        mlindex_content['index']['connection']['id'] = AISTUDIO_SEARCH_CONN_RESOURCEID
        mlindex_content['index']['endpoint'] = aisearch_endpoint
        mlindex_content['index']['index'] = index_name

        # Convert the updated mlindex_content back to a string
        stream = StringIO()
        yaml.dump(mlindex_content, stream)
        node['inputs']['mlindex_content'] = stream.getvalue()

# Save the updated YAML file
with open('pf-fsi-be-chatflow/flow.dag.yaml', 'w') as file:
    yaml.dump(data, file)

print("Updated the connection fields successfully.")