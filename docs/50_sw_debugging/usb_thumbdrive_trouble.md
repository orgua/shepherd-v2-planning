# USB Flash-Drive storage troubles

## TLDR

Thumb-drive was the culprit - it got not even warm, but refused to take additional data after first ~ 200 mb. Even Syncs in between confirmed that writing was done up to this point...

## Problem

Saving measurement-data to usb thumb-drives seems to trigger a chain-reaction with high cpu-load and missed sample-buffers.

System:

- BBone Black
- Philips 256 GB USB 3.0 Thumb-drives

expected suspects:

- py-code
- faulty kernel-driver for usb
- bad thumb-drive

## Bug in more Detail

Used code:

```Shell
sudo shepherd-sheep -vv run --config /etc/shepherd/example_config_harvest.yml
sudo shepherd-sheep -vv run --config /etc/shepherd/example_config_emulation.yml
# used 600 s db_traces.h5 as input, 521 mb, 870 kb/s
```

- flash drive contains source and destination, 180 s worked, 600 s failed after 293 s (run out of buffers), 224 mb
- failing because of full msg-fifo, with cpu-usage of ~ 86 %, no significant ram or nw usage
- despite mount-option "commit=2" the data is written every ~ 20 to 30 s with peek rates of 12-21 mb/s
  - h5py-trouble? ⇾ changed h5.driver to stdio and _nslots from 521 to 100, without success
  - smaller write cache ⇾ worse performance (~ 230 s), but sysutil shows
    - source: <https://unix.stackexchange.com/questions/292024/how-to-reduce-linux-write-buffer-for-removable-devices>
    - sudo echo 5000000 > /proc/sys/vm/dirty_bytes ⇾ 5 mb instead of 200 ? or 20% ram-ratio ⇾ 93 mb
    - echo 300 > /proc/sys/vm/dirty_expire_centisecs    ⇾ 3 s instead of 30
  - bigger write cache ⇾ no difference (~ 280 s)
    - echo 300000000 > /proc/sys/vm/dirty_bytes
    - echo 6000 > /proc/sys/vm/dirty_expire_centisecs
- just heat-throttling? 150 mA * 5V = 0.75 W in a plastic case ⇾ opened and cooled a stick
- usb-errors? the flash drive seems to be the troublemaker ⇾ even on other systems it shows a wavy write-trend
- lower cpu-usage does not work (mean ~ 80 %, instead of ~86% with monitors)
- **reading from mmc, writing to flash drive ⇾ failed also**

## Linux-Optimizations for file-writes

Adding Flash drive

- power-increase from 322 mA to 387 mA (passive), ~590 mA (active)
- detected as philips USB Flash Drive, high speed, usb mass storage,
- 512-byte logical blocks, 231 GiB, Mode Sense 45 00 00 00, write cache disabled, read cache enabled, doesn't support DPO or FUA
- DPO: Disable Page out -
- FUA: Force unit access - FUA write command will not return until data is written to media, thus data written by a completed FUA write command is on permanent media
- run playbook "setup-ext-storage" with mod for sda1 ⇾ fails because of "p1"-addition

Getting storage ready, by following tutorials:

- <https://www.thegeekdiary.com/what-are-the-mount-options-to-improve-ext4-filesystem-performance-in-linux/>
- <https://www.linuxliteos.com/forums/tutorials/fast-disk-io-with-ext4-howto/>

```Shell
sudo umount -f -v /dev/sda1
sudo mkfs.ext4 -F /dev/sda1
add to /etc/fstab:
/dev/sda1  /var/shepherd/recordings  ext4  defaults,noiversion,auto_da_alloc,noatime,errors=continue,commit=20,inode_readahead_blks=64,delalloc,barrier=0,data=writeback,noexec,nosuid,lazytime,noacl,nouser_xattr,users,noauto  0  0
sudo chmod 777 /var/shepherd/recordings
sudo mount -a
sudo mount /dev/sda1
sudo chmod 777 /var/shepherd/recordings
sudo chown hans /var/shepherd/recordings

mount -t ext4 -o defaults,noiversion,auto_da_alloc,noatime,errors=continue,commit=20,\
inode_readahead_blks=64,delalloc,barrier=0,data=writeback,noexec,nosuid,lazytime,\
noacl,nouser_xattr,users /dev/sda1 /var/shepherd/recordings
```

Meaning of mount-options

| option                  | description                                                                                                                                             |
|-------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| noiversion              | no tracking of inode-modifications                                                                                                                      |
| auto_da_alloc           | avoids the "zero-length" problem                                                                                                                        |
| noatime                 | no tracking of access-time                                                                                                                              |
| errors=remount-ro       | Seems not optimal (TODO: changed to continue for now)                                                                                                   |
| commit=20               | number of seconds for each data and meta data sync (default=5)                                                                                          |
| inode_readahead_blks=64 | pre-read into buffer cache (default=32)                                                                                                                 |
| delalloc                | Deferring block allocation until write-out time                                                                                                         |
| barrier=0               | Write barriers are used to enforce proper on-disk ordering of journal commits, they will degrade the performance of the file system (default = 1)       |
| discard                 | enable trim for ssd (TODO: not for our usb drive)                                                                                                       |
| data=writeback          | data ordering will not be preserved, data may be written to the file system after its metadata has been committed to the journal (default data=ordered) |
| noexec                  | Do not allow execution of any binaries                                                                                                                  |
| nosuid                  | Do not allow set-user-identifier or set-group-identifier bits to take effect.                                                                           |
| extent                  | more efficient mapping of logical blocks (TODO: seems to be no real option)                                                                             |
| lazytime                | reduces writes to inode table for random writes to preallocated files                                                                                   |
| noacl                   | disable access control lists (todo: is marked deprecated)                                                                                               |
| nouser_xattr            | disable Extended User Attributes (todo: is marked deprecated)                                                                                           |
| users                   | FSTAB, allows mount and umount without sudo                                                                                                             |
| noauto                  | FSTAB, disable auto-mount                                                                                                                               |
| async                   | should already be default                                                                                                                               |
