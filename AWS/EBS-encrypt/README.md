# AWS DevOps

This script converts EBS not-encrypted to EBS-encrypted: 
- Stop the EC2 instance.
- Find EC2 instance given in arguments of the script. 
- Load all EBS in this instance.
- Find snapshots for given EC2 instance with a creation time leass 30minutes and use it OR
    - Make a snapshot of EBS, then detach it from EC2-instance. 
- Create a new Encrypted EBS with the same options (return drive back at the instance)
- Start EC2 instance.

## Check out before starting

1. A path to the python - in the beging of the script.
2. `aws configure` your credentials - make sure you have enougth access to perform each command (EC2, EBS, etc) 
  
