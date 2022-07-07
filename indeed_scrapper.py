import requests
from bs4 import BeautifulSoup

LIMIT = 50
PAGINATION_LEN = 5 # 페이지 하단부 다른 페이지로 가는 인덱싱 된 링크의 수

def get_page_soup(url):
    web_page = requests.get(url)
    soup = BeautifulSoup(web_page.text, "html.parser")
    return soup

def get_pagination_list(url):
    soup = get_page_soup(url)
    pagi_list = []
    pagi_data = soup.find("div", {"class":"pagination"}).find("ul", {"class":"pagination-list"}).find_all("li")
    for each_data in pagi_data:
        page_num = each_data.string
        if page_num:
            pagi_list.append(int(page_num))

    return pagi_list

def get_site_page_cnt(url):
    # 가장 마지막 페이지 나올때까지 최대 크기의 페이지로 이동하여 마지막 페이지 값을 찾아낸다...
    pagi_list = get_pagination_list(url)

    current_middle_page_num = pagi_list[PAGINATION_LEN // 2]
    #지금 당장 이 사이트에서는 먹일 건데 그래도 더 좋은 방법이 없을까...
    # html에 있는 정보로 현재 있는 페이지 판단하도록 수정...
    current_last_page_num = pagi_list[-1]

    while current_middle_page_num is not current_last_page_num:
        pagi_list = get_pagination_list(f"{url}&start={LIMIT*(current_last_page_num-1)}")
        current_middle_page_num = current_last_page_num
        current_last_page_num = pagi_list[-1]

    return current_last_page_num

def extract_job_data(raw_data):
    job_data = {}
    job_data['title'] = raw_data.find("h2", {"class": "jobTitle"}).find("a").string
    job_data['company'] = raw_data.find("span", {"class": "companyName"}).string
    job_data['location'] = raw_data.find("div", {"class": "companyLocation"}).string
    job_id = raw_data.find("h2", {"class": "jobTitle"}).find("a")["data-jk"]
    job_data['link'] = f"https://kr.indeed.com/viewjob?jk={job_id}"

    return job_data

def get_jobs(searched_job):
    first_page_url = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q={searched_job}&limit={LIMIT}"
    last_page = get_site_page_cnt(first_page_url)
    jobs = []

    for page_num in range(last_page):
        print(f"""Scrapping "{searched_job}" results from indeed.com / page : {page_num} of {last_page}""")
        soup = get_page_soup(f"{first_page_url}&start={LIMIT*page_num}")
        page_job_data = soup.find_all("td", {"class": "resultContent"}) #### 페이지에 나오는 각 직업 정보 모두 가져오기

        for each_data in page_job_data:
            jobs.append(extract_job_data(each_data))

    return jobs