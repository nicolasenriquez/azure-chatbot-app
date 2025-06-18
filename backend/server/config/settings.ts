export const settings = {
  // Azure OpenAI Configuration
  azureOpenaiApiKey: process.env.AZURE_OPENAI_API_KEY || process.env.OPENAI_API_KEY || "",
  azureOpenaiEndpoint: process.env.AZURE_OPENAI_ENDPOINT || "",
  azureOpenaiDeploymentName: process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "gpt-4",
  azureOpenaiApiVersion: process.env.AZURE_OPENAI_API_VERSION || "2024-02-01",
  
  // Azure AI Search Configuration
  azureSearchEndpoint: process.env.AZURE_SEARCH_ENDPOINT || "",
  azureSearchApiKey: process.env.AZURE_SEARCH_API_KEY || "",
  azureSearchIndexName: process.env.AZURE_SEARCH_INDEX_NAME || "knowledge-base",
  
  // Azure Storage Configuration
  azureStorageConnectionString: process.env.AZURE_STORAGE_CONNECTION_STRING || "",
  azureStorageContainerName: process.env.AZURE_STORAGE_CONTAINER_NAME || "documents",
  
  // Application Configuration
  port: parseInt(process.env.PORT || "8000"),
  environment: process.env.NODE_ENV || "development",
  logLevel: process.env.LOG_LEVEL || "info",
};

// Validate required environment variables
export function validateSettings() {
  const requiredVars = [
    'AZURE_OPENAI_API_KEY',
    'AZURE_OPENAI_ENDPOINT',
    'AZURE_SEARCH_ENDPOINT',
    'AZURE_SEARCH_API_KEY'
  ];
  
  const missing = requiredVars.filter(varName => !process.env[varName]);
  
  if (missing.length > 0) {
    console.warn(`Missing environment variables: ${missing.join(', ')}`);
    console.warn('Some features may not work correctly.');
  }
}
