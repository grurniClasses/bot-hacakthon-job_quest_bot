from pymongo import MongoClient


class MongoStorage:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.get_database('job_application')
        self.job_collection = self.db.get_collection('job_application')

    def findAllByChatId(self, chat_id):
        return list(self.job_collection.find({"chat_id": str(chat_id)}))

    def findAllAppliedByChatId(self, chat_id):
        return list(self.job_collection.find({"chat_id": str(chat_id), "status": "Applied"}))

    def findJobByCompany(self, chat_id, company):
        return self.job_collection.find_one({"chat_id": str(chat_id), "company": company})

    def updateJobStatus(self, chat_id, company):
        self.job_collection.find_one_and_update({"chat_id": str(chat_id), "company": company, "status": "Applied"},
                                                {"$set": {"status": 'Rejected'}})

    def insertJob(self, chat_id, app):
        self.job_collection.insert_one({"chat_id": str(chat_id), "company": app.get_company(),
                                        "title": app.get_title(), "stack": app.get_stack(),
                                        "date_applied": str(app.get_date_applied()), "status": app.get_status(),
                                        "date_response": str(app.get_date_response())})
