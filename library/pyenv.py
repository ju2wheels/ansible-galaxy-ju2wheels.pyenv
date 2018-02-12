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
  - "Installs pyenv from a GIT repository."
module: pyenv
options:
  accept_hostkey:
    choices: [ "yes", "no" ]
    default: "no"
    description:
      - if C(yes), ensure that "-o StrictHostKeyChecking=no" is
        present as an ssh options. Only used when C(state=present).
    required: false
    version_added: "1.5"
  dest:
    default: ".pyenv"
    description:
      - The path of where the repository should be checked out.
    required: false
  executable:
    default: null
    description:
      - Path to git executable to use. If not supplied,
        the normal mechanism for resolving binary paths will be used.
        Only used when C(state=present).
    required: false
    version_added: "1.4"
  force:
    choices: [ "yes", "no" ]
    default: "yes"
    description:
      - If C(yes), any modified files in the working
        repository will be discarded. Only used when C(state=present).
    required: false
    version_added: "0.7"
  key_file:
    default: None
    description:
      - Specify an optional private key file to use for the checkout.
        Only used when C(state=present).
    required: false
    version_added: "1.5"
  refspec:
    default: null
    description:
      - Add an additional refspec to be fetched.
        If version is set to a I(SHA-1) not reachable from any branch
        or tag, this option may be necessary to specify the ref containing
        the I(SHA-1).
        Uses the same syntax as the 'git fetch' command.
        An example value could be "refs/meta/config".
        Only used when C(state=present).
    required: false
    version_added: "1.9"
  remote:
    default: "origin"
    description:
      - Name of the git remote. Only used when C(state=present).
    required: false
  repo:
    default: "https://github.com/yyuu/pyenv.git"
    description:
      - git, SSH, or HTTP(S) protocol address of the git repository.
        Only used when C(state=present).
    required: false
  ssh_opts:
    default: None
    description:
      - Creates a wrapper script and exports the path as GIT_SSH
        which git then automatically uses to override ssh arguments.
        An example value could be "-o StrictHostKeyChecking=no".
        Only used when C(state=present).
    required: false
    version_added: "1.5"
  state:
    choices: ["absent", "present"]
    default: present
    description: Whether to install or remove pyenv.
    required: false
  track_submodules:
    choices: ["yes", "no"]
    default: "no"
    description:
      - if C(yes), submodules will track the latest commit on their
        master branch (or other branch specified in .gitmodules).  If
        C(no), submodules will be kept at the revision specified by the
        main project. This is equivalent to specifying the --remote flag
        to git submodule update. Only used when C(state=present).
    required: false
    version_added: "1.8"
  umask:
    default: '022'
    description:
      - The umask to set before doing any checkouts, or any other
        repository maintenance. Only used when C(state=present).
    required: false
    version_added: "2.2"
  update:
    choices: [ "yes", "no" ]
    default: "yes"
    description:
      - If C(no), do not retrieve new revisions from the origin repository.
        Only used when C(state=present).
    required: false
    version_added: "1.2"
  verify_commit:
    choices: ["yes", "no"]
    default: "no"
    description:
      - if C(yes), when cloning or checking out a C(version) verify the
        signature of a GPG signed commit. This requires C(git) version>=2.1.0
        to be installed. The commit MUST be signed and the public key MUST
        be present in the GPG keyring. Only used when C(state=present).
    required: false
    version_added: "2.0"
  version:
    default: "HEAD"
    description:
      - What version of the repository to check out.  This can be the
        the literal string C(HEAD), a branch name, a tag name.
        It can also be a I(SHA-1) hash, in which case C(refspec) needs
        to be specified if the given revision is not already available.
        Only used when C(state=present).
    required: false
short_description: Installs pyenv from a GIT repository.
requirements:
  - git>=1.7.1 (the command line tool)
version_added: "2.4"
'''

EXAMPLES = '''
---

- name: Install pyenv
  pyenv:

- name: Uninstall pyenv
  pyenv:
    state: absent
'''

RETURN = '''
after:
  description: Last commit revision of the repository retrieved during the update. Returned when C(state=present).
  returned: success
  sample: 4c020102a9cd6fe908c9a4a326a38f972f63a903
  type: string
before:
  description: >
    Commit revision before the repository was updated, "null" for new repository. Returned when C(state=present).
  returned: success
  sample: 67c04ebe40a003bda0efb34eacfb93b0cafdf628
  type: string
pyenv:
  description: The destination of the pyenv install being installed or removed.
  returned: success
  sample: /home/user/.pyenv
  type: string
remote_url_changed:
  description: Contains True or False whether or not the remote URL was changed. Returned when C(state=present).
  returned: success
  sample: True
  type: boolean
warnings:
  description: >
    List of warnings if requested features were not available due to a too old git version.
    Returned when C(state=present).
  returned: error
  sample: Your git version is too old to fully support the depth argument. Falling back to full checkouts.
  type: string
'''
