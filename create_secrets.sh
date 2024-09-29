source .env

OPENAI_API_KEY_SECRET_NAME=$PROJECT_NAME-llm-router-openai-api-key
APP_API_KEY_SECRET_NAME=$PROJECT_NAME-llm-router-app-api-key
MARKET_API_KEY_SECRET_NAME=$PROJECT_NAME-llm-router-api-key
APP_COMPLETIONS_ENDPOINT_SECRET_NAME=$PROJECT_NAME-llm-router-app-completions-endpoint

aws secretsmanager create-secret --name $OPENAI_API_KEY_SECRET_NAME --secret-string $OPENAI_API_KEY
aws secretsmanager create-secret --name $APP_API_KEY_SECRET_NAME --secret-string $APP_API_KEY
aws secretsmanager create-secret --name $MARKET_API_KEY_SECRET_NAME --secret-string $MARKET_API_KEY
aws secretsmanager create-secret --name $APP_COMPLETIONS_ENDPOINT_SECRET_NAME --secret-string $APP_COMPLETIONS_ENDPOINT