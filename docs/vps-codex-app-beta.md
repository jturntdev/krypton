# Krypton VPS Codex App Beta

Use this guide when you want a Linux VPS to be the machine that runs the work
while Codex App on your Mac or Windows machine controls it over SSH.

The target shape is simple:

```text
Codex App on your computer -> SSH alias -> VPS
VPS -> repo, Codex CLI, tools, builds, tests, tmux/cmux, dev servers
GitHub -> code source of truth
Local config and secrets -> explicit, selected setup only
```

Do not install or describe the desktop Codex App as running on the VPS. The VPS
needs the Codex CLI and your project toolchain so Codex App can start the remote
Codex app server through SSH.

## Start With The Setup State

Codex should ask:

```text
Do you already have a VPS with SSH access, or are we starting before the VPS is
created?
```

If there is no VPS yet, provision one first. Recommended baseline:

- Ubuntu 24.04 LTS unless your project needs something else.
- Non-root daily user with sudo.
- SSH key auth.
- Password SSH disabled after key auth is confirmed.
- Firewall limited to SSH unless you intentionally expose something else.
- Enough CPU, memory, disk, and swap for your project builds and agent sessions.

If the provider starts you as `root`, use it only for bootstrap. Create or use a
non-root daily user before normal Codex work.

## Create The SSH Alias

Codex App discovers concrete aliases from `~/.ssh/config`. Codex should show the
snippet and ask before editing the file.

```sshconfig
Host krypton-vps
  HostName 203.0.113.10
  User dev
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes
  ServerAliveInterval 30
  ServerAliveCountMax 3
```

Prove it from the computer running Codex App:

```bash
ssh krypton-vps 'hostname; whoami; pwd'
```

## Install The VPS Toolchain

Install the tools your repo actually needs. A typical agent box needs:

- `git`
- `gh`
- `curl`
- `jq`
- `python3`
- `rg`
- `build-essential`
- `tmux`
- `unzip`
- `node`
- `corepack`
- `pnpm`
- Docker and Compose when your project needs containers
- `cmux` when your workflow uses it
- Codex CLI, installed through the current official path

Do not guess project install commands. Read the repo README, package manager
files, and setup docs first.

## Authenticate Codex On The VPS

The remote shell must find `codex`:

```bash
ssh krypton-vps '$SHELL -lc "command -v codex && codex --version"'
```

For headless login, prefer device auth when available:

```bash
ssh krypton-vps
codex login --device-auth
```

If you copy `~/.codex/auth.json`, treat it like a password. Never paste it in
chat, commit it, or print its contents.

## Choose The GitHub Code Path

Codex should ask:

```text
Do you want GitHub to be the source of truth for this VPS checkout? That is the
recommended path. It keeps code transfer clean, repeatable, and reviewable.
```

Then choose one access path:

- GitHub CLI login: best for normal development, private repo access, issues,
  PRs, and pushes from the VPS.
- Account SSH key: good for a personal dev VPS, but it can access every repo the
  account can access.
- Read-only deploy key: best for cloning one private repo with least privilege.
  It cannot push branches unless write access is explicitly enabled.
- Public HTTPS clone: fine for public repos.
- `rsync` or archive from the Mac: fallback when the code is not in GitHub.

Do not paste GitHub tokens into chat. Do not put tokens in Git remote URLs.

### GitHub CLI Path

```bash
ssh krypton-vps
gh auth login
gh auth status
mkdir -p ~/src
gh repo clone ORG/REPO ~/src/REPO
cd ~/src/REPO
```

### SSH Key Path

```bash
ssh krypton-vps
ssh-keygen -t ed25519 -C "krypton-vps" -f ~/.ssh/github-krypton-vps
cat ~/.ssh/github-krypton-vps.pub
```

Add the printed public key to GitHub as an account SSH key or as a repo deploy
key. Then prove access and clone:

```bash
ssh -T git@github.com
mkdir -p ~/src
git clone git@github.com:ORG/REPO.git ~/src/REPO
cd ~/src/REPO
```

## Handle Local Config Separately

Codex should ask:

```text
Do you want to recreate local config on the VPS from examples, copy selected
ignored files from this machine, or skip local config for now?
```

Use this order:

1. Recreate config from checked-in examples like `.env.example`, README setup,
   or project docs.
2. Copy selected ignored files only when you approve the exact files.
3. Skip secrets until the app tells you what is missing.

Safe selected-file copy:

```bash
rsync -av --chmod=F600,D700 .env.local krypton-vps:~/src/REPO/.env.local
```

Do not bulk-copy your home directory, `.ssh`, `.codex`, browser profiles,
`node_modules`, build outputs, caches, private keys, or random dotfiles.

## Connect Codex App

On the computer running Codex App:

1. Open Codex App.
2. Open Settings > Connections.
3. Add or enable the SSH alias.
4. Choose the remote project folder, such as `~/src/REPO`.
5. Start a thread in that remote project.

This is a user-operated app step unless the current Codex session has explicit
desktop/app-control tools and you ask it to use them.

First proof prompt:

```text
Run pwd, hostname, whoami, command -v codex, codex --version, git status --short,
and do not modify files.
```

The result should show the VPS hostname, the remote repo path, a working Codex
binary, and a clean or understood Git state.

## Use SSH Port Forwarding For Browser Proof

Run the dev server on the VPS and inspect it from your local browser through an
SSH tunnel:

```bash
ssh -L 3000:127.0.0.1:3000 krypton-vps
```

Then open:

```text
http://127.0.0.1:3000
```

Do not expose private dev servers, databases, dashboards, Docker sockets, or
Codex app-server ports to the public internet.

## Audit The Setup

From this repo:

```bash
skills/krypton-vps-codex-app/scripts/audit-vps-codex-app.sh \
  --host krypton-vps \
  --repo-url git@github.com:ORG/REPO.git \
  --repo-path ~/src/REPO
```

The audit is read-only. It checks SSH reachability, Linux/Ubuntu details,
required tools, Codex CLI path, Codex auth-cache presence without printing
secrets, GitHub repo reachability, repo state, root-user risk, and common
agent-workflow tools.

Passing this audit does not prove the Codex App UI connection by itself. Finish
with a real Codex App remote-thread proof.
