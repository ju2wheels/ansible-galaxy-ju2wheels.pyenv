# ju2wheels.pyenv Ansible Modules

## pyenv_users_home

### Synopsis

The `pyenv_users_home` Ansible module retrieves the `HOME` path for specified users from the remote host using platform specific commands.

### Requirements

* getent (Linux)

### Options

|parameter|required|default            |choices|comments                                                                   |
|---------|--------|-------------------|-------|---------------------------------------------------------------------------|
|users    |no      |[`ansible_user_id`]|       |The users for which to retrieve the C(HOME) path. Defaults to current user.|

### Returns

|name              |description                              |returned|type   |sample                                          |
|------------------|-----------------------------------------|--------|-------|------------------------------------------------|
|pyenv\_users\_home|The C(HOME) path for the specified users.|success |complex|{"user1": "/home/user1", "user2": "/home/user2"}|
