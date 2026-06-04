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

## Shell superpowers — what `.zshrc` depends on

`.zshrc` only *references* these; install them once per machine:

```sh
# oh-my-zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# External theme + plugins (Homebrew)
brew install powerlevel10k zsh-autosuggestions zsh-syntax-highlighting
```

The config guards every optional integration (`[ -f … ] && source …`,
`command -v … && …`), so a missing tool never breaks the shell — the same file
is safe to drop on any machine.

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
