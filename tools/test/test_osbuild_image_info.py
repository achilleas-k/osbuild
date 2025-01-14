import os
import subprocess as sp

import pytest

from osbuild.testutil import make_fake_tree
from osbuild.testutil.imports import import_module_from_path

osbuild_image_info = import_module_from_path("osbuild_image_info", "tools/osbuild-image-info")


@pytest.mark.parametrize("fake_tree,entries", (
    # no entries
    ({}, []),
    # one entry
    (
        {
            "/boot/loader/entries/0649288e52434223afde4c36460a375e-6.11.9-100.fc39.x86_64.conf": """title Fedora Linux (6.11.9-100.fc39.x86_64) 39 (Thirty Nine)
version 6.11.9-100.fc39.x86_64
linux /boot/vmlinuz-6.11.9-100.fc39.x86_64
initrd /boot/initramfs-6.11.9-100.fc39.x86_64.img
options root=UUID=a7e970a5-14fb-4a8a-ab09-603d1ac3fee9 ro crashkernel=auto net.ifnames=0 rhgb console=tty0 console=ttyS0,115200n8
grub_users $grub_users
grub_arg --unrestricted
grub_class fedora""",
        },
        [
            {
                "title": "Fedora Linux (6.11.9-100.fc39.x86_64) 39 (Thirty Nine)",
                "version": "6.11.9-100.fc39.x86_64",
                "linux": "/boot/vmlinuz-6.11.9-100.fc39.x86_64",
                "initrd": "/boot/initramfs-6.11.9-100.fc39.x86_64.img",
                "options": "root=UUID=a7e970a5-14fb-4a8a-ab09-603d1ac3fee9 ro crashkernel=auto net.ifnames=0 rhgb console=tty0 console=ttyS0,115200n8",
                "grub_users": "$grub_users",
                "grub_arg": "--unrestricted",
                "grub_class": "fedora",
            },
        ]
    ),
    # two entries
    (
        {
            "/boot/loader/entries/0649288e52434223afde4c36460a375e-6.11.9-100.fc39.x86_64.conf": """title Fedora Linux (6.11.9-100.fc39.x86_64) 39 (Thirty Nine)
version 6.11.9-100.fc39.x86_64
linux /boot/vmlinuz-6.11.9-100.fc39.x86_64
initrd /boot/initramfs-6.11.9-100.fc39.x86_64.img
options root=UUID=a7e970a5-14fb-4a8a-ab09-603d1ac3fee9 ro crashkernel=auto net.ifnames=0 rhgb console=tty0 console=ttyS0,115200n8
grub_users $grub_users
grub_arg --unrestricted
grub_class fedora""",
            "/boot/loader/entries/0649288e52434223afde4c36460a375e-6.11.9-101.fc39.x86_64.conf": """title Fedora Linux (6.11.9-101.fc39.x86_64) 39 (Thirty Nine)
version 6.11.9-101.fc39.x86_64
linux /boot/vmlinuz-6.11.9-101.fc39.x86_64
initrd /boot/initramfs-6.11.9-101.fc39.x86_64.img
options root=UUID=a7e970a5-14fb-4a8a-ab09-603d1ac3fee9 ro crashkernel=auto net.ifnames=0 rhgb console=tty0 console=ttyS0,115200n8
grub_users $grub_users
grub_arg --unrestricted
grub_class fedora""",
        },
        [
            {
                "title": "Fedora Linux (6.11.9-100.fc39.x86_64) 39 (Thirty Nine)",
                "version": "6.11.9-100.fc39.x86_64",
                "linux": "/boot/vmlinuz-6.11.9-100.fc39.x86_64",
                "initrd": "/boot/initramfs-6.11.9-100.fc39.x86_64.img",
                "options": "root=UUID=a7e970a5-14fb-4a8a-ab09-603d1ac3fee9 ro crashkernel=auto net.ifnames=0 rhgb console=tty0 console=ttyS0,115200n8",
                "grub_users": "$grub_users",
                "grub_arg": "--unrestricted",
                "grub_class": "fedora",
            },
            {
                "title": "Fedora Linux (6.11.9-101.fc39.x86_64) 39 (Thirty Nine)",
                "version": "6.11.9-101.fc39.x86_64",
                "linux": "/boot/vmlinuz-6.11.9-101.fc39.x86_64",
                "initrd": "/boot/initramfs-6.11.9-101.fc39.x86_64.img",
                "options": "root=UUID=a7e970a5-14fb-4a8a-ab09-603d1ac3fee9 ro crashkernel=auto net.ifnames=0 rhgb console=tty0 console=ttyS0,115200n8",
                "grub_users": "$grub_users",
                "grub_arg": "--unrestricted",
                "grub_class": "fedora",
            },
        ]
    ),
    # one entry with extra newlines
    (
        {
            "/boot/loader/entries/0649288e52434223afde4c36460a375e-6.11.9-100.fc39.x86_64.conf": """title Fedora Linux (6.11.9-100.fc39.x86_64) 39 (Thirty Nine)
version 6.11.9-100.fc39.x86_64
linux /boot/vmlinuz-6.11.9-100.fc39.x86_64
initrd /boot/initramfs-6.11.9-100.fc39.x86_64.img
options root=UUID=a7e970a5-14fb-4a8a-ab09-603d1ac3fee9 ro crashkernel=auto net.ifnames=0 rhgb console=tty0 console=ttyS0,115200n8
grub_users $grub_users
grub_arg --unrestricted
grub_class fedora

""",
        },
        [
            {
                "title": "Fedora Linux (6.11.9-100.fc39.x86_64) 39 (Thirty Nine)",
                "version": "6.11.9-100.fc39.x86_64",
                "linux": "/boot/vmlinuz-6.11.9-100.fc39.x86_64",
                "initrd": "/boot/initramfs-6.11.9-100.fc39.x86_64.img",
                "options": "root=UUID=a7e970a5-14fb-4a8a-ab09-603d1ac3fee9 ro crashkernel=auto net.ifnames=0 rhgb console=tty0 console=ttyS0,115200n8",
                "grub_users": "$grub_users",
                "grub_arg": "--unrestricted",
                "grub_class": "fedora",
            },
        ]
    ),
    # one entry with comments
    (
        {
            "/boot/loader/entries/0649288e52434223afde4c36460a375e-6.11.9-100.fc39.x86_64.conf": """title Fedora Linux (6.11.9-100.fc39.x86_64) 39 (Thirty Nine)
# this is a very useful comment
version 6.11.9-100.fc39.x86_64
linux /boot/vmlinuz-6.11.9-100.fc39.x86_64
initrd /boot/initramfs-6.11.9-100.fc39.x86_64.img
options root=UUID=a7e970a5-14fb-4a8a-ab09-603d1ac3fee9 ro crashkernel=auto net.ifnames=0 rhgb console=tty0 console=ttyS0,115200n8
# this is another very useful comment
grub_users $grub_users
grub_arg --unrestricted
grub_class fedora""",
        },
        [
            {
                "title": "Fedora Linux (6.11.9-100.fc39.x86_64) 39 (Thirty Nine)",
                "version": "6.11.9-100.fc39.x86_64",
                "linux": "/boot/vmlinuz-6.11.9-100.fc39.x86_64",
                "initrd": "/boot/initramfs-6.11.9-100.fc39.x86_64.img",
                "options": "root=UUID=a7e970a5-14fb-4a8a-ab09-603d1ac3fee9 ro crashkernel=auto net.ifnames=0 rhgb console=tty0 console=ttyS0,115200n8",
                "grub_users": "$grub_users",
                "grub_arg": "--unrestricted",
                "grub_class": "fedora",
            },
        ]
    ),
))
def test_read_boot_entries(tmp_path, fake_tree, entries):
    make_fake_tree(tmp_path, fake_tree)
    assert osbuild_image_info.read_boot_entries(tmp_path / "boot") == entries


@pytest.mark.parametrize("env,parsed", (
    ("", {}),
    ("# empty", {}),
    ("""
# COMMENT
DESKTOP_SESSION=plasma
EDITOR=/usr/bin/vim
XDG_RUNTIME_DIR=/run/user/1000
     """,
     {
         "DESKTOP_SESSION": "plasma",
         "EDITOR": "/usr/bin/vim",
         "XDG_RUNTIME_DIR": "/run/user/1000",
     }),
    ("""
DEVNAME=/dev/sda
PTUUID=56ffaa19-3d6e-ae4d-8bd5-2dc82fc6f680
PTTYPE=gpt
     """,
     {
        "DEVNAME": "/dev/sda",
        "PTUUID": "56ffaa19-3d6e-ae4d-8bd5-2dc82fc6f680",
        "PTTYPE": "gpt",
     }),
))
def test_parse_environmenr_vars(env, parsed):
    assert osbuild_image_info.parse_environment_vars(env) == parsed


@pytest.mark.parametrize("size,commands,expected", (
    (10 * 1024 * 1024, """
label: gpt
label-id: C394C8F9-5AD1-4F93-9DB7-38D5B7E07672
start="2048", size="2048", type="21686148-6449-6E6F-744E-656564454649", uuid="320D5AD6-C760-46BD-9B92-60A0CE8F07DC"
start="4096", size="8053", type="E6D6D379-F507-44C2-A23C-238F2A3DF928", uuid="626E6AD4-2AF9-4179-9B14-6222A57DD075"
start="12149", size="2048", type="0FC63DAF-8483-4772-8E79-3D69D8477DE4", uuid="F32F152B-CA55-439D-8330-F78977451C45"
    """,
     {
         "partition-table": "gpt",
         "partition-table-id": "C394C8F9-5AD1-4F93-9DB7-38D5B7E07672",
         "partitions": [
             {
                 'bootable': False,
                 'partuuid': '320D5AD6-C760-46BD-9B92-60A0CE8F07DC',
                 'size': 1048576,
                 'start': 1048576,
                 'type': '21686148-6449-6E6F-744E-656564454649',
             },
             {
                 'bootable': False,
                 'partuuid': '626E6AD4-2AF9-4179-9B14-6222A57DD075',
                 'size': 4123136,
                 'start': 2097152,
                 'type': 'E6D6D379-F507-44C2-A23C-238F2A3DF928',
             },
             {
                 'bootable': False,
                 'partuuid': 'F32F152B-CA55-439D-8330-F78977451C45',
                 'size': 1048576,
                 'start': 6220288,
                 'type': '0FC63DAF-8483-4772-8E79-3D69D8477DE4',
             },
         ],
     }),
))
def test_read_partition_table(tmp_path, size, commands, expected):
    disk_path = tmp_path / "disk.raw"
    disk_path.write_bytes(b"")
    os.truncate(disk_path, size)

    sp.run(["sfdisk", "--no-tell-kernel", disk_path], input=commands, encoding="utf-8", check=True)
    assert osbuild_image_info.read_partition_table(disk_path) == expected
