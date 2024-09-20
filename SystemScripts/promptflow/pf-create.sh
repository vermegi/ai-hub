#!/bin/bash

# Check if the environment variables are set
if [ -z "$path_variable" ] || [ -z "$rg_variable" ] || [ -z "$project_variable" ]; then
    echo "Please ensure the environment variables path_variable, rg_variable, and project_variable are set."
    exit 1
fi

# Run the command with the environment variables
pfazure flow create --flow "$path_variable" --set display_name="fsi-be-flow" description="Flow for the backend services running the FSI AI Avatar Industry Accelerator Kit" type="chat" --resource-group "$rg_variable" --workspace-name "$project_variable"