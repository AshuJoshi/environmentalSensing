#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Script for automation of AWS IoT

"""
import os
import sys
import json
import boto3
import click
from pprint import pprint
from os import environ
import glob

session = None
iot = None

@click.group()
@click.option('--region', default=None,
              help='Use a given AWS region.')

def cli(region):
    """Commands for IoT automation."""
    global session, iot

    if environ.get('AWS_ACCESS_KEY_ID') is None or environ.get('AWS_SECRET_ACCESS_KEY') is None:
        print('Please specify AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY') 
        sys.exit()

    session = boto3.Session(
        aws_access_key_id = environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key = environ['AWS_SECRET_ACCESS_KEY'],
        region_name = region
    )
    # print(session)
    iot = session.client('iot')

@cli.command('create-and-setup-thing')
@click.argument('thing-name')
def create_and_setup_thing(thing_name):
    """Create a Thing, and set it up."""
    # print(session)
    # print(session.region_name)

    THING_EXISTS = False

    try:
        response = iot.describe_thing(
            thingName=thing_name
        )
        print('Thing with name: {} exists in this region {}. Pick another name or region. Exiting program.'.format(thing_name, session.region_name))
        THING_EXISTS = True
        # sys.exit()
    
    except:
        print()
        # print('An exception happened - {} thing name not found'.format(thing_name))

    if THING_EXISTS:
        sys.exit()

    print('Creating a Thing with the name: {}'.format(thing_name))
    print('First create keys and certificate..')
    keys_cert = iot.create_keys_and_certificate(setAsActive=True)

    print('Created, copying to the keys subdirectory')
    with open('./keys/' + thing_name + '-certifcate.pem', 'w') as key_file:
        key_file.write(keys_cert['certificatePem'])

    with open('./keys/' + thing_name + '-private.key', 'w') as key_file:
        key_file.write(keys_cert['keyPair']['PrivateKey'])

    with open('./keys/' + thing_name + '-public.key', 'w') as key_file:
        key_file.write(keys_cert['keyPair']['PublicKey'])

    iot_thing = iot.create_thing(thingName=thing_name)

    iot.attach_thing_principal(
        thingName=iot_thing['thingName'],
        principal=keys_cert['certificateArn'])

    policy_doc = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["iot:Publish", "iot:Subscribe", "iot:Connect", "iot:Receive", "iot:GetThingShadow", "iot:DeleteThingShadow", "iot:UpdateThingShadow"],
                "Resource": ["arn:aws:iot:" + session.region_name + ":*:*"]
            }
        ]
    }

    policyNameString = thing_name + '_Thing_Policy'

    policy = iot.create_policy(
        policyName=policyNameString,
        policyDocument=json.dumps(policy_doc))

    iot.attach_principal_policy(
        policyName=policy['policyName'],
        principal=keys_cert['certificateArn'])


@cli.command('delete-and-cleanup-thing')
@click.argument('thing-name')
# @click.option('thing-type')
def delete_and_cleanup_thing(thing_name):
    """Deletes a thing, and associated policy, certificates."""

    THING_EXISTS = False

    try:
        response = iot.describe_thing(
            thingName=thing_name
        )
        print('Thing with name: {} exists in this region {}.'.format(thing_name, session.region_name))
        THING_EXISTS = True
        # sys.exit()
    
    except:
        print()
        # print('An exception happened - {} thing name not found'.format(thing_name))


    if not THING_EXISTS:
        print('Thing does not exist, exiting program')
        sys.exit()

    print('Getting read to delete & cleanup... ')
    print()
    print('Thing:      ' + response['thingName'])
    print('Thing ID:   ' + response['thingId'])
    print('Thing ARN:   ' + response['thingId'])

    response = iot.list_thing_principals(
        thingName = thing_name
    )

    for prnc in response['principals']:
        print(prnc)
        args = {}
        args['target'] = prnc
        while True:
            pols = iot.list_attached_policies(**args)
            for pol in pols['policies']:
                print('----------------------------------------------')
                pprint(pol)
                polName = pol['policyName']
                # target = prnc
                tmpargs = {}
                tmpargs['policyName'] = polName
                tmpargs['target'] = prnc
                result = iot.detach_policy(**tmpargs)
                tmpargs = {}
                tmpargs['policyName'] = polName
                result = iot.delete_policy(**tmpargs)

            if 'nextMarker' in pols:
                args = pols['nextMarker']
            else:
                break

        # Detach the certificate from the thing, and delete
        args = {}
        args['principal'] = prnc
        args['thingName'] = thing_name
        print(args)
        result = iot.detach_thing_principal(**args)
        print('Deleting the certificate... ')
        # No easy way of getting certificateId from above...
        args = {}
        while True:
            certs = iot.list_certificates(**args)
            for cert in certs['certificates']:
                # print('----------------------------------------------')
                # pprint(cert)
                if cert['certificateArn'] == prnc:
                    print(prnc)
                    print('Certificate ARN: ', cert['certificateArn'])
                    print('Certificate ID: ', cert['certificateId'])
                    ags = {}
                    ags['certificateId'] = cert['certificateId']
                    ags['newStatus'] = 'INACTIVE'
                    response = iot.update_certificate(**ags)
                    ags = {}
                    ags['certificateId'] = cert['certificateId']
                    ags['forceDelete'] = True
                    response = iot.delete_certificate(**ags)

            if 'nextMarker' in certs:
                args = certs['nextMarker']
            else:
                break


    
    # Delete the thing now
    args = {}
    args['thingName'] = thing_name
    result = iot.delete_thing(**args)
    # Now delete files in the keys directory
    fileremovalstring = './keys/' + thing_name + '-' + '*'
    print(fileremovalstring)
    for f in glob.glob(fileremovalstring):
        os.remove(f)



        # print()
        # print('Number of Policies: ', len(pols['policies']))



@cli.command('list-things')
def list_things():
    """List IoT Things."""
    args = {}
    while True:
        things = iot.list_things(**args)
        for thing in things['things']:
            print('----------------------------------------------')
            pprint(thing)

        if 'NextToken' in things:
            args = things['NextToken']
        else:
            break

    print()
    print('Number of Things: ', len(things['things']))


@cli.command('list-certificates')
def list_certificates():
    """List Certificates"""
    args = {}
    while True:
        certs = iot.list_certificates(**args)
        for cert in certs['certificates']:
            print('----------------------------------------------')
            pprint(cert)

        if 'nextMarker' in certs:
            args = certs['nextMarker']
        else:
            break

    print()
    print('Number of Certs: ', len(certs['certificates']))


@cli.command('list-policies')
def list_policies():
    """List Policies"""
    args = {}
    while True:
        pols = iot.list_policies(**args)
        for pol in pols['policies']:
            print('----------------------------------------------')
            pprint(pol)

        if 'nextMarker' in pols:
            args = pols['nextMarker']
        else:
            break

    print()
    print('Number of Policies: ', len(pols['policies']))



@cli.command('list-attached-policies', help='Certificate ARN for which you want to find attached policies')
@click.argument('targetarn')
def list_attached_policies(targetarn):
    """List Attached Policies"""
    args = {}
    args['target'] = targetarn
    # args['recursive'] = False
    print(args)

    response = iot.list_attached_policies(**args)
    # print(response)
    while True:
        pols = iot.list_attached_policies(**args)
        for pol in pols['policies']:
            print('----------------------------------------------')
            pprint(pol)

        if 'nextMarker' in pols:
            args = pols['nextMarker']
        else:
            break

    print()
    print('Number of Policies: ', len(pols['policies']))


if __name__ == '__main__':
    cli()
