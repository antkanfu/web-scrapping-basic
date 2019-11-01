from indeed import get_jobs as i_jobs
from stackoverflow import get_jobs as s_jobs

import csv
def save_to_file(jobs):
    file = open("jobs.csv", "w")
    writer = csv.writer(file)
    writer.writerow(["title, company, location, link"])
    for job in jobs:
        writer.writerow(list(job.values()))