import time
import random
from typing import Iterable
import requests
# from myfunctions import execute_this
from scrape_google import get_google_search_results
from language_detector import multi_detect_language_response, multi_detect_language_url, detect_language_url
from fetch_response import multi_get_response, get_response
from Link import Link
from similarity_calculator import calculate_dissimilarity, get_enocoded_sentences, get_multi_sentence_cosine, multi_match_cosine_thresh, non_similar_filtering
from robots import multi_get_robots_txt, get_robots_txt
from logger import simpleWebCrawlerLogger
from datetime import datetime
import traceback



restricted_domains = {}


def setup():
    # search_results1 = get_google_search_results("history of languages", 1)
    search_results1 = get_google_search_results("python", 1)

    search_results = search_results1 #+ search_results2 + search_results3

    # print(search_results)

    link_register = {link: Link(link) for link in search_results}
    link_list = [link for link in search_results]

    print("sleeping after getting google search results")
    # time.sleep(2)

    responses: list[requests.Request] = tuple(
        filter(
            lambda x: x[1] is not None
            and x[1].ok,
            # and Link._extract_domain_name(x[0]) not in restricted_domains,
            multi_get_response(search_results),
        )
    )

    for link, response in responses:
        response.url = link
        link_register[link].add_response(response)
        link_register[link].increase_domain_count()

    for response, lang in multi_detect_language_response(responses):
        link_register[response.url].add_language(lang)
        # try:
        #     link_register[response.url].title_encoding = get_enocoded_sentences([link_register[response.url].title])[0]
        # except TypeError:
        #     print(link_register[response.url].title)
        #     input('>')

    return link_list, link_register


def language_distribution(link_register: dict[str, Link]) -> dict[str, int]:
    language_distribution = {}
    for link in link_register:
        try:
            language_distribution[link_register[link].language] += 1
        except KeyError:
            language_distribution[link_register[link].language] = 1

    return language_distribution

def get_language_scores(links:Iterable[str]) -> dict[str, int]:
    language_scores = {}
    for _, lang in multi_detect_language_url(links):
        try:
            language_scores[lang] += 1
        except KeyError:
            language_scores[lang] = 1
    
    return language_scores


def _iterate_filtered_approved_list(approved_links: list[str]):
    try:
        for approved_link in random.sample(approved_links, 10):
            yield approved_link
    except ValueError:
        for approved_link in approved_links:
            yield approved_link


def _standard_link_filtering(link_list:list[str], link_register:dict[str, Link]):
    domain_exhaustion_limit = 50

    filtered_link_list = filter(lambda x: x is not None and x not in link_register and Link.get_domain_count(x) < domain_exhaustion_limit, link_list)
    links_crawl_results = map(lambda x: x[0].can_fetch('*', x[1]), zip(multi_get_robots_txt(link_list), filtered_link_list))
    approved_links = map(lambda y: y[0], filter(lambda x: x[1], zip(link_list, links_crawl_results)))

    return approved_links


def ml_crawler_strategy(og_link:Link, link_list: list[str], link_register: dict[str, Link]):

    # standard filtering to remove links that have already been visited or are restricted by robots.txt
    approved_links = tuple(_standard_link_filtering(link_list, link_register))

    if not approved_links:
        return [], link_list, link_register

    # Crawl the links in this current page
    approved_links_objects = []
    for url, response in filter(lambda x: x is not None and x[1] is not None and x[1].ok, multi_get_response(approved_links)):
        approved_links_objects.append(Link(url, response))
        link_register[url] = approved_links_objects[-1]

    # get the vector embeddings for the links in this page
    for idx, encoding in enumerate(get_enocoded_sentences([x.title for x in approved_links_objects])):
        approved_links_objects[idx].title_encoding = encoding
    
    # filter out links that are similar to the current page
    approved_objects = filter(lambda x: x[0] > 0.4, zip(get_multi_sentence_cosine(og_link.title_encoding, [x.title_encoding for x in approved_links_objects]), [x.link for x in approved_links_objects]))

    # return whatever pased through our filter
    return [x[1] for x in approved_objects], approved_links, link_register


def ml_crawler(visit_list: list[str], link_register: dict[str, Link]):

    cnt = 0

    random_sample = set()
    visit_list = list(set(visit_list))

    while any(visit_list) or cnt != 1000:

        curr_link = visit_list.pop(0)

        # get links in this page
        in_page_links = link_register[curr_link].links_in_this_page

        if in_page_links is None or not in_page_links:
            if curr_link not in random_sample:
                link_register[curr_link] = None
            continue
        
        # use our crawl strategy to get the links we want to visit
        approved_links, new_links_to_visit, link_register = ml_crawler_strategy(link_register[curr_link], in_page_links, link_register)

        # dereference the object we won't be using anymore so the garbage collector takes care of it
        if curr_link not in random_sample:
            link_register[curr_link] = None
        
        if not approved_links:
            continue
        
        # Here we match approved links with themselves to weed out similar links in the current page
        approved_links_filtered = tuple(map(lambda y: y[1], filter(lambda x: x[0], zip(non_similar_filtering([link_register[link].title_encoding for link in approved_links], threshold=0.1), approved_links))))

        truly_approved_links = []


        if random_sample:
            # If there are some sampled links we match approved links with the sampled links to find dissimilar links to our collection
            for x, result in enumerate(multi_match_cosine_thresh([link_register[x].title_encoding for x in approved_links_filtered], [link_register[x].title_encoding for x in random_sample])):
                if result:
                    truly_approved_links.append(approved_links[x])
                    link_register[truly_approved_links[-1]].sampled = True
                    random_sample.add(truly_approved_links[-1])
                    cnt += 1
        else:
            # If there are no sampled links we just sample 10 links from the approved links
            for approved_link in _iterate_filtered_approved_list(approved_links_filtered):
                truly_approved_links.append(approved_link)
                random_sample.add(approved_link)
                link_register[approved_link].sampled = True

        new_links_to_visit = set(new_links_to_visit)
        new_links_to_visit = list(new_links_to_visit.difference(set(truly_approved_links)))

        #shuffling things around for randomness
        random.shuffle(new_links_to_visit)
        random.shuffle(truly_approved_links)
        # New approved links are put to the fron to be explored before the older links
        visit_list = truly_approved_links + visit_list

        #Older links are put to the back
        visit_list.extend(new_links_to_visit)

        print("Done with", curr_link) 


def crawl_strategy2(og_link:Link, link_list: list[str], link_register: dict[str, Link]):

    approved_links = tuple(_standard_link_filtering(link_list, link_register))

    if not approved_links:
        return [], link_list, link_register

    approved_link_objects:list[Link] = []
    for response, lang in filter(lambda x: x is not None and x[1] is not None and x[0] is not None and x[0].ok, multi_detect_language_response(multi_get_response(approved_links))):
        approved_link_objects.append(Link(response.url, response, lang))
        link_register[response.url] = approved_link_objects[-1]
    
    approved_objects = filter(lambda x: x.language != og_link.language, approved_link_objects)

    return [x.link for x in approved_objects], approved_links, link_register


def crawl4(visit_list: list[str], link_register: dict[str, Link]):

    cnt = 0

    random_sample = set()
    visit_list = list(set(visit_list))

    while any(visit_list) or cnt != 1000:

        curr_link = visit_list.pop(0)

        in_page_links = link_register[curr_link].links_in_this_page

        if in_page_links is None or not in_page_links:
            if curr_link not in random_sample:
                link_register[curr_link] = None
            continue

        approved_links, new_links_to_visit, link_register = crawl_strategy2(link_register[curr_link], in_page_links, link_register)

        if curr_link not in random_sample:
            link_register[curr_link] = None
        
        if not approved_links:
            continue
        
        for approved_link in _iterate_filtered_approved_list(approved_links):
            random_sample.add(approved_link)
            link_register[approved_link].sampled = True

        new_links_to_visit = set(new_links_to_visit)
        new_links_to_visit = list(new_links_to_visit.difference(set(approved_links)))

        random.shuffle(new_links_to_visit)
        random.shuffle(approved_links)
        visit_list = approved_links + visit_list
        visit_list.extend(new_links_to_visit)

        print("Done with", curr_link) 


def traditional_crawler_next_step_strategy(og_link:Link, link_list: list[str], link_register: dict[str, Link], visit_list: list[str], gen_logger:simpleWebCrawlerLogger):
    
    # Increment age of links already in queue
    # tuple(map(lambda x: link_register[x[0]].increment_age(), visit_list))
    for x in visit_list.copy():
        try:
            link_register[x[0]].increment_age()
        except AttributeError:
            visit_list.remove(x)

    # standard filtering to remove links that have already been visited or are restricted by robots.txt
    approved_links = tuple(_standard_link_filtering(link_list, link_register))

    if not approved_links:
        return None, link_register, visit_list
    
    # Pages have a lot link we try to sample 150 out, prioritsing links that go outward
    probabilites = []
    link_count = 0
    for link in approved_links:
        curr_prob = 1
        if Link._extract_domain_name(link) == og_link.domain_name:
            curr_prob -= 0.6
        
        link_count += 1
        probabilites.append(curr_prob)

    approved_links = random.choices(approved_links, weights=probabilites, k=min(150, link_count))
    
    # Crawl all the links we just filtered out 
    temp_link_objs = []
    for url, response in filter(lambda x: x is not None and x[1] is not None, multi_get_response(approved_links)):
        log_string = f"{url} | {response.status_code} | {len(response.content)} | {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}"
        gen_logger.log_link_info(log_string)
        if response.ok:
            temp_link_objs.append(Link(url, response))

    if not temp_link_objs:
        return None, link_register, visit_list

    # further reduce this set by penalising links with too many outward links or too few
    probabilites = []
    link_count = 0
    for link in temp_link_objs:
        curr_prob = 1
        
        curr_prob = max(curr_prob - Link.get_percentile_of_links(link.num_links) * 0.35, 0.2)
        try:
            curr_prob = max(curr_prob - (1/(link.num_links**0.8)), 0.2)
        except ZeroDivisionError:
            pass
        
        link_count += 1
        probabilites.append(curr_prob)
    
    og_link._links_in_this_page = []
    for choice in random.choices(temp_link_objs, weights=probabilites, k=min(75, link_count)):
        visit_list.append((choice.link, 0))
        link_register[choice.link] = choice
        og_link._links_in_this_page.append(choice.link)
        choice.increase_domain_count()
    
    # With all these added links we need to re-evaluate our percentile of domains
    Link.re_eval_domain_score()

    temp_list = []
    for link in visit_list:
        link_obj = link_register[link[0]]
        # Asssigning scores to each link in this page using the formula
        try:
            temp_list.append((link[0], (Link.get_domain_score(link[0]) * link_obj.num_links * 0.8 + 10*link_obj.age)*(1 + (og_link.domain_name == link_obj.domain_name)*0.6) - len(tuple(filter(lambda x: x not in link_register, link_obj.links_in_this_page)))))
        except AttributeError:
            continue
    
    # Sort it in descending order
    temp_list.sort(key=lambda x: x[1], reverse=True)

    # We sort it in descending order since the pop function here can run in O(1) time
    next_step = temp_list.pop()[0]
    if next_step == og_link.link:
        next_step = temp_list.pop()[0]
    
    return next_step, link_register, temp_list

def traditional_crawler_sampling_strategy(og_link:Link, previous_sampled:bool, sample_domain_distribution:dict[str, int]) -> bool:
    sample_prob = 1
    
    # if a link was sampled recently we reduce current node's sampling probability a little bit
    if previous_sampled:
        sample_prob *= 0.9

    domain_score = Link.get_domain_score(og_link.link)

    # Based on how common this link is in our store, we penalise if too common or boost it if its rare
    if domain_score < 0.05:
        sample_prob *= 1.5
    elif 0.05 <= domain_score < 0.1:
        sample_prob *= 1.4
    elif 0.1 <= domain_score < 0.2:
        sample_prob *= 1.3
    elif 0.2 <= domain_score < 0.3:
        sample_prob *= 1.2
    elif 0.3 <= domain_score < 0.5:
        sample_prob *= 1.1
    if 0.5 <= domain_score < 0.7:
        sample_prob *= 0.9
    elif 0.7 <= domain_score < 0.9:
        sample_prob *= 0.8
    elif  0.9 <= domain_score:
        sample_prob *= 0.7

    # Penalise the current link if it has a high number of links
    sample_prob = max(sample_prob - Link.get_percentile_of_links(og_link.num_links) * 0.4, 0.2)
    
    # Penalise the current link if it has too few links
    try:
        sample_prob = max(sample_prob - (1/(og_link.num_links**0.8)), 0.2)
    except ZeroDivisionError:
        pass
    
    # If the current domain seems to appear many times we penalise proportional to how many times it appears
    # we limit a domain to 50 in the sample and it can can noticed from this line of code
    sample_prob -= (sample_domain_distribution.setdefault(og_link.domain_name, 0) / 50)
    
    # Now we see if the current link is unlucky it gets penalised
    sample_prob *= (1 - random.choices((True, False), weights=(0.3, 0.7), k=1)[0] * 0.25)

    sample_prob = min(1, max(0, sample_prob))

    return random.choices((True, False), weights=(sample_prob, 1-sample_prob), k=1)[0]

def traditional_crawler(visit_list: list[str], link_register: dict[str, Link]):
    
    # Create the logger
    gen_logger = simpleWebCrawlerLogger("general","gen_crawl5.log")
    
    cnt = 0
    random_sample = set()
    random_sample_domain_distribution:dict[str, int] = {}
    visit_list = set(visit_list)
    visit_list = [(link, 0) for link in visit_list]
    next_step = None
    pity_counter = 0
    previous_sampled_penalty = False

    while any(visit_list) and cnt < 1000:
        
        # pop the queue if we did not get a next steo
        curr_link = visit_list.pop(0)[0] if next_step is None else next_step
        next_step = None

        try:
            in_page_links = link_register[curr_link].links_in_this_page
        except AttributeError:
            continue

        if in_page_links is None or not in_page_links:
            # Remove any reference to the object with no external links to let the garbage collector handle it
            if curr_link not in random_sample:
                link_register[curr_link] = None
            continue
        
        # Get the next node to go to
        next_step, link_register, visit_list = traditional_crawler_next_step_strategy(link_register[curr_link], in_page_links, link_register, visit_list, gen_logger)
        
        # Now to decide if we want to sample the current link
        crawl_curr_link = traditional_crawler_sampling_strategy(link_register[curr_link], previous_sampled_penalty, random_sample_domain_distribution)


        if crawl_curr_link:
            random_sample.add(curr_link)
            random_sample_domain_distribution[link_register[curr_link].domain_name] = random_sample_domain_distribution.setdefault(link_register[curr_link].domain_name, 0) + 1
            pity_counter = 0
            previous_sampled_penalty = True
            cnt += 1
        else: 
            # If the code doesn't sample the node we increase the pity count. Increased pity means higher chance the code samples it
            pity_counter += 1
            p = pity_counter / 20
            if random.choices((True, False), weights=(p, 1-p), k=1)[0]:
                random_sample.add(curr_link)
                random_sample_domain_distribution[link_register[curr_link].domain_name] = random_sample_domain_distribution.setdefault(link_register[curr_link].domain_name, 0) + 1
                pity_counter = 0
                previous_sampled_penalty = True
                cnt += 1
            elif pity_counter > 5:
                previous_sampled_penalty = False
        
        # print(previous_sampled, pity_counter)

        # logger.log_link_info([curr_link, link_register[curr_link].num_links, crawl_probability_used, pity_counter == 0 and crawl_curr_link is not True, previous_sampled, cnt])

        # Removing any reference to the current node so the garbage collector handles it.
        link_register[curr_link] = None

        print("Done with", curr_link, cnt)
        time.sleep(2)

    print('finished')

    sampled_crawler = simpleWebCrawlerLogger("sampled", "sampled_crawl5.log")
    for link in random_sample:
        log_string = f"{link} | {detect_language_url(link)} | {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}"
        sampled_crawler.log_link_info(log_string)


def practical_crawler_next_step_strategy(og_link:Link, link_list: list[str], link_register: dict[str, Link], visit_list: list[str], queue_len:int):
    
    # Increment age of links already in queue
    for x in visit_list.copy():
        try:
            link_register[x].increment_age()
        except AttributeError:
            visit_list.remove(x)

    # approved_links = tuple(_standard_link_filtering(link_list, link_register))

    # We don't perform standard filtering because that means fetching robots.txt for every link
    # However in this method we don't crawl current page's links to identify next step
    approved_links = tuple(filter(lambda x: (x is not None) and (x not in link_register) and (Link.get_domain_count(x) < 60), link_list))


    if not approved_links:
        return None, link_register, visit_list, queue_len
    
    # Current page can have many links so we try to filter out about 200 of them
    # As mentioned before we give higher priority to ouward links and shorter links
    probabilites = []
    link_count = 0
    for link in approved_links:
        curr_prob = 2
        if Link._extract_domain_name(link) == og_link.domain_name:
            curr_prob *= 0.3
        
        if 90 < (length_link := len(link)) < 100:
            curr_prob *= 0.8
        elif 100 <= length_link < 120:
            curr_prob *= 0.7
        elif 120 <= length_link < 140:
            curr_prob *= 0.5
        elif 140 <= length_link:
            curr_prob *= 0.35
        
        link_count += 1
        probabilites.append(curr_prob)

    approved_links = list(random.choices(approved_links, weights=probabilites, k=min(175, link_count)))

    # approved_links.sort(key=lambda x: Link.get_domain_score(x))

    # We add these links to our register
    og_link._links_in_this_page = []
    for link in approved_links:
        # if link in link_register:
        #     continue
        visit_list.append(link)
        queue_len += 1
        link_register[link] = Link(link)
        link_register[link].increase_domain_count()
        og_link._links_in_this_page.append(link)

    # We re-evaluate the domain scores based on these new domains we just added to our store
    Link.re_eval_domain_score()
    # visit_list = list(set(visit_list))

    # We sort our list to put links with lower scores ahead
    visit_list.sort(key=lambda x: (75*Link.get_domain_score(x) + link_register[x].age + 1.1*len(x))*(1 + (og_link.domain_name == link_register[x].domain_name)*0.8), reverse=True)
    
    next_step = visit_list.pop()
    queue_len -= 1
    while link_register[next_step].title != '-2':
        next_step = visit_list.pop()
        queue_len -= 1

    # If the queue get bigger than a set threshold reduce it.
    if queue_len >= 5000:
        visit_list = list(random.sample(visit_list, 3500))
        queue_len = 3500

    return next_step, link_register, visit_list, queue_len

def practical_crawler_sample_strategy(og_link:Link, previous_sampled_penalty:float, same_domain:bool, sample_domain_distribution:dict[str, int]) -> bool:
    sample_prob = 1
    
    # if a link was sampled recently we reduce current node's sampling probability
    # However if links keep getting sampled this penalty keeps on getting increased
    if previous_sampled_penalty > 0:
        sample_prob -= 0.22*previous_sampled_penalty

    if sample_prob < 0:
        return False
    
    # if the current link is the same domain as the previous link
    if same_domain:
        sample_prob *= 0.65

    domain_score = Link.get_domain_score(og_link.link)
    
    # In this method we only penanlise common domains, we do not boost uncommon domains because it takes time to create a stable distribution
    if 0.5 <= domain_score < 0.7:
        sample_prob *= 0.8
    elif 0.7 <= domain_score < 0.9:
        sample_prob *= 0.7
    elif  0.9 <= domain_score:
        sample_prob *= 0.6

    # Penalising a link if it has too many links inside it
    sample_prob = max(sample_prob - Link.get_percentile_of_links(og_link.num_links) * 0.45, 0)
    try:
        # Penalising link if it has too less links in it
        sample_prob = max(sample_prob - (1/(og_link.num_links**0.5)), 0)
    except ZeroDivisionError:
        pass

    # If the current domain seems to appear many times we penalise proportional to how many times it appears
    # we limit a domain to 50 in the sample and it can can noticed from this line of code
    sample_prob -= (sample_domain_distribution.setdefault(og_link.domain_name, 0) / 60)
    
    # Now we do a coin flip to see if the current node gets penalised
    # sample_prob *= (1 - random.choices((True, False), k=1)[0] * 0.5)

    sample_prob = min(1, max(0, sample_prob))

    return random.choices((True, False), weights=(sample_prob, 1-sample_prob), k=1)[0]

def practical_crawler(visit_list: list[str], link_register: dict[str, Link], gen_logger:simpleWebCrawlerLogger):

    # Create a logger
    
    cnt = 0
    random_sample = set()
    random_sample_domain_distribution:dict[str, int] = {}
    visit_list = list(set(visit_list))
    next_step = None
    pity_counter = 0
    previous_sampled_penalty = False
    prev_domain = ""
    queue_len = 10
    crawled_len = 10

    try:
        while any(visit_list) and crawled_len < 12000:
            
            # We try to fetch as and when we go to link
            curr_link = visit_list.pop(0) if next_step is None else next_step
            rp = get_robots_txt(curr_link)
            if rp is not None and not rp.can_fetch('*', curr_link):
                if next_step is not None:
                    next_step = None
                else:
                    queue_len -= 1
                continue
            
            try:
                tot_links = link_register[curr_link].num_links
            except AttributeError:
                if next_step is not None:
                    next_step = None
                else:
                    queue_len -= 1
                continue
            else:
                if tot_links == 0:
                    try:
                        response = get_response(curr_link)
                    except (requests.exceptions.RequestException):
                        if next_step is not None:
                            next_step = None
                        else:
                            queue_len -= 1
                        continue
                    # As and when we get a response we log it
                    gen_logger.log_link_info(f"{curr_link} | {response.status_code} | {len(response.content)} | {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}")
                    if response is None or not response.ok:
                        if next_step is not None:
                            next_step = None
                        else:
                            queue_len -= 1
                        continue
                    link_register[curr_link].add_response(response)

            crawled_len += 1
            # This algorithm tries to figure out if this link is sampled or not.
            if practical_crawler_sample_strategy(link_register[curr_link], previous_sampled_penalty, prev_domain == link_register[curr_link].domain_name, random_sample_domain_distribution):
                random_sample.add(curr_link)
                random_sample_domain_distribution[link_register[curr_link].domain_name] = random_sample_domain_distribution.setdefault(link_register[curr_link].domain_name, 0) + 1
                # If a link gets sampled penalty is calculated accordingly
                previous_sampled_penalty += ((12-pity_counter)/12)*1.2
                pity_counter = 0
                cnt += 1
            else: 
                # If the current node gets rejected we increase pity
                pity_counter += 1
                p = pity_counter / 35
                if random.choices((True, False), weights=(p, 1-p), k=1)[0]:
                    random_sample.add(curr_link)
                    random_sample_domain_distribution[link_register[curr_link].domain_name] = random_sample_domain_distribution.setdefault(link_register[curr_link].domain_name, 0) + 1
                    # If a link gets sampled penalty is calculated accordingly
                    previous_sampled_penalty += ((12-pity_counter)/12)*1.2
                    pity_counter = 0
                    cnt += 1
                elif pity_counter > 12:
                    # It's no longer recent and we remove the penalty
                    previous_sampled_penalty = 0

            try:
                in_page_links = link_register[curr_link].links_in_this_page
            except AttributeError:
                continue

            # We try to get the next step and woosh we go
            next_step, link_register, visit_list, queue_len = practical_crawler_next_step_strategy(link_register[curr_link], in_page_links, link_register, visit_list, queue_len)
            
            prev_domain = link_register[curr_link].domain_name

            link_register[curr_link] = None

            print(curr_link, cnt, queue_len, crawled_len)
    
    except Exception as err:
        tb = err.__traceback__  # Get the traceback object
        err = err.with_traceback(tb)
        print("error")
        traceback.print_exc()
            # time.sleep(0.1)

    # except Exception:
    #     pass

    print('finished')

    sampled_crawler = simpleWebCrawlerLogger("sampled", "sampled_crawl6_6.log")
    for link, lang in multi_detect_language_url(random_sample):
        log_string = f"{link} | {lang} | {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}"
        sampled_crawler.log_link_info(log_string)

def main():
    start = time.process_time_ns()

    gen_logger = simpleWebCrawlerLogger("general","gen_crawl6_6.log")
    link_list, link_register = setup()

    print("starting crawl")

    # Only practical crawler supports logging
    practical_crawler(link_list, link_register, gen_logger)

    end = time.process_time_ns()

    # gen_logger.log_link_info(f"Time taken: {execution_time(end - start, show_time=False)}")


# execute_this(stack_trace=True)
if __name__ == "__main__":
    # execute_this(main)
    main()
