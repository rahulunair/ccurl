#!/usr/bin/env bash
echo "Refreshes 'auth_token' in ccurl.conf by requesting a new token from openstack"
sed -i -E "s/^auth_token.*$/$(openstack token issue  | awk 'NR==5 {print "auth_token="$4}')/g" ccurl.conf
