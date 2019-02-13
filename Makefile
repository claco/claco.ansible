.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo 'Usage: make [target] [argument=value] ...'
	@echo
	@echo 'Targets:'
	@echo
	@egrep '^(.+)\:\s+##\ (.+)' ${MAKEFILE_LIST} | column -t -c 2 -s ':#'

.PHONY: all
all: ## run all targets
all: bootstrap clean lint

.PHONY: bootstrap
bootstrap: ## bootstrap host with minimum requirements to run playbooks
bootstrap:
	@./bootstrap.sh

.PHONY: build-depends
build-depends: ## install image building dependencies
build-depends:
	@ANSIBLE_PYTHON_INTERPRETER=$$PWD/.venv/bin/python ansible-playbook playbooks/building.yml

.PHONY: build-image
build-image: ## build a packer image
build-image:
	@cd packer &&  packer build -var 'distro=$(distro)' -var 'version=$(version)' build.json

.PHONY: build-packer
build-packer: ## build all packer images for molecule
build-packer: ./packer/debian/*.json ./packer/ubuntu/*.json
	@for varsfile in $^; do \
		cd packer; \
		packer build --var-file=../$$varsfile ./build.json; \
		cd ../; \
	done

.PHONY: clean
clean: ## clean build/execution artifacts
clean: clean-ansible clean-docker clean-python clean-venv

.PHONY: clean-ansible
clean-ansible: ## clean ansible related files
clean-ansible:
	@rm -rf roles/claco.skeleton_test *.retry playbooks/*.retry roles/*/molecule/*/*.retry

.PHONY: clean-docker
clean-docker: ## clean Docker containers, images, networks, and volumes
clean-docker:
	@if [ $$(docker container ls -q | wc -l) != 0 ];then docker stop $$(docker container ls -a -q); fi
	@docker container prune -f
	@docker image prune -f -a
	@docker network prune -f
	@docker volume prune -f

.PHONY: clean-python
clean-python: ## clean .pyc and __pycache__ bits
clean-python:
	@rm -rf rules/*.pyc rules/__pycache__ roles/*/molecule/*/tests/*.pyc roles/*/molecule/*/tests/__pycache__

.PHONY: clean-venv
clean-venv: ## clean .venv
clean-venv:
	@sudo rm -rf .venv

.PHONY: depends
depends: ## install all dependencies
depends: build-depends lint-depends test-depends

.PHONY: execute
execute: ## run the specified ansible playbook - make execute name=site
execute:
	@ansible-playbook -b playbooks/$(name).yml

.PHONY: install-hooks
install-hooks: ## install the repository hooks
install-hooks:
	@pre-commit install-hooks
	@gitlint install-hook

.PHONY: pre-commit
pre-commit: ## run the pre-commit hooks
pre-commit:
	@pre-commit run

.PHONY: lint
lint: ## lint project
lint: lint-yaml lint-ansible lint-python lint-security

.PHONY: lint-ansible
lint-ansible: ## lint all ansible roles and playbooks
lint-ansible: lint-ansible-roles lint-ansible-playbooks

.PHONY: lint-ansible-playbooks
lint-ansible-playbooks: ## lint ansible playbook files using ansible-lint
lint-ansible-playbooks:
	@ANSIBLE_PYTHON_INTERPRETER=$$PWD/.venv/bin/python .venv/bin/ansible-lint -c .ansible-lint -R -v roles/*/molecule/*/*.yml playbooks/*.yml playbooks/*/*.yml

.PHONY: lint-ansible-roles
lint-ansible-roles: ## lint ansible roles only using ansible-lint
lint-ansible-roles:
	@ANSIBLE_PYTHON_INTERPRETER=$$PWD/.venv/bin/python .venv/bin/ansible-lint -c .ansible-lint -R -v roles/*/

.PHONY: lint-depends
lint-depends: ## install linting dependencies
lint-depends:
	@ANSIBLE_PYTHON_INTERPRETER=$$PWD/.venv/bin/python .venv/bin/ansible-playbook playbooks/linting.yml

.PHONY: lint-git
lint-git: ## lint git commit message
lint-git:
	@.venv/bin/gitlint

.PHONY: lint-python
lint-python: ## lint python code in ansible rules
lint-python:
	@.venv/bin/pylama

.PHONY: lint-security
lint-security: ## lint code for undesired usage patterns
lint-security:
	@true

.PHONY: lint-yaml
lint-yaml: ## lint yaml files using yamllint
lint-yaml:
	@.venv/bin/yamllint -c .yamllint --strict .ansible-lint .yamllint .

.PHONY: role
role: ## create a new role in this project - make roles name=foop
role:
	@ansible-galaxy init ./roles/claco.$(name)

.PHONY: test
test: ## run all tests for this project
test: test-ansible test-molecule test-security

.PHONY: test-ansible
test-ansible: ## run all ansible tests for this project
test-ansible:
	@make role name=skeleton_test
	@ansible-lint -c .ansible-lint -R -v roles/claco.skeleton_test/
	@make lint-python
	@make lint-yaml
	@make clean-ansible

.PHONY: test-depends
test-depends: ## install testing dependencies
test-depends:
	@ANSIBLE_PYTHON_INTERPRETER=$$PWD/.venv/bin/python ansible-playbook playbooks/testing.yml

.PHONY: test-molecule
test-molecule: ## run all molecule role tests
test-molecule: ./roles/*
	@for role in $^; do \
		if [ -f "$$role/molecule/default/molecule.yml" ]; then \
			cd $$role; \
			molecule test; \
			cd ../../; \
		fi \
	done

.PHONY: test-security
test-security: ## run all security checks against the artifacts
test-security:
	@true
