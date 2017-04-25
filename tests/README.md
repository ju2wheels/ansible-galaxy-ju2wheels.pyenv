# ju2wheels.pyenv Unit Tests

The `ju2wheels.pyenv` unit tests leverage `docker` images to run unit tests against multiple Linux distribution releases.

## Requirements

In order to run the unit tests you need to have the following installed on your testing host:

* ansible >= 2.1
* docker
* docker Python module (or docker-py >= 1.7.0 for older docker versions) (for the `docker_container` Ansible module)

## Running the Unit Tests

The `tests` directory contains a faux Ansible playbook directory with two playbooks (`docker_test.yml` and `test.yml`). The `test.yml`
playbook runs the `ju2wheels.pyenv` unit tests against the `localhost` (its not recommended you directly run this on your host unless
you are on a VM). The `docker_test.yml` will start a `docker` container with Ansible 2.x pre-installed and run the unit tests inside the
container as if it were executed against a remote machine.

```
git clone https://github.com/ju2wheels/ansible-galaxy-ju2wheels.pyenv.git ju2wheels.pyenv
cd ju2wheels.pyenv/tests
ansible-playbook docker_test.yml

# or from any CWD
# ANSIBLE_CONFIG=/<base_path>/ju2wheels.pyenv/tests/ansible.cfg ansible-playbook /<base_path>/ju2wheels.pyenv/tests/docker_test.yml
```

## Customizing the Unit Tests

The `docker_test.yml` uses the `docker_container` Ansible module and nearly all of its options are exposed for overriding from the command
line. Variables take the name `docker_container_<docker_container_parameter>` (ie to set the `api_version` parameter for the `docker_container`
task in `docker_test.yml` you would set the value `docker_container_api_version=1.20` as an extra value passed to ansible-playbook as follows:

```
ansible-playbook --extra-vars 'docker_container_api_version=1.20' docker_test.yml
```

If you are passing more than one value, it is recommended to use JSON format for passing the extra vars.

In addition to `docker_container` parameters, you can also define the `docker_container_images` array to control which `docker` images the unit tests are run against.

If you want to control the behavior of the Ansible command thats actually run inside the container (since we are using Ansible to run Ansible in the `docker` container),
you can override the values for `docker_container_command` and `docker_container_env`. Note that `docker_container_command` must always disable the
`ansible_become` parameter via `extra-vars` as well as having the path to the `test.yml` playbook if you override the value to customize variables in
`vars/pyenv_test.yml`.

## Unit Testing Docker Images

The unit tests leverage pre-built `docker` images with Ansible 2.x pre-installed. The images can be found on Docker Hub at
[ju2wheels/ansible](https://hub.docker.com/r/ju2wheels/ansible/) and the `Dockerfile`s used to make them on GitHub at
[ju2wheels/docker-ansible](https://github.com/ju2wheels/docker-ansible).
