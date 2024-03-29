# blog-application
A Django/Python blog application implementing CRUD functionality and a robust user authentication system with API integration.

<h2>Sections</h2>
<p>
  <ul>
    <li><a href="#desc">Project Description</a></li>
    <li><a href="#feat">Features</a></li>
    <li><a href="#image">Screenshots</a></li>
    <li><a href="#tech">Technology</a></li>
    <li><a href="#setup">Setup</a></li>
    <li><a href="#test">Unit Test</a></li>
    <li><a href="#status">Project Status</a></li>
    <li><a href="#contribute">Contributing</a></li>
    <li><a href="#contact">Author</a></li>
    <li><a href="#licence">Licence</a></li>
   </ul>
</p>

<h2 id="desc">Project Description</h2>
<p> This project is a fully featured django blog application where authors can register and write blog post for visitors.
The app has the necessary authentications and permissions in place.
</p>

<h2 id="feat">Features</h2>
<ul>
  <li>Author Authentication</li>
  <li>Author Password Reset</li>
  <li>Author Profile</li>
  <li>Pagination</li>
</ul>

 <h2 id="image">Screenshots</h2>
  
  Home Page or Post List Page
  :------------------:
  ![Post List Page](https://github.com/KwabenaYeboah/blog-application/blob/master/mysite/screenshots/home_page_or_post_list_page.png)
  
   Post Detail Page
  :--------------------------:
  ![Post Detail Page](https://github.com/KwabenaYeboah/blog-application/blob/master/mysite/screenshots/post_detail_page.png)
  
   Author Post Detail Page
  :------------------:
  ![Author Post Detail Page](https://github.com/KwabenaYeboah/blog-application/blob/master/mysite/screenshots/author_permissions.png)
  
   Author Profile Page
  :------------------:
  ![Author Profile Page](https://github.com/KwabenaYeboah/blog-application/blob/master/mysite/screenshots/author_profile_page.png)
  
   Sign Up Page
  :------------------:
  ![Signu Up Page](https://github.com/KwabenaYeboah/blog-application/blob/master/mysite/screenshots/signup_page.png)
  
   Author Post List Page
  :------------------------:
  ![Author Posts](https://github.com/KwabenaYeboah/blog-application/blob/master/mysite/screenshots/posts_by_a_specific_author.png)
  
   New Post Page
  :------------------:
  ![Create New Post](https://github.com/KwabenaYeboah/blog-application/blob/master/mysite/screenshots/create_new_post.png)
  
   Delete Post Page
  :------------------:
  ![Delete Post](https://github.com/KwabenaYeboah/blog-application/blob/master/mysite/screenshots/delete_post_page.png)

<h2 id="tech">Technology</h2>
<ul>
  <li>Python</li>
  <li>Django</li>
  <li>Django Rest</li>
  <li>HTML5</li>
  <li>CSS3</li>
  <li>Boostrap4</li>

</ul>

<h2 href=#setup>Setup</h2>
To run the application, please follow guidlines below
<p>
1. Requirements
 <ul>
  <li>You need a PC or Macbook</li>
  <li>You have Git installed</li>
  <li>A Text Editor or IDE(eg.Vscode, Sublime, Pycharm)</li>
</ul></p>
<p>2. Install python3 and Pipenv</p>

<p>3. Now you setup as indicated below:</p>


 ```
  # Clone this repository into the directory of your choice
  $ git clone https://github.com/KwabenaYeboah/blog-application.git
  
  # Move into project directory
  $ cd blog-application
  
  # Install from Pipfile
  $ pipenv install
  
  # Move into mysite directory
  $ cd mysite
  
  # Migrate database models
  (blog-application-xxx) $ python manage.py migrate
  
  # Create superuser account
  (blog-application-XXXX) $ python manage.py createsuperuser
  
  # start server
  (blog-application-XXXX) $  python manage.py runserver
  
  # Copy the IP address provided once your server is up and running. (you will see something like >> Serving at 127.0.0.1....).
  
  # Open the address in the browser
  >>> http://127.0.0.1:XXXX/
  
  
  # Django Admin
  >>> http://127.0.0.1:XXXX/admin/
  ```

<h2 id="test">Unit Test Command</h2>

```
$ pytest -v
```

<h2 id="status">Project Status</h2>
Project is: Done

<h2 id="contribute">Contributing</h2>
Pull requests and stars are always welcome

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request

<h2 id="contact">Author</h2>

[KwabenaYeboah](https://github.com/KwabenaYeboah/)

<h2 id="licence">Licence</h2>

  **MIT** Licence
  
