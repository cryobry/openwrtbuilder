

# openwrtbuilder

This program will install [JRiver Media Center](https://www.jriver.com/) (JRMC) and associated services on most major Linux distros.

## Executing

`openwrtbuilder [--option [ARGUMENT]]`

Running `installJRMC` without any options will install the latest version of JRiver Media Center from the official JRiver repository (Ubuntu/Debian) or my [unofficial repository](https://repos.bryanroessler.com/jriver/) (Fedora/CentOS) using the system package manager (`--install repo`). If any other option is specified, then the default install method (i.e. `--install repo` or `--install local`) will need to be explicitly specified. This makes it possible to install services and containers independent of MC.

**Note**: As of 1.0b14 major version library migrations are performed if the destination config directory `$HOME/.jriver/Media Center XX` is missing for major release `XX`. However, it is still a good idea to create a manual library backup before migrating major versions.

## Options

```text
$ installJRMC --help
--install, -i repo|local
    repo: Install MC from repository, future updates will be handled by the system package manager
    local: Build and install MC package locally
--build[=suse|fedora|centos]
    Build RPM from source DEB but do not install
    Optionally, specify a target distro for cross-building (ex. --build=suse, note the '=')
--compat
    Build/install MC without minimum library specifiers
--mcversion VERSION
    Build or install a specific MC version, ex. "30.0.5"
--outputdir PATH
    Generate rpmbuild output in this PATH (Default: ./output)
--restorefile RESTOREFILE
    Restore file location for automatic license registration
--betapass PASSWORD
    Enter beta team password for access to beta builds
--service, -s SERVICE
    See SERVICES section below for the list of services to deploy
  --service-type user|system
      Starts services at boot (system) or user login (user) (Default: system)
--container, -c CONTAINER (TODO: Under construction)
    See CONTAINERS section below for a list of containers to deploy
--createrepo[=suse|fedora|centos]
    Build rpm, copy to webroot, and run createrepo.
    Optionally, specify a target distro for non-native repo (ex. --createrepo=fedora, note the '=')
  --createrepo-webroot PATH
      The webroot directory to install the repo (Default: /var/www/jriver/)
  --createrepo-user USER
      The web server user if different from the current user
--version, -v
    Print this script version and exit
--debug, -d
    Print debug output
--help, -h
    Print help dialog and exit
--uninstall, -u
    Uninstall JRiver MC, cleanup service files, and remove firewall rules (does not remove library or media files)
```

## Examples

* `installJRMC`

    Install the latest version of MC from the best available repository.

* `installJRMC --install local --compat`

    Install a more widely-compatible version of the latest MC (for older distros).

* `installJRMC --install repo --service jriver-mediacenter --service-type user`

    Install MC from the repository and start/enable `jriver-mediacenter.service` as a user service.

* `installJRMC --install local --compat --restorefile /path/to/license.mjr --mcversion 30.0.17`

    Build and install an MC 30.0.17 comptability RPM locally and activate it using the `/path/to/license.mjr`

* `installJRMC --createrepo --createrepo-webroot /srv/jriver/repo --createrepo-user www-user`

     Build an RPM locally for the current distro, move it to the webroot, and run createrepo as `www-user`.

* `installJRMC --service jriver-createrepo --createrepo-webroot /srv/jriver/repo --createrepo-user www-user`

    Install the jriver-createrepo timer and service to build the RPM, move it to the webroot, and run createrepo as `www-user` hourly.

* `installJRMC --install repo --service jriver-x11vnc --service jriver-mediacenter --vncpass "letmein"`

    Install services to share the existing local desktop via VNC and automatically run MC on startup.

* `installJRMC --install repo --service jriver-xvnc --display ":2"`

    Install an Xvnc server on display ':2' that starts MC.

* `installJRMC --uninstall`

    Uninstall MC and its associated services and firewall rules. This will **not** remove your media, media library/database, or automated library backup folder.

## Additional Info

Did you find `openwrtbuilder` useful? [Buy me a coffee!](https://paypal.me/bryanroessler?locale.x=en_US)

