# from myfunctions import execute_this
from logger import simpleWebCrawlerLogger
from language_detector import multi_detect_language_url
from datetime import datetime



def main():
    lines = []
    with open("logs copy/sampled_crawl6_6.log", 'r', encoding='utf-8') as file:
        lines = file.readlines()
        lines = map(lambda x: x.split('|')[0].strip(), lines)

    sampled_crawler = simpleWebCrawlerLogger("sampled", "sampled_crawl6_7.log")
    cnt = 0
    for link, lang in multi_detect_language_url(lines):
        log_string = f"{link} | {lang} | {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}"
        sampled_crawler.log_link_info(log_string)
        cnt+= 1
        print(cnt)

if __name__ == "__main__":
    # execute_this(main)


    main()
        