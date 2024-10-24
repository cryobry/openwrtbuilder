# openwrtbuilder

Sanely build and deploy OpenWRT images using the Image Builder or from source code.

## Usage

`openwrtbuilder [--option [VALUE]]... -p PROFILE [-p PROFILE]...`

## Options

```(text)
--profile,-p PROFILE
--release,-r,--version,-v RELEASE ("snapshot", "22.03.3")
--buildroot,-b PATH (Default: script directory)
--source
  Build image from source, not from Image Builder
  Allows make config options to be passed in profile
--ssh-upgrade HOST
  Example: root@192.168.1.1
--ssh-backup SSH_PATH
  Enabled by default for --ssh-upgrade
--flash,-f DEVICE
  Example: /dev/sdX
--reset
  Cleanup all source and output files
  Can be combined with -p to reset a specific profile
--yes,-y
  Assume yes for all questions (automatic mode)
--debug,-d
--help,-h
```

## Profiles

See `./profiles` for example device profile definitions.

## Examples

* `./openwrtbuilder -p r4s -r snapshot --debug`
* `./openwrtbuilder -p ax6000 -r 23.05.5 --source --debug`
* `./openwrtbuilder -p rpi4 -r 23.05.5 --flash /dev/sdX`
* `./openwrtbuilder -p linksys -r snapshot --ssh-upgrade root@192.168.1.1`

## Additional Info

Did you find `openwrtbuilder` useful? [Buy me a coffee!](https://paypal.me/bryanroessler)
