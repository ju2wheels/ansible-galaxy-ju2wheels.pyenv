# ju2wheels.pyenv Ansible Modules

## pyenv

### Synopsis

Manages the installation of pyenv from a GIT repo.

### Requirements

* git>=1.7.1 (the command line tool)

### Options

|parameter        |required|default                          |choices        |comments                                                                                                         |
|-----------------|--------|---------------------------------|---------------|-----------------------------------------------------------------------------------------------------------------|
|accept\_hostkey  |no      |no                               |yes, no        |if `yes`, ensure that "-o StrictHostKeyChecking=no" is present as an ssh options. Only used when `state=present`.|
|dest             |no      |.pyenv                           |               |The path of where the repository should be checked out.                                                          |
|executable       |no      |                                 |               |Path to git executable to use. If not supplied, the normal mechanism for resolving binary paths will be used. Only used when `state=present`.|
|force            |no      |yes                              |yes, no        |If `yes`, any modified files in the working repository will be discarded. Only used when `state=present`.        |
|key\_file        |no      |                                 |               |Specify an optional private key file to use for the checkout. Only used when `state=present`.                    |
|refspec          |no      |                                 |               |Add an additional refspec to be fetched. If version is set to a `SHA-1` not reachable from any branch or tag, this option may be necessary to specify the ref containing the `SHA-1`. Uses the same syntax as the 'git fetch' command. An example value could be "refs/meta/config". Only used when `state=present`.              |
|remote           |no      |origin                           |               |Name of the git remote. Only used when `state=present`.                                                          |
|repo             |no      |https://github.com/yyuu/pyenv.git|               |git, SSH, or HTTP(S) protocol address of the git repository. Only used when `state=present`.                     |
|ssh\_opts        |no      |                                 |               |Creates a wrapper script and exports the path as GIT\_SSH which git then automatically uses to override ssh arguments. An example value could be "-o StrictHostKeyChecking=no". Only used when `state=present`.|
|state            |no      |present                          |absent, present|Whether to install or remove pyenv.                                                                              |
|track\_submodules|no      |no                               |yes, no        |if `yes`, submodules will track the latest commit on their master branch (or other branch specified in .gitmodules). If `no`, submodules will be kept at the revision specified by the main project. This is equivalent to specifying the --remote flag to git submodule update. Only used when `state=present`.                  |
|umask            |no      |022                              |               |The umask to set before doing any checkouts, or any other repository maintenance. Only used when `state=present`.|
|update           |no      |yes                              |yes, no        |If `no`, do not retrieve new revisions from the origin repository. Only used when `state=present`.               |
|verify\_commit   |no      |no                               |yes, no        |if `yes`, when cloning or checking out a `version` verify the signature of a GPG signed commit. This requires `git` version>=2.1.0 to be installed. The commit MUST be signed and the public key MUST be present in the GPG keyring. Only used when `state=present`.|
|version          |no      |HEAD                             |               |What version of the repository to check out.  This can be the the literal string `HEAD`, a branch name, a tag name. It can also be a `SHA-1` hash, in which case `refspec` needs to be specified if the given revision is not already available. Only used when `state=present`.|

### Examples

```
- name: Install pyenv
  pyenv:

- name: Uninstall pyenv
  pyenv:
    state: absent
```

### Returns

|name                |description                                                                                                           |returned|type   |sample                                          |
|--------------------|----------------------------------------------------------------------------------------------------------------------|--------|-------|------------------------------------------------|
|after               |Last commit revision of the repository retrieved during the update. Returned when `state=present`.                    |success |string |4c020102a9cd6fe908c9a4a326a38f972f63a903        |
|before              |Commit revision before the repository was updated, "null" for new repository. Returned when `state=present`.          |success |string |67c04ebe40a003bda0efb34eacfb93b0cafdf628        |
|pyenv               |The destination of the pyenv install being installed or removed.                                                      |success |string |/home/user/.pyenv                               |
|remote\_url\_changed|Contains True or False whether or not the remote URL was changed. Returned when `state=present`.                      |success |boolean|True                                            |
|warnings            |List of warnings if requested features were not available due to a too old git version. Returned when `state=present`.|error   |string |Your git version is too old to fully support the depth argument. Falling back to full checkouts.|

## pyenv_users_home

### Synopsis

The `pyenv_users_home` Ansible module retrieves the `HOME` path for specified users from the remote host using platform specific commands.

### Requirements

* getent (Linux)

### Options

|parameter|required|default            |choices|comments                                                                   |
|---------|--------|-------------------|-------|---------------------------------------------------------------------------|
|users    |no      |[`ansible_user_id`]|       |The users for which to retrieve the C(HOME) path. Defaults to current user.|

### Examples

```
---

- name: Retrieve HOME path for current user
  pyenv_users_home:

- name: Retrieve HOME path for specific users
  pyenv_users_home:
    users:
      - user1
      - user2
```

### Returns

|name              |description                              |returned|type   |sample                                          |
|------------------|-----------------------------------------|--------|-------|------------------------------------------------|
|pyenv\_users\_home|The C(HOME) path for the specified users.|success |complex|{"user1": "/home/user1", "user2": "/home/user2"}|
