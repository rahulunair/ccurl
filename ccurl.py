#!/usr/bin/env python

"""A simple wrapper for request"""
import requests
import argparse
import ConfigParser
import urlparse


def get_config_opts():
    """Get config options from command line"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--config_file", help="specify a config file", metavar="FILE")
    args, remaining_argv = parser.parse_known_args()
    if args.config_file:
        config = ConfigParser.SafeConfigParser()
        config.read([args.config_file])
        defaults = dict(config.items("Defaults"))

    parser.set_defaults(**defaults)
    parser.add_argument("--header", "-H", help="Headers")
    parser.add_argument("--base_url", "-b", help="Base url")
    parser.add_argument("--rel_url", "-r", help="Relative url")
    parser.add_argument("--debug", "-d", help="Show the entire request")
    parser.add_argument("--method", "-M", help="Request method, default: GET")
    parser.add_argument("--content_type", "-C", help="Content type")
    parser.add_argument("--accept_type", "-A", help="Acceptable content type")
    parser.add_argument("--payload", "-p", help="payload to be sent")
    parser.add_argument("--auth_token", "-t", help="Auth token")
    args = parser.parse_args(remaining_argv)
    if args.debug:
        print("\n{}\n".format(args))
    return args


def ccurl():
    args = get_config_opts()
    url = urlparse.urljoin(args.base_url, args.rel_url)
    headers = {
        "content-type": args.content_type,
        "accept": args.accept_type,
        "X-Auth-Token": args.auth_token
    }
    if args.method == 'POST':
        r = requests.post(url, json=args.payload, headers=headers)
    elif args.method == 'PUT':
        r = requests.post(url, json=args.payload, headers=headers)
    elif args.method == 'HEAD':
        r = requests.post(url, headers=headers)
    elif args.method == 'OPTIONS':
        r = requests.post(url, headers=headers)
    else:
        r = requests.get(url, headers=headers)
    try:
        response = r.json()
    except:
        response = r.text()
    return response


if __name__ == '__main__':
    print(ccurl())
