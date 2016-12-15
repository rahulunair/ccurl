#!/usr/bin/env python
"""A simple wrapper for request"""
import argparse
import ConfigParser
import os
import requests
import urlparse


def get_config_opts():
    """Get config options from command line"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--config_file", help="specify a config file", metavar="FILE")
    args, remaining_argv = parser.parse_known_args()
    if os.path.isfile("ccurl.conf"):
        args.config_file = "ccurl.conf"
    if args.config_file:
        config = ConfigParser.SafeConfigParser()
        config.read([args.config_file])
        defaults = dict(config.items("Defaults"))
        parser.set_defaults(**defaults)
    parser.add_argument("--header", "-H", help="Headers")
    parser.add_argument("--base_url", "-b", help="Base url")
    parser.add_argument("--rel_url", "-r", help="Relative url")
    parser.add_argument("--debug", "-D", help="Show the entire request")
    parser.add_argument("--method", "-X", help="Request method, default: GET")
    parser.add_argument("--content_type", "-C", help="Content type")
    parser.add_argument("--accept_type", "-A", help="Acceptable content type")
    parser.add_argument("--content_length", "-l", help="Content length")
    parser.add_argument("--payload", "-d", help="payload to be sent")
    parser.add_argument("--auth_token", "-t", help="Auth token")
    parser.add_argument("--file", "-f", help="Binary file to be uploaded")
    args = parser.parse_args(remaining_argv)
    if args.debug:
        print("\n{}\n".format(args))
    return args


def ccurl():
    args = get_config_opts()
    url = urlparse.urljoin(args.base_url, args.rel_url)
    if url is None:
        print("No URL provided, exiting...")
        exit(1)
    if args.payload:
        # Eval to evaluate python expressions to create fuzz_data
        # This is dangerous, so use it with known scipts
        if args.payload.strip().startswith('eval:'):
            args.payload = eval(args.payload[5:])
        # warning !! >> Nuclear <<
        elif args.payload.strip()[-3:] == ".py":
            args._payload = eval(open(args.payload))
    headers = {
        "content-type": args.content_type,
        "accept": args.accept_type,
        "X-Auth-Token": args.auth_token,
        "Content-Length": args.content_length
    }
    if args.header:
        headers.update(args.header)
    if args.method == 'POST':
        if args.file:
            r = requests.post(
                url, files={"file": open(args.file, "rb")}, headers=headers)
        elif args.payload:
            try:
                r = requests.post(url, data=args.payload, headers=headers)
            except Exception:
                r = requests.post(url, json=args.payload, headers=headers)
        else:
            r = requests.post(url, headers=headers)
    elif args.method == 'PUT':
        if args.payload:
            try:
                r = requests.put(url, data=args.payload, headers=headers)
            except Exception:
                r = requests.put(url, json=args.payload, headers=headers)
        else:
            r = requests.put(url, headers=headers)
    elif args.method == 'HEAD':
        print("url and headers are : {0} and {1}".format(url, headers))
        r = requests.head(url, headers=headers)
    elif args.method == 'OPTIONS':
        r = requests.options(url, headers=headers)
    else:
        r = requests.get(url, headers=headers)
    try:
        response = r.text
    except Exception:
        response = r.content
    if not response:
        # if the reponse is empty, return the headers
        # This, is used to see response for HEAD requests
        response = r.headers
    return response


if __name__ == '__main__':
    print(ccurl())
