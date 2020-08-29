echo $ACTVID
echo $ACTVCODE
echo $REGION

mkdir /tmp/ssm
sudo curl https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/debian_arm/amazon-ssm-agent.deb -o /tmp/ssm/amazon-ssm-agent.deb
sudo dpkg -i /tmp/ssm/amazon-ssm-agent.deb
sudo service amazon-ssm-agent stop
sudo amazon-ssm-agent -register -id $ACTVID -code $ACTVCODE -region $REGION
sudo service amazon-ssm-agent start
sudo systemctl enable amazon-ssm-agent
sudo service amazon-ssm-agent status