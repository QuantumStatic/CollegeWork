Files in this Submission:
- robots_store - Folder containing the robot.txt files for each website
- fetch_response.py - Python file to fetch responses from websites (uses multiprocessing)
- language_detector.py - Python file to detect language of fetched responses or urls (uses multiprocessing)
- Link.py - Python file - Python file containing the Link class. This class is used to store the links and use them.
- logger.py - Python file containing the logger class.
- robots.py - Python file containing function to access and or fetch robots.txt files. It stores them in robots_store folder. (uses multiprocessing)
- scrape_google.py - Python file containing function to scrape google search results.
- scraper.py - Python file containing the actual crawler(s).
- similarity_calculator.py - Python file containing function to calculate similarity between two strings.
- langstats.py - Creates code used to generate statistics on logs
- gen_crawl5.log - General Log file for the traditional crawler.
- sampled_crawl5.log - Sampled Log file for the traditional crawler.
- readme.txt - Readme file for this assignment
- explain.txt - Explaination of the code for this assignment


How to run the crawler:
-This crawler is written & tested in Python 3.11.5 on MacOS Sonoma 14.0.

- [library Installation] It uses the following addtional libraries that may requires installing:
 -- BeautifulSoup - pip3.11 install BeautifulSoup4
 -- langid - pip3.11 install langid (https://github.com/saffsd/langid.py)
 -- Requests - pip3.11 install requests (to make web queries)
 -- urllib3 - pip3.11 install urllib3 (to fetch & parse robots.txt files)
 -- tldextract - pip3.11 install tldextract (to extract domain names from urls)
 -- SortedContainers - pip3.11 install sortedcontainers (to create data structures that are always ordered)
 -- pathlib - requires Python 3.4 or higher (to create directories)
 -- scipy - pip3.11 install scipy (to calculate cosine similarity)
 -- sentence_transformers - pip3.11 install sentence-transformers (contains the model to generate multi-lingual sentence embeddings)
 -- iso639 - pip3.11 install iso-639 (convert language iso encoded names to their full names)

- [Running the crawler] To run the crawler, run the following command:
- All you need to do is run scraper.py

Please reach out to me at uj299@nyu.edu/utkarshworkemail@gmail.com or alternatively at 347-896-3363 if there are any problems

