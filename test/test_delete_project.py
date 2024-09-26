from model.project import Project
import random
def test_del_some_project(app):
    app.session.login(app.login, app.password)
    if len(app.project.get_project_list()) == 0:
        some_project = Project(name='some', status='release', igc=True, view_status='private',
                              description='to delete')
        app.project.add(some_project)
    old_projects = app.soap.get_project_list()
    some_project = random.choice(old_projects)
    app.project.delete(some_project)
    old_projects.remove(some_project)
    app.project.project_cache = None
    new_projects = app.soap.get_project_list()
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)