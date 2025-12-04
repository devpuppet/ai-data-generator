# AI Data Generator

Install Poetry
```
pip install poetry
```

Then install the dependencies using Poetry

```
poetry install
```

Add .env file

```
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ai_data
POSTGRES_USER=myuser
POSTGRES_PASSWORD=secret
GEMINI_API_KEY=<your_key>
LANGFUSE_SECRET_KEY=<your_key>
LANGFUSE_PUBLIC_KEY=<your_key>
LANGFUSE_BASE_URL=https://cloud.langfuse.com
```

Run PostgreSQL
```
docker compose up -d
```

Run the application:
```
GEMINI_API_KEY=your_key python -m streamlit run src/__main__.py
```

## Guardrails Hub

Login to `https://guardrailsai.com/hub` and generate API key.

Configure guardrails:
```
guardrails configure
```
And install validator:
```
guardrails hub install hub://guardrails/valid_sql
```