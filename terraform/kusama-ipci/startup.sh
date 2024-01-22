#!/bin/bash


if sudo blkid /dev/sdb;then 
        exit
else 
        sudo mkfs.ext4 -m 0 -F -E lazy_itable_init=0,lazy_journal_init=0,discard /dev/sdb; \
        sudo mkdir -p /mnt/base
        sudo mount -o discard,defaults /dev/sdb /mnt/base
fi