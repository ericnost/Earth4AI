# Earth4AI
Code and data for an analysis of data-driven climate initiatives

## `GoogleSearch.html`
Accesses Google's custom search engine results, configured to search the entire web rather than a custom domain. Configures the search and then executes it based on user input. Can find up and return up to 100 results per query. Requires a Google Search API key.

## `Observatory.py`
Python script to compile the JSON outputs from `GoogleSearch.html` Compiles, de-duplicates, and then scrapes each website to find a pattern of search terms/phrases such as "artificial intelligence will"...

## `google search results.csv`
Results from running `Observatory.py` on the original `GoogleSearch.html` queries.
