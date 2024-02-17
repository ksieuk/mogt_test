NENV = node_modules
PRETTIER = $(NENV)/.bin/prettier

SHELL = /bin/bash
.PHONY: init
init:
	@echo 'Installing node version...'
	@. $(HOME)/.nvm/nvm.sh && nvm install

	@echo 'Installing node dependencies...'
	@npm install

	@echo 'Installing husky pre-commit...'
	@npm run prepare-husky

.PHONY: lint
lint:
	@echo 'Running prettier checks...'
	@$(PRETTIER) --check .

.PHONY: lint-fix
lint-fix:
	@echo 'Running prettier auto-fixes...'
	@$(PRETTIER) --write .

.PHONY: test
test:
	@echo 'Running tests...'

.PHONY: clean
clean:
	@echo 'Cleaning up node dependencies...'
	@rm -rf $(NENV)

	@$(foreach package, $(sort $(wildcard src/*)), \
		echo "Cleaning $(package)..."; \
		make -C $(package) clean || exit 1; \
	)

# Commands for every package

.PHONY: all-init
all-init:
	@$(foreach package, $(sort $(wildcard src/*)), \
		echo "Initializing $(package)..."; \
		make -C $(package) init || exit 1; \
	)

.PHONY: all-lint
all-lint:
	@$(foreach package, $(sort $(wildcard src/*)), \
		echo "Linting $(package)..."; \
		make -C $(package) lint || exit 1; \
	)

.PHONY: all-lint-fix
all-lint-fix:
	@$(foreach package, $(sort $(wildcard src/*)), \
		echo "Fixing lint issues for $(package)..."; \
		make -C $(package) lint-fix || exit 1; \
	)

.PHONY: all-test
all-test:
	@$(foreach package, $(sort $(wildcard src/*)), \
		echo "Testing $(package)..."; \
		make -C $(package) test || exit 1; \
	)

.PHONY: all-clean
all-clean:
	@$(foreach package, $(sort $(wildcard src/*)), \
		echo "Cleaning $(package)..."; \
		make -C $(package) clean || exit 1; \
	)

.PHONY: all-dependencies-update
all-dependencies-update:
	@$(foreach package, $(sort $(wildcard src/*)), \
		echo "Updating dependencies for $(package)..."; \
		make -C $(package) dependencies-update || exit 1; \
	)

# CI-specific

.PHONY: ci-init
ci-init:
	@echo 'Installing node dependencies...'
	@npm install
