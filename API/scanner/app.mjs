import {Configuration, OpenAIApi} from "openai";

import {
  SecretsManagerClient,
  GetSecretValueCommand,
} from "@aws-sdk/client-secrets-manager";

export const lambdaHandler = async (event, context) => {
  try {
    const secret_name = "open_ai_api_key";
    const client = new SecretsManagerClient({
      region: "us-east-2",
    });

    let openai;

    const response = await client.send(
      new GetSecretValueCommand({
          SecretId: secret_name,
          VersionStage: "AWSCURRENT",
      }),
    );

    const parsedSecretString = JSON.parse(response.SecretString);
    openai = new OpenAIApi(
      new Configuration({
        apiKey: parsedSecretString.OPENAI_API_KEY,
        organization: parsedSecretString.ORG,
      }),
    );

    const res = await openai.createImage({
      ...JSON.parse(event.body),
      n: 1,
      size: '1024x1024',
    });

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        "Access-Control-Allow-Methods": "POST",
      },
      body: JSON.stringify(res.data.data[0].url),
    };
  } catch (err) {
    return {
      statusCode: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        "Access-Control-Allow-Methods": "POST",
      },
      body: err.message || err,
    };
  }
};