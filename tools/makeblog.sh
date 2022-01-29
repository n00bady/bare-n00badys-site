#!/bin/bash

rm ../site/blog/*

python3 ./spsg.py template.html index_template.html && mv ./blog/* ../site/blog/ || echo "Something gone wrong !!!"

rm -rf ./blog