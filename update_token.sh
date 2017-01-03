#!/usr/bin/env bash
sed -i -E "s/^auth_token.*$/$(openstack token issue  | awk 'NR==5 {print "auth_token="$4}')/g" ccurl.conf
