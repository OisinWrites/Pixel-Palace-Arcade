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
    3. Solution: Base.html was missing {% load static %}, whether this should have been performed by the existing same line in index.html after extending base or otherwise, the mock server is now functioning as desired.

    1. Styling was incomplete when viewing site with runserver.
    Base.css was clearly attached correctly, as background image evident, however text is blue, and background div for delivery message unaffected.
    2. I was not using the important override for specificity correctly, and had omitted the exclamation mark prefix from the code.
    3. Corrected styling/targeting error and page is working correctly. 

    1. Need to find correct way to target my image files in media from a django admin panel for products models. Currently the image file is clicked and dropped.
    2. Admin panel sought to add chosen file from coomputer folders, but saved chosen file in media directory. Allowed admin system to drop them there for it to find, rather than force it to pick up from there, where they were already. Likely though, that I was entering the url wrong, which the panel kept insisting was an invalid format.

    1. The badge span to indicate selected categories for shown products list is not inverting colour on hover.
    2. This resolved after pushing, exiting, and reentry.

    1. The sorting text is not updating with the current search from the nav bar.
    2. The code in the html was fine, but the view, on line 46, had the words sort and direction in regular brackets instead of the necessary curlies.

    1. Added script, styling, and html div for a button to bring viewer to the top of a products page. However, thoguh the button should float at the bottom right of the screen, it is static at the bottom of the page, after all products.
    2. After running server and using inspect tool, it is evident the the div is not picking up it the styling from css.
    3. Like the previous issue, this one resolved itself on shutting down gitpod and rebooting. Must be missing a command to refresh or update environmental server manually.
    4. Note to self: Turn it off and on again before staring at code for an hour.

    1. In checkout, the payment field in the form is not working. This may be because we 're not activated on Stripe in our account.

    1. The error messages for the stripe form float on top of the nav banner.

    1. The images for products are called on from the database, not the cloud file storage. In the project example, boutique ado, these images are used as fixtures. Is there a way I can have the product models find their relevant picture from the cloud instead?


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
16. Created seperate files for the navbar, and for mobile navbar and included into base.html.
17. Created categories and subcategories for products with anchors to be filled in.
18. Added product images to media
19. Created app Products, copied json fixtures- categories and products.
20. Created models for Categories and Products and made migrations.
21. Registered new models in admin.py file.
22. Installed Pillow and updatedd requirements.txt
23. Ran command python3 manage.py loaddata categories. Had to run migrate cmnd prior. Installed 9 objects successfully.
24. Removed fixtures as that is prior gathered data for boutique ado project. Instead, build product list from scratch in admin panel.
25. Add views for products
26. Customise admin via admin.py for abiltiy to sort and search.
27. Create a view function for products details, url, and template.
28. Add functionality to search bar using django database model: Q
29. Add functionality to sort items by category, price, rating.
30. Create bag app to handle the shopping bag function.
31. Create a context.py file to handle the bag across any other template. Update settings for templates, and add delivery threshold and percentage.
32. Give content to bag view.
33. Using shell command update models to include boolean toggle for variants on selected categories.
34. In product details add content to select console for games.
35. Have label for variant render in shopping bag or else N/A.
36. Refine quantity selection in details and bag templates.
37. Give messages to the user to affirm actions..
38. Create checkout app once bag is finished.