import os
import json
import google.generativeai as genai
from openai import OpenAI
import config
import data_fetch

def query_llm(ticker, summary, provider):
    prompt = f"""Expert options trader. Analyze {ticker} for hourly options trade.
Data: {summary}

Return ONLY valid JSON:
{{"ticker":"{ticker}","signal":"buy_call|buy_put|sell_call|sell_put|hold","confidence":0-100,"reasoning":"short","strategy":"e.g. ATM call"}}"""

    try:
        if provider == "gemini":
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            text = response.text.strip("```json").strip("```").strip()
            return json.loads(text)
        elif provider == "openrouter":
            client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
            response = client.chat.completions.create(model="openai/gpt-4o-mini", messages=[{"role":"user","content":prompt}])
            return json.loads(response.choices[0].message.content)
        else:  # groq
            client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")
            response = client.chat.completions.create(model="llama-3.1-70b-versatile", messages=[{"role":"user","content":prompt}])
            return json.loads(response.choices[0].message.content)
    except:
        return {"ticker": ticker, "signal": "hold", "confidence": 0, "reasoning": "error"}

def get_consensus_signals():
    good_signals = []
    for ticker in config.TICKERS:
        summary = data_fetch.get_market_summary(ticker)
        results = []
        for provider in ["gemini", "openrouter", "groq"]:
            res = query_llm(ticker, summary, provider)
            if res.get("confidence", 0) >= config.MIN_CONFIDENCE:
                results.append(res)
        if len(results) >= 2:
            good_signals.append(results[0])
    return good_signals
