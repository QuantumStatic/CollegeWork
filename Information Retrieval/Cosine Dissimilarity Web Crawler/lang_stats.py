# from myfunctions import execute_this
from iso639 import languages

# @execute_this
def lang_stats():
    with open(f"logs copy/sampled_crawl6_7.log", 'r', encoding='utf-8') as file:
        lines = file.readlines()
        lines = map(lambda x: x.split('|')[1].strip(), lines)
    
    langs = {}
    crawled = 0
    for lang in lines:
        try:
            langs[languages.get(alpha2=lang).name] += 1
        except KeyError:
            try:
                langs[languages.get(alpha2=lang).name] = 1
            except KeyError:
                try:
                    langs[lang] += 1
                except KeyError:
                    langs[lang] = 1

        crawled += 1

    cumulative = {"other":0}
    special = {"English", "Spanish", "Chinese", "Polish", "not found"}
    for lang, lang_val in langs.items():
        if lang in special:
            cumulative[lang] = lang_val
        else:
            cumulative["other"] += lang_val
        
    print(cumulative, crawled)
    
    # print(langs)

# @execute_this
def other_stats():

    error_codes = {}
    with open(f"logs copy/gen_crawl6_6.log", 'r', encoding='utf-8') as file:
        lines = file.readlines()
        f = 0
        for x in lines:
            try:
                x = x.split('|')[1].strip()
            except IndexError:
                f += 1

            try:
                error_codes[x] += 1
            except KeyError:
                error_codes[x] = 1
    
        print(error_codes, f)