# Managing a Scientific Linux

Management of a scientific Linux station is generally a hard task. Given the always changing software versions and keeping compatibility while remaining user-friendly can be a real nightmare. Although containerization is assumed by IT people to be a reasonable solution and in practice it can solve several problems, it can also prove to be unusable from a scientific developer standpoint. It is easier to keep formatting a station for different projects (*e.g.* producing a standard image for deployment) than developping inside a container with all the associated limitations (specially graphics).

In what follows we discuss the configuration of a recent Ubuntu 22.04 instance for a single user. This version is not yet very stable but was chosen given the date of this writting and for its out-of-the-box compatibility with recent GPU drivers.

---
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

---
## Base installation

It is important to have a base operating system with a easy to use and customizable user interface. The following applications are recommended to be installed with package manager `apt`:

- `terminator`: an improved terminal experience with possibility to split the screen.
- `htop`: a better `top` alternative for checking system loading (with colors).
- `texlive-full`: the complete LaTeX distribution to avoid looking for packages later.
- `texstudio`: probably the best open source LaTeX editor.
- `podman`: an open source alternative containerization system.
- `rsync`: good disk synchronization tool for automated backups.
- `ntfs-3g`: required to mount shared NTFS drives automatically.

To install it all at once:

```
sudo apt install -y \
    terminator      \
    htop            \
    texlive-full    \
    texstudio       \
    podman          \
    rsync           \
    ntfs-3g
```

To provide a base programming system the following are recommeded:

```
sudo apt install -y \
    build-essential \
    curl            \
    git             \
    vim             \
    make            \
    cmake           \
    cmake-curses-gui\
    gcc             \
    gcc-fortran     \
    g++             \
    doxygen         \
    python3-pip     \
    pandoc
```

---
## Manual Debian packages

- `VS Code`: the state of the art open source code editor (download [here](https://code.visualstudio.com/download)).
- `jabref`: bibliography manager for LaTeX (download [here](https://downloads.jabref.org/)).
- `SALOME`: CAD system with mesh generation (download [here](https://www.salome-platform.org/?page_id=15)).

Once the packages are downloaded, install with:

```
sudo dpkg -i <package-name>.deb
```

---
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

---
## Alternative compiler suite

If for any reason an older compiler (currently the previous version is 10) is required, you can specify the version to be installed with package manager as in:

```
sudo apt install -y \
    gcc-10          \
    g++-10          \
    gfortran-10
```

To make an alternative compiler the default, run the following (replacing `<compiler>` and `<version>` as applicable):

```
sudo update-alternatives --install \
    /usr/bin/<compiler>            \
    <compiler>                     \
    /usr/bin/<compiler>-<version> 0

sudo update-alternatives --config <compiler>
```

**NOTE:** when using `nvcc` the version of alternative compiler might not be updated and that could produce unpredictable problems. Generally NVidia integration with the rest of GNU suite is quite poor.

---
## Managing NTFS mounts

To get an NTFS drive to automatically mount on Linux with `rw` permissions, an entry has to be added to `/etc/fstab` and package `ntfs-3g` is required. First one needs to discover the UUID of the partition to be mounted, which are displayed with the following

```
ls -1l /dev/disk/by-uuid/ | grep <partition>
```

For instance, to get the `UUID=26A22034A21FE3D9` of `sda2` one could run:

```
user@pc:~$ ls -1l /dev/disk/by-uuid/ | grep sda2
lrwxrwxrwx 1 root root 10 août   9 10:04 26A22034A21FE3D9 -> ../../sda2
```

Now, to automatically mount `/dev/sda2` at root directory under `/DiskSda2` one can run `sudo vim /etc/fstab` and add the following entry:

```
UUID=26A22034A21FE3D9  /DiskSda2  ntfs-3g  rw,user,auto,gid=100,uid=1000,nls=utf8,umask=002 0 0
```

Replacing the `/DiskSda2` by some other path at your convenience is generally what is needed above. Often one wishes to have all files, including external drives, mounted under `/home/<user>/` directory.

**NOTE:** if the filesystem was previously mounted on Windows, consider running `ntfsfix` and reboot once again to ensure `rw` rights.

---
## Automating backups

You can use `crontab` to ensure automatic backup (or other automations) of your system. To perform a disk mirror to some external location you can create a bash script following the template:

```bash
#!/usr/bin/env bash

# Select the verbosity level (for manual debug).
#VERB="--progress"
VERB=""

# Root of backups.
DEST="/path/to/backup/drive/"

# Path to folders to be mirrored.
SRCA="/home/<user>/"

# Perform backup and delete files only in destination.
rsync -aAX --delete ${VERB} ${SRCA} ${DESA}
```

**NOTE:** the use of a leading slash on a directory path change the behavior of `rsync`. For details run `man rsync`.

Once you have tested that the script has the expected behaviour, you can add an entry to `crontab` by running `crontab -e`. The following example runs a backup every day at 1AM:

```
  0 1  *   *   *     /path/to/backup/script.sh
```

---
## Recommended scientific applications and libraries

Generally scientific applications provided by `apt` are outdated but are much simpler to install than trying to compile them locally. The following scientific applications are suggested to be installed with it:

```
sudo apt install -y \
    paraview        \
    graphviz        \
    octave          \
    gmsh            \
    lammps          \
    syrthes         \
    code_saturn
```

**NOTE:** although `paraview` is already packaged with some versions of OpenFOAM (see below), it is necessary to have a local independent version for use with other software such as `code_saturn`.

Additionally, the following libraries are recommended:

```
sudo apt install -y        \
    libboost-all-dev       \
    petsc-dev              \
    libmetis-dev           \
    libscotchparmetis-dev  \
    libptscotch-dev        \
    libopenblas-openmp-dev \
    libcgns-dev            \
    libhdf5-dev            \
    libhdf5-openmpi-dev    \
    libfmt-dev
```

---
## Installation of OpenFOAM

There are two main OpenFOAM distributions. These differ mainly by the availability of some solvers and boundary conditions. Generally if a project or model is started with a given version, it sticks to that until completion. To install both with package manager check:

- [openfoam.org](https://openfoam.org/download/10-ubuntu/) version 10.
- [openfoam.com](https://develop.openfoam.com/Development/openfoam/-/wikis/precompiled/debian) version 2206.

---
## Install Python packages

For a scientific development environment based currently on Python 3.10, this [requirements.txt](https://github.com/WallyStuff/python-download-requirements/blob/main/requirements-prod.txt) lists a compatible set of packages. These range from physical applications to data science and general purpose. Once downloaded the file run:

```
pip3 install --user -r requirements-prod.txt
```

---