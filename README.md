# AWS batch pipeline and builder job dashboard

## What this dashboad shows

This application allows users to view the logs generated by AWS batch pipeline and builder jobs.

It serves up the contents of the dl-batch-logs S3 bucket (in the digital land dev aws account).

Batch job runs puts three files, capturing the exit code, standard out, standard error of the job run,
into the bucket keyed by collection/builder name, then date of job run, the AWS batch job id and the file name.

For example:

```
/2021-11-17/document-type-collection/[AWS_BATCH_JOB_ID]/exit_code.txt
/2021-11-17/document-type-collection/[AWS_BATCH_JOB_ID]/stderr.txt
/2021-11-17/document-type-collection/[AWS_BATCH_JOB_ID]/stdout.txt
```

##

The application is deployed to heroku and can be seen at [https://dl-batch-dashboard.herokuapp.com/](https://dl-batch-dashboard.herokuapp.com/)

## Local development

Make a virtualenv for the project and install python dependencies

    pip install

Set environment variables or provide a config file (see `config/config.py`).


Start the application

    flask run


