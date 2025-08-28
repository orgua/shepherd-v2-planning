# Debug kernel panics caused by the kernel module

**TLDR**: use-after-free race condition

## Problem

System crashes while unloading the module - currently more often than before.

What changed?

https://github.com/nes-lab/shepherd/compare/orgua:shepherd:main...orgua:shepherd:dev?diff=unified

## Listen to kernel errors

- connect uart adapter, or logic analyzer to pin 5 of J1 (Header above P9)
- listen with 115200 kbaud/s

## Triggering a panic

```Shell
sudo modprobe -rf shepherd
sudo modprobe -a shepherd
```

## Log of a panic

```
[  942.541300] Unable to handle kernel NULL pointer dereference at virtual address 000001c1
[  942.549458] pgd = 1a431801
[  942.552176] [000001c1] *pgd=00000000
[  942.555778] Internal error: Oops: 5 [#1] PREEMPT SMP ARM
[  942.561116] Modules linked in: shepherd(O-) pru_rproc irq_pruss_intc pruss wkup_m3_rproc pm33xx wkup_m3_ipc pruss_soc_bus uio_pdrv_genirq uio usb_f_acm u_serial usb_f_ncm usb_f_rndis u_ether libcomposite sch_fq_codel remoteproc virtio virtio_ring [last unloaded: shepherd]
[  942.585343] CPU: 0 PID: 1726 Comm: modprobe Tainted: G           O      4.19.94-ti-r73 #1focal
[  942.593991] Hardware name: Generic AM33XX (Flattened Device Tree)
[  942.600170] PC is at pru0_comm_receive_msg+0x28/0x94 [shepherd]
[  942.606129] LR is at coordinator_callback+0x9c/0x374 [shepherd]
[  942.612073] pc : [<bf19b018>]    lr : [<bf19ca58>]    psr: 20000193
[  942.618367] sp : d9535b10  ip : d9535b30  fp : d9535b2c
[  942.623612] r10: bf19f45c  r9 : bf19f418  r8 : bf19f3e4
[  942.628859] r7 : bf1a12a8  r6 : 000001c1  r5 : d9535b58  r4 : bf1a0610
[  942.635414] r3 : 00000000  r2 : 36df9ab0  r1 : 63f9e969  r0 : d9535b58
[  942.641971] Flags: nzCv  IRQs off  FIQs on  Mode SVC_32  ISA ARM  Segment none
[  942.649223] Control: 10c5387d  Table: 8d040019  DAC: 00000051
[  942.654994] Process modprobe (pid: 1726, stack limit = 0x6f328d04)
[  942.661201] Stack: (0xd9535b10 to 0xd9536000)
[  942.665580] 5b00:                                     00000006 d9535b58 bf1a0660 bf1a12a8
[  942.673797] 5b20: d9535b94 d9535b30 bf19ca58 bf19affc d9535b5c c016e508 bf19f374 bf19f3ac
[  942.682014] 5b40: 63f9e969 36df9ab0 63f9e969 00000000 36df9ab0 d9535b60 c0d58c60 c0d524d4
[  942.690231] 5b60: bf1a12a8 c1506e08 d9535b94 bf1a12a8 df9328a8 d9534000 df932840 df9328f0
[  942.698447] 5b80: 00000028 bf19c9bc d9535bfc d9535b98 c01cdcf8 bf19c9c8 0001017d c10ef7f4
[  942.706663] 5ba0: c15deaee ffffe000 000000db 70702a15 00000004 c1506e34 053666da 17470c05
[  942.714880] 5bc0: 053666da 17470c05 df9328f0 c1506e08 7fffffff df932840 20000193 00000003
[  942.723097] 5be0: df932918 df9328f0 df9328c8 ffffffff d9535c64 d9535c00 c01cee48 c01cdb60
[  942.731314] 5c00: 20000193 0000000f 000000db 70702a15 df9329c0 df932970 df932990 df93284c
[  942.739531] 5c20: d9535c74 d9535c30 7fffffff c017762c 1e467000 c0180ddc d9535cac c150d900
[  942.747746] 5c40: dc0b2c68 dc0b2c68 00000001 00000010 d9534000 00000000 d9535c74 d9535c68
[  942.755964] 5c60: c0126488 c01ced14 d9535cbc d9535c78 c01af55c c012645c df935b00 c14cf400
[  942.764180] 5c80: dc0b2c00 c15df118 d9535cc0 c1506e34 dc08822c dc0b2c00 dc0b2c68 dc0b2c68
[  942.772396] 5ca0: 00000001 00000000 dc0b5800 d9535d70 d9535cdc d9535cc0 c01af7c0 c01af4fc
[  942.780613] 5cc0: 00000000 c1506e08 dc0b2c00 dc0b2c68 d9535cfc d9535ce0 c01af868 c01af78c
[  942.788830] 5ce0: dc0b2c00 dc0b2c68 c14ce690 00000001 d9535d14 d9535d00 c01b396c c01af82c
[  942.797046] 5d00: c14ce690 00000000 d9535d24 d9535d18 c01ae604 c01b389c d9535d54 d9535d28
[  942.805263] 5d20: c01aed08 c01ae5dc d9535d70 c1660e68 60000013 ffffffff d9535da4 00000001
[  942.813480] 5d40: d9534000 00000001 d9535d6c d9535d58 c01022c0 c01aec88 c01ad388 60000013
[  942.821696] 5d60: d9535e04 d9535d70 c0101a0c c0102288 60000093 1e467000 00000000 c14c6428
[  942.829913] 5d80: c1621938 0000001d 00000245 00000000 00000001 60000013 00000001 d9535e04
[  942.838130] 5da0: d9535dc0 d9535dc0 c01ad384 c01ad388 60000013 ffffffff 00000051 bf000000
[  942.846347] 5dc0: bf19e920 d9535e64 d9534000 dc001e00 00000246 00000000 d9535e1c 00000000
[  942.854563] 5de0: bf19e920 d9535e64 00000000 db45d844 d9534000 00000081 d9535e1c d9535e08
[  942.862780] 5e00: c01ad688 c01ad1f4 bf19e920 d9535e64 d9535e44 d9535e20 c01ae35c c01ad664
[  942.870996] 5e20: c01ce984 c01cd3cc bf1a0610 00000000 bf1a02f0 db6e4044 d9535e5c d9535e48
[  942.879213] 5e40: c01ada38 c01ae264 d9535e64 c1506e08 d9535e84 d9535e70 bf19aba0 c01ada08
[  942.887430] 5e60: bf19e920 00000000 00000000 00000000 db6e4000 00000000 d9535e9c d9535e88
[  942.895646] 5e80: bf19d258 bf19ab44 db6e4010 db6e4010 d9535eb4 d9535ea0 c08f7240 bf19d240
[  942.903863] 5ea0: db6e4010 db45d810 d9535edc d9535eb8 c08f51c8 c08f7218 db6e4010 bf1a02f0
[  942.912079] 5ec0: 00000000 00000081 c0101204 d9534000 d9535ef4 d9535ee0 c08f5300 c08f5048
[  942.920295] 5ee0: bf1a02f0 00000a00 d9535f0c d9535ef8 c08f3a78 c08f52a0 bf1a02f0 00000a00
[  942.928512] 5f00: d9535f24 d9535f10 c08f5dd0 c08f3a24 bf1a0340 00000a00 d9535f34 d9535f28
[  942.936729] 5f20: c08f731c c08f5da4 d9535f44 d9535f38 bf19d7ac c08f730c d9535fa4 d9535f48
[  942.944945] 5f40: c01ebf08 bf19d7a0 70656873 64726568 00000000 c016a698 d9535f8c d9535f68
[  942.953162] 5f60: c015ed4c c1506e08 d9534000 c0101204 d9535fb0 00000006 c0101204 d9534000
[  942.961378] 5f80: 00535fac c1506e08 c010df34 00e38470 00e38470 00e38470 00000000 d9535fa8
[  942.969595] 5fa0: c0101000 c01ebd40 00e38470 00e38470 00e384ac 00000a00 00000000 00000001
[  942.977811] 5fc0: 00e38470 00e38470 00e38470 00000081 00000000 beea98f9 00e36190 00e38470
[  942.986027] 5fe0: 00457f60 beea8414 0043c4af b6ce9bb8 20000030 00e384ac 00000000 00000000
[  942.994301] [<bf19b018>] (pru0_comm_receive_msg [shepherd]) from [<bf19ca58>] (coordinator_callback+0x9c/0x374 [shepherd])
[  943.005424] [<bf19ca58>] (coordinator_callback [shepherd]) from [<c01cdcf8>] (__hrtimer_run_queues+0x1a4/0x410)
[  943.015564] [<c01cdcf8>] (__hrtimer_run_queues) from [<c01cee48>] (hrtimer_interrupt+0x140/0x2e0)
[  943.024491] [<c01cee48>] (hrtimer_interrupt) from [<c0126488>] (omap2_gp_timer_interrupt+0x38/0x40)
[  943.033594] [<c0126488>] (omap2_gp_timer_interrupt) from [<c01af55c>] (__handle_irq_event_percpu+0x6c/0x290)
[  943.043471] [<c01af55c>] (__handle_irq_event_percpu) from [<c01af7c0>] (handle_irq_event_percpu+0x40/0xa0)
[  943.053172] [<c01af7c0>] (handle_irq_event_percpu) from [<c01af868>] (handle_irq_event+0x48/0x6c)
[  943.062089] [<c01af868>] (handle_irq_event) from [<c01b396c>] (handle_level_irq+0xdc/0x158)
[  943.070482] [<c01b396c>] (handle_level_irq) from [<c01ae604>] (generic_handle_irq+0x34/0x44)
[  943.078961] [<c01ae604>] (generic_handle_irq) from [<c01aed08>] (__handle_domain_irq+0x8c/0xf8)
[  943.087706] [<c01aed08>] (__handle_domain_irq) from [<c01022c0>] (omap_intc_handle_irq+0x44/0xa0)
[  943.096621] [<c01022c0>] (omap_intc_handle_irq) from [<c0101a0c>] (__irq_svc+0x6c/0xa8)
[  943.104659] Exception stack(0xd9535d70 to 0xd9535db8)
[  943.109733] 5d60:                                     60000093 1e467000 00000000 c14c6428
[  943.117950] 5d80: c1621938 0000001d 00000245 00000000 00000001 60000013 00000001 d9535e04
[  943.126165] 5da0: d9535dc0 d9535dc0 c01ad384 c01ad388 60000013 ffffffff
[  943.132813] [<c0101a0c>] (__irq_svc) from [<c01ad388>] (vprintk_emit+0x1a0/0x2c0)
[  943.140334] [<c01ad388>] (vprintk_emit) from [<c01ad688>] (vprintk_default+0x30/0x38)
[  943.148203] [<c01ad688>] (vprintk_default) from [<c01ae35c>] (vprintk_func+0x104/0x1c0)
[  943.156247] [<c01ae35c>] (vprintk_func) from [<c01ada38>] (printk+0x40/0x68)
[  943.163348] [<c01ada38>] (printk) from [<bf19aba0>] (mem_interface_exit+0x68/0x70 [shepherd])
[  943.171942] [<bf19aba0>] (mem_interface_exit [shepherd]) from [<bf19d258>] (shepherd_drv_remove+0x24/0x84 [shepherd])
[  943.182621] [<bf19d258>] (shepherd_drv_remove [shepherd]) from [<c08f7240>] (platform_drv_remove+0x34/0x4c)
[  943.192421] [<c08f7240>] (platform_drv_remove) from [<c08f51c8>] (device_release_driver_internal+0x18c/0x234)
[  943.202386] [<c08f51c8>] (device_release_driver_internal) from [<c08f5300>] (driver_detach+0x6c/0xa0)
[  943.211651] [<c08f5300>] (driver_detach) from [<c08f3a78>] (bus_remove_driver+0x60/0xd8)
[  943.219782] [<c08f3a78>] (bus_remove_driver) from [<c08f5dd0>] (driver_unregister+0x38/0x58)
[  943.228260] [<c08f5dd0>] (driver_unregister) from [<c08f731c>] (platform_driver_unregister+0x1c/0x20)
[  943.237538] [<c08f731c>] (platform_driver_unregister) from [<bf19d7ac>] (shepherd_driver_exit+0x18/0x86c [shepherd])
[  943.248138] [<bf19d7ac>] (shepherd_driver_exit [shepherd]) from [<c01ebf08>] (sys_delete_module+0x1d4/0x290)
[  943.258014] [<c01ebf08>] (sys_delete_module) from [<c0101000>] (ret_fast_syscall+0x0/0x54)
[  943.266313] Exception stack(0xd9535fa8 to 0xd9535ff0)
[  943.271389] 5fa0:                   00e38470 00e38470 00e384ac 00000a00 00000000 00000001
[  943.279606] 5fc0: 00e38470 00e38470 00e38470 00000081 00000000 beea98f9 00e36190 00e38470
[  943.287819] 5fe0: 00457f60 beea8414 0043c4af b6ce9bb8
[  943.292899] Code: e34b4f1a e30061c1 e1a05000 e5943000 (e7d33006)
[  943.299023] ---[ end trace 9358d1fc4259ae2f ]---
[  943.303662] Kernel panic - not syncing: Fatal exception in interrupt
[  943.310061] ---[ end Kernel panic - not syncing: Fatal exception in interrupt ]---
```

What to read out of this?

- crash in pru0_comm_receive_msg
- cause: mem_interface was unloaded before msg_system was halted ⇾ classic race condition for use after free
- after switching two lines of code: testsuite runs through!

## Are there more skeletons?

While running the testsuite a second time it caused an allocation error::

```
[   27.554353] PM: Cannot get wkup_m3_ipc handle
[   27.997689] PM: Cannot get wkup_m3_ipc handle
[   32.066431] shepherd 4a300000.pruss:shepherd: Not yet able to parse pru device node
[   32.247849] shepherd 4a300000.pruss:shepherd: Not yet able to parse pru device node
[   33.007085] shepherd 4a300000.pruss:shepherd: Not yet able to parse pru device node
[   33.118827] shepherd 4a300000.pruss:shepherd: Not yet able to parse pru device node
[ 1961.035398] shprd.k: Faulty behavior - PRU did not answer to trigger-request in time!
[ 1961.134416] shprd.k: forwards timestamp-jump detected (sync-loop, 300 ms)
[ 2137.835229] cma: cma_alloc: alloc failed, req-size: 3811 pages, ret: -16
[ 2137.842105] pru-rproc 4a334000.pru: failed to allocate dma memory: len 0xee2800
[ 2137.853633] remoteproc remoteproc1: Failed to process resources: -12
[ 2137.863924] shprd.k: Couldn't boot PRU0
[ 2151.973367] cma: cma_alloc: alloc failed, req-size: 3811 pages, ret: -16
[ 2151.980265] pru-rproc 4a334000.pru: failed to allocate dma memory: len 0xee2800
[ 2151.991722] remoteproc remoteproc1: Failed to process resources: -12
[ 2152.001506] shprd.k: Couldn't boot PRU0
```

⇾ never caught in the wild, so maybe just triggered for massive loading/unloading the kernel-module, includes reinitializing the PRUs.

There was also some kind of pru crash. The message or sample buffer to the PRU was suddenly full, probably because the PRU wasn't working as expected.
