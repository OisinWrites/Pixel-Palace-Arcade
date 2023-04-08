Pixel Palace Arcade

Site Goals

Agile Development
    Epics and User Stories

Example Sites

Design 

    UX/UI
        Wireframes
        Colour choice
        Image Selection
        Font choices

    Logic
        Class Models
        Python logic flowcharts

    Search Engine Optimization

    Web Marketing

Features

Testing
    Error Log
    1. In connecting static files, specifically base.css into the base.html file the line {5 static 'css/base.css' %} throws back an error requesting missing endblock.
    2. Stackoverflow suggests moving the static directory under the app, opposed to the example project boutique_ado. And additionally directing to the new file location in settings. However this has not solved issue.
    Validation and Accessibility

Deployment

Credits

Project Process
1. Install Django, create app and superuser. Created .gitignore file for app.
2. Begin ReadMe with section headings.
3. Create project in github for agile stories, set to public, linked to repository.
4. Install Allauth, make necessary changes to settings, and create url path.
5. Migrate app, runserver, sign in with superuser info.
6. Edit site name, for easier authentication later with social media apps.
7. Create email backend and sign in/up settings in settings.py.
8. Create requirements.txt with pip freeze.
9. Open email address in admin models and select verify and primary for admin email.
10. Make templates, and allauth, directories.
11. Copy template directories from allauth to folders made in last step.
12. Create base.html under templates directory. Copy boilerplate from bootstrap.
13. Add meta lines, move script up, add load static.
14. Wrap sections in {% %} blocks.
15. Create home app. Create templates, views, urls for index page and test.
16. 