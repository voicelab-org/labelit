# How to deploy

## Step 1: Configure the environment

In order to deploy LabelIt, you should configure the following environment variables:

| Name                                 | Required | Default value                            | Description                                                                                                                                                                                                              |
|--------------------------------------|--------|------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| DB_HOST                              | *      | postgres                                 | Host name for the Postgres DB                                                                                                                                                                                            |
| DB_NAME                              | *      | labelit_db                               | Database name for the Postgres DB                                                                                                                                                                                        |
| DB_USER                              | *      | postgres                                 | User name for the Postgres DB                                                                                                                                                                                            |
| DB_PASSWORD                          | *      | postgres                                 | User password for the Postgres DB                                                                                                                                                                                        |
| AUDIO_FILE_STORAGE                   |        | storages.backends.s3boto3.S3Boto3Storage | Kind of storage to use for audio files. At the moment, just `storages.backends.s3boto3.S3Boto3Storage` is provided by default.                                                                                           |
| AWS_AUDIO_STORAGE_BUCKET_NAME        | *      | labelit-audio-bucket                     | Name of the bucket to be used to serve audio files.                                                                                                                                                                      |
| AWS_REGION_NAME                      |        | eu-west-1                                | Name of the region in which audio files are stored (just needed in case we are using AWS S3).                                                                                                                            |
| AWS_ENDPOINT_URL                     |        | http://minio:9000/                       | Endpoint for the bucket storage system. Use it in case you don't want to use AWS S3 (for instance, if you want to use MinIO or other alternative bucket compatible with boto3).                                          |
| AWS_ACCESS_KEY_ID                    | *      | EXAMPLEKEYID                             | Access key for the storage bucket.                                                                                                                                                                                       |
| AWS_SECRET_ACCESS_KEY                | *      | EXAMPLEKEYCONTENT                        | Secret access key for the storage bucket.                                                                                                                                                                                |
| IMAGE_FILE_STORAGE                   | *      | storages.backends.s3boto3.S3Boto3Storage | Kind of storage to use for image files. At the moment, just `storages.backends.s3boto3.S3Boto3Storage` is provided by default.                                                                                           |
| AWS_IMAGE_STORAGE_BUCKET_NAME        | *      | uploaded-images                          | Name of the bucket to be used to serve image files.                                                                                                                                                                      |
| S3_DIRECT_SERVE                      | *      | false                                    | In case you want to provide directe serving of audio files, set it to true; if you want to use presigned urls, set it to false. More information on this is provided on the section `Audio serving configuration` below. |
| SEGMENT_EXPIRATION_TIME_IN_SECONDS   |        | 3600                                     | Timeout of presigned urls in case you want to use them. See the `Audio serving configuration` section below.                                                                                                             |
                
### Quick launch (local deployment)

Use the [docker-compose.yml](../docker-compose.yml) file and do:

```bash
docker-compose up -d
```

 ### Audio serving configuration

LabelIt provides two ways to serve your files.

1. Direct serve: requires making your bucket public, not recommended except for internal use.
2. Presigned URLS: requires configuring CORS on your bucket, not recommended except for internal use.

Here we provide information for deployment using MinIO (preferred for local deployments, or self-managed buckets), and
for AWS S3 if you are using it in your cloud deployment.

#### Configuration for MinIO

Define the following ENV variables:

| Name                                 | Used value                                      |
|--------------------------------------|-------------------------------------------------|
| AWS_ENDPOINT_URL                     | Enpoint of MinIO deployment                     |
| AWS_ACCESS_KEY_ID                    | Access key for the MinIO storage bucket.        |
| AWS_SECRET_ACCESS_KEY                | Secret access key for the MinIO storage bucket. |
| S3_DIRECT_SERVE                      | true                                            |

The rest of variables are unrelated to MinIO, configure them as needed.

#### Configuration for AWS S3

1. First, configure the permissions on your bucket:

** Using presigned URLS (recommended) **

Go to the permissions tab on the S3 bucket screen on AWS console. 

Then, on `Bucket policy`, configure the permissions of the bucket as follows (or use your own desired permissions, 
this is just a reference): 

```yaml
{
    "Version": "2012-10-17",
    "Id": "<GIVE_IT_A_NAME>",
    "Statement": [
        {
            "Sid": "<GIVE_IT_A_NAME>",
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::<your-bucket-name>",
                "arn:aws:s3:::<your-bucket-name>/*"
            ],
            "Condition": {
                "NotIpAddress": {
                    "aws:SourceIp": [
                        // List of IPS from which you allow access, or `0.0.0.0/0` in case you don't want to block by IP              
                        "A.B.C.D/32",
                        or
                        "0.0.0.0/0",
                    ]
                }
            }
        }
    ]
}
```

** Using direct serve (not recommended) **

Go to the permissions tab on the S3 bucket screen on AWS console. 

Then, on `Block public access (bucket settings)`, click on `Edit` an unselect `Block all public accesss`. For more 
fine-grain access control select/unselect the rest of options.

2. Configure CORS

Go to the permissions tab on the S3 bucket screen on AWS console. 

Then, on `Cross-origin resource sharing (CORS)`, configure the CORS configurations as follows (or use your own configuration, 
this is just a reference): 


```yaml
[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "GET"
        ],
        "AllowedOrigins": [
            "https://your_host.your_domain.com",
            "http://localhost*",    // In case you want to provide access for localhost, during development (not recommended in production)
            "http://0.0.0.0*"    // In case you want to provide access for localhost, during development (not recommended in production)
        ],
        "ExposeHeaders": []
    }
]
```

3. Configure the variables next:

** Using presigned urls (recommended) **

| Name                               | Description                                                                                                                                                            | 
|------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| AWS_REGION_NAME                    | Name of the region in which audio files are stored.                                                                                                                    | 
| ~~AWS_ENDPOINT_URL~~                 | Actually, you should **unset** this one.                                                                                                                             | 
| AWS_ACCESS_KEY_ID                  | Access key for the storage bucket.                                                                                                                                     |
| AWS_SECRET_ACCESS_KEY              | Secret access key for the storage bucket.                                                                                                                              |
| S3_DIRECT_SERVE                    | Set this one to **false**.                                                                                                                                             |
| SEGMENT_EXPIRATION_TIME_IN_SECONDS | Timeout of presigned urls. This timeout prevents the file being reached longer than the time specified. If the time expires, a new presigned url should be obtained.   |

** Using direct serve (not recommended) **

| Name                               | Description                                         | 
|------------------------------------|-----------------------------------------------------|
| AWS_REGION_NAME                    | Name of the region in which audio files are stored. | 
| ~~AWS_ENDPOINT_URL~~                 | Actually, you should **unset** this one.          | 
| AWS_ACCESS_KEY_ID                  | Access key for the storage bucket.                  |
| AWS_SECRET_ACCESS_KEY              | Secret access key for the storage bucket.           |
| S3_DIRECT_SERVE                    | Set this one to **true**.                           |

## Step 2: Create a dataset

In order to create a dataset, the best way is by going into your backend bucket. For instance, if you are using your
local `docker-compose.yaml` deployment.

```bash
docker exec -it labelit_backend_1 python manage.py create_dataset \
    --dataset-name <the-name-of-dataset>  \
    --source-bucket-name <the-bucket-audio-files-will-be-taken-to-the-destination-one>  \
    --aws-key-id ${AWS_ACCESS_KEY_ID} \
    --aws-key-content ${AWS_SECRET_ACCESS_KEY} \
    --is-streamed true
```

* You can choose the name you want for your dataset with `dataset-name` (required).
* Audios will be downloaded from the source-bucket-name and stored into the bucket defined in the
`AWS_AUDIO_STORAGE_BUCKET_NAME` variable.
* Use is-streamed to define if you want to use HLS for audio serving (recommended) or just the original audio file. If 
HLS is selected, original files will be automatically converted to HLS (you will see an `hls` folder on the 
`AWS_AUDIO_STORAGE_BUCKET_NAME` bucket).

Check other interesting management commands by doing `docker exec -it labelit_backend_1 python manage.py <command> -h`, 
with one of the following commands:

* `clear_all_annotations`
* `create_dataset`
* `create_dataset_for_transcript_annotation`
* `create_dataset_from_csv`
* `create_timed_transcript`
* `update_files_in_dataset_to_hls`

## Step 3: Prepare a task

In the django admin, follow the steps next:

* Create one or more tasks (i.e., `CategoricalTasks`).
* Create a project, and assign the desired tasks to it.
* Create the needed manager users, at least one with staff and superuser permissions (this one should be able to create the Batches).
* Create as many annotator users and needed (those which are not superuser and staff at the same time).
* After that, you should be able to create your batches using the superuser.

