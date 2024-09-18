from model.project import Project
import re
class ProjectHelper:
    def __init__(self, app):
        self.app = app


    def go_to_manage_project(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/manage_proj_page.php")):
            wd.find_element_by_link_text("Manage").click()
            wd.find_element_by_link_text("Manage Projects").click()

    def add(self, new_project):
        wd = self.app.wd
        self.go_to_manage_project()
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()
        self.populate_data(new_project)
        wd.find_element_by_xpath("//input[@value='Add Project']").click()
        self.go_to_manage_project()
        self.project_cache = None


    def populate_data(self, project):
        self.populate("name", project.name)
        self.select_value('status',project.status)
        self.set_checkbox("enabled", project.enabled)
        self.set_checkbox("inherit_global", project.igc)
        self.select_value('view_state', project.view_status)
        self.populate("description", project.description)

    def populate(self, fieldname, value):
        wd = self.app.wd
        if value is not None:
            wd.find_element_by_name(fieldname).click()
            wd.find_element_by_name(fieldname).clear()
            wd.find_element_by_name(fieldname).send_keys(value)

    def select_value(self, fieldname, value):
        wd = self.app.wd
        if value is not None:
            wd.find_element_by_xpath("//select[@name='%s']/option[text()='%s']" % (fieldname,value)).click()

    def set_checkbox(self, fieldname, value):
        wd = self.app.wd
        if value is not None:
            checkbox = wd.find_element_by_xpath("//td/input[@name='%s']" % fieldname)
            if ((not checkbox.is_selected() and value)
                    or (checkbox.is_selected() and not value)):
                checkbox.click()

    def delete(self, project):
        wd = self.app.wd
        self.go_to_manage_project()
        self.open_project(project)
        self.delete_project()

    def open_project(self, project):
        wd = self.app.wd
        wd.find_element_by_link_text(project.name).click()

    def delete_project(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//input[@value = 'Delete Project']").click()
        wd.find_element_by_xpath("//input[@value = 'Delete Project']").click()
        if not wd.current_url.endswith("manage_proj_page.php"):
            self.go_to_manage_project()

    def exists(self, project):
        wd = self.app.wd
        self.go_to_manage_project()
        if len(wd.find_elements_by_link_text(project.name))>0:
            return True
        else:
            return False


    project_cache = None
    def get_project_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.go_to_manage_project()
            self.project_cache = []
            rows = wd.find_elements_by_xpath('//table[3]/tbody/tr[contains(@class, "row-1") or contains(@class, "row-2")]')
            for element in rows:
                name = element.find_element_by_xpath('.//td[1]').text
                id = re.compile(r'(\d+)$').search(element.find_element_by_xpath('.//td[1]/a').get_attribute('href')).group(1)
                status = element.find_element_by_xpath(".//td[2]").text
                enabled = element.find_element_by_xpath(".//td[3]").text
                view_status = element.find_element_by_xpath(".//td[4]").text
                description = element.find_element_by_xpath(".//td[5]").text
                self.project_cache.append(Project(name=name, status=status, enabled=enabled, view_status = view_status,
                                                  description=description, id=id))
        return list(self.project_cache)








