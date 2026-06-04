# dev-config

Personal development config — shell setup and AI coding-agent rules — tracked
with a **bare git repo** whose work-tree is `$HOME`. The tracked files (e.g.
`~/.zshrc`, `~/AGENTS.md`) stay as real files in their normal location — no
symlinks, no special filenames. The repo is invisible day-to-day; you only
touch it to save or pull changes.

## New machine bootstrap

Prerequisites: `git`, and an SSH key registered with GitHub (`gh auth login` or
manual key upload).

```sh
# 1. Clone the bare repo into ~/.dotfiles
git clone --bare git@github.com:hatsyio/dev-config.git "$HOME/.dotfiles"

# 2. Check out the tracked files into $HOME
#    If this fails because a file (e.g. ~/.zshrc) already exists, back it up first:
#       mkdir -p ~/.dotfiles-backup
#       git --git-dir=$HOME/.dotfiles --work-tree=$HOME checkout 2>&1 \
#         | egrep '\s+\.' | awk '{print $1}' | xargs -I{} mv {} ~/.dotfiles-backup/{}
git --git-dir=$HOME/.dotfiles --work-tree=$HOME checkout

# 3. Don't show every untracked file in $HOME as "untracked"
git --git-dir=$HOME/.dotfiles --work-tree=$HOME config --local status.showUntrackedFiles no
```

After this, your real `~/.zshrc` is in place. The shell "superpowers" it
references (oh-my-zsh, powerlevel10k, plugins) still need installing — see below.

## Shell superpowers — what `.zshrc` depends on

The `.zshrc` only *references* these; install them once per machine:

```sh
# oh-my-zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# External theme + plugins (Homebrew)
brew install powerlevel10k zsh-autosuggestions zsh-syntax-highlighting
```

Everything-as-code note: the `.zshrc` guards all optional integrations
(`[ -f … ] && source …`, `command -v … && …`) so a missing tool never breaks the
shell — the same file is safe to drop on any machine.

## Daily use

```sh
git --git-dir=$HOME/.dotfiles --work-tree=$HOME status
git --git-dir=$HOME/.dotfiles --work-tree=$HOME add ~/.zshrc
git --git-dir=$HOME/.dotfiles --work-tree=$HOME commit -m "feat: add z plugin"
git --git-dir=$HOME/.dotfiles --work-tree=$HOME push
```

## Tracked files

- `~/.zshrc` — zsh + oh-my-zsh + powerlevel10k config
- `~/AGENTS.md` — project-agnostic engineering rules for AI coding agents
- `~/README.md` — this file
