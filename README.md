# GCP Idle Persistent Disk Snapshot And Delete

![GitHub repo size](https://img.shields.io/github/repo-size/scottydocs/README-template.md)
![GitHub contributors](https://img.shields.io/github/contributors/scottydocs/README-template.md)
![GitHub stars](https://img.shields.io/github/stars/scottydocs/README-template.md?style=social)

GCP Persistent Disk Snapshot And Delete is a `python script` that will `take a list of persistent disks with their zones to create snapshots and then delete the idle PD` in an effort to `reduce indexed custom metrics which impact our Datadog bill`.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* Script was created and tested with `python3.11`
* Install the requirements.txt
```
pip3 install -r requirements.txt
```
* You must have a GCP service account with the proper permissions
* Create a GCP service account following these instructions or using Terraform: [Create Service Accounts](https://cloud.google.com/iam/docs/service-accounts-create#console).
* Ensure you download the json key for the service account and export in local env var as well as gcp project id. Example:
```
export GCP_SVC_ACCT=~/Downloads/gcp-project-name-1ebddc5e3049.json
export GCP_PROJECT_ID="YOUR-GCP-PROJECT-ID"
```

## Using GCP Idle Persistent Disk Snapshot And Delete Script

To use GCP Idle Persistent Disk Snapshot And Delete script, follow these steps:

* Firstly, put together a list of persistent disk name and it's associated zone formatted as such `format 'diskName1:zone1,diskName2:zone2,...'`
* Running the script 
```
./gcp-pd-snap-delete.py
```
* Script will ask for input `Enter disk names and zones (format 'diskName1:zone1,diskName2:zone2,...'):`
    * Add the list you put together in a previous step. You should batch disks by groups of 15-20. There is some input or arguement limitation that is a *TO DO* that should be fixed.
* Output will display something like this: 

```
pvc-1ca58d38-7da4-4649-96ee-9726737488fc
us-east1-d
Creating snapshot for pvc-1ca58d38-7da4-4649-96ee-9726737488fc
Snapshot created successfully for pvc-1ca58d38-7da4-4649-96ee-9726737488fc
Deleting disk pvc-1ca58d38-7da4-4649-96ee-9726737488fc
Disk pvc-1ca58d38-7da4-4649-96ee-9726737488fc was deleted
pvc-861cacd5-e67f-4caa-8374-567322cbf4d3
us-east1-d
Creating snapshot for pvc-861cacd5-e67f-4caa-8374-567322cbf4d3
Snapshot created successfully for pvc-861cacd5-e67f-4caa-8374-567322cbf4d3
Deleting disk pvc-861cacd5-e67f-4caa-8374-567322cbf4d3
Disk pvc-861cacd5-e67f-4caa-8374-567322cbf4d3 was deleted
```
* Open GCP console to the snapshots page to monitor snapshot being created