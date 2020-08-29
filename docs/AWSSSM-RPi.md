# Install AWS SSM Agent on Raspberry Pi for SSH Access

AWS [Systems Management (SSM) Agent](https://docs.aws.amazon.com/systems-manager/latest/userguide/ssm-agent.html) enables you to remotely monitor, update, configure, and SSH into a machine from anywhere, without needing to know it's IP address.  Very handy when using Raspberry Pi's across networks.

## DESKTOP: One time only, install the SSM Session Manager

This only needs to be done once on this desktop.

```bash
curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/mac/sessionmanager-bundle.zip" -o "sessionmanager-bundle.zip"
unzip sessionmanager-bundle.zip
sudo ./sessionmanager-bundle/install -i /usr/local/sessionmanagerplugin -b /usr/local/bin/session-manager-plugin
```

## DESKTOP: Create an activation

Replacing '[COMPUTER_NAME_HERE]' with the name you want to give the Raspberry Pi.  This is what you'll see in the AWS [SSM Console](https://us-west-2.console.aws.amazon.com/systems-manager/managed-instances?region=us-west-2#)
Note that the IAM Role 'SSMServiceRole' must have been created granting the right permissions. You follow the [steps here](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-service-role.html) on how to create the role.

```bash
# run this one line
aws ssm create-activation --default-instance-name [COMPUTER_NAME_HERE] --iam-role SSMServiceRole --registration-limit 4 --region us-west-2

# example output
{
    "ActivationId": "daa1bda7-e552-41c2-ba6e-40703c45xxxx",
    "ActivationCode": "7gT3oks2jNCCbZZOxxxx"
}
```

You can replace the region - with the appropriate region. If you wanted to use a different AWS Profile - then provide the --profile option in the command.

## Raspberry Pi: Install SSM Agent

Run these commands on the RPi.  
Replace the 'id' and 'code' fields with values returned from previous step's command.

```bash
mkdir /tmp/ssm
sudo curl https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/debian_arm/amazon-ssm-agent.deb -o /tmp/ssm/amazon-ssm-agent.deb
sudo dpkg -i /tmp/ssm/amazon-ssm-agent.deb
sudo service amazon-ssm-agent stop
sudo amazon-ssm-agent -register -id "daa1bda7-e552-41c2-ba6e-40703c45xxxx" -code "7gT3oks2jNCCbZZOxxxx" -region "us-west-2"
sudo service amazon-ssm-agent start
sudo systemctl enable amazon-ssm-agent
sudo service amazon-ssm-agent status
```

You can use the script [setupSSM-RPi.sh](./setupSSM-RPi.sh) to set the SSM agent.

## Raspberry Pi: Get instance-id

From the `sudo amazon-ssm-agent -register ...` line already run above, look for something like  
`2020-02-13 00:22:52 INFO Successfully registered the instance with AWS SSM using Managed instance-id: mi-042b51b7a2e68xxxx`  
And save that instance-id `mi-042b51b7a2e68xxxx` name.  You'll need to keep that handy.

## DESKTOP: Update ssh config

One time only. Edit your `~/.ssh/config` file and add these lines to the end:

```bash
# SSH over Session Manager
host i-* mi-*
  ProxyCommand sh -c "aws ssm start-session --target %h --document-name AWS-StartSSHSession --parameters 'portNumber=%p'"
```

## DESKTOP: Remote into new host

Replace `mi-042b51b7a2e68xxxx` with your device's instance-id:

```bash
ssh pi@mi-042b51b7a2e68xxxx
```

View your list of instances on the AWS Console at:  

https://us-west-2.console.aws.amazon.com/systems-manager/managed-instances?region=us-west-2#

You should replace the region with the appropriate one where you have setup the SSM agent.

That's it!  You should be able to SSH now into this host as long as it has network connectivitiy.

## Pro Tips

* Run `touch .hushlogin` on the RPi to quiet the login message.
* Run `ssh-copy-id pi@mi-042b51b7a2e68xxxx` on your desktop to enable you to remote in from this desktop without requiring a password.

* Get the instance IDs of your registered agents from:

```bash
brew install jq
aws ssm describe-instance-information | jq '.InstanceInformationList[] | [.Name,.InstanceId]'
```

* Give your host a friendly name in `~/.ssh/config` by adding lines to the end such as these.  Then you can SSH in with just `ssh mypi`.

```bash
host mypi
  user pi
  ProxyCommand sh -c "aws ssm start-session --target mi-042b51b7a2e68xxxx --document-name AWS-StartSSHSession --parameters 'portNumber=%p'"
```
