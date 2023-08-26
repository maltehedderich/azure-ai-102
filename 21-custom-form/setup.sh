#!/usr/bin/env bash

# Set variable values
SUBSCRIPTION_ID="YOUR_SUBSCRIPTION_ID"
RESOURCE_GROUP="YOUR_RESOURCE_GROUP"
LOCATION="YOUR_LOCATION_NAME"
EXPIRY_DATE="2024-01-01T00:00:00Z"

# Get random numbers to create unique resource names
unique_id="$RANDOM$RANDOM"

# Create a storage account in your Azure resource group
echo "Creating storage..."
az storage account create --name "ai102form${unique_id}" --subscription "$SUBSCRIPTION_ID" --resource-group "$RESOURCE_GROUP" --LOCATION "$LOCATION" --sku Standard_LRS --encryption-services blob --default-action Allow --output none

echo "Uploading files..."
# Get storage key to create a container in the storage account
KEY_JSON=$(az storage account keys list --subscription "$SUBSCRIPTION_ID" --resource-group "$RESOURCE_GROUP" --account-name "ai102form${unique_id}" --query "[?keyName=='key1'].{keyName:keyName, permissions:permissions, value:value}")
KEY_STRING=${KEY_JSON:'[ { "keyName": "key1", "permissions": "Full", "value": "'}
AZURE_STORAGE_KEY=${KEY_STRING:'" } ]'}
# Create container
az storage container create --account-name "ai102form${unique_id}" --name sampleforms --public-access blob --auth-mode key --account-key "$AZURE_STORAGE_KEY" --output none
# Upload files from your local sampleforms folder to a container called sampleforms in the storage account
# Each file is uploaded as a blob
az storage blob upload-batch -d sampleforms -s ./sample-forms --account-name "ai102form${unique_id}" --auth-mode key --account-key "$AZURE_STORAGE_KEY" --output none
# Set a variable value for future use
STORAGE_ACCOUNT="ai102form${unique_id}"

# Get a Shared Access Signature (a signed URI that points to one or more storage resources) for the blobs in sampleforms
SAS_TOKEN=$(az storage container generate-sas \
  --account-name "ai102form${unique_id}" \
  --name sampleforms \
  --expiry "$EXPIRY_DATE" \
  --permissions 'rwl' \
  --https-only)

URI="https://${STORAGE_ACCOUNT}.blob.core.windows.net/sampleforms?${SAS_TOKEN}"
# Print the generated Shared Access Signature URI, which is used by Azure Storage to authorize access to the storage resource
echo "-------------------------------------"
echo "SAS URI: ${URI}"
