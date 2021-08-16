# attacktool

> *This is my attacktool. There are many like it, but this one is mine.*

`attacktool` is a very simple framework to save on boilerplate code when pentesting, it is based on a couple of scripts I used for my OSCP and OSWE exams. The idea here is to provide a framework with basic convenience functions that can be extended to save time in when trying to estabilish a foothold on a target system.
Let's say there is a SQL injection vulnerability that allows you to read files through UNION queries, you might want to write a module that exploits this and then run that module through the wordlist function to obtain your favorite Linux system files. Or maybe there is a convenient LFI vulnerability, it might be useful to have the attacktool readline interface and urlencoding convenience to run some commands on the remote system while you're working on getting that reverse shell up and running.
`attacktool` aims to save time and not get in the way of the user, once you select a tool all input is sent to that tool and interacting with `attacktool` itself is done using `.` commands.

## Functionality

- Load project settings from json config file
- Batch run tools with wordlists as input
- Global variables to keep session information and reuse between modules
- Switching between loaded tools

## Sample session

Demonstrating the supplied sample.json config file and a wordlist

```
$ echo "a" > a
$ echo "b" > b
$ echo -e "a\nb" > files
$ ./attacktool.py --config sample.json --tool read_file
(read_file)$ .w files
a

b

```