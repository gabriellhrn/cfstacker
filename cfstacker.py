
import sys
import os
import argparse
import yaml
import boto3

PROG = sys.argv[0]
VERSION = 0.1

# functions
def parse_args():
    parser = argparse.ArgumentParser(prog=PROG,
            description='Manages CloudFormation template files (YAML or JSON) stored at "templates/"')

    parser.add_argument('-V', '--version', action='version', version='%s version %s' % (PROG, VERSION))

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-b', '--boilerplate', action='store_true',
            help='generate boilerplate for TEMPLATE')
    group.add_argument('-c', '--create', action='store_true',
            help='create an ecs stack based on TEMPLATE')
    group.add_argument('-d', '--delete', action='store_true',
            help='delete TEMPLATE\'s stack')
    group.add_argument('-u', '--update', action='store_true',
            help='update TEMPLATE\'s stack')

    parser.add_argument('template', metavar='TEMPLATE', type=str,
            help='name of a CloudFormation file (YAML or JSON) to be managed')
    parser.add_argument('parameters', metavar='PARAMETERS', type=str, nargs='?',
            help='name of a json file containing parameters to be used in TEMPLATE (optional)')

    return parser.parse_args()

def boilerplate(template_name, parameters_name):
    print 'creating boilerplate for "%s" ...' % template_name

    template_dir = 'templates/%s' % template_name
    template_file = '%s/%s.yaml' % (template_dir, template_name)

    if not os.path.exists(template_dir):
        os.makedirs(template_dir)

    template = {
        'AWSTemplateFormatVersion': '2010-09-09',
        'Description': 'CloudFormation template "%s" generated by %s' % (template_name, PROG),
        'Parameters': {},
        'Mappings': {},
        'Resources': {
            'AnEc2Instance': {
                'Type': 'AWS::EC2::Instance',
                'Properties': {
                    'ImageId': 'ami-12ab34cd',
                    'KeyName': 'somekey',
                    'BlockDeviceMappings': {
                        'DeviceName': '/dev/xvda',
                        'Ebs': {
                            'VolumeType': 'gp2',
                            'VolumeSize': '8',
                            'DeleteOnTermination': True
                        }
                    }
                }
            }
        },
        'Outputs': {}
    }

    with open(template_file, 'w') as tplf:
        yaml.dump(template, tplf, default_flow_style=False)

    print 'template created at %s' % template_file

    return True

def create(template_name, parameters_name):
    template_dir = 'templates/%s' % template_name
    template_file = '%s/%s.yaml' % (template_dir, template_name)

    client = boto3.client('cloudformation')
    client.create_stack(StackName=template_name, TemplateBody=template_file)

    return True

def delete(template_name, parameters_name):
    client = boto3.client('cloudformation')
    client.delete_stack(StackName=template_name)

    return True

def update(template_name, parameters_name):
    template_dir = 'templates/%s' % template_name
    template_file = '%s/%s.yaml' % (template_dir, template_name)

    client = boto3.client('cloudformation')
    client.update_stack(StackName=template_name, TemplateBody=template_file)

    return True

# main
def main():
    args = parse_args()

    if args.boilerplate:
        boilerplate(args.template, args.parameters)
    elif args.create:
        create(args.template, args.parameters)
    elif args.delete:
        delete(args.template, args.parameters)
    elif args.update:
        update(args.template, args.parameters)


if __name__ == "__main__":
    main()

