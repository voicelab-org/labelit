## Labelit

Labelit is an extensible web-based annotation tool currently supporting:

* Text and audio annotation (summative)
* Categorical, ordinal classification
* Transcription
* Named entity annotation (highlighting and labeling)
* Text edition (correction, punctuation, etc.)

The tool comes with utilities for distributing work across multiple annotators,
monitoring progress and (where applicable) annotator agreement, Quality Assurance (QA)
 and managing datasets.

Multiple annotation tasks (e.g. classification + transcription) can be combined
in a single project

Labelit is designed for extensibility: new annotation tasks / schemas
can be created by contributors, while retaining generic features.

The code uses Django for the backend, and VueJS for the frontend.

-----------------------

Entity annotation (WIP) in labelit in QA mode. Annotations can be validated or sent for review:

![Entity annotation](./screenshots/entities_qa.png)

Annotation on labelit is divided into projects. Each project defines a set of annotation tasks and is further 
divided into batches. The following screenshot shows the creation of a batch. Labelit
enables annotation managers to configure for each batch: which data to annotate and how much, the number of participants,
the number of annotators per document and how the documents are distributed among annotators (even or possibly varying
number of documents across annotators)

![Batch creation](./screenshots/batch_creation.png)

Generic and task-specific information and statistics are provided for each batch.
For some tasks, agreement and other quality metrics are automatically computed.

![Batch stats](./screenshots/batch_stats.png)

The global dashboard (WIP) provides a global overview of the work:

![Stats dashboard](./screenshots/stats_dashboard.png)

HTML instructions can be edited by annotation managers and enriched with images and links:

![Guidelines](./screenshots/annotation_task_guidelines.png)

You are free to choose which tasks to combine in a project. Here, two ordinal tasks are combined, but different
types of tasks (ex. transcription + categorization) can also be combined. For each project you can specify if you want
audio, text or both to be annotated

![Two-task setup](./screenshots/qa_multi_task_ordinal_annotation.png)

## How to deploy

Information on how to deploy LabelIt is available at [docs/how_to_deploy.md](docs/how_to_deploy.md).

