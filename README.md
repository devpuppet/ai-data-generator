# AI Data Generator

Install Poetry
```
pip install poetry
```

Then install the dependencies using Poetry

```
poetry install
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