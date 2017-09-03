# ju2wheels.pyenv

`ju2wheels.pyenv` is an [Ansible Galaxy](https://galaxy.ansible.com/ju2wheels/pyenv/) role for [pyenv](https://github.com/yyuu/pyenv).
It is designed to be highly modular for use with the `include_role` module across multiple platforms.

## Supported Platforms

|Platform     |Versions                  |
|-------------|--------------------------|
|Alpine       |3.3, 3.4, 3.5, 3.6        |
|Amazon       |2016.09, 2017.03          |
|Debian       |7, 8, 9                   |
|CentOS       |6, 7                      |
|Fedora       |20, 21, 22, 23, 24, 25, 26|
|Linux Mint   |18                        |
|openSUSE     |13.2                      |
|openSUSE Leap|42.2                      |
|Oracle Linux |6, 7                      |
|RedHat       |6, 7                      |
|Scientific   |6, 7                      |
|Ubuntu       |12.04, 14.04, 16.04       |

## Requirements

Ansible >= 2.1

## Role Variables

|Role Variable             |Description                                                                                                                                                                   |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|`pyenv`                   |GIT clone parameters (except for `dest`) to pass to the `git` Ansible module for cloning/installing the `pyenv` repository (these settings are used for all users).           |
|`pyenv_build_dependencies`|Build dependencies required for building Python versions with `pyenv`. Dictionary whose key is an `ansible_distribution` and value is a `pyenv_package` object (see below).   |
|`pyenv_git_dependencies`  |GIT dependencies required for installing GIT on the platform which is required to install `pyenv` and `pyenv-virutalenv`. Dictionary whose key is an `ansible_distribution` and value is a `pyenv_package` object (see below).|
|`pyenv_repositories`      |Configure repositories required to install dependencies. Dictionary whose key is an `ansible_distribution` and value is a `pyenv_repository` object (see below).              |
|`pyenv_repository_keys`   |Configure repository keys required to install dependencies. Dictionary whose key is an `ansible_distribution` and value is a `pyenv_repository_key` object (see below).       |
|`pyenv_users`             |Configure `pyenv` Python versions, shell autoloading and optionally plugins like `pyenv-virtualenv` and virtualenvs. Array of `pyenv_user` objects (see below).               |
|`pyenv_virtualenv`        |GIT clone parameters (except for `dest`) to pass to the `git` Ansible module for cloning/installing the `pyenv-virtualenv` repository (these settings are used for all users).|

### pyenv_package

The `pyenv_package` object is a dictionary used for pairing a list of packages with package manager Ansible module (`apt`, `dnf`, `yum`, etc) parameters.

|pyenv_package key|Description                       |
|-----------------|----------------------------------|
|`package_manager`|Dictionary containing parameters for the package manager Ansible module (`apt`, `dnf`, `yum`, etc). Most parameters are accepted if they make sense in the context of the task except for `state`.|
|`packages`       |Array of package names to install.|

### pyenv_repository

The `pyenv_repository` object is a dictionary used for defining repository configuration Ansible module (`apt_repositry`, `yum_repository`, etc) parameters.
The current key values supported are `epel` or `git`. The value for `epel` or `git` are a dictionary of `yum_repository` or `apt_repository` Ansible module parameters respectively (except for `state`).

### pyenv_repository_key

The `pyenv_repository` object is a dictionary used for defining repository key configuration Ansible module (`apt_key`, `rpm_key`, etc) parameters.
The current key values support are `epel` or `git`. The value for `epel` or `git` are a dictionary of `rpm_key` or `apt_key` Ansible module parameters respectively (except for `state`).

### pyenv_user

The `pyenv_user` object is a dictionary and is the main driver for all `ju2wheels.pyenv` task sets for controlling the configuration behavior of `pyenv` for each user.

|`pyenv_user` key                |Description                                                                                                  |
|--------------------------------|-------------------------------------------------------------------------------------------------------------|
|`username`                      |The username of the user to become when configuring `pyenv`.                                                 |
|`plugins`                       |Array specifying `pyenv` plugins to install. Currently only supports `pyenv-virtualenv`.                     |
|`pyenv_dest`                    |The destination where `pyenv` gets installed. If its a relative path, its relative to the user's `HOME` directory. This is used in combination with the `pyenv` role variable.|
|`shell_rc_blockinfile_properties`|Dictionary of `blockinfile` parameters used when configuring shell autoloading for `pyenv` in shell rc files.|
|`shell_rc_files`                |Array of shell rc file destinations in which to enable `pyenv` shell autoloading. If its a relative path, its relatvie to the user's `HOME` directory.|
|`python_versions`               |Array of `pyenv` Python versions to be compiled and installed for the user.                                  |
|`virtualenvs`                   |Array of `pyenv_virtualenv` objects (see below) that define virtualenvs to create.                           |

### pyenv_virtualenv

The `pyenv_virtualenv` object is a dictionary that links a virtualenv name to a specific Python version.

|`pyenv_virtualenv` key|Description                                                                                                                                                  |
|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
|`name`                |The name of the virtualenv.                                                                                                                                  |
|`python_version`      |The Python version the virtualenv will use. This should be a version that is listed in the `python_versions` array of the current user's `pyenv_user` object.|

For actual example implementations of these role variables see `defaults\main.yml` and the unit test vars (its less complicated than the above makes it seem :-) ).

## Task Sets

The `ju2wheels.pyenv` role is designed in a modular fashion and has different task sets defined which can be used independently of each other with the same role variables using the
Ansible `include_role` module. For a full description and requirements of each task set see the [task sets README](https://github.com/ju2wheels/ansible-galaxy-ju2wheels.pyenv/tree/master/tasks/README.md).

## Example Playbook

```
---

- hosts: localhost
  vars:
    # If you already have epel-release installed or EPEL configured on EL
    # platforms or dont want to add the latest GIT PPA for Ubuntu/Linux Mint,
    # uncomment these to disable repository configuration.
    # This is added so that this role works in a standalone fashion, but
    # is recommended you add these to a more general task/role in your playbook.
    #pyenv_repositories: {}
    #pyenv_repository_keys: {}

    # If you dont customize pyenv_users, the role will setup Python 2.x and
    # 3.x under the user accessing the hosts by default
    # (ie hostvars[inventory_hostname].ansible_env.USER ).
    pyenv_users:
      - username: myuser
        # Only virtualenv plugin is currently supported
        plugins:
          - pyenv-virtualenv
        # If the destination paths are relative, they are converted to be
        # relative to the user's HOME directory
        pyenv_dest: '.pyenv'
        # Shell environment autoloading configuration for blockinfile module
        # (can be empty dictionary if you dont want to customize it).
        shell_rc_blockinfile_properties:
          backup: yes
          create: yes
          follow: yes
        # If the destination paths are relative, they are converted to be
        # relative to the user's HOME directory
        shell_rc_files:
          - '.bashrc'
        python_versions:
          - 2.7.13
          - 3.6.0
        virtualenvs:
          - name: venv-2.7.13
            python_version: 2.7.13
          - name: venv-3.6.0
            python_version: 3.6.0
  roles:
    - ju2wheels.pyenv

# Alternative include_role syntax
- hosts: localhost
  vars:
    # Same variables as above
  tasks:
    - include_role:
        name: ju2wheels.pyenv
        # This can be omitted as main.yml and install.yml are equivalent
        #tasks_from: install
```

## Unit Testing

See the [Unit Testing README](https://github.com/ju2wheels/ansible-galaxy-ju2wheels.pyenv/tree/master/tests/README.md) for requirements and unit testing process.

## Contributing

Feel free to open an issue request to add support for other platforms. Additional platforms should only require adding
platform specific sections under `build_dependencies\`, `git_dependencies\`, and `repository\` as well as updating
`defaults\main.yml` with platform default values.

## License

GPLv2

## Author Information

Julio Lajara \<GH user at Gmail>
