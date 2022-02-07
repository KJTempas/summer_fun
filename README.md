# Summer Fun

### An app to schedule fun summer activities at a camp.  
Add students, add activities, schedule and edit activites for a student.  Run reports.

#### Virtual Environment
Create and activate a virtual environment. Use Python3 as the interpreter. Suggest locating the venv/ directory outside of the code directory

Mac Version:
python3 -m venv env
source env/bin/activate

Windows Version:
python -m venv env
env\Scripts\activate

#### Install required modules
pip install -r requirements.txt (pip3 for Mac)
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

#### View Site
Local site available at http://127.0.0.1:8000

#### Create superuser
python manage.py createsuperuser

enter username and password

will be able to use these to log into admin console at

https://127.0.0.1:8000/admin


#### Screenshots
![Screen Shot 2022-02-04 at 12 33 33 PM](https://user-images.githubusercontent.com/54478043/152585667-af254177-1a55-4ae0-a58d-6c943155d58f.png)
![Screen Shot 2022-02-04 at 12 33 52 PM](https://user-images.githubusercontent.com/54478043/152585721-40bf8ca3-66b8-4bce-9717-a60895e70f96.png)
![Screen Shot 2022-02-04 at 12 33 44 PM](https://user-images.githubusercontent.com/54478043/152585755-7f1df198-ac85-4181-8b18-7e8682c3d164.png)
![Screen Shot 2022-02-04 at 12 34 08 PM](https://user-images.githubusercontent.com/54478043/152585790-55d046ab-cfd8-471f-8d21-f3f35de0f00c.png)
![Screen Shot 2022-02-04 at 12 34 01 PM](https://user-images.githubusercontent.com/54478043/152585863-7d10434e-a12f-4c63-b02e-25fbe21a8725.png)
![Screen Shot 2022-02-04 at 12 34 17 PM](https://user-images.githubusercontent.com/54478043/152585898-4d7829ec-3b49-446a-a70c-65dc2b7bde72.png)
![Screen Shot 2022-02-04 at 12 34 27 PM](https://user-images.githubusercontent.com/54478043/152585925-d21678e8-be89-4680-b2b8-1b2bd62abd43.png)




#### Run tests
python manage.py test