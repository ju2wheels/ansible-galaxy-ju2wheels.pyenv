# ju2wheels.pyenv Task Sets

The `ju2wheels.pyenv` Ansible role has a number of task sets which are organized so that they all leverage the
same role variables and can be triggered independently using `include_role` for maximum flexibility. Each task set
also exposes all Ansible module parameters for customization via the role variables if customizing/using the parameter
makes sense within the context of the given task. By exposing the module parameters, almost everything can be customized
to meet different end user scenarios without needing to rewrite a particular task set at all.

Any tasks in the top level `tasks/` directory can be used with the `include_role` Ansible module.

All task sets set the state for all tasks and therefore state is not configurable via role variables (ie install task
sets explicity set all task states to `present` and uninstall task sets set all task states to `absent`).

## Task Sets

### install (aka main)

The `install` task set runs all install task sets and is also the task set run by default using `main.yml`.

It runs the following task sets in order:

1. repository_install
2. build_dependencies_install
3. git_dependencies_instal
4. pyenv_install
5. pyenv_virtualenv_install
6. pyenvs_install
7. pyenv_virtualenvs_install
8. pyenv_shell_env_install

See the descriptions for each task set below for required role variables.

Example:

```
---

- hosts: localhost
  vars:
    # See task requirements below
  roles:
    - ju2wheels.pyenv

- hosts: localhost
  vars:
    # See task requirements below
  tasks:
    - include_role:
        name: ju2wheels.pyenv

- hosts: localhost
  vars:
    # See task requirements below
  tasks:
    - include_role:
        name: ju2wheels.pyenv
        tasks_from: install
```

### uninstall

The `uninstall` task set runs all uninstall task sets.

It runs the following task sets in order:

1. pyenv_shell_env_uninstall
2. pyenv_virtualenvs_uninstall
3. pyenvs_uninstall
4. pyenv_virtualenv_uninstall
5. pyenv_uninstall
6. git_dependencies_uninstall
7. build_dependencies_uninstall
8. repository_uninstall

Example:

```
---

- hosts: localhost
  vars:
    # See task requirements below
  tasks:
    - include_role:
        name: ju2wheels.pyenv
        tasks_from: uninstall
```

### repository_install

Configures repositories needed to install any dependencies.

Required role variables:

1. `pyenv_repositories`
    1. One of the keys must match the current `ansible_distribution`
    2. The key for the current `ansible_distribution` should have a `pyenv_repository` object for either `epel` or `git`
2. `pyenv_repository_keys`
    1. One of the keys must match the current `ansible_distribution`
    2. The key for the current `ansible_distribution` should have a `pyenv_repository_key` object for either `epel` or `git`

If the requirements are not met, the respective tasks in the task set are skipped.

Example:

```
---

- hosts: localhost
  vars:
    pyenv_repositories:
      ansible_distribution:
        epel:
          # properties
    pyenv_repository_keys:
      ansible_distribution:
        epel:
          # properties
  tasks:
    - include_role:
        name: ju2wheels.pyenv
        tasks_from: repository_install
```

### repository_uninstall

Removes configured repositories needed to install any dependencies.

Required role variables:

1. `pyenv_repositories`
    1. One of the keys must match the current `ansible_distribution`
    2. The key for the current `ansible_distribution` should have a `pyenv_repository` object for either `epel` or `git`
2. `pyenv_repository_keys`
    1. One of the keys must match the current `ansible_distribution`
    2. The key for the current `ansible_distribution` should have a `pyenv_repository_key` object for either `epel` or `git`

If the requirements are not met, the respective tasks in the task set are skipped.

Example:

```
---

- hosts: localhost
  vars:
    pyenv_repositories:
      ansible_distribution:
        epel:
          # properties
    pyenv_repository_keys:
      ansible_distribution:
        epel:
          # properties
  tasks:
    - include_role:
        name: ju2wheels.pyenv
        tasks_from: repository_uninstall
```

### build_dependencies_install

Installs build dependencies required by `pyenv` to build Python versions.

Required role variables:

1. `pyenv_build_dependencies`
    1. One of the keys must match the current `ansible_distribution`
    2. The key for the current `ansible_distribution` should have a `pyenv_package` object value (`package_manager` key may be an empty dictionary)

If the requirements are not met, the respective tasks in the task set are skipped.

Example:

```
---

- hosts: localhost
  vars:
    pyenv_build_dependencies:
      ansible_distribution:
        package_manager:
          # package manager parameters or empty dictionary
        packages:
          # List of packages
  tasks:
    - include_role:
        name: ju2wheels.pyenv
        tasks_from: build_dependencies_install
```

### build_dependencies_uninstall

Uninstalls build dependencies required by `pyenv` to build Python versions.

Required role variables:

1. `pyenv_build_dependencies`
    1. One of the keys must match the current `ansible_distribution`
    2. The key for the current `ansible_distribution` should have a `pyenv_package` object value (`package_manager` key may be an empty dictionary)

If the requirements are not met, the respective tasks in the task set are skipped.

WARNING: Please ensure to reduce the default package list as well depending on whether you are running this in a container, server, or desktop install
so you dont accidentally remove packages that are required by desktop packages for example. Its recommended to reduce the package list to only uninstall
the development libraries if you are unsure (see unit tests).

Example:

```
---

- hosts: localhost
  vars:
    pyenv_build_dependencies:
      ansible_distribution:
        package_manager:
          # package manager parameters or empty dictionary
        packages:
          # List of packages
  tasks:
    - include_role:
        name: ju2wheels.pyenv
        tasks_from: build_dependencies_uninstall
```

### git_dependencies_install

Installs git dependencies required by `pyenv` to clone/install `pyenv` and its plugins.

Required role variables:

1. `pyenv_git_dependencies`
    1. One of the keys must match the current `ansible_distribution`
    2. The key for the current `ansible_distribution` should have a `pyenv_package` object value (`package_manager` key may be an empty dictionary)

If the requirements are not met, the respective tasks in the task set are skipped.

Example:

```
---

- hosts: localhost
  vars:
    pyenv_git_dependencies:
      ansible_distribution:
        package_manager:
          # package manager parameters or empty dictionary
        packages:
          # List of packages
  tasks:
    - include_role:
        name: ju2wheels.pyenv
        tasks_from: git_dependencies_install
```

### git_dependencies_uninstall

Uninstalls git dependencies required by `pyenv` to clone/install `pyenv` and its plugins.

Required role variables:

1. `pyenv_git_dependencies`
    1. One of the keys must match the current `ansible_distribution`
    2. The key for the current `ansible_distribution` should have a `pyenv_package` object value (`package_manager` key may be an empty dictionary)

If the requirements are not met, the respective tasks in the task set are skipped.

Example:

```
---

- hosts: localhost
  vars:
    pyenv_git_dependencies:
      ansible_distribution:
        package_manager:
          # package manager parameters or empty dictionary
        packages:
          # List of packages
  tasks:
    - include_role:
        name: ju2wheels.pyenv
        tasks_from: git_dependencies_uninstall
```

### pyenv_install

Clones/installs `pyenv` for each user defined in `pyenv_users` while running as that user.

Required role variables:

1. `pyenv`
    1. Must contain properties for `git` Ansible module (except `dest`) to clone the `pyenv` repository (at a minimun `repo`).
2. `pyenv_users`
    1. Must contain an array of `pyenv_user` objects, each with the following properties:
        * `username`
        * `pyenv_dest`

If the requirements are not met, the respective tasks in the task set are skipped.

Example:

```
---

- hosts: localhost
  vars:
    pyenv:
      repo: #url
    pyenv_users:
      - username: myuser
        pyenv_dest: '.pyenv'
  tasks:
    - include_role:
        name: ju2wheels.pyenv
        tasks_from: pyenv_install
```

### pyenv_uninstall

Uninstalls `pyenv` for each user defined in `pyenv_users` while running as that user.

Required role variables:

1. `pyenv_users`
    1. Must contain an array of `pyenv_user` objects, each with the following properties:
        * `username`
        * `pyenv_dest`

If the requirements are not met, the respective tasks in the task set are skipped.

Example:

```
---

- hosts: localhost
  vars:
    pyenv_users:
      - username: myuser
        pyenv_dest: '.pyenv'
  tasks:
    - include_role:
        name: ju2wheels.pyenv
        tasks_from: pyenv_uninstall
```

### pyenv_virtualenv_install

Clones/installs `pyenv-virtualenv` for each user defined in `pyenv_users` while running as that user.

Required role variables:

1. `pyenv_users`
    1. Must contain an array of `pyenv_user` objects, each with the following properties:
        * `username`
        * `pyenv_dest`
        * `plugins` (must have `pyenv-virtualenv` included)
2. `pyenv_virtualenv`
    1. Must contain properties for `git` Ansible module (except `dest`) to clone the `pyenv-virtualenv` repository (at a minimun `repo`).

If the requirements are not met, the respective tasks in the task set are skipped.

Example:

```
---

- hosts: localhost
  vars:
    pyenv_users:
      - username: myuser
        pyenv_dest: '.pyenv'
        plugins:
          - pyenv-virtualenv
    pyenv_virtualenv:
      repo: #url
  tasks:
    - include_role:
        name: ju2wheels.pyenv
        tasks_from: pyenv_virtualenv_install
```

### pyenv_virtualenv_uninstall

Uninstalls `pyenv-virtualenv` for each user defined in `pyenv_users` while running as that user.

Required role variables:

1. `pyenv_users`
    1. Must contain an array of `pyenv_user` objects, each with the following properties:
        * `username`
        * `pyenv_dest`
        * `plugins` (must have `pyenv-virtualenv` included)

If the requirements are not met, the respective tasks in the task set are skipped.

Example:

```
---

- hosts: localhost
  vars:
    pyenv_users:
      - username: myuser
        pyenv_dest: '.pyenv'
        plugins:
          - pyenv-virtualenv
  tasks:
    - include_role:
        name: ju2wheels.pyenv
        tasks_from: pyenv_virtualenv_uninstall
```

### pyenvs_install

Installs Python versions for each user in `pyenv_users` while running as that user.

Note: This step is compiling each Python version from scratch for each user and can take a while to complete.

Required role variables:

1. `pyenv_users`
    1. Must contain an array of `pyenv_user` objects, each with the following properties:
        * `username`
        * `pyenv_dest`
        * `python_versions` (must be defined even if its just an empty array, otherwise the task set will fail)

If the requirements are not met, the respective tasks in the task set are skipped.

Example:

```
---

- hosts: localhost
  vars:
    pyenv_users:
      - username: myuser
        pyenv_dest: '.pyenv'
        python_versions:
          - 2.7.13
  tasks:
    - include_role:
        name: ju2wheels.pyenv
        tasks_from: pyenvs_install
```

### pyenvs_uninstall

Uninstalls Python versions for each user in `pyenv_users` while running as that user.

Required role variables:

1. `pyenv_users`
    1. Must contain an array of `pyenv_user` objects, each with the following properties:
        * `username`
        * `pyenv_dest`
        * `python_versions` (must be defined even if its just an empty array, otherwise the task set will fail)

If the requirements are not met, the respective tasks in the task set are skipped.

Example:

```
---

- hosts: localhost
  vars:
    pyenv_users:
      - username: myuser
        pyenv_dest: '.pyenv'
        python_versions:
          - 2.7.13
  tasks:
    - include_role:
        name: ju2wheels.pyenv
        tasks_from: pyenvs_uninstall
```

### pyenv_virtualenvs_install

Installs Python virtualenvs for each user in `pyenv_users` while running as that user.

Required role variables:

1. `pyenv_users`
    1. Must contain an array of `pyenv_user` objects, each with the following properties:
        * `username`
        * `pyenv_dest`
        * `plugins` (must have `pyenv-virtualenv` included)
        * `virtualenvs` (must contain an array of `pyenv_virtualenv` objects, each with `name` and `python_version` properties and must be defined even if its an empty array, otherwise the task set will fail)

If the requirements are not met, the respective tasks in the task set are skipped.

Example:

```
---

- hosts: localhost
  vars:
    pyenv_users:
      - username: myuser
        pyenv_dest: '.pyenv'
        plugins:
          - pyenv-virtualenv
        virtualenvs:
          - name: venv-2.7.13
            python_version: 2.7.13
  tasks:
    - include_role:
        name: ju2wheels.pyenv
        tasks_from: pyenv_virtualenvs_install
```

### pyenv_virtualenvs_uninstall

Uninstalls Python virtualenvs for each user in `pyenv_users` while running as that user.

Required role variables:

1. `pyenv_users`
    1. Must contain an array of `pyenv_user` objects, each with the following properties:
        * `username`
        * `pyenv_dest`
        * `plugins` (must have `pyenv-virtualenv` included)
        * `virtualenvs` (must contain an array of `pyenv_virtualenv` objects, each with the `name` property and must be defined even if its an empty array, otherwise the task set will fail)

If the requirements are not met, the respective tasks in the task set are skipped.

Example:

```
---

- hosts: localhost
  vars:
    pyenv_users:
      - username: myuser
        pyenv_dest: '.pyenv'
        plugins:
          - pyenv-virtualenv
        virtualenvs:
          - name: venv-2.7.13
  tasks:
    - include_role:
        name: ju2wheels.pyenv
        tasks_from: pyenv_virtualenvs_uninstall
```

### pyenv_shell_env_install

Installs shell autoloading for bash completions for `pyenv` and/or `pyenv-virtualenv` for each user in `pyenv_users` while running as that user.

Required role variables (for `pyenv`):

1. `pyenv_users`
    1. Must contain an array of `pyenv_user` objects, each with the following properties:
        * `username`
        * `pyenv_dest`
        * `shell_rc_blockinfile_properties` (must be defined even if its just an empty dictionary, otherwise the task set will fail; should contain `blockinfile` Ansible module parameters)
        * `shell_rc_files` (must be defined even if its just an empty array, otherwise the task set will fails)

Required role variables (for `pyenv-virtualenv`):

1. `pyenv_users`
    1. Must contain an array of `pyenv_user` objects, each with the following properties:
        * `username`
        * `pyenv_dest`
        * `plugins` (must have `pyenv-virtualenv` included)
        * `shell_rc_blockinfile_properties` (must be defined even if its just an empty dictionary, otherwise the task set will fail; should contain `blockinfile` Ansible module parameters)
        * `shell_rc_files` (must be defined even if its just an empty array, otherwise the task set will fails)

If the requirements are not met, the respective tasks in the task set are skipped.

Example:

```
---

- hosts: localhost
  vars:
    pyenv_users:
      - username: myuser
        pyenv_dest: '.pyenv'
        plugins:
          - pyenv-virtualenv
        shell_rc_blockinfile_properties:
          backup: yes
        shell_rc_files:
          - '.bashrc'
  tasks:
    - include_role:
        name: ju2wheels.pyenv
        tasks_from: pyenv_shell_env_install
```

### pyenv_shell_env_uninstall

Uninstalls shell autoloading for bash completions for `pyenv` and/or `pyenv-virtualenv` for each user in `pyenv_users` while running as that user.

Required role variables (for `pyenv`):

1. `pyenv_users`
    1. Must contain an array of `pyenv_user` objects, each with the following properties:
        * `username`
        * `pyenv_dest`
        * `shell_rc_blockinfile_properties` (must be defined even if its just an empty dictionary, otherwise the task set will fail; should contain `blockinfile` Ansible module parameters)
        * `shell_rc_files` (must be defined even if its just an empty array, otherwise the task set will fails)

Required role variables (for `pyenv-virtualenv`):

1. `pyenv_users`
    1. Must contain an array of `pyenv_user` objects, each with the following properties:
        * `username`
        * `pyenv_dest`
        * `plugins` (must have `pyenv-virtualenv` included)
        * `shell_rc_blockinfile_properties` (must be defined even if its just an empty dictionary, otherwise the task set will fail; should contain `blockinfile` Ansible module parameters)
        * `shell_rc_files` (must be defined even if its just an empty array, otherwise the task set will fails)

If the requirements are not met, the respective tasks in the task set are skipped.

Example:

```
---

- hosts: localhost
  vars:
    pyenv_users:
      - username: myuser
        pyenv_dest: '.pyenv'
        plugins:
          - pyenv-virtualenv
        shell_rc_blockinfile_properties:
          backup: yes
        shell_rc_files:
          - '.bashrc'
  tasks:
    - include_role:
        name: ju2wheels.pyenv
        tasks_from: pyenv_shell_env_uninstall
```
