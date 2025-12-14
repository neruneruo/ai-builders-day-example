SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
MAKEFLAGS += --no-builtin-rules
.SILENT:

PYTHON_DIRS="./script/agents"
TERRAFORM_DIRS="./terraform"
CLEAN_EXCLUDES ?= \
	-e terraform.tfstate \
	-e terraform.tfstate.backup

terraform:
	cd terraform
	terraform fmt
	terraform $(ARG)
.PHONY: terraform

agent-build:
	docker buildx build ./agents/ -t agentcore-local
.PHONY: agent-build

agent-local-run:
	. ./agents/env.sh
	docker-compose -f ./agents/docker-compose.yml up 
.PHONY: agent-local-run

streamlit-local-run:
	cd script/interface
	PYTHONPATH=src python -m interface
.PHONY: streamlit-local-run

################################################################################
bootstrap:
	$(MAKE) setup-lefthook
	$(MAKE) setup-uv
	$(MAKE) setup-terraform
.PHONY: bootstrap

setup-lefthook:
	if ! command -v lefthook >/dev/null 2>&1; then
		echo "[WARN] lefthook not found. Please Install lefthook: https://github.com/evilmartians/lefthook";
		exit 0;
	fi

	echo "[INFO] lefthook install ..."
	lefthook install || true
.PHONY: setup-lefthook

setup-uv:
	if ! command -v uv >/dev/null 2>&1; then
		echo "[WARN] uv not found. Please Install uv: https://docs.astral.sh/uv/";
		exit 0;
	fi

	echo "[INFO] Python target dirs:"
	printf " - %s\n" $(PYTHON_DIRS)
	for d in $(PYTHON_DIRS); do
		echo "[INFO] cd $$d"
		cd $$d
		echo "[INFO] uv sync (pyproject.toml)"
		uv sync
		echo "[INFO] uv pip install -r requirements.txt"
		uv pip install -r requirements.txt
	done
.PHONY: setup-uv

setup-terraform:
	if ! command -v terraform >/dev/null 2>&1; then
		echo "[WARN] Terraform not found. Please Install Terraform: https://developer.hashicorp.com/terraform/downloads";
		exit 0;
	fi

	echo "[INFO] Terraform target dirs:"
	printf " - %s\n" $(TERRAFORM_DIRS)
	for d in $(TERRAFORM_DIRS); do
		echo "[INFO] terraform -chdir=$$d init -upgrade"
		terraform -chdir="$$d" init -upgrade -input=false || true
	done
.PHONY: setup-terraform

################################################################################
clean:
	echo "[INFO] >>> Dry run:"
	git clean -xdn $(CLEAN_EXCLUDES)
	echo
	read -r -p "[INFO] Proceed with 'git clean -xdn $(CLEAN_EXCLUDES)' ? [y/N] " ans
	case "$$ans" in \
	  y|Y|yes|YES) \
	    echo "[INFO] >>> Executing:"; \
	    git clean -xdf $(CLEAN_EXCLUDES); \
	    echo "[INFO] Done."; \
	    ;; \
	  *) \
	    echo "[INFO] Aborted."; \
	    ;; \
	esac
.PHONY: clean
