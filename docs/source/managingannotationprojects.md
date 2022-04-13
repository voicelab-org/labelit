# Managing annotation projects

## Set up annotation tasks

In labelit, you can annotate text and/or audio documents in different ways. For instance, you might be transcribing speech audio
to later train an ASR model, or highlighting entities in a text or transcript, or classifying entire documents.

Labelit allows you to define different kinds of tasks and then combine them in arbitrary ways inside projects.

The code is designed in such a way that extending to support other types of tasks is straightforward.

To create a task, go to the Django admin panel (local deployment: `0.0.0.0:8000/admin`). The "Labelit" table
contains all Labelit models, including models for tasks.

The following task types are currently available:

* categorical tasks (flat categories, single- or multi-select)
* nested categorical tasks (two-level categories)
* entity tasks (named entities)
* ordinal tasks (discrete, ordinal labeling)
* text edition tasks (e.g. correction of transcription, manual punctuation of ASR transcripts, orthographic correction, normalization)
* transcription tasks (for transcription of audio)

Here we explain how to configure categorical tasks, but the process is similar for other tasks.

First, go to the admin page for categorical tasks `/admin/labelit/categoricaltask/` then click on "Add Categorical task".

The form enables you to configure the tasks and the associated labels (here, categories).

Similarly, any other type of task can be configured in the django admin.

## Set up projects

Next, go to the admin page for projects `/admin/labelit/project/` and create a new project.

At this stage you can decide whether audio, text or both are annotated (for some tasks, it can also make sense
to leave both unchecked.)

This is also where you attach one or more tasks to the project.

## Add annotators and QA users

There are two types of users on labelit. QA users (`is_staff = true`) can create annotation batches,
assign annotation work, and review annotations. Annotators (`is_staff = false`) do the actual annotation,
QA users cannot annotate.

User creation in labelit is the same as in any standard django project. Make sure to set `is_staff` according to the 
desired role of each user.

## Create datasets

Datasets are sets of documents. Each document can contain text and/or a reference to an audio file.
Audio files are assumed to be stored on S3 buckets (planned: extending to other audio storage backends)

Since datasets typically contain many documents, it is recommended to create them programmatically.

For an example, see `backend/labelit/management/commands/create_dataset.py`

## Launch annotation batches

Once projects, tasks and datasets are configured, the remaining setup can be done from the labelit frontend
(local deployment: `localhost:8081`).

To create your first batch, find and click on the project in the list of projects (`/projects`).

Now click on the "create batch" button, which will open the batch creation dialog. Here, you can
select the dataset from which you want to annotate, the number of documents, the desired number of
annotators per document, and the distribution mode (equal distribution of work or "all-you-can-annotate")

Note that only non-QA users will appear in the "annotator dropdown list"

## Monitor progress and review

You can follow annotation work in different ways in Labelit.

The global dashboard (`/dashboard`) gives you an overview of all projects, but you can also
filter by projects and annotators.

Each project has a stats tab containing project-level annotation stats and visualizations.

Likewise, each batch has a stats tab containing batch-level stats and visualizations.
