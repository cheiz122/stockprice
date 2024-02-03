import streamlit as st
import requests

def get_news_sentiment(api_key, tickers=None, topics=None, time_from=None, time_to=None, sort=None, limit=None):
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'NEWS_SENTIMENT',
        'apikey': api_key
    }
    if tickers:
        params['tickers'] = tickers
    if topics:
        params['topics'] = topics
    if time_from:
        params['time_from'] = time_from
    if time_to:
        params['time_to'] = time_to
    if sort:
        params['sort'] = sort
    if limit:
        params['limit'] = limit

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad responses
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {str(e)}")
        return None
    except Exception as ex:
        st.error(f"An unexpected error occurred: {str(ex)}")
        return None

def main():
    st.title("Market News Sentiment Analysis")

    api_key = 'GF9IGY262QOKWTLV'  # Replace 'YOUR_API_KEY_HERE' with your actual API key

    # Fetch news sentiment data
    st.write("Fetching news sentiment data...")
    news_sentiment_data = get_news_sentiment(api_key)

    if news_sentiment_data is not None:
        items = news_sentiment_data.get('items', 0)
        feed = news_sentiment_data.get('feed', [])

        st.write(f"Total items: {items}")

        for item in feed:
            st.markdown('---')
            st.subheader(item.get('title', 'Title not found'))
            st.write(f"Source: {item.get('source', 'Source not found')}")
            st.write(f"Summary: {item.get('summary', 'Summary not found')}")
            st.write(f"Overall Sentiment: {item.get('overall_sentiment_label', 'Sentiment label not found')} ({item.get('overall_sentiment_score', 'Sentiment score not found')})")

            st.write("Ticker Sentiment:")
            for ticker_sentiment in item.get('ticker_sentiment', []):
                st.write(f"- Ticker: {ticker_sentiment.get('ticker', 'Ticker not found')}, Score: {ticker_sentiment.get('ticker_sentiment_score', 'Score not found')}, Label: {ticker_sentiment.get('ticker_sentiment_label', 'Label not found')}")

            # Display image and URL
            if 'banner_image' in item:
                st.image(item['banner_image'], caption='Banner Image')
            if 'url' in item:
                st.write(f"URL: [{item['title']}]({item['url']})")

if __name__ == "__main__":
    main()

