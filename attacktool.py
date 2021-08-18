#!/usr/bin/env python3

import attacktool
import json
import argparse
import readline
import sys
import os

def write_text(line, **kwargs):
    print(line)

def execute_cmd(command, **kwargs):
    print(os.system(command))

def read_file(filename, **kwargs):
    try:
        with open(filename) as file:
            print(file.read())
    except:
        print("Could not read %s" % Filename)

# Set/get global variables to preserve sessions etc
variables = {}
def set_global(name, value):
    attacktool.variables[name] = value

def get_global(name, default_value=''):
    if name in attacktool.variables:
        return attacktool.variables[name]
    return default_value

# Mirror remote files relative to cwd
def write_file_cwd_recursive(remote_filename, content):
    path = "%s%s" % (os.getcwd(), os.path.dirname(remote_filename))
    filename = "%s%s" % (os.getcwd(), remote_filename)
    print("Making %s" % path)
    print("Writing %s" % filename)
    os.makedirs(path, exist_ok=True)
    with open(filename, 'w') as local_file:
        local_file.write(content)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True, help='Config file')
    parser.add_argument('--tool', help='Tool')
    parser.add_argument('--command', help='Command')
    args = parser.parse_args()

    tools = {}
    settings = { 'tools': []}
    with open(args.config, 'r') as jsonfile:
        settings = json.load(jsonfile)

    # Add config file to path to load local modules
    config_path = os.path.dirname(args.config)
    if not config_path in sys.path:
        sys.path.append(config_path)

    # Load tools from settings
    for tool in settings['tools']:
        # If a tool is in another directory add that to path
        if 'path' in tool:
            if not tool['path'] in sys.path:
                sys.path.append(tool['path'])
        package = __import__(tool['package'])
        tools[tool['name']] = {
            'name': tool['name'],
            'function': getattr(package, tool['function']),
            'parameters': tool['parameters']
        }
        # Run tool init if available (setup sessions etc)
        if 'init' in tool:
            getattr(package, tool['init'])(**tool['parameters'])

    # Set default tool if specified
    current_tool = ''
    if args.tool:
        current_tool = args.tool

    # Command loop
    while True:
        line = input("(%s)$ " % current_tool)
        command = line.split(' ')[0]
        if command in ['.q', '.quit']:
            sys.exit(0)
        elif command in ['.v', '.variables']:
            print(attacktool.variables)
        elif command in ['.w', '.wordlist']:
            with open(line.split(' ')[1], 'r') as file:
                for line in file:
                    tools[current_tool]['function'](line.strip(), **tools[current_tool]['parameters'])
        elif command in ['.t', '.tool']:
            tool = line.split(' ')[1]
            if tool in tools:
                current_tool = tool
                print("Switched tool %s" % tool)
        elif not "" == current_tool:
            tools[current_tool]['function'](line, **tools[current_tool]['parameters'])
        else:
            print("'%s' is not supported" % line)