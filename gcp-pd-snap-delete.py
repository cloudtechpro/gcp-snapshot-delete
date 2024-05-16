#!/usr/bin/env python3
# Must be the first line
from __future__ import print_function

"""
Delete unattached persistent disks and create snapshots before deletion
"""

# modify these variables for your environment:
project = os.environ.get('GCP_PROJECT_ID')

# Imports
from datetime import datetime
import time
from google.cloud import compute_v1
from google.oauth2 import service_account
import dateutil.parser
import pytz
import os

# Path to your service account key file
key_path = os.environ.get('GCP_SVC_ACCT')

credentials = service_account.Credentials.from_service_account_file(
    key_path,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

# Initialize clients with the given credentials
compute_disks_client = compute_v1.DisksClient(credentials=credentials)
zone_operations_client = compute_v1.ZoneOperationsClient(credentials=credentials)

# Define helper functions
def waitForZoneOperation(project, zone, operation_name):
    while True:
        operation = zone_operations_client.get(project=project, zone=zone, operation=operation_name)
        if operation.status == compute_v1.Operation.Status.DONE:
            if operation.error:
                print("Error during operation:", operation.error)
                return False
            return True
        time.sleep(3)

# Function to create a snapshot
def createSnapshot(project, zone, disk_name):
    snapshot_name = disk_name + "-snapshot-1"
    snapshot = compute_v1.Snapshot()
    snapshot.name = snapshot_name
    operation = compute_disks_client.create_snapshot(project=project, zone=zone, disk=disk_name, snapshot_resource=snapshot)
    return waitForZoneOperation(project, zone, operation.name)

# Main function
def delete_unattached_pds(disk_names_with_zones):
    for diskName, diskZone in disk_names_with_zones.items():
        print(diskName)
        print(diskZone)

        # Create a snapshot before deleting
        print(f"Creating snapshot for {diskName}")
        if createSnapshot(project, diskZone, diskName):
            print(f"Snapshot created successfully for {diskName}")

            # Proceed to delete the disk
            print(f"Deleting disk {diskName}")
            operation = compute_disks_client.delete(project=project, zone=diskZone, disk=diskName)
            if waitForZoneOperation(project, diskZone, operation.name):
                print(f"Disk {diskName} was deleted")
        else:
            print(f"Snapshot creation failed for {diskName}")

    return "Disk deletion completed"

# Example usage
if __name__ == "__main__":
    input_string = input("Enter disk names and zones (format 'diskName1:zone1,diskName2:zone2,...'): ")
    disk_names_with_zones = {item.split(":")[0]: item.split(":")[1] for item in input_string.split(",")}
    print(delete_unattached_pds(disk_names_with_zones))