# dev-config

Personal development config — shell setup and AI coding-agent rules. Public on
purpose: grab whole files or just the bits you want.

## Quick start on a new machine

Pull the files you want straight from raw GitHub — take all of them, or
cherry-pick:

```sh
# zsh config
curl -fsSL https://raw.githubusercontent.com/hatsyio/dev-config/main/.zshrc -o ~/.zshrc

# AI coding-agent rules
curl -fsSL https://raw.githubusercontent.com/hatsyio/dev-config/main/AGENTS.md -o ~/AGENTS.md
```

Or open the raw files in a browser and copy only the parts you care about:

- <https://raw.githubusercontent.com/hatsyio/dev-config/main/.zshrc>
- <https://raw.githubusercontent.com/hatsyio/dev-config/main/AGENTS.md>

> Heads-up: `.zshrc` contains a few machine-specific paths (e.g. the gcloud
> credentials path under `$HOME`). After copying, adjust those to your machine.

## Fresh installation

On a brand-new machine, install these once — in order. The `.zshrc` expects
powerlevel10k and the two plugins to live in oh-my-zsh's `custom` dir (it loads
them by name), so they are git-cloned there, not installed via brew.

```sh
# 1. Homebrew (package manager — install first)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. zsh (ships with modern macOS; install to be sure, then set as default shell)
brew install zsh
chsh -s "$(which zsh)"

# 3. oh-my-zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# 4. powerlevel10k theme (into oh-my-zsh custom themes)
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git \
  "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k"

# 5. zsh plugins (into oh-my-zsh custom plugins)
git clone https://github.com/zsh-users/zsh-autosuggestions \
  "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-autosuggestions"
git clone https://github.com/zsh-users/zsh-syntax-highlighting \
  "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting"

# 6. VS Code
brew install --cask visual-studio-code

# 7. pnpm — Node package manager AND Node version manager (replaces nvm).
#    Install via the standalone script, NOT Homebrew: only the standalone
#    install lets pnpm manage Node versions (`pnpm env`). A Homebrew-installed
#    pnpm errors with ERR_PNPM_CANNOT_MANAGE_NODE.
curl -fsSL https://get.pnpm.io/install.sh | sh -
pnpm env use --global lts   # install the current Node LTS, managed by pnpm

# 8. uv — Python package and version manager (replaces pyenv + poetry)
brew install uv
uv python install --default 3.12   # uv-managed global python/python3 in ~/.local/bin
#   `--default` is experimental in uv 0.11. The .zshrc prepends ~/.local/bin so
#   this python3 wins over Homebrew's. Per project, prefer `uv python pin` + `uv venv`.
```

The `.zshrc` guards every optional integration (`[ -f … ] && source …`,
`command -v … && …`), so anything not installed simply no-ops — the same file is
safe to drop on any machine.

## Files

- `.zshrc` — zsh + oh-my-zsh + powerlevel10k config
- `AGENTS.md` — project-agnostic engineering rules for AI coding agents
- `vscode-profiles/` — exported VS Code profiles: Default, Python, Node.js (see [VS Code profiles](#vs-code-profiles))
- `zsh-plugins.txt` — inventory of the oh-my-zsh plugins enabled in `.zshrc` (see [oh-my-zsh plugins](#oh-my-zsh-plugins))
- `README.md` — this file

## VS Code profiles

The editor is tracked as three exported VS Code **profiles** under
`vscode-profiles/` — each a self-contained bundle of extensions, settings, and
keybindings. Profiles are the source of truth for the editor; there is no flat
extension list.

| Profile | File | Purpose |
| --- | --- | --- |
| Default | `vscode-profiles/Default.code-profile` | General / infra / ops — DevOps, IaC, containers, Kubernetes, docs |
| Python | `vscode-profiles/Python.code-profile` | Python development (ruff + uv) |
| Node.js | `vscode-profiles/Node.js.code-profile` | JavaScript / TypeScript development (pnpm) |

### Importing a profile

In VS Code: **Cmd+Shift+P → `Profiles: Import Profile...`**, then select the
`.code-profile` file (or paste its raw GitHub URL). VS Code recreates the
profile with its extensions and settings; switch to it from the gear menu
(bottom-left) → **Profiles**.

### Shared baseline

Every profile carries this common set — VS Code profiles don't inherit, so it is
duplicated in each by design:

- `eamodio.gitlens` — supercharges Git: inline blame, history, authorship, and repo insights.
- `github.vscode-github-actions` — author, run, and monitor GitHub Actions workflows from the editor.
- `ms-azuretools.vscode-containers` — Container Tools: manage containers, images, volumes, and networks.
- `docker.docker` — Docker DX: Dockerfile / Compose / Bake authoring, linting, and IntelliSense.
- `hashicorp.terraform` — Terraform / HCL syntax, validation, IntelliSense, and formatting.
- `ms-vscode-remote.remote-ssh` — develop on a remote machine over SSH.
- `ms-vscode-remote.remote-ssh-edit` — editing support for SSH config files.
- `ms-vscode-remote.remote-containers` — develop inside a dev container.
- `ms-vscode.remote-explorer` — unified sidebar for remote targets (SSH hosts, containers, tunnels).
- `ms-vscode.remote-server` — backing server component for remote / tunnel sessions.
- `redhat.vscode-yaml` — YAML language support with schema validation and autocompletion.
- `mikestead.dotenv` — syntax highlighting for `.env` files.
- `davidanson.vscode-markdownlint` — Markdown linting and style checking.
- `yzhang.markdown-all-in-one` — Markdown editing: TOC, shortcuts, list editing, preview, tables.
- `hediet.vscode-drawio` — edit draw.io / diagrams.net diagrams directly in the editor.
- `sonarsource.sonarlint-vscode` — on-the-fly static analysis for bugs, code smells, and security issues.
- `usernamehw.errorlens` — inline display of diagnostics (errors/warnings) right on the line.
- `streetsidesoftware.code-spell-checker` — spell checking for code and prose (camelCase-aware).
- `editorconfig.editorconfig` — applies `.editorconfig` rules (indentation, charset, EOL) per project.
- `aaron-bond.better-comments` — color-codes comment types (TODO, alerts, queries, highlights).
- `christian-kohler.path-intellisense` — autocompletes filesystem paths in imports and strings.
- `zhuangtongfa.material-theme` — "One Dark Pro" color theme.
- `vscode-icons-team.vscode-icons` — file/folder icon theme.
- `ms-ceintl.vscode-language-pack-es` — Spanish (Español) UI localization.

### Default profile — extras

On top of the baseline:

- `anthropic.claude-code` — Claude Code agent inside VS Code: run and manage agentic coding sessions.
- `ms-kubernetes-tools.vscode-kubernetes-tools` — browse clusters, manage workloads, edit/apply manifests, Helm.
- `mechatroner.rainbow-csv` — colorizes CSV/TSV columns and runs SQL-like queries over them.

### Python profile — extras

On top of the baseline:

- `ms-python.python` — core Python: debugging, interpreter / env selection, test discovery.
- `ms-python.vscode-pylance` — fast IntelliSense and type checking.
- `ms-python.debugpy` — the Python debugger.
- `ms-python.vscode-python-envs` — environment management; detects `uv`-created virtual envs.
- `charliermarsh.ruff` — lint, format, and import sorting (replaces Black + isort).
- `njpwerner.autodocstring` — generate docstring stubs from signatures.
- `tamasfe.even-better-toml` — TOML support (`pyproject.toml`, etc.).
- `inferrinizzard.prettier-sql-vscode` — SQL formatter for embedded / standalone SQL.

### Node.js profile — extras

On top of the baseline:

- `dbaeumer.vscode-eslint` — ESLint integration (uses each project's config).
- `esbenp.prettier-vscode` — Prettier formatting.
- `orta.vscode-jest` — Jest test runner integration.
- `humao.rest-client` — send HTTP requests from `.http` files.
- `pflannery.vscode-versionlens` — shows latest dependency versions inline in `package.json`.

## oh-my-zsh plugins

`zsh-plugins.txt` is the inventory of the plugins enabled in the `plugins=(…)`
array of `.zshrc`. Most are bundled with oh-my-zsh and activate automatically
once listed — no install step. The two **custom** plugins are the exception:
they are git-cloned into `$ZSH_CUSTOM` (see [Fresh installation](#fresh-installation)).

pnpm has no oh-my-zsh plugin; its shell completion is wired directly in `.zshrc`
(generated via `pnpm completion zsh` and cached on first run).

What each one does, grouped by purpose:

### Git & GitHub

- `git` — aliases and helper functions for common Git workflows.
- `gitignore` — generate `.gitignore` files from gitignore.io templates (`gi` command).
- `gh` — completions for the GitHub CLI.

### Cloud, infra & containers

- `gcloud` — completions for the Google Cloud SDK (`gcloud`).
- `kubectl` — `kubectl` aliases and completion.
- `docker` — Docker CLI completion and aliases.
- `terraform` — Terraform completion and prompt info.

### Shell productivity & navigation

- `z` — jump to frequently used directories by frecency.
- `extract` — single `extract` command that unpacks any archive type.
- `globalias` — expand global aliases inline by pressing space.
- `history-substring-search` — type a substring, then arrow up/down through matching history.
- `direnv` — hooks direnv to auto-load/unload per-directory environments.
- `command-not-found` — suggests the package to install when a command isn't found.

### macOS & system

- `macos` — macOS helpers (`ofd`, `cdf`, `pfd`, Finder/Spotlight integration).
- `brew` — Homebrew aliases and completion.
- `colored-man-pages` — adds color to man pages.

### Custom (git-cloned into `$ZSH_CUSTOM`)

- `zsh-autosuggestions` — fish-like inline command suggestions drawn from history.
- `zsh-syntax-highlighting` — real-time syntax highlighting of the command line.

## How this repo is maintained

The files live at `$HOME` and are tracked with a **bare git repo** at
`~/.dotfiles` whose work-tree is `$HOME` — so they stay real files in place, no
symlinks. Day-to-day, the repo is invisible; drive it with the full git form:

```sh
git --git-dir=$HOME/.dotfiles --work-tree=$HOME status
git --git-dir=$HOME/.dotfiles --work-tree=$HOME add ~/.zshrc
git --git-dir=$HOME/.dotfiles --work-tree=$HOME commit -m "feat: add z plugin"
git --git-dir=$HOME/.dotfiles --work-tree=$HOME push
```

To re-create that maintenance setup on a new machine (rather than just copying
files), clone the repo bare and check it out into `$HOME`:

```sh
git clone --bare git@github.com:hatsyio/dev-config.git "$HOME/.dotfiles"
git --git-dir=$HOME/.dotfiles --work-tree=$HOME checkout
git --git-dir=$HOME/.dotfiles --work-tree=$HOME config --local status.showUntrackedFiles no
```
