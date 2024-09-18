from model.project import Project
import random
import re

def test_login(app):
    app.session.login("administrator", "root")
    assert app.session.is_logged_in_as("administrator")

def test_add_project(app):
    new_project = Project(name='project3', status='release', igc=True, view_status='private',
                          description='project3 description')
    if app.project.exists(new_project):
        app.project.delete(new_project)
    old_list = app.project.get_project_list()
    app.project.add(new_project)
    new_project.enabled = 'X'
    old_list.append(new_project)
    new_list = app.project.get_project_list()
    assert sorted(old_list, key=Project.id_or_max) == sorted(new_list, key=Project.id_or_max)

def test_del_some_project(app):
    if len(app.project.get_project_list()) == 0:
        some_project = Project(name='some', status='release', igc=True, view_status='private',
                              description='to delete')
        app.project.add(some_project)
    old_projects = app.project.get_project_list()
    some_project = random.choice(old_projects)
    app.project.delete(some_project)
    old_projects.remove(some_project)
    app.project.project_cache = None
    new_projects = app.project.get_project_list()
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)

