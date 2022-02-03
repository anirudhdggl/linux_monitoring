#!/bin/bash
# Send TCP dumps to S3

die() { status=$1; shift; echo "FATAL: $*"; exit $status; }

# Ensure that apparmor does not block tcpdump
sudo apparmor_parser -R /etc/apparmor.d/usr.sbin.tcpdump

# Replace with actual bucket name
BUCKET_NAME="tag-storage/tcpdump/stage";

# Get instance id for imdsv1
#INSTANCE_ID="`wget -q -O - http://169.254.169.254/latest/meta-data/instance-id || die \"wget instance-id has failed: $?\"`"

# Get instance ID for imdsv2
TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" || die \"wget instance-id has failed: $?\"`
INSTANCE_ID=`curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id || die \"wget instance-id has failed: $?\"`

# Init temp file
touch temp.pcap

while true :
do
  # Capture 5k packets
  sudo tcpdump -i ens5 -w temp.pcap -c 5000 port 80

  # Build filename
  YEAR=$(date +%Y);
  MONTH=$(date +%m);
  DAY=$(date +%d);
  HOUR=$(date +%H);
  MINUTE=$(date +%M);
  S3_KEY="s3://${BUCKET_NAME}/${INSTANCE_ID}/${YEAR}/${MONTH}/${DAY}/${HOUR}:${MINUTE}-${INSTANCE_ID}.pcap";
  # Upload file to bucket with date
  echo "Writing temp.pcap to ${S3_KEY}"
  aws s3 cp --quiet temp.pcap $S3_KEY
  # Clear temp pcap
  rm -f temp.pcap
done