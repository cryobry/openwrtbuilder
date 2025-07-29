# openwrtbuilder

Build and deploy OpenWRT images using shell-style device profiles, via source code or the official Image Builder.

## Usage

`openwrtbuilder [OPTION [VALUE]]... -p PROFILE [-p PROFILE]...`

## Options

```(text)
--profile,-p PROFILE
--release,-r,--version,-v RELEASE ("snapshot", "22.03.3")
--buildroot,-b PATH (Default: script directory)
--source
  Build image from source, not from Image Builder
  Allows make config options to be passed in profile
  Uses git worktree for multi-profile deduplication
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
  Ignores .dependencies files
--yes,-y
  Assume yes for all questions (automatic mode)
--debug,-d
--help,-h
```

## Profiles

See `profiles` for example device profile definitions. Multiple `--profile` can be passed at once.

The default build mode is  `imagebuilder` unless `--source` is passed. Default profile modes can be set individually in `profiles`.

## Examples

* `openwrtbuilder -p r4s -p ax6000`
* `openwrtbuilder -p r4s -r snapshot --debug`
* `openwrtbuilder -p ax6000 -r 23.05.5 --source --debug`
* `openwrtbuilder -p rpi4 -r 23.05.5 --flash /dev/sdX`
* `openwrtbuilder -p linksys -r snapshot --ssh-upgrade root@192.168.1.1`

## Additional Info

Find `openwrtbuilder` useful? [Paypal me a coffee!](https://paypal.me/bryanroessler)

[↓ ↓ ↓ Bitcoin ↓ ↓ ↓](bitcoin:bc1q7wy0kszjavgcrvkxdg7mf3s6rh506rasnhfa4a)

[![Bitcoin](https://repos.bryanroessler.com/files/bc1q7wy0kszjavgcrvkxdg7mf3s6rh506rasnhfa4a.png)](bitcoin:bc1q7wy0kszjavgcrvkxdg7mf3s6rh506rasnhfa4a)
