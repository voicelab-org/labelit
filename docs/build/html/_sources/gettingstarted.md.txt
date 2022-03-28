# Getting started

## Local installation

```bash
cd <labelit-project-root>
docker-compose build
docker-compose up
```


Once all services are running, labelit can be accessed at `localhost:8081`. The django admin panel
will be accessed at `0.0.0.0/admin`

Create a Django superuser:


```bash
docker-compose run backend bash
root@a397d8e22e87:/code# python manage.py createsuperuser
```

Follow the instructions to create the super user, taking note of credentials.

You can now login into the admin panel and add other users.

If you want a user to be a QA user, check "staff status" in the user edit form.

Now, you can load some toy data to get going:


```bash docker-compose run backend bash
root@a397d8e22e87:/code# python manage.py loaddata toydata
```

This will create a dataset and a project containing two types of tasks, one categorical and one ordinal task.
This step also creates two users, one QA user (janedoe-qa@levoicelab.org) and an annotator user (jogndoe@levoicelab.org).

In the future, you can create datasets, tasks, projects and users via management commands or the admin panel.

As the admin user, you can now go inside a project from the projects list and create annotation batches by clicking on the "Create batch" button.
The dialog form should be self-explanatory.

Add (non-QA) annotators to the batch.
Note that QA users will have access to all projects and will be able to review all annotations.


