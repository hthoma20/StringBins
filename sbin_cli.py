#!/usr/bin/env python3

# CLI client for stringbins.harryanddaylin.com

import argparse
import requests

HOST = 'http://localhost'
PORT = '5867'
BASE_URL = '{}:{}'.format(HOST, PORT)

CLI_DESCRIPTION = 'Store named strings'

CREATE_METHOD = 'create'
RETRIEVE_METHOD = 'retrieve'
UPDATE_METHOD = 'update'

METHOD_HELP = 'whether to create, retrieve, or update the given bin'
NAME_HELP = 'the name of the bin'
UUID_HELP = 'flag to append a UUID to the name when creating a new bin'
CONTENT_HELP = 'specify the string to store'

UUID_IGNORED_MESSAGE = 'uuid flag ignored because method is not create'
CONTENT_MISSING_MESSAGE = 'no content provided. Specify with -c or --content'
UNRECOGNIZED_METHOD_MESSAGE = 'unrecognized method. this indicates an issue with this CLI itself'

CREATE_ERROR_MESSAGE = 'Failed to create bin {bin_name}: {error_detail}'
CREATE_SUCCESS_MESSAGE = 'Created bin with name:{bin_name}'
RETRIEVE_ERROR_MESSAGE = 'Failed to retrieve bin {bin_name}: {error_detail}'
UPDATE_ERROR_MESSAGE = 'Failed to update {bin_name}: {error_detail}'
UPDATE_SUCCESS_MESSAGE = 'Updated bin {bin_name}'
CONNECTION_ERROR_MESSAGE = 'Connection error'
UNEXPECTED_ERROR_MESSAGE = 'There was an unexpected error'


def create_arg_parser():
    parser = argparse.ArgumentParser(description=CLI_DESCRIPTION)

    parser.add_argument('method', choices=[CREATE_METHOD, RETRIEVE_METHOD, UPDATE_METHOD], help=METHOD_HELP)
    parser.add_argument('name', help=NAME_HELP)
    parser.add_argument('-u', '--uuid', action='store_true', help=UUID_HELP)
    parser.add_argument('-c', '--content', help=CONTENT_HELP)
    
    return parser

def create(name: str, uuid: bool):
    url = '{}/create'.format(BASE_URL)
    
    params = {
        'name': name,
        'uuid': uuid
    }
    
    try:
        response = requests.post(url, params=params)
    except:
        print(CONNECTION_ERROR_MESSAGE)
        exit(1)
        
    json = response.json()
    
    if response.ok:
        print(CREATE_SUCCESS_MESSAGE.format(bin_name=json['bin-name']))
        exit(0)
    
    print(CREATE_ERROR_MESSAGE.format(bin_name=name, error_detail=json['detail']))
    exit(1)

def retrieve(name: str):
    url = '{}/retrieve'.format(BASE_URL)
    
    params = {
        'name': name
    }
    
    try:
        response = requests.get(url, params=params)
    except:
        print(CONNECTION_ERROR_MESSAGE)
        exit(1)
    
    if response.ok:
        print(response.json())
        exit(0)
    
    print(RETRIEVE_ERROR_MESSAGE.format(bin_name=name, error_detail=response.json()['detail']))
    exit(1)

def update(name: str, content: str):
    print('update {} {}'.format(name, content))
    
    url = '{}/update'.format(BASE_URL)
    
    params = {
        'name': name
    }
    
    body = {
        'content': content
    }
    
    try:
        response = requests.put(url, params=params, json=body)
    except:
        print(CONNECTION_ERROR_MESSAGE)
        exit(1)
    
    if response.ok:
        print(UPDATE_SUCCESS_MESSAGE.format(bin_name=name))
        exit(0)
    
    print(UPDATE_ERROR_MESSAGE.format(bin_name=name, error_detail=response.json()['detail']))
    exit(1)
    
def run_cli(args):
    
    if args.method == CREATE_METHOD:
        create(args.name, args.uuid)
        exit(0)
    
    if args.uuid:
        print(UUID_IGNORED_MESSAGE)
    
    if args.method == RETRIEVE_METHOD:
        retrieve(args.name)
        exit(0)
    
    if args.method == UPDATE_METHOD:
        if args.content == None:
            print(CONTENT_MISSING_MESSAGE)
            exit(1)
        
        update(args.name, args.content)
        exit(0)
    
    print(UNRECOGNIZED_METHOD_MESSAGE)
    exit(1)
    
    
if __name__ == '__main__':
    parser = create_arg_parser()
    args = parser.parse_args()
    
    try:
        run_cli(args)
    except Exception as e:
        print(UNEXPECTED_ERROR_MESSAGE)
        print(e)
        exit(1)