import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"

def get_last_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    pagingation = soup.find("div", {"class":"pagination"})
    links = pagingation.find_all("a")
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
    max_page = pages[-1]
    return max_page

def extract_job(html):
    title = html.find("div", {"class":"title"}).find("a")["title"]
    company = html.find("span", {"class":"company"})
    company_anchor = company.find("a")
    company_value = company.string if company_anchor is None else company_anchor.string.strip()
    location = html.find("div", {"class":"recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    return {'title': title, 'company': company_value, 'location':location, "link":f"https://www.indeed.com/viewjob?jk={job_id}"}

def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed: page: {page}")
        result = requests.get(f"{URL}&start={page*50}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class":"jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs():
    last_page = get_last_pages()
    jobs = extract_jobs(last_page)
    return jobs