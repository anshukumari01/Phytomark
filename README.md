
<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">Phytomark</h3>

  <p align="center">
    <a href="http://phytomark.com">View Site</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#running-this-project">Running this project</a>
    </li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>






## Running this project

To get this project up and running you should start by installing Python on your computer. You should create a virtual environment to store your project's dependencies separately. You can install virtualenv with

```
pip install virtualenv
```

Clone or download this repository and open it in your editor of choice. In a terminal (mac/linux) or windows terminal, run the following command in the base directory of this project

```
virtualenv venv
```

That will create a new folder `env` in your project directory. Next, activate it with this command on mac/linux:

```
source venv/bin/active
```

Then install the project dependencies with

```
pip install -r requirements.txt
```
Set up a `.env` file in the below format
```
SECRET_KEY= <your_django_secret_key>
DEBUG= <True or False>


EMAIL_HOST_USER= <email_from_which_all_mail_to_be_sent>
EMAIL_HOST_PASSWORD= <app_password_for_your_mail>

RAZORPAY_SECRET_KEY= <your_razorpay_secret_key>
RAZORPAY_KEY_ID= <your_razorpay_key_id>


```

Apply migrations and create your database
```
python manage.py migrate
```
Create a user with manage.py
```
python manage.py createsuperuser
```

Now you can run the project with this command

```
python manage.py runserver
```

<br>





## Contact

<div align='left'>

<a href="https://www.linkedin.com/in/anshu-kumari-2aa4ab207/" target="_blank">
<img src="https://img.shields.io/badge/linkedin-%2300acee.svg?color=405DE6&style=for-the-badge&logo=linkedin&logoColor=white" alt=linkedin style="margin-bottom: 5px;"/>
</a>

		

</div>
