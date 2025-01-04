import feedparser
import requests
import os

# Function to query arXiv and get articles
def fetch_arxiv_articles(search_query="cat:cs.AI", start=0, max_results=10):
    base_url = "http://export.arxiv.org/api/query"
    # query = f"{base_url}?search_query={search_query}&start={start}&max_results={max_results}"
    query = "http://export.arxiv.org/api/query?search_query=(cat:q-bio+OR+cat:physics.gen-ph+OR+cat:cs.AI+OR+cat:cs.LG+OR+cat:physics.ao-ph+OR+cat:econ.GN)+ANDNOT+(abs:niche+OR+abs:specialized+OR+abs:topological)&start=0&max_results=1000"
    feed = feedparser.parse(query)
    return feed.entries

# Function to download PDFs
def download_pdfs(articles, download_folder="arxiv_pdfs"):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    for article in articles:
        pdf_url = article.get('link').replace('abs', 'pdf')
        pdf_title = article.get('title').replace(' ', '_').replace('/', '_')
        pdf_path = os.path.join(download_folder, f"{pdf_title}.pdf")
        
        print(f"Downloading {pdf_title}...")
        response = requests.get(pdf_url)
        if response.status_code == 200:
            with open(pdf_path, 'wb') as f:
                f.write(response.content)
            print(f"Saved to {pdf_path}")
        else:
            print(f"Failed to download {pdf_title}")

# Query and download
if __name__ == "__main__":
    articles = fetch_arxiv_articles(search_query="cat:cs.AI", max_results=10)
    download_pdfs(articles)
