from pprint import pprint

import requests
import random
def get_jobs(title):
    url = "https://insider.geektime.co.il/wp-content/uploads/all_jobs.json"
    db = requests.get(url)
    # pprint(random.choice(db.json()))

    result = []
    for job in db.json():
        if title.lower() in job["title"].lower():
            result.append(job)
    result2 = []
    if result:
        # pprint(result)
        # print(len(result))
        for job in result:
            # print(job["job_description"])
            # start_index = job["job_description"].index('We')
            # end_index = job["job_description"][start_index:].index('</p>') + start_index
            # description_result = job["job_description"][start_index:end_index]
            d = {
                    "company": job["company_name"],
                    # "job description": description_result,
                    "city": job["city"],
                    "link": job["link_to_form"],
                }
            # print('add')
            result2.append(d)
    # pprint(result2)
    return result2

# get_jobs('Software Engineer')

# class JobSearch:
#     def __init__(self):
#         self.where = ''
#         self.what = ''
#
#     def set_where(self, company):
#         self.where = company
#
#     def set_what(self, name):
#         print('in set what')
#         self.what = name
#
#     def findJob(self):
#         url = f'http://rss.jobsearch.monster.com/rssquery.ashx?q={self.what}&where={self.where}'
#         res = requests.get(url)
#         lst = []
#         if res.status_code == 200:
#             s = res.text
#             end_index = s.find('</item>')
#             start_index = s.find('<item>')
#             while start_index != -1:
#                 job_info = s[start_index : end_index]
#                 title = job_info[job_info.find('<title>') + len('<title>') : job_info.find('</title>')]
#                 description = job_info[job_info.find('<description>') + len('<description>') : job_info.find('</description>')]
#                 link = job_info[job_info.find('<link>') + len('<link>') : job_info.find('</link>')]
#                 lst.append({'title' : title, 'description' : description, 'link' : link})
#                 s = s[end_index:]
#                 start_index = s.find('<item>')
#         else:
#             print("error")
#         if len(lst) == 1 and lst[0]['link'] == 'http://jobview.monster.com/':
#             return []
#         return lst

# job = JobSearch()
# print(job.findJob())
     


    

