from model.project import Project
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