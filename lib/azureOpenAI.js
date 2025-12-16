import { AzureOpenAI } from "openai";

export function getAzureClient() {
  let endpoint = process.env.AZURE_OPENAI_ENDPOINT;
  const apiKey = process.env.SECRET_AZURE_OPENAI_API_KEY;
  const apiVersion = process.env.AZURE_OPENAI_API_VERSION || "2024-02-15-preview";
  const deployment = process.env.AZURE_OPENAI_DEPLOYMENT_NAME;

  if (!endpoint || !apiKey || !deployment) {
    throw new Error("Azure OpenAI credentials are missing. Check your .env file.");
  }

  // --- CRITICAL FIX: SANITIZE ENDPOINT ---
  // The SDK *only* wants "https://your-resource.openai.azure.com"
  // If your URL has "/openai/deployments/..." we must remove it.
  if (endpoint.includes("/openai")) {
      endpoint = endpoint.split("/openai")[0];
  }
  // Remove trailing slash if present
  if (endpoint.endsWith("/")) {
      endpoint = endpoint.slice(0, -1);
  }

  console.log("--- Azure Connection Debug ---");
  console.log("Endpoint:", endpoint);
  console.log("Deployment:", deployment);
  console.log("Version:", apiVersion);
  console.log("------------------------------");

  return new AzureOpenAI({
    endpoint,
    apiKey,
    apiVersion,
    deployment, 
    dangerouslyAllowBrowser: true 
  });
}