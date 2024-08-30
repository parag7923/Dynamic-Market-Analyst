import requests

def analyze_market(symbol):
    alpha_vantage_api_key = 'A9Y517V48D7CYOF7'
    news_api_key = '6c31f7e6ffb54c2093dc51a2903cd690'

    # Initialize variables
    analysis = {
        "stock_symbol": symbol,
        "open_price": 'N/A',
        "high_price": 'N/A',
        "low_price": 'N/A',
        "close_price": 'N/A',
        "volume": 'N/A',
        "company_name": 'N/A',
        "description": 'N/A',
        "sector": 'N/A',
        "industry": 'N/A',
        "market_cap": 'N/A',
        "current_trend": 'N/A',
        "total_change": 'N/A',
        "global_impact": 'N/A',
        "latest_news": []
    }

    # Fetch time series data
    try:
        response = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={alpha_vantage_api_key}')
        response.raise_for_status()
        time_series_data = response.json()

        if 'Time Series (Daily)' in time_series_data:
            latest_data = list(time_series_data['Time Series (Daily)'].values())[0]
            open_price = float(latest_data['1. open'])
            high_price = float(latest_data['2. high'])
            low_price = float(latest_data['3. low'])
            close_price = float(latest_data['4. close'])
            volume = int(latest_data['5. volume'])
            total_change = (close_price - open_price) / open_price * 100

            analysis.update({
                "open_price": f"{open_price:.2f}",
                "high_price": f"{high_price:.2f}",
                "low_price": f"{low_price:.2f}",
                "close_price": f"{close_price:.2f}",
                "volume": volume,
                "total_change": f"{total_change:.2f}%"
            })
    except Exception as e:
        analysis['error'] = f"Failed to fetch time series data: {e}"

    # Fetch company overview
    try:
        response = requests.get(f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={alpha_vantage_api_key}')
        response.raise_for_status()
        company_overview = response.json()

        analysis.update({
            "company_name": company_overview.get('Name', 'N/A'),
            "description": company_overview.get('Description', 'N/A'),
            "sector": company_overview.get('Sector', 'N/A'),
            "industry": company_overview.get('Industry', 'N/A'),
            "market_cap": company_overview.get('MarketCapitalization', 'N/A')
        })
    except Exception as e:
        analysis['error'] = f"Failed to fetch company overview: {e}"

    # Fetch news articles
    try:
        news_response = requests.get(f'https://newsapi.org/v2/everything?q={symbol}&sortBy=publishedAt&apiKey={news_api_key}')
        news_response.raise_for_status()
        news_data = news_response.json()
        articles = news_data.get('articles', [])

        if articles:
            latest_article = articles[0]
            sentiment = get_sentiment_analysis(latest_article['description'])
            analysis['latest_news'].append({
                "title": latest_article['title'],
                "description": latest_article['description'],
                "sentiment": sentiment
            })
    except Exception as e:
        analysis['error'] = f"Failed to fetch news articles: {e}"

    return analysis

def get_sentiment_analysis(text):
    # Placeholder for actual sentiment analysis
    return {"label": "POSITIVE", "score": 0.98}  # Example sentiment
