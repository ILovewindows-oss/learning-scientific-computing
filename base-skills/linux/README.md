# Managing a Scientific Linux

Management of a scientific Linux station is generally a hard task. Given the always changing software versions and keeping compatibility while remaining user-friendly can be a real nightmare. Although containerization is assumed by IT people to be a reasonable solution and in practice it can solve several problems, it can also prove to be unusable from a scientific developer standpoint. It is easier to keep formatting a station for different projects (*e.g.* producing a standard image for deployment) than developping inside a container with all the associated limitations (specially graphics).

In what follows we discuss the configuration of a recent Ubuntu 22.04 instance for a single user. This version is not yet very stable but was chosen given the date of this writting and for its out-of-the-box compatibility with recent GPU drivers.

## First steps

It is not cool to start with an outdated system. Once finished with base installation and user creation, update and upgrade system:

```
sudo apt update && sudo apt upgrade -y
```

Since the machine is intended for a single user, remove authentication every single time a `sudo` has to be issued. Assuming an user called `theuser`, run `sudo visudo` and add the following lines somewhere by the end of the text document that will be open:

```
theuser ALL=(ALL:ALL) ALL
Defaults:theuser !authenticate
```

It is a personal choice, but I don't like mounted drives in the dock. If possible, all external or extra drives will be mounted automatically at proper places I like to choose. You can remove that feature with the command:

```
gsettings set org.gnome.shell.extensions.dash-to-dock show-mounts false
```

Another default feature from Ubuntu interface that can be disabled are the default user home directories. You can redirect them to your home path (so remove the directories) by modifying `$HOME/.config/user-dirs.dirs`. In general I recommend keeping `Desktop`, `Downloads` (so that browsers work fine), and rename `Templates` to `.templates` so that it gets hidden.

## Base development



## Graphics card setup

It is generally a good practice to install the recommended GPU driver as proposed by the operating system. Automatic installation can be done in Ubuntu as follows:

```
ubuntu-drivers devices
sudo ubuntu-drivers autoinstall
```

To make changes into effect you need to `reboot` the machine. Once you log back logged in, check if it worked with `nvidia-smi` (might require `nvidia-utils-<xxx>`, where `<xxx>` denotes the driver version number as installed above). Next you can install additional NVidia features (such as Cuda support) with:

```
sudo apt update && sudo apt install -y \
    nvidia-cuda-toolkit \
    nvidia-cuda-toolkit-gcc
```
