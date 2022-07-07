import requests
from bs4 import BeautifulSoup

PAGINATION_LEN = 10

def get_page_soup(url):
    web_page = requests.get(url)
    soup = BeautifulSoup(web_page.text, "html.parser")
    return soup

def get_pagination_list(url):
    soup = get_page_soup(url)
    pagi_data = soup.find("div", {"class":"tplPagination"}).find_all("li")
    pagi_list = []

    for each_data in pagi_data:
        anker = each_data.find("a")
        if not anker:
            page_num = each_data.find("span", {"class":"now"}).string
        else:
            page_num = anker.string
        pagi_list.append(int(page_num))

    return pagi_list

def get_site_page_cnt(first_page_url):
    pagi_list = get_pagination_list(first_page_url)

    current_middle_page_num = pagi_list[PAGINATION_LEN // 2]
    current_last_page_num = pagi_list[-1]

    while current_middle_page_num is not current_last_page_num:
        pagi_list = get_pagination_list(f"{first_page_url}&Page_No={current_last_page_num-1}")
        current_middle_page_num = current_last_page_num
        current_last_page_num = pagi_list[-1]

    return current_last_page_num

def extract_job_data(raw_data):
    job_data = {}
    job_data['title'] = str(raw_data.find("div", {"class":"post-list-info"}).find("a").get_text()).strip()
    job_data['company'] = raw_data.find("div", {"class":"post-list-corp"}).find("a").string
    job_data['location'] = raw_data.find("div", {"class":"post-list-info"}).find("span", {"class":"loc long"}).string
    job_id = raw_data['data-gno']
    job_data['link'] = f"https://www.jobkorea.co.kr/Recruit/GI_Read/{job_id}"
    return job_data

def get_jobs(searched_job):
    first_page_url = f"https://www.jobkorea.co.kr/search/?stext={searched_job}"
    last_page = get_site_page_cnt(first_page_url)
    jobs = []

    for page_num in range(last_page):
        print(f"""Scrapping "{searched_job}" results from jobkorea.co.kr / page : {page_num} of {last_page}""")
        page_soup = get_page_soup(f"{first_page_url}&Page_No={page_num}")
        page_job_data = page_soup.find("div", {"class":"list-default"}).find("ul", {"class":"clear"}).find_all("li", {"class":"list-post"})

        for each_data in page_job_data:
            jobs.append(extract_job_data(each_data))

    return jobs