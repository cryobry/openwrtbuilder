# openwrtbuilder

Sanely build and deploy OpenWRT images using the Image Builder (or git source)

## Usage

`openwrtbuilder [--option [VALUE]]... -p PROFILE [-p PROFILE]...`

## Options

```(text)
--profile,-p PROFILE
--release,-r,--version,-v RELEASE ("snapshot", "22.03.3")
--buildroot,-b PATH
    Default: location of openwrtbuilder script
--source
    Build image from source, not from Image Builder
--ssh-upgrade HOST
    Example: root@192.168.1.1
--ssh-backup SSH_PATH
    (Enabled by default for --ssh-upgrade)
--flash,-f DEVICE
    Example: /dev/sdX
--reset
    Cleanup all source and output files
    Can be combined with -p to reset a specific profile
--debug,-d
--help,-h
```

## Additional Info

Did you find `openwrtbuilder` useful? [Buy me a coffee!](https://paypal.me/bryanroessler?locale.x=en_US)
