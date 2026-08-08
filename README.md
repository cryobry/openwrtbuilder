# openwrtbuilder

Build and deploy OpenWRT images using shell-style device profiles, via source code or the official Image Builder.

## Usage

`openwrtbuilder [OPTION [VALUE]]... -p PROFILE [-p PROFILE]...`

## Options

```(text)
--profile,-p PROFILE
--release,-r,--version,-v RELEASE ("snapshot", "22.03.3")
--buildroot,-b PATH (Default: script directory)
--cpus,-c NUM
	Default: # of host CPUS minus 1
--mode,-m imagebuilder|source
  Default: imagebuilder
--clean clean|targetclean|dirclean|distclean
  Optional clean step for source mode
--ssh-upgrade HOST
  Example: root@192.168.1.1
--ssh-backup SSH_PATH
  Enabled by default for --ssh-upgrade
--flash,-f DEVICE
  Example: /dev/sdX
--reset
  Cleanup all source and output files
  Can be combined with -p to reset a specific profile
--depends
  Force dependency installation
--yes,-y
  Assume yes for all questions (automatic mode)
--debug,-d
--help,-h
```

## Profiles

See `profiles` for example device profile definitions. Multiple `--profile` can be passed at once.

The default build mode is  `imagebuilder` unless `--mode=source` is passed. Default profile modes can be set individually in `profiles`.

`--mode=imagebuilder` inherits `CONFIG_TARGET_ROOTFS_PARTSIZE=`, but all other kconfigs only work in `--mode=source`. 

Profile keys:

| Key | Required | Description |
|---|---|---|
| `mode` | No | Build mode for this profile: `imagebuilder` or `source`. CLI `--mode` overrides profile value. |
| `device` | Yes | OpenWrt device/profile id used by build commands (for example `friendlyarm_nanopi-r4s`). |
| `target` | Yes | OpenWrt target/subtarget (for example `rockchip/armv8`, `x86/64`). |
| `filesystem` | No | Root filesystem type (`squashfs`, `ext4`, etc). Defaults to `squashfs`. |
| `packages` | No | Space-separated package list. Prefix with `-` to remove a package in Image Builder or source config generation. |
| `kconfigs` | No | Space-separated Kconfig symbols. In `imagebuilder` mode only `CONFIG_TARGET_ROOTFS_PARTSIZE=<MB>` is used (mapped to `ROOTFS_PARTSIZE`). In `source` mode all entries are written to `.config` seed. |
| `files` | No | Host directory containing custom overlay files. In `imagebuilder` mode this is passed as `FILES=<dir>`. In `source` mode contents are synced into `<build dir>/files/` before build. Defaults to `<buildroot>/src/files`. |
| `cherrypicks` | No | Space-separated source-mode cherry-picks in `URL@branch:commit` form. The target is inferred from the repo basename: `openwrt` applies to the main source tree, any other basename applies to `feeds/<basename>` after feeds update/install. |
| `branches` | No | Space-separated `URL@branch` entries to merge into the source worktree in `source` mode. |
| `release` | No | Default release/ref for the profile (for example `snapshot`, `25.12.5`). CLI `--release` overrides it. |
| `clean` | No | Optional source cleanup step (`clean`, `targetclean`, `dirclean`, `distclean`). CLI `--clean` overrides it. |
| `repo` | No | Extra Image Builder repository line appended to `repositories.conf` before build. |

Notes:

* The profile file uses associative arrays (`declare -Ag name=( [key]="value" ... )`).
* `packages`, `kconfigs`, `cherrypicks`, and `branches` are parsed as scalar whitespace-separated strings.
* `cherrypicks` entries always use `URL@branch:commit` format; target selection is automatic from repo basename.
* If a profile-specific `files` path is configured, it must exist.

## Examples

* `openwrtbuilder -p r4s -p ax6000`
* `openwrtbuilder -p r4s -r snapshot --debug`
* `openwrtbuilder -p ax6000 -r 25.12.5 --mode source --debug`
* `openwrtbuilder -p rpi4 -r 25.12.5 --flash /dev/sdX`
* `openwrtbuilder -p linksys -r snapshot --ssh-upgrade root@192.168.1.1`

## Additional Info

Find `openwrtbuilder` useful? [Paypal me a coffee!](https://paypal.me/bryanroessler)

[↓ ↓ ↓ Bitcoin ↓ ↓ ↓](bitcoin:bc1q7wy0kszjavgcrvkxdg7mf3s6rh506rasnhfa4a)

[![Bitcoin](https://repos.bryanroessler.com/files/bc1q7wy0kszjavgcrvkxdg7mf3s6rh506rasnhfa4a.png)](bitcoin:bc1q7wy0kszjavgcrvkxdg7mf3s6rh506rasnhfa4a)
