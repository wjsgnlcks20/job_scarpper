import csv

def export_jobs_as_csv(jobs):
    file = open("jobs.csv", mode="w", encoding="UTF-8", newline="")
    writer = csv.writer(file)
    writer.writerow(['title', 'company', 'location', 'link'])
    for job in jobs:
        writer.writerow(job.values())

    return