from suds.client import Client
from suds import WebFault
from model.project import Project
class SoapHelper:
    def __init__(self, app, username, password):
        self.app = app
        self.username = username
        self.password = password
        self.client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")

    def can_login(self, username, password):
        try:
            self.client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_project_list(self):
        client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        try:
            l = client.service.mc_projects_get_user_accessible(self.username, self.password)
            project_list = []
            for element in l:
                name = element.name
                status = element.status.name
                id = element.id
                description = element.description
                enabled = element.enabled
                view_status = element.view_state.name
                project_list.append(Project(name=name, status=status, enabled=enabled, view_status=view_status,
                                                  description=description, id=id))
            return project_list
        except WebFault:
            return False

    def destroy(self):
        pass




