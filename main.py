from flask import Flask, render_template, request, redirect, send_file
from indeed_scrapper import get_jobs as get_indeed_jobs
from jobKorea_scrapper import get_jobs as get_jobKorea_jobs
from exporter import export_jobs_as_csv

def get_jobs(job):
    return get_jobKorea_jobs(job) + get_indeed_jobs(job)

app = Flask("SuperScrapper")

@app.route("/")
def home():
    return render_template("home.html")

db = {}

@app.route("/result")
def result():
    searched_word = request.args.get("q")

    if not searched_word:
        return redirect("/")

    searched_word = searched_word.lower()
    search_result = db.get(searched_word)

    if not search_result:
        search_result = get_jobs(searched_word)
        db[searched_word] = search_result

    return render_template(
        "result.html",
        resultNumber=len(search_result),
        searched_word=searched_word,
        jobs=search_result
    )

@app.route("/export")
def export():
    try:
        searched_word = request.args.get("q")
        if not searched_word:
            raise Exception()

        searched_word = searched_word.lower()
        search_result = db[searched_word]

        if not search_result:
            raise Exception()

        export_jobs_as_csv(search_result)
        return send_file("jobs.csv")

    except:
        return redirect("/")

app.run()