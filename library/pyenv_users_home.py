#!/usr/bin/python
# Copyright (c) 2018 Julio Lajara
# GNU General Public License v2.0 (see COPYING or https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['stableinterface'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---

author: Julio Lajara (@ju2wheels)
description:
  - Retrieves the C(HOME) path for the specified users.
module: pyenv_users_home
options:
  users:
    default: []
    description: The users for which to retrieve the C(HOME) path. Defaults to current user.
    required: false
    type: list of str
short_description: Retrieves the C(HOME) path for the specified users.
requirements:
  - gentent (Linux)
  - dscl (MacOSX)
version_added: "2.4"
'''

EXAMPLES = '''
---

- name: Retrieve HOME path for current user
  pyenv_users_home:

- name: Retrieve HOME path for specific users
  pyenv_users_home:
    users:
      - user1
      - user2
'''

RETURN = '''
pyenv_users_home:
    contains:
      user_name:
        description: The C(HOME) path for an individual user.
        returned: always
        sample: "/home/user1"
        type: str
    description: The C(HOME) path for the specified users.
    returned: success
    sample: {"user1": "/home/user1", "user2": "/home/user2"}
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.facts.namespace import PrefixFactNamespace
from ansible.module_utils.facts import ansible_collector, default_collectors

def user_home(facts, module, user):
    """
    Returns the `HOME` path for user using platform specific commands.

    :kw facts: Ansible facts dict.
    :kw module: An AnsibleModule instance.
    :kw user: User name to retrieve `HOME` path for.
    :returns: The `HOME` path for user.
    """

    cli_command = {
        'Linux': ('getent', ['passwd', user]),
    }
    patterns = [
        '_'.join([facts['ansible_distribution'], facts['ansible_distribution_version'],
                  facts['ansible_distribution_release']]),
        '_'.join([facts['ansible_distribution'], facts['ansible_distribution_version']]),
        '_'.join([facts['ansible_distribution'], facts['ansible_distribution_major_version']]),
        facts['ansible_distribution'],
        facts['ansible_os_family'],
        facts['ansible_system']
    ]

    matches = [cli_command.get(pattern, None) for pattern in patterns if cli_command.get(pattern, None)]

    if not matches:
        module.fail_json(msg="Unsupported OS distribution")

    command = module.get_bin_path(matches[0][0], required=True)

    result = module.run_command([command] + matches[0][1], check_rc=True)

    return result[1].split(':')[5]

def run_module():
    # module args
    module_args = dict(
        users=dict(type='list', required=False, default=[])
    )
    result = dict(
        changed=False,
        ansible_facts=dict(pyenv_users_home=dict())
    )

    # facts args
    all_collector_classes = default_collectors.collectors
    filter_spec = '*'
    gather_subset = ['distribution', 'platform', 'user']
    minimal_gather_subset = gather_subset
    namespace = PrefixFactNamespace(namespace_name='ansible', prefix='ansible_')

    # Create module and validate argument specification
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Dont actually do anything if we are in check_mode
    if module.check_mode:
        return result

    # Collect OS and user facts
    fact_collector = \
        ansible_collector.get_ansible_collector(all_collector_classes=all_collector_classes,
                                                filter_spec=filter_spec,
                                                namespace=namespace,
                                                gather_subset=gather_subset,
                                                minimal_gather_subset=minimal_gather_subset)

    facts_dict = fact_collector.collect(module=module)

    # Get our specified users or use the current user
    users = module.params['users']

    if len(users) == 0:
        users = [facts_dict['ansible_user_id'] or 'root']

    # Collect reported HOME path for users
    for user in users:
        result['ansible_facts']['pyenv_users_home'][user] = user_home(facts_dict, module, user)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
