# cloudnews

GPU Cloud Markt Monitoring Dashboard mit News-Extraktion und LlamaIndex-Integration

## Setup & Proxy-Konfiguration

1. Kopiere `.env.template` zu `.env` und passe die Variablen an:
   - `OPENAI_API_KEY` (dein Key)
   - `OPENAI_API_BASE` (z.B. https://admin-litellm.internal.sanjo.foo)
   - `OPENAI_MODEL` (z.B. gpt-4-turbo)
2. Installiere Abhängigkeiten:
   ```
   pip install -r requirements.txt
   ```
3. Starte das Dashboard:
   ```
   streamlit run gpu_market_dashboard/ui/dashboard.py --server.port 53848 --server.address 0.0.0.0
   ```

**Hinweis:**
- LlamaIndex/OpenAI nutzt Proxy/Modell aus `.env`.
- News-Extraktion & Filter im Dashboard testen.

