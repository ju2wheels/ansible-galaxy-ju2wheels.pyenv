from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os

from ansible.errors import AnsibleError
from ansible.module_utils.parsing.convert_bool import boolean
from ansible.plugins.action import ActionBase

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()

class ActionModule(ActionBase):
    ALLOWED_STATES = frozenset([
        'absent',
        'present'
    ])
    DEFAULT_PARAMETER_VALUES = dict(
        dest='.pyenv',
        force='yes',
        repo='https://github.com/yyuu/pyenv.git',
        umask='022',
        update='yes',
        version='master'
    )
    SUPPORTED_PARAMETERS = frozenset([
        'accept_hostkey',
        'dest',
        'executable',
        'force',
        'key_file',
        'refspec',
        'remote',
        'repo',
        'ssh_opts',
        'state',
        'track_submodules',
        'umask',
        'update',
        'verify_commit',
        'version'
    ])
    TRANSFERS_FILES = False

    def manage_pyenv(self, tmp=None, task_vars=None):
        module_args = self._task.args.copy()
        state = module_args['state']

        if state == 'absent':
            file_module_args = {k:module_args[k] for k in ('dest', 'state')}

            return self._execute_module(
                module_name='file',
                module_args=file_module_args,
                task_vars=task_vars,
                tmp=tmp
            )
        elif state == 'present':
            git_module_args = self.DEFAULT_PARAMETER_VALUES.copy()
            
            git_module_args.update(module_args)

            del git_module_args['state']

            return self._execute_module(
                module_name='git',
                module_args=git_module_args,
                task_vars=task_vars,
                tmp=tmp
            )

    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)

        result.update(
            dict(
                changed=False,
                failed=True,
                skipped=False
            )
        )

        self._supports_check_mode = True
        self._supports_async = False

        verify_module_args_result = self.verify_module_args()

        if verify_module_args_result:
            result.update(verify_module_args_result)

            return result

        if self._play_context.check_mode:
            result['failed'] = False
            result['skipped'] = True

            return result

        update_dest_result = self.update_dest(tmp=tmp, task_vars=task_vars)

        if update_dest_result:
            result.update(update_dest_result)

            return result

        module_args = self._task.args
        result['failed'] = False
        result['pyenv'] = self._task.args['dest']
        
        result.update(self.manage_pyenv(tmp=tmp, task_vars=task_vars))

        return result

    def update_dest(self, tmp=None, task_vars=None):
        module_args = self._task.args
        module_name = self._task.action
        result = {}

        if module_args.get('dest', None) is None or not os.path.isabs(module_args['dest']):
            pyenv_users_home_result = self._execute_module(
                module_name='pyenv_users_home',
                module_args={}, # explicitly required otherwise self._task.args will be provided if it defaults to None
                task_vars=task_vars,
                tmp=tmp
            )

            display.debug('pyenv_users_home: %s' % str(pyenv_users_home_result))

            if pyenv_users_home_result.get('failed', False):
                result.update(pyenv_users_home_result)

                return result

            # We should only get one user back (the user as which the module was run), if we get more thats a problem
            if len(pyenv_users_home_result['ansible_facts']['pyenv_users_home']) != 1:
                result['msg'] = '(%s) module expected pyenv_users_home for one user, received: %s' % \
                                (module_name, str(pyenv_users_home_result['ansible_facts']))

                return result

            user_home = pyenv_users_home_result['ansible_facts']['pyenv_users_home'].values()[0]

            module_args['dest'] = (os.path.sep).join([
                user_home,
                module_args.get('dest', None) or self.DEFAULT_PARAMETER_VALUES['dest']
            ])

        return result

    def verify_module_args(self):
        result = {}

        module_args = self._task.args
        module_name = self._task.action

        if 'state' not in module_args:
            module_args['state'] = 'present'

        if module_args['state'] not in self.ALLOWED_STATES:
            result['msg'] = 'Required parameter state for (%s) module must be one of: %s' % \
                            (module_name, ', '.join(self.ALLOWED_STATES))

            return result

        # Unfortunately action plugins dont have arg specs like modules but Ansible devs are working on it
        supported = frozenset(module_args.keys()).difference(self.SUPPORTED_PARAMETERS)
        verify_supported = not bool(supported)

        if not verify_supported:
            result['msg'] = ' '.join(['Unsupported parameters for (%s) module: %s .',
                                      'Supportedparameters include: %s .']) % \
                                      (module_name, ', '.join(supported),
                                       ', '.join(self.SUPPORTED_PARAMETERS))

        return result
