from datetime import date

class Application:
    def __init__(self, company, title, stack):
        self.company = company
        self.title = title
        self.stack = stack
        self.date_applied = date.today()
        self.status = "Applied"
        self.date_response = None

    def __str__(self):
        return f"{self.company} - {self.title} - {self.stack} - {self.status} - {self.date_applied}"

    def __repr__(self):
        return f"{self.company} - {self.title} - {self.stack}"

    def set_status(self, status):
        self.status = status
        if status == "Rejected":
            self.date_response = date.today()

    def get_status(self):
        return self.status

    def get_date_applied(self):
        return self.date_applied

    def get_company(self):
        return self.company

    def get_title(self):
        return self.title

    def get_stack(self):
        return self.stack

    def get_date_response(self):
        return self.date_response
