from bs4 import BeautifulSoup
import requests
import time

print('Input any skill(s) you are unfamiliar with (comma-separated):')
unfamiliar_skills_input = input('>')
unfamiliar_skills = [skill.strip() for skill in unfamiliar_skills_input.split(',')]
print(f'Filtering out {unfamiliar_skills}')

def find_jobs():
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=ft&searchTextText=&txtKeywords=Python&txtLocation=').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

    with open('all_jobs.txt', 'a') as all_jobs_file:  # Open a single file to store all jobs
        for index, job in enumerate(jobs):
            publised_date = job.find('span', class_='sim-posted').span.text
            if 'few' in publised_date:

                company_name = job.find('h3', class_='joblist-comp-name').text.replace(' ', '')
                skills = job.find('span', class_='srp-skills').text.replace(' ', '')
                more_info = job.header.h2.a['href']

                if not any(skill in skills for skill in unfamiliar_skills):
                    all_jobs_file.write(f"Company Name: {company_name.strip()} \n")
                    all_jobs_file.write(f"Required Skills: {skills.strip()} \n")
                    all_jobs_file.write(f'More Info: {more_info} \n\n')
                    print(f'{index} job saved to all_jobs.txt')

if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 10
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait * 60)
