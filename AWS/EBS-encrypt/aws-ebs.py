#!/home/abndev/aws/awsenv/bin/python
# /usr/bin/python3
#
# dir for this file is : /home/abndev/aws/
# 
# This file makes encrypting attached EC2 `instance-id`
# 


import boto3
import sys
from time import sleep
from datetime import datetime, timezone, timedelta

if len(sys.argv) != 2:
    print("Usage: aws-ebs.py <instance-id>")
    sys.exit(1)

instance_id = sys.argv[1]

# Initialize EC2 client
ec2 = boto3.client('ec2')

# Step 1: Stop the EC2 instance
print(f"Stopping EC2 instance {instance_id}...")
ec2.stop_instances(InstanceIds=[instance_id])
ec2.get_waiter('instance_stopped').wait(InstanceIds=[instance_id])
print(f"EC2 instance {instance_id} is stopped.")

# Step 2: Get the list of attached EBS volumes with details
volumes_response = ec2.describe_volumes(
    Filters=[{'Name': 'attachment.instance-id', 'Values': [instance_id]}]
)

# Step 3: Create snapshots for each volume
snapshot_ids = {}
volume_details = {}

now = datetime.now(timezone.utc)
snapshot_ttl = timedelta(minutes=30)

for volume in volumes_response['Volumes']:
    volume_id = volume['VolumeId']
    device_name = volume['Attachments'][0]['Device']
    volume_type = volume['VolumeType']
    iops = volume.get('Iops')
    throughput = volume.get('Throughput')
    size = volume['Size']
    availability_zone = volume['AvailabilityZone']

    # Поиск существующего свежего snapshot
    print(f"Checking existing snapshots for volume {volume_id}...")
    snapshots = ec2.describe_snapshots(
        Filters=[
            {'Name': 'volume-id', 'Values': [volume_id]},
            {'Name': 'status', 'Values': ['completed']}
        ],
        OwnerIds=['self']
    )

    existing_snapshot_id = None
    for snapshot in snapshots['Snapshots']:
        start_time = snapshot['StartTime']
        if now - start_time <= snapshot_ttl:
            existing_snapshot_id = snapshot['SnapshotId']
            print(f"Found recent snapshot {existing_snapshot_id} for volume {volume_id}")
            break

    if existing_snapshot_id:
        snapshot_id = existing_snapshot_id
        print(f"Using existing snapshot {snapshot_id} for volume {volume_id}")
    else:

        print(f"Creating snapshot for volume {volume_id}...")
        snapshot_response = ec2.create_snapshot(
            VolumeId=volume_id,
            Description=f"Snapshot for encryption of {volume_id} ({device_name}) from instance {instance_id}"
        )
        snapshot_id = snapshot_response['SnapshotId']
        snapshot_ids[volume_id] = snapshot_id

        volume_details[volume_id] = {
            'DeviceName': device_name,
            'VolumeType': volume_type,
            'Iops': iops,
            'Throughput': throughput,
            'Size': size,
            'AvailabilityZone': availability_zone
        }

        # Add tags to snapshot for easier identification
        ec2.create_tags(
            Resources=[snapshot_id],
            Tags=[
                {'Key': 'InstanceId', 'Value': instance_id},
                {'Key': 'OriginalVolumeId', 'Value': volume_id},
                {'Key': 'DeviceName', 'Value': device_name},
                {'Key': 'flag', 'Value': 'backup_250407'}
            ]
        )
        print(f"Snapshot created and tagged: {snapshot_id}")

    # Snapshot is Ready for using?
    waiter = ec2.get_waiter('snapshot_completed')
    waiter.config.max_attempts = 120  # Increase max attempts ~ 30 minutes
    waiter.config.delay = 15  # Set polling interval

    print(f"Waiting for snapshot {snapshot_id} to become 'completed' (with extended timeout)...")
    waiter.wait(SnapshotIds=[snapshot_id])
    print(f"Snapshot {snapshot_id} is now completed.")


# Step 4: Create encrypted volumes from the snapshots
new_volume_ids = {}
for volume_id, snapshot_id in snapshot_ids.items():
    details = volume_details[volume_id]
    create_params = {
        'SnapshotId': snapshot_id,
        'AvailabilityZone': details['AvailabilityZone'],
        'Encrypted': True,
        'KmsKeyId': 'alias/aws/ebs',
        'VolumeType': details['VolumeType'],
        'Size': details['Size']
    }

    volume_type = details['VolumeType']
    print(f"Volume type: {volume_type}")

    if volume_type == 'gp3':
        if details['Iops']:
            create_params['Iops'] = details['Iops']
        if details['Throughput']:
            create_params['Throughput'] = details['Throughput']

    print(f"Creating encrypted volume from snapshot {snapshot_id} with params: {create_params}...")
    new_volume_response = ec2.create_volume(**create_params)
    new_volume_id = new_volume_response['VolumeId']
    new_volume_ids[volume_id] = new_volume_id

    print(f"Encrypted volume created: {new_volume_id}")

# Step 4.5: Detach old volumes from the instance
for volume_id, details in volume_details.items():
    device_name = details['DeviceName']
    print(f"Detaching old volume {volume_id} from instance {instance_id} (device {device_name})...")
    ec2.detach_volume(
        VolumeId=volume_id,
        InstanceId=instance_id,
        Device=device_name,
        Force=True
    )
    print(f"Waiting for volume {volume_id} to become 'available'...")
    ec2.get_waiter('volume_available').wait(VolumeIds=[volume_id])
    print(f"Old volume {volume_id} is now detached and available.")

# Step 5: Attach the new encrypted volumes to the EC2 instance with the same device names
for old_volume_id, new_volume_id in new_volume_ids.items():
    device_name = volume_details[old_volume_id]['DeviceName']
    print(f"Waiting for new encrypted volume {new_volume_id} to become 'available' before attaching...")
    ec2.get_waiter('volume_available').wait(VolumeIds=[new_volume_id])
    print(f"New encrypted volume {new_volume_id} is available. Attaching to instance {instance_id} at {device_name}...")
    ec2.attach_volume(
        VolumeId=new_volume_id,
        InstanceId=instance_id,
        Device=device_name
    )
    print(f"Encrypted volume {new_volume_id} attached at {device_name}.")
    print(f"Waiting for encrypted volume {new_volume_id} to become 'in-use' after attaching...")
    ec2.get_waiter('volume_in_use').wait(VolumeIds=[new_volume_id])
    print(f"Encrypted volume {new_volume_id} is now attached and in use.")

# Step 6: Tag the old volumes to mark them as "old"
for volume_id in volume_details.keys():
    print(f"Tagging old volume {volume_id}...")
    ec2.create_tags(
        Resources=[volume_id],
        Tags=[{'Key': 'Description', 'Value': 'Old volume - to be replaced'}]
    )

# Step 7: Start the EC2 instance again
print(f"Starting EC2 instance {instance_id}...")
ec2.start_instances(InstanceIds=[instance_id])
ec2.get_waiter('instance_running').wait(InstanceIds=[instance_id])
print(f"EC2 instance {instance_id} is started with new encrypted volumes.")

