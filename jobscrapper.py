import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request # render_template allows us to take the index.html and rendr it when the app is run

app = Flask(__name__) # instantiating the app / creating a flask instance and assigning it to app

def scrape_job_listings(keyword, location):
    base_url = 'https://www.timesjobs.com/candidate/job-search.html'

    params = {
        'searchType': 'personalizedSearch',
        'from': 'submit',
        'txtKeywords': keyword,
        'txtLocation': location,
    }

    response = requests.get(base_url, params=params)
    print(response)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        job_elements = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

        job_listings = []
        for job in job_elements:

            job_title = job.find('h2').text.strip()
            company_name = job.find('h3', class_='joblist-comp-name').text.strip()
            job_location = job.find('ul', class_='top-jd-dtl clearfix').find_all('li')[-1].span.text 
            skills = job.find('span', class_='srp-skills').text.strip().replace(' ', '')
            job_experience = job.find('ul', class_='top-jd-dtl clearfix').find_all('li')[0].text.split('card_travel')[1]
            publish_date = job.find('span', class_='sim-posted').span.text

            job_info = {
                "Job Title": job_title,
                "Company": company_name,
                "Location": job_location,
                "Skills": skills,
                "Experience": job_experience,
                "Publish Date": publish_date
            } # creating a json object for the job information

            job_listings.append(job_info) # appending the job info to the job_listing list
        return job_listings
    else:
        print("returned no job listing")
        return None

@app.route('/jobs', methods=['GET']) # using the route() decorator to tell Flask what URL should trigger our function.    
def get_jobs():
    keyword = request.args.get('keyword')
    location = request.args.get('location')
    if(keyword is None and location is None):
        print("keyword, location = null")
        return render_template('index.html')
    else:
        if(keyword == ""):
            keyword = None
        else:
            print(keyword)
        if(location == ""):
            location = None
        else:
            print(location)
        job_listings = scrape_job_listings(keyword, location)
        if job_listings:
            return render_template('index.html', job_listings=job_listings)
        else:
            return render_template('search_error.html')
    
if __name__ == "__main__":
    app.run(debug=True)
    
