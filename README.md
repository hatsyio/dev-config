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
```

The `.zshrc` guards every optional integration (`[ -f … ] && source …`,
`command -v … && …`), so anything not installed simply no-ops — the same file is
safe to drop on any machine.

## Files

- `.zshrc` — zsh + oh-my-zsh + powerlevel10k config
- `AGENTS.md` — project-agnostic engineering rules for AI coding agents
- `README.md` — this file

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
