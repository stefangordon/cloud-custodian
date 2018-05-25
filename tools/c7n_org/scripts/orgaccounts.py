# Copyright 2018 Capital One Services, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import boto3
import click
import yaml

ROLE_TEMPLATE = "arn:aws:iam::{Id}:role/OrganizationAccountAccessRole"


@click.command()
@click.option(
    '--role',
    default=ROLE_TEMPLATE,
    help="Role template for accounts in the config, defaults to %s" % ROLE_TEMPLATE)
@click.option('--ou', multiple=True, default=["/"],
              help="Only export the given subtrees of an organization")
@click.option('-r', '--region', multiple=True,
              help="If specified, set regions per account in config")
@click.option('--assume', help="Role to assume for Credentials")
@click.option('--profile', help="AWS CLI Profile to use for Credentials")
@click.option(
    '-f', '--output', type=click.File('w'),
    help="File to store the generated config (default stdout)")
def main(role, ou, assume, profile, output, region):
    """Generate a c7n-org accounts config file using AWS Organizations

    With c7n-org you can then run policies or arbitrary scripts across
    accounts.
    """

    client = boto3.client('organizations')
    accounts = []
    for path in ou:
        ou = get_ou_from_path(client, path)
        accounts.extend(get_accounts_for_ou(client, ou))

    results = []
    for a in accounts:
        tags = []
        path_parts = a['Path'].strip('/').split('/')
        for idx, _ in enumerate(path_parts):
            tags.append("path:/%s" % "/".join(path_parts[:idx + 1]))

        ainfo = {
            'account_id': a['Id'],
            'email': a['Email'],
            'name': a['Name'],
            'tags': tags,
            'role': role.format(**a)}
        if region:
            ainfo['regions'] = region
        results.append(ainfo)

    print(
        yaml.safe_dump(
            {'accounts': results},
            default_flow_style=False),
        file=output)


def get_ou_from_path(client, path):
    ou = client.list_roots()['Roots'][0]

    if path == "/":
        ou['Path'] = path
        return ou

    ou_pager = client.get_paginator('list_organizational_units_for_parent')
    for part in path.strip('/').split('/'):
        found = False
        for page in ou_pager.paginate(ParentId=ou['Id']):
            for child in page.get('OrganizationalUnits'):
                if child['Name'] == part:
                    found = True
                    ou = child
                    break
            if found:
                break
        if found is False:
            raise ValueError(
                "No OU named:%r found in path: %s" % (
                    path, path))
    ou['Path'] = path
    return ou


def get_sub_ous(client, ou):
    results = [ou]
    ou_pager = client.get_paginator('list_organizational_units_for_parent')
    for sub_ou in ou_pager.paginate(
            ParentId=ou['Id']).build_full_result().get(
                'OrganizationalUnits'):
        sub_ou['Path'] = "/%s/%s" % (ou['Path'].strip('/'), sub_ou['Name'])
        results.extend(get_sub_ous(client, sub_ou))
    return results


def get_accounts_for_ou(client, ou, recursive=True):
    results = []
    ous = [ou]
    if recursive:
        ous = get_sub_ous(client, ou)

    account_pager = client.get_paginator('list_accounts_for_parent')
    for ou in ous:
        for a in account_pager.paginate(
            ParentId=ou['Id']).build_full_result().get(
                'Accounts', []):
            a['Path'] = ou['Path']
            results.append(a)

    return results


if __name__ == '__main__':
    main()
