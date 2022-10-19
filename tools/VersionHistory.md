# SerialUPDI
## 1.2.3 - Fix standalone read
Jan 15, 2022 (text finally updated)
At the very end of 1.2.0 development, it was discovered that the D11C-as-serial-adapter for UPDI that was the reason for their involvement in the project... ah... didn't actually work. Investigation revealed that there was a certain size of data that if received or sent would crash the programmer. There was already a facility to control this for write, but it also happeend for read, so some solution was needed in a hurry, and the -rc option was added. The standalone read action was not tested after that was added. The implementation there was botched, and reading could never be done. Only write and verify, which of course were tested. Oooops. This was repored on DxCore on 1/14/22, and the issue was not challenging to correct. Additionally, mistake in 1.2.2 relating to the clock speed of the UPDI manager on the target was corrected in order to improve robustness during programming at 460800 baud. This file was added.

## 1.2.2 - Fixing writedelay
Jan 10, 2022, text printed at startup still said 1.2.0.
write_delay did not have enough granularity, especially on windows. Typically a single millisecond would be enough to keep the write from failing... but even -wd 1 would add over 3ms of delay on many systems. This wound up adding several seconds to the programming time in some cases. It was modified to use a pause functionality that does not call sleep() and just busywaits until the condition is met.
Additionally, write delay was applied to fuses in addition to flash - we had observed failures at high baud rates similar to the ones encountered due to too-fast writes.
This was introduced in megaTinyCore 2.5.6; notably, it also added a crapload of programmer definitions to the core as it had been found through feedback that behavior between systems and adapters as to when writedelay is needed while the operating voltage impacts the maximum speed at which data should be uploaded.  This version was never included in DxCore.

## 1.2.1 - Part support update
Mid-late 2021, text printed at startup not updated.
Part of the promise of using pymcuprog was a steady stream of updates to support new parts. Unfortunately that has not happened: While Microchip is keeping it updated internally, there is an in-house quality control process before it is released to github, and by all appearances this must be very thorough, because even in late 2021, long after the 64 and 32 DA and DB-series parts had been released, the device files for pymcuprog were still missing. And we're stuck with it's disadvantages, namely that the codebase is a sprawling mess written by multiple individuals none of whom speak python fluently (and you can be sure Spence hasn't helped matters in this fork).
The missing files were synthecized from existing files and publlically available information on the parts.

## 1.2.0 - Performance Improvement push
By the early summer of 2021, those who had pushed for SerialUPDI were starting to recognize the issue with upload speed. A meeting was convened over Zoom to discuss the problem, and an intensive period of performance improvement ensued. During that week, mostly by Spence's hand. Performance improved by leaps and bounds. By the end of the week write speeds speeds had increased from 600-1k bytes/s to 20k, and by the time 1.2.0 was released, writes occurred at 22-24k/s on Dx-series, and up to 14-16k on tinyAVR (where the time was dominated by USB latency, data transfer time), while reads as high as 32k/s were documented at 460800 baud (since then, it has been demonstrated that 42k/s readas are entirely possible on DxCore, while; 24k/s is the fundamental limit for write.) This was included in DxCore 1.3.6 and megaTinyCore 2.3.2. This is also when options like -wd (write delay) and -rc (read chunks) were implemented.

Attempts to merge this with the latest official pymcuprog were unsuccessful.

## 1.0.0 - initial version
The first version, based very tightly on pymcuprog, was released in late 2020 or early 2021.
This version worked, but it was not practical, as write speed rarely exceeded 1kb/s. The majority of this work was done by Quentin, as he was skilled in python Spence was most certainly not.
This was made available starting from megaTinyCore 2.2.0 and DxCore 1.3.0
