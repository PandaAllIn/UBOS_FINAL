# Balaur Hardware Inventory
Generated: 2025-10-07T09:17:08+00:00

## CPU
### lscpu
```
Architecture:                         x86_64
CPU op-mode(s):                       32-bit, 64-bit
Address sizes:                        39 bits physical, 48 bits virtual
Byte Order:                           Little Endian
CPU(s):                               8
On-line CPU(s) list:                  0-7
Vendor ID:                            GenuineIntel
Model name:                           Intel(R) Core(TM) i7-4790K CPU @ 4.00GHz
CPU family:                           6
Model:                                60
Thread(s) per core:                   2
Core(s) per socket:                   4
Socket(s):                            1
Stepping:                             3
CPU(s) scaling MHz:                   62%
CPU max MHz:                          4400.0000
CPU min MHz:                          800.0000
BogoMIPS:                             7981.98
Flags:                                fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc cpuid aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm cpuid_fault epb pti ssbd ibrs ibpb stibp tpr_shadow flexpriority ept vpid ept_ad fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid xsaveopt dtherm ida arat pln pts vnmi md_clear flush_l1d
Virtualization:                       VT-x
L1d cache:                            128 KiB (4 instances)
L1i cache:                            128 KiB (4 instances)
L2 cache:                             1 MiB (4 instances)
L3 cache:                             8 MiB (1 instance)
NUMA node(s):                         1
NUMA node0 CPU(s):                    0-7
Vulnerability Gather data sampling:   Not affected
Vulnerability Itlb multihit:          KVM: Mitigation: VMX disabled
Vulnerability L1tf:                   Mitigation; PTE Inversion; VMX conditional cache flushes, SMT vulnerable
Vulnerability Mds:                    Mitigation; Clear CPU buffers; SMT vulnerable
Vulnerability Meltdown:               Mitigation; PTI
Vulnerability Mmio stale data:        Unknown: No mitigations
Vulnerability Reg file data sampling: Not affected
Vulnerability Retbleed:               Not affected
Vulnerability Spec rstack overflow:   Not affected
Vulnerability Spec store bypass:      Mitigation; Speculative Store Bypass disabled via prctl
Vulnerability Spectre v1:             Mitigation; usercopy/swapgs barriers and __user pointer sanitization
Vulnerability Spectre v2:             Mitigation; Retpolines; IBPB conditional; IBRS_FW; STIBP conditional; RSB filling; PBRSB-eIBRS Not affected; BHI Not affected
Vulnerability Srbds:                  Mitigation; Microcode
Vulnerability Tsx async abort:        Not affected
```

### cat /proc/cpuinfo (model/cache/clock)
```
model name	: Intel(R) Core(TM) i7-4790K CPU @ 4.00GHz
cpu MHz		: 2996.862
cache size	: 8192 KB
model name	: Intel(R) Core(TM) i7-4790K CPU @ 4.00GHz
cpu MHz		: 2993.266
cache size	: 8192 KB
model name	: Intel(R) Core(TM) i7-4790K CPU @ 4.00GHz
cpu MHz		: 2993.234
cache size	: 8192 KB
model name	: Intel(R) Core(TM) i7-4790K CPU @ 4.00GHz
cpu MHz		: 2993.623
cache size	: 8192 KB
model name	: Intel(R) Core(TM) i7-4790K CPU @ 4.00GHz
cpu MHz		: 800.000
cache size	: 8192 KB
model name	: Intel(R) Core(TM) i7-4790K CPU @ 4.00GHz
cpu MHz		: 2997.962
cache size	: 8192 KB
model name	: Intel(R) Core(TM) i7-4790K CPU @ 4.00GHz
cpu MHz		: 2996.756
cache size	: 8192 KB
model name	: Intel(R) Core(TM) i7-4790K CPU @ 4.00GHz
cpu MHz		: 2993.643
cache size	: 8192 KB
```

### cpupower frequency-info
```
analyzing CPU 1:
  driver: intel_cpufreq
  CPUs which run at the same hardware frequency: 1
  CPUs which need to have their frequency coordinated by software: 1
  maximum transition latency: 20.0 us
  hardware limits: 800 MHz - 4.40 GHz
  available cpufreq governors: conservative ondemand userspace powersave performance schedutil
  current policy: frequency should be within 800 MHz and 4.40 GHz.
                  The governor "schedutil" may decide which speed to use
                  within this range.
  current CPU frequency: Unable to call hardware
  current CPU frequency: 798 MHz (asserted by call to kernel)
  boost state support:
    Supported: yes
    Active: yes
```

### cpupower idle-info
```
CPUidle driver: intel_idle
CPUidle governor: menu
analyzing CPU 3:

Number of idle states: 6
Available idle states: POLL C1 C1E C3 C6 C7s
POLL:
Flags/Description: CPUIDLE CORE POLL IDLE
Latency: 0
Usage: 72371
Duration: 2681913
C1:
Flags/Description: MWAIT 0x00
Latency: 2
Usage: 256689
Duration: 47062833
C1E:
Flags/Description: MWAIT 0x01
Latency: 10
Usage: 332117
Duration: 34520586
C3:
Flags/Description: MWAIT 0x10
Latency: 33
Usage: 439284
Duration: 87521940
C6:
Flags/Description: MWAIT 0x20
Latency: 133
Usage: 113419
Duration: 36549149
C7s:
Flags/Description: MWAIT 0x32
Latency: 166
Usage: 9475000
Duration: 82076036165

```

### CPU governors
```
/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor: schedutil
/sys/devices/system/cpu/cpu1/cpufreq/scaling_governor: schedutil
/sys/devices/system/cpu/cpu2/cpufreq/scaling_governor: schedutil
/sys/devices/system/cpu/cpu3/cpufreq/scaling_governor: schedutil
/sys/devices/system/cpu/cpu4/cpufreq/scaling_governor: schedutil
/sys/devices/system/cpu/cpu5/cpufreq/scaling_governor: schedutil
/sys/devices/system/cpu/cpu6/cpufreq/scaling_governor: schedutil
/sys/devices/system/cpu/cpu7/cpufreq/scaling_governor: schedutil
```

### Available governors
```
/sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors
conservative ondemand userspace powersave performance schedutil 
```

### lscpu -C
```
NAME ONE-SIZE ALL-SIZE WAYS TYPE        LEVEL SETS PHY-LINE COHERENCY-SIZE
L1d       32K     128K    8 Data            1   64        1             64
L1i       32K     128K    8 Instruction     1   64        1             64
L2       256K       1M    8 Unified         2  512        1             64
L3         8M       8M   16 Unified         3 8192        1             64
```

### getconf CACHE
```
LEVEL1_ICACHE_SIZE                 32768
LEVEL1_ICACHE_ASSOC                
LEVEL1_ICACHE_LINESIZE             64
LEVEL1_DCACHE_SIZE                 32768
LEVEL1_DCACHE_ASSOC                8
LEVEL1_DCACHE_LINESIZE             64
LEVEL2_CACHE_SIZE                  262144
LEVEL2_CACHE_ASSOC                 8
LEVEL2_CACHE_LINESIZE              64
LEVEL3_CACHE_SIZE                  8388608
LEVEL3_CACHE_ASSOC                 16
LEVEL3_CACHE_LINESIZE              64
LEVEL4_CACHE_SIZE                  
LEVEL4_CACHE_ASSOC                 
LEVEL4_CACHE_LINESIZE              
```

### sensors
```
amdgpu-pci-0100
Adapter: PCI adapter
vddgfx:      850.00 mV 
edge:         +59.0°C  (crit = +110.0°C, hyst = -273.1°C)
PPT:          15.03 W  (cap = 110.00 W)

coretemp-isa-0000
Adapter: ISA adapter
Package id 0:  +59.0°C  (high = +80.0°C, crit = +100.0°C)
Core 0:        +59.0°C  (high = +80.0°C, crit = +100.0°C)
Core 1:        +54.0°C  (high = +80.0°C, crit = +100.0°C)
Core 2:        +54.0°C  (high = +80.0°C, crit = +100.0°C)
Core 3:        +54.0°C  (high = +80.0°C, crit = +100.0°C)

applesmc-isa-0300
Adapter: ISA adapter
Main :       1197 RPM  (min = 1200 RPM, max = 3178 RPM)
TA0P:         +22.2°C  
TA0V:         +31.0°C  
TA0p:         +42.2°C  
TC0E:         -40.2°C  
TC0F:         -39.0°C  
TC0J:          +1.0°C  
TC0P:         +54.2°C  
TC0T:          +0.0°C  
TC0c:         +58.0°C  
TC0p:         +54.2°C  
TC1c:         +55.0°C  
TC2c:         +54.0°C  
TC3c:         +54.0°C  
TCGc:         +55.0°C  
TCSc:         +55.0°C  
TCXR:         -41.2°C  
TCXc:         +58.8°C  
TCXr:         -41.2°C  
TG0D:         +59.0°C  
TG0E:         +59.8°C  
TG0F:         +60.0°C  
TG0J:          +0.0°C  
TG0P:         +51.8°C  
TG0T:          -0.2°C  
TG0d:         +59.0°C  
TG0p:         +51.8°C  
TG1P:         +52.0°C  
TG1d:         +56.0°C  
TG1p:         +52.0°C  
TG2P:         +52.5°C  
TG2p:         +52.5°C  
TG3P:         +54.8°C  
TG3p:         +54.8°C  
TH0A:        -127.0°C  
TH0B:        -127.0°C  
TH0C:        -127.0°C  
TH0F:        -127.0°C  
TH0O:          +9.0°C  
TH0P:        -127.0°C  
TH0R:        -127.0°C  
TH0a:        -127.0°C  
TH0b:        -127.0°C  
TH0c:        -127.0°C  
TH0e:          +1.0°C  
TH1A:         +46.8°C  
TH1B:         +46.8°C  
TH1C:        -127.0°C  
TH1F:         -34.2°C  
TH1O:          +9.0°C  
TH1P:        -127.0°C  
TH1R:         -34.2°C  
TH1a:         +46.8°C  
TH1b:         +46.8°C  
TH1c:        -127.0°C  
TL0P:         +37.2°C  
TL0V:         +35.8°C  
TL0p:         +37.2°C  
TL1P:         +36.5°C  
TL1V:         +33.2°C  
TL1p:         +36.5°C  
TL1v:         +33.2°C  
TM0P:         +49.5°C  
TM0V:         +54.2°C  
TM0p:         +49.5°C  
TM1P:         +41.0°C  
TM1a:         +62.5°C  
TM1p:         +41.0°C  
TM2P:         +46.0°C  
TM2a:         +57.0°C  
TM2b:         +59.8°C  
TM2c:         +56.2°C  
TM2d:         +63.8°C  
TM2p:         +46.0°C  
TM3P:         +46.8°C  
TM3a:         +59.8°C  
TM3b:         +58.5°C  
TM3c:         +58.5°C  
TM3d:         +55.8°C  
TM3p:         +46.8°C  
TM4a:         +54.2°C  
TMXP:         +49.5°C  
TPCD:         +61.0°C  
TS0V:         +41.2°C  
Tb0P:         +58.0°C  
Tb0p:         +58.0°C  
Tm0P:         +48.5°C  
Tm0p:         +48.5°C  
Tm1P:         +50.2°C  
Tm1p:         +50.2°C  
Tm2P:         +52.8°C  
Tm2p:         +52.8°C  
Tp2F:         +46.2°C  
Tp2H:         +46.2°C  
Tp2h:         +46.2°C  

```

### Thermal zones
```
/sys/class/thermal/thermal_zone0 (x86_pkg_temp): 60000 m°C
```

## GPU
### lspci -nnk (VGA)
```
01:00.0 VGA compatible controller [0300]: Advanced Micro Devices, Inc. [AMD/ATI] Tonga XT / Amethyst XT [Radeon R9 380X / R9 M295X] [1002:6938]
	Subsystem: Apple Inc. Radeon R9 M295X Mac Edition [106b:013a]
	Kernel driver in use: amdgpu
	Kernel modules: amdgpu
```

### clinfo
```
Number of platforms                               2
  Platform Name                                   Clover
  Platform Vendor                                 Mesa
  Platform Version                                OpenCL 1.1 Mesa 25.0.7-0ubuntu0.24.04.2
  Platform Profile                                FULL_PROFILE
  Platform Extensions                             cl_khr_icd
  Platform Extensions function suffix             MESA

  Platform Name                                   rusticl
  Platform Vendor                                 Mesa/X.org
  Platform Version                                OpenCL 3.0 
  Platform Profile                                FULL_PROFILE
  Platform Extensions                             cl_khr_icd
  Platform Extensions with Version                cl_khr_icd                                                       0x400000 (1.0.0)
  Platform Numeric Version                        0xc00000 (3.0.0)
  Platform Extensions function suffix             MESA
  Platform Host timer resolution                  1ns

  Platform Name                                   Clover
Number of devices                                 1
  Device Name                                     AMD Radeon R9 200 Series (radeonsi, tonga, ACO, DRM 3.57, 6.8.0-85-generic)
  Device Vendor                                   AMD
  Device Vendor ID                                0x1002
  Device Version                                  OpenCL 1.1 Mesa 25.0.7-0ubuntu0.24.04.2
  Device Numeric Version                          0x401000 (1.1.0)
  Driver Version                                  25.0.7-0ubuntu0.24.04.2
  Device OpenCL C Version                         OpenCL C 1.1 
  Device OpenCL C Numeric Version                 0x401000 (1.1.0)
  Device Type                                     GPU
  Device Profile                                  FULL_PROFILE
  Device Available                                Yes
  Compiler Available                              Yes
  Max compute units                               32
  Max clock frequency                             850MHz
  Max work item dimensions                        3
  Max work item sizes                             256x256x256
  Max work group size                             256
=== CL_PROGRAM_BUILD_LOG ===
In file included from <built-in>:1:
/usr/include/clc/clc.h:19:10: fatal error: 'clc/clcfunc.h' file not found
  Preferred work group size multiple (kernel)     <getWGsizes:1980: create kernel : error -46>
  Preferred / native vector sizes                 
    char                                                16 / 16      
    short                                                8 / 8       
    int                                                  4 / 4       
    long                                                 2 / 2       
    half                                                 0 / 0        (n/a)
    float                                                4 / 4       
    double                                               2 / 2        (cl_khr_fp64)
  Half-precision Floating-point support           (n/a)
  Single-precision Floating-point support         (core)
    Denormals                                     No
    Infinity and NANs                             Yes
    Round to nearest                              Yes
    Round to zero                                 No
    Round to infinity                             No
    IEEE754-2008 fused multiply-add               No
    Support is emulated in software               No
    Correctly-rounded divide and sqrt operations  No
  Double-precision Floating-point support         (cl_khr_fp64)
    Denormals                                     Yes
    Infinity and NANs                             Yes
    Round to nearest                              Yes
    Round to zero                                 Yes
    Round to infinity                             Yes
    IEEE754-2008 fused multiply-add               Yes
    Support is emulated in software               No
  Address bits                                    64, Little-Endian
  Global memory size                              4294967296 (4GiB)
  Error Correction support                        No
  Max memory allocation                           1073741824 (1024MiB)
  Unified memory for Host and Device              No
  Minimum alignment for any data type             128 bytes
  Alignment of base address                       32768 bits (4096 bytes)
  Global Memory cache type                        None
  Image support                                   No
  Local memory type                               Local
  Local memory size                               65536 (64KiB)
  Max number of constant args                     16
  Max constant buffer size                        67108864 (64MiB)
  Max size of kernel argument                     1024
  Queue properties                                
    Out-of-order execution                        No
    Profiling                                     Yes
  Profiling timer resolution                      0ns
  Execution capabilities                          
    Run OpenCL kernels                            Yes
    Run native kernels                            No
    ILs with version                              (n/a)
  Built-in kernels with version                   (n/a)
  Device Extensions                               cl_khr_byte_addressable_store cl_khr_global_int32_base_atomics cl_khr_global_int32_extended_atomics cl_khr_local_int32_base_atomics cl_khr_local_int32_extended_atomics cl_khr_int64_base_atomics cl_khr_int64_extended_atomics cl_khr_fp64 cl_khr_extended_versioning
  Device Extensions with Version                  cl_khr_byte_addressable_store                                    0x400000 (1.0.0)
                                                  cl_khr_global_int32_base_atomics                                 0x400000 (1.0.0)
                                                  cl_khr_global_int32_extended_atomics                             0x400000 (1.0.0)
                                                  cl_khr_local_int32_base_atomics                                  0x400000 (1.0.0)
                                                  cl_khr_local_int32_extended_atomics                              0x400000 (1.0.0)
                                                  cl_khr_int64_base_atomics                                        0x400000 (1.0.0)
                                                  cl_khr_int64_extended_atomics                                    0x400000 (1.0.0)
                                                  cl_khr_fp64                                                      0x400000 (1.0.0)
                                                  cl_khr_extended_versioning                                       0x400000 (1.0.0)

  Platform Name                                   rusticl
Number of devices                                 0

NULL platform behavior
  clGetPlatformInfo(NULL, CL_PLATFORM_NAME, ...)  Clover
  clGetDeviceIDs(NULL, CL_DEVICE_TYPE_ALL, ...)   Success [MESA]
  clCreateContext(NULL, ...) [default]            Success [MESA]
  clCreateContext(NULL, ...) [other]              <error: no devices in non-default plaforms>
  clCreateContextFromType(NULL, CL_DEVICE_TYPE_DEFAULT)  Success (1)
    Platform Name                                 Clover
    Device Name                                   AMD Radeon R9 200 Series (radeonsi, tonga, ACO, DRM 3.57, 6.8.0-85-generic)
  clCreateContextFromType(NULL, CL_DEVICE_TYPE_CPU)  No devices found in platform
  clCreateContextFromType(NULL, CL_DEVICE_TYPE_GPU)  Success (1)
    Platform Name                                 Clover
    Device Name                                   AMD Radeon R9 200 Series (radeonsi, tonga, ACO, DRM 3.57, 6.8.0-85-generic)
  clCreateContextFromType(NULL, CL_DEVICE_TYPE_ACCELERATOR)  No devices found in platform
  clCreateContextFromType(NULL, CL_DEVICE_TYPE_CUSTOM)  No devices found in platform
  clCreateContextFromType(NULL, CL_DEVICE_TYPE_ALL)  Success (1)
    Platform Name                                 Clover
    Device Name                                   AMD Radeon R9 200 Series (radeonsi, tonga, ACO, DRM 3.57, 6.8.0-85-generic)

ICD loader properties
  ICD loader Name                                 OpenCL ICD Loader
  ICD loader Vendor                               OCL Icd free software
  ICD loader Version                              2.3.2
  ICD loader Profile                              OpenCL 3.0
```

### vulkaninfo head
```
'DISPLAY' environment variable not set... skipping surface info
==========
VULKANINFO
==========

Vulkan Instance Version: 1.3.275


Instance Extensions: count = 24
===============================
	VK_EXT_acquire_drm_display             : extension revision 1
	VK_EXT_acquire_xlib_display            : extension revision 1
	VK_EXT_debug_report                    : extension revision 10
	VK_EXT_debug_utils                     : extension revision 2
	VK_EXT_direct_mode_display             : extension revision 1
	VK_EXT_display_surface_counter         : extension revision 1
	VK_EXT_headless_surface                : extension revision 1
	VK_EXT_surface_maintenance1            : extension revision 1
	VK_EXT_swapchain_colorspace            : extension revision 5
	VK_KHR_device_group_creation           : extension revision 1
	VK_KHR_display                         : extension revision 23
	VK_KHR_external_fence_capabilities     : extension revision 1
	VK_KHR_external_memory_capabilities    : extension revision 1
	VK_KHR_external_semaphore_capabilities : extension revision 1
	VK_KHR_get_display_properties2         : extension revision 1
	VK_KHR_get_physical_device_properties2 : extension revision 2
	VK_KHR_get_surface_capabilities2       : extension revision 1
	VK_KHR_portability_enumeration         : extension revision 1
	VK_KHR_surface                         : extension revision 25
	VK_KHR_surface_protected_capabilities  : extension revision 1
	VK_KHR_wayland_surface                 : extension revision 6
	VK_KHR_xcb_surface                     : extension revision 6
	VK_KHR_xlib_surface                    : extension revision 6
	VK_LUNARG_direct_driver_loading        : extension revision 1

Layers: count = 3
=================
VK_LAYER_INTEL_nullhw (INTEL NULL HW) Vulkan version 1.1.73, layer version 1:
	Layer Extensions: count = 0
	Devices: count = 2
		GPU id = 0 (AMD Radeon R9 200 Series (RADV TONGA))
		Layer-Device Extensions: count = 0

		GPU id = 1 (llvmpipe (LLVM 20.1.2, 256 bits))
		Layer-Device Extensions: count = 0

VK_LAYER_MESA_device_select (Linux device selection layer) Vulkan version 1.4.303, layer version 1:
	Layer Extensions: count = 0
	Devices: count = 2
		GPU id = 0 (AMD Radeon R9 200 Series (RADV TONGA))
		Layer-Device Extensions: count = 0

		GPU id = 1 (llvmpipe (LLVM 20.1.2, 256 bits))
		Layer-Device Extensions: count = 0

VK_LAYER_MESA_overlay (Mesa Overlay layer) Vulkan version 1.4.303, layer version 1:
	Layer Extensions: count = 0
	Devices: count = 2
		GPU id = 0 (AMD Radeon R9 200 Series (RADV TONGA))
		Layer-Device Extensions: count = 0

		GPU id = 1 (llvmpipe (LLVM 20.1.2, 256 bits))
		Layer-Device Extensions: count = 0

Device Properties and Extensions:
=================================
GPU0:
VkPhysicalDeviceProperties:
---------------------------
	apiVersion        = 1.4.305 (4210993)
	driverVersion     = 25.0.7 (104857607)
	vendorID          = 0x1002
	deviceID          = 0x6938
	deviceType        = PHYSICAL_DEVICE_TYPE_DISCRETE_GPU
	deviceName        = AMD Radeon R9 200 Series (RADV TONGA)
	pipelineCacheUUID = ae798981-fd4f-e005-931c-b6efd5d7c3ab

VkPhysicalDeviceLimits:
-----------------------
	maxImageDimension1D                             = 16384
	maxImageDimension2D                             = 16384
	maxImageDimension3D                             = 2048
	maxImageDimensionCube                           = 16384
	maxImageArrayLayers                             = 2048
	maxTexelBufferElements                          = 4294967295
	maxUniformBufferRange                           = 4294967295
	maxStorageBufferRange                           = 4294967295
	maxPushConstantsSize                            = 256
	maxMemoryAllocationCount                        = 4294967295
	maxSamplerAllocationCount                       = 65536
	bufferImageGranularity                          = 0x00000001
	sparseAddressSpaceSize                          = 0xfffffffc
	maxBoundDescriptorSets                          = 32
	maxPerStageDescriptorSamplers                   = 8388606
	maxPerStageDescriptorUniformBuffers             = 8388606
	maxPerStageDescriptorStorageBuffers             = 8388606
	maxPerStageDescriptorSampledImages              = 8388606
	maxPerStageDescriptorStorageImages              = 8388606
	maxPerStageDescriptorInputAttachments           = 8388606
	maxPerStageResources                            = 8388606
	maxDescriptorSetSamplers                        = 8388606
	maxDescriptorSetUniformBuffers                  = 8388606
	maxDescriptorSetUniformBuffersDynamic           = 16
	maxDescriptorSetStorageBuffers                  = 8388606
	maxDescriptorSetStorageBuffersDynamic           = 8
	maxDescriptorSetSampledImages                   = 8388606
	maxDescriptorSetStorageImages                   = 8388606
	maxDescriptorSetInputAttachments                = 8388606
	maxVertexInputAttributes                        = 32
	maxVertexInputBindings                          = 32
	maxVertexInputAttributeOffset                   = 4294967295
	maxVertexInputBindingStride                     = 2048
	maxVertexOutputComponents                       = 128
	maxTessellationGenerationLevel                  = 64
	maxTessellationPatchSize                        = 32
	maxTessellationControlPerVertexInputComponents  = 128
	maxTessellationControlPerVertexOutputComponents = 128
	maxTessellationControlPerPatchOutputComponents  = 120
	maxTessellationControlTotalOutputComponents     = 4096
	maxTessellationEvaluationInputComponents        = 128
	maxTessellationEvaluationOutputComponents       = 128
```

### radeontop snapshot
```
radeontop not available
```

### amdgpu_pm_info
```
no debug access
```

## Memory
### dmidecode -t memory
```
# dmidecode 3.5
Getting SMBIOS data from sysfs.
SMBIOS 2.4 present.

Wrong DMI structures length: 3333 bytes announced, only 2895 bytes available.
Handle 0x0005, DMI type 16, 15 bytes
Physical Memory Array
	Location: System Board Or Motherboard
	Use: System Memory
	Error Correction Type: None
	Maximum Capacity: 16 GB
	Error Information Handle: Not Provided
	Number Of Devices: 4

Handle 0x0007, DMI type 17, 34 bytes
Memory Device
	Array Handle: 0x0005
	Error Information Handle: No Error
	Total Width: Unknown
	Data Width: Unknown
	Size: 8 GB
	Form Factor: SODIMM
	Set: None
	Locator: DIMM0
	Bank Locator: BANK 0
	Type: DDR3
	Type Detail: Synchronous
	Speed: 1600 MT/s
	Manufacturer: 0x0198
	Serial Number: 0x533EAAD0
	Asset Tag: Unknown
	Part Number: 0x393930353432382D3139332E4130304C4620
	Rank: Unknown
	Configured Memory Speed: Unknown

Handle 0x0009, DMI type 17, 34 bytes
Memory Device
	Array Handle: 0x0005
	Error Information Handle: No Error
	Total Width: Unknown
	Data Width: Unknown
	Size: 8 GB
	Form Factor: SODIMM
	Set: None
	Locator: DIMM0
	Bank Locator: BANK 1
	Type: DDR3
	Type Detail: Synchronous
	Speed: 1600 MT/s
	Manufacturer: 0x0198
	Serial Number: 0x553E09D1
	Asset Tag: Unknown
	Part Number: 0x393930353432382D3139332E4130304C4620
	Rank: Unknown
	Configured Memory Speed: Unknown

Handle 0x000B, DMI type 17, 34 bytes
Memory Device
	Array Handle: 0x0005
	Error Information Handle: No Error
	Total Width: Unknown
	Data Width: Unknown
	Size: 8 GB
	Form Factor: SODIMM
	Set: None
	Locator: DIMM1
	Bank Locator: BANK 0
	Type: DDR3
	Type Detail: Synchronous
	Speed: 1600 MT/s
	Manufacturer: 0x0198
	Serial Number: 0x533EA7D0
	Asset Tag: Unknown
	Part Number: 0x393930353432382D3139332E4130304C4620
	Rank: Unknown
	Configured Memory Speed: Unknown

Handle 0x000D, DMI type 17, 34 bytes
Memory Device
	Array Handle: 0x0005
	Error Information Handle: No Error
	Total Width: Unknown
	Data Width: Unknown
	Size: 8 GB
	Form Factor: SODIMM
	Set: None
	Locator: DIMM1
	Bank Locator: BANK 1
	Type: DDR3
	Type Detail: Synchronous
	Speed: 1600 MT/s
	Manufacturer: 0x0198
	Serial Number: 0x553E2AD1
	Asset Tag: Unknown
	Part Number: 0x393930353432382D3139332E4130304C4620
	Rank: Unknown
	Configured Memory Speed: Unknown

Wrong DMI structures count: 53 announced, only 50 decoded.
```

### numactl --hardware
```
available: 1 nodes (0)
node 0 cpus: 0 1 2 3 4 5 6 7
node 0 size: 32036 MB
node 0 free: 21487 MB
node distances:
node   0 
  0:  10 
```

### swapon --show
```
NAME      TYPE SIZE USED PRIO
/swap.img file   8G   0B   -2
```

### /proc/swaps
```
Filename				Type		Size		Used		Priority
/swap.img                               file		8388604		0		-2
```

### /proc/meminfo (first 40 lines)
```
MemTotal:       32805412 kB
MemFree:        22003472 kB
MemAvailable:   31849836 kB
Buffers:          211020 kB
Cached:          9726868 kB
SwapCached:            0 kB
Active:          1414716 kB
Inactive:        8608728 kB
Active(anon):      95872 kB
Inactive(anon):        0 kB
Active(file):    1318844 kB
Inactive(file):  8608728 kB
Unevictable:       27444 kB
Mlocked:           27444 kB
SwapTotal:       8388604 kB
SwapFree:        8388604 kB
Zswap:                 0 kB
Zswapped:              0 kB
Dirty:              1008 kB
Writeback:           140 kB
AnonPages:        113164 kB
Mapped:           164172 kB
Shmem:              1536 kB
KReclaimable:     387312 kB
Slab:             529820 kB
SReclaimable:     387312 kB
SUnreclaim:       142508 kB
KernelStack:        4056 kB
PageTables:         4664 kB
SecPageTables:         0 kB
NFS_Unstable:          0 kB
Bounce:                0 kB
WritebackTmp:          0 kB
CommitLimit:    24791308 kB
Committed_AS:     638080 kB
VmallocTotal:   34359738367 kB
VmallocUsed:       83936 kB
VmallocChunk:          0 kB
Percpu:            10976 kB
HardwareCorrupted:     0 kB
```

## Storage
### lsblk
```
NAME                        SIZE TYPE MOUNTPOINT FSTYPE      MODEL            SERIAL
sda                       931.8G disk                        APPLE SSD SM1024 S1K6NYAG405813
├─sda1                        1G part /boot/efi  vfat                         
├─sda2                        2G part /boot      ext4                         
└─sda3                    928.8G part            LVM2_member                  
  └─ubuntu--vg-ubuntu--lv   100G lvm  /          ext4                         
```

### smartctl /dev/sda
```
sudo: smartctl: command not found
[command failed: sudo smartctl -a /dev/sda]
```

### df -h
```
Filesystem                         Size  Used Avail Use% Mounted on
tmpfs                              3.2G  1.5M  3.2G   1% /run
/dev/mapper/ubuntu--vg-ubuntu--lv   98G   23G   71G  24% /
tmpfs                               16G     0   16G   0% /dev/shm
tmpfs                              5.0M     0  5.0M   0% /run/lock
/dev/sda2                          2.0G  193M  1.6G  11% /boot
/dev/sda1                          1.1G  6.2M  1.1G   1% /boot/efi
tmpfs                              3.2G   12K  3.2G   1% /run/user/1000
```

### du -sh /srv/janus/*
```
47M	/srv/janus/agent
14M	/srv/janus/agent-backup-2025-10-07-0824.tgz
14M	/srv/janus/agent-backup-2025-10-07-0832.tgz
11M	/srv/janus/bin
12K	/srv/janus/config
156K	/srv/janus/controls
3.1M	/srv/janus/docs
144K	/srv/janus/intel_cache
8.0K	/srv/janus/metrics
386M	/srv/janus/mission_log.jsonl
32K	/srv/janus/missions
4.6G	/srv/janus/models
11M	/srv/janus/philosophy
144K	/srv/janus/proposals.jsonl
20K	/srv/janus/repo
4.0K	/srv/janus/tool_use.jsonl
4.0K	/srv/janus/workspaces
```

### I/O scheduler
```
/sys/block/loop0/queue/scheduler: [none] mq-deadline 
/sys/block/loop1/queue/scheduler: [none] mq-deadline 
/sys/block/loop2/queue/scheduler: [none] mq-deadline 
/sys/block/loop3/queue/scheduler: [none] mq-deadline 
/sys/block/loop4/queue/scheduler: [none] mq-deadline 
/sys/block/loop5/queue/scheduler: [none] mq-deadline 
/sys/block/loop6/queue/scheduler: [none] mq-deadline 
/sys/block/loop7/queue/scheduler: [none] mq-deadline 
/sys/block/sda/queue/scheduler: none [mq-deadline] 
```

## Thermal & Power
### sensors -A
```
amdgpu-pci-0100
vddgfx:      850.00 mV 
edge:         +59.0°C  (crit = +110.0°C, hyst = -273.1°C)
PPT:          15.04 W  (cap = 110.00 W)

coretemp-isa-0000
Package id 0:  +63.0°C  (high = +80.0°C, crit = +100.0°C)
Core 0:        +63.0°C  (high = +80.0°C, crit = +100.0°C)
Core 1:        +59.0°C  (high = +80.0°C, crit = +100.0°C)
Core 2:        +57.0°C  (high = +80.0°C, crit = +100.0°C)
Core 3:        +57.0°C  (high = +80.0°C, crit = +100.0°C)

applesmc-isa-0300
Main :       1198 RPM  (min = 1200 RPM, max = 3177 RPM)
TA0P:         +22.2°C  
TA0V:         +31.0°C  
TA0p:         +42.2°C  
TC0E:         -26.5°C  
TC0F:         -23.0°C  
TC0J:          +3.5°C  
TC0P:         +54.8°C  
TC0T:          +1.0°C  
TC0c:         +62.0°C  
TC0p:         +54.8°C  
TC1c:         +58.0°C  
TC2c:         +58.0°C  
TC3c:         +57.0°C  
TCGc:         +56.0°C  
TCSc:         +58.0°C  
TCXR:         -35.0°C  
TCXc:         +65.0°C  
TCXr:         -35.0°C  
TG0D:         +59.0°C  
TG0E:         +59.5°C  
TG0F:         +59.8°C  
TG0J:          +0.0°C  
TG0P:         +51.5°C  
TG0T:          -0.2°C  
TG0d:         +59.0°C  
TG0p:         +51.5°C  
TG1P:         +52.0°C  
TG1d:         +55.8°C  
TG1p:         +52.0°C  
TG2P:         +52.5°C  
TG2p:         +52.5°C  
TG3P:         +54.5°C  
TG3p:         +54.5°C  
TH0A:        -127.0°C  
TH0B:        -127.0°C  
TH0C:        -127.0°C  
TH0F:        -127.0°C  
TH0O:          +9.0°C  
TH0P:        -127.0°C  
TH0R:        -127.0°C  
TH0a:        -127.0°C  
TH0b:        -127.0°C  
TH0c:        -127.0°C  
TH0e:          +1.0°C  
TH1A:         +46.8°C  
TH1B:         +46.8°C  
TH1C:        -127.0°C  
TH1F:         -34.2°C  
TH1O:          +9.0°C  
TH1P:        -127.0°C  
TH1R:         -34.2°C  
TH1a:         +46.8°C  
TH1b:         +46.8°C  
TH1c:        -127.0°C  
TL0P:         +37.2°C  
TL0V:         +35.8°C  
TL0p:         +37.2°C  
TL1P:         +36.5°C  
TL1V:         +33.2°C  
TL1p:         +36.5°C  
TL1v:         +33.2°C  
TM0P:         +49.5°C  
TM0V:         +54.2°C  
TM0p:         +49.5°C  
TM1P:         +41.0°C  
TM1a:         +62.8°C  
TM1p:         +41.0°C  
TM2P:         +45.8°C  
TM2a:         +57.0°C  
TM2b:         +59.8°C  
TM2c:         +56.2°C  
TM2d:         +63.8°C  
TM2p:         +45.8°C  
TM3P:         +46.8°C  
TM3a:         +59.8°C  
TM3b:         +58.5°C  
TM3c:         +58.5°C  
TM3d:         +55.8°C  
TM3p:         +46.8°C  
TM4a:         +54.2°C  
TMXP:         +49.5°C  
TPCD:         +61.0°C  
TS0V:         +41.2°C  
Tb0P:         +57.8°C  
Tb0p:         +57.8°C  
Tm0P:         +48.5°C  
Tm0p:         +48.5°C  
Tm1P:         +50.0°C  
Tm1p:         +50.0°C  
Tm2P:         +52.8°C  
Tm2p:         +52.8°C  
Tp2F:         +46.2°C  
Tp2H:         +46.0°C  
Tp2h:         +46.0°C  

```

### Fan speeds
```
[command failed: bash -c sensors | grep -i fan]
```

### Power supply uevent
```
[command failed: bash -c for p in /sys/class/power_supply/*/uevent; do [ -e "$p" ] && echo "=== $p" && cat "$p"; done]
```

### turbostat
```
5.001764 sec
PkgWatt
7.73
7.73
```

## System Information
### dmidecode -t system
```
# dmidecode 3.5
Getting SMBIOS data from sysfs.
SMBIOS 2.4 present.

Wrong DMI structures length: 3333 bytes announced, only 2895 bytes available.
Handle 0x0010, DMI type 1, 27 bytes
System Information
	Manufacturer: Apple Inc.
	Product Name: iMac15,1
	Version: 1.0
	Serial Number: DGKPN0X5FY14
	UUID: 4ff6f33e-c0c1-9255-8875-53ed0702a600
	Wake-up Type: Power Switch
	SKU Number: System SKU#
	Family: iMac

Handle 0x002B, DMI type 12, 5 bytes
System Configuration Options

Handle 0x002D, DMI type 32, 20 bytes
System Boot Information
	Status: No errors detected

Wrong DMI structures count: 53 announced, only 50 decoded.
```

### dmidecode -t baseboard
```
# dmidecode 3.5
Getting SMBIOS data from sysfs.
SMBIOS 2.4 present.

Wrong DMI structures length: 3333 bytes announced, only 2895 bytes available.
Handle 0x0011, DMI type 2, 16 bytes
Base Board Information
	Manufacturer: Apple Inc.
	Product Name: Mac-FA842E06C61E91C5
	Version: iMac15,1
	Serial Number: C02504200BAGG3NAT
	Asset Tag: Base Board Asset Tag#
	Features:
		Board is a hosting board
		Board is replaceable
	Location In Chassis: Part Component
	Chassis Handle: 0x0012
	Type: Motherboard
	Contained Object Handles: 0

Handle 0x0026, DMI type 10, 6 bytes
On Board Device Information
	Type: Video
	Status: Enabled
	Description: Not Specified

Handle 0x0027, DMI type 10, 6 bytes
On Board Device Information
	Type: Sound
	Status: Enabled
	Description: Azalia Audio Codec

Handle 0x0028, DMI type 10, 6 bytes
On Board Device Information
	Type: Ethernet
	Status: Enabled
	Description: Caesar IV Ethernet Controller

Handle 0x0029, DMI type 10, 6 bytes
On Board Device Information
	Type: Other
	Status: Enabled
	Description: SATA

Wrong DMI structures count: 53 announced, only 50 decoded.
```

### dmidecode -t chassis
```
# dmidecode 3.5
Getting SMBIOS data from sysfs.
SMBIOS 2.4 present.

Wrong DMI structures length: 3333 bytes announced, only 2895 bytes available.
Handle 0x0012, DMI type 3, 21 bytes
Chassis Information
	Manufacturer: Apple Inc.
	Type: All In One
	Lock: Not Present
	Version: Mac-FA842E06C61E91C5
	Serial Number: DGKPN0X5FY14
	Asset Tag: Not Specified
	Boot-up State: Safe
	Power Supply State: Safe
	Thermal State: Other
	Security Status: Other
	OEM Information: 0x00000000
	Height: Unspecified
	Number Of Power Cords: Unspecified
	Contained Elements: 0

Wrong DMI structures count: 53 announced, only 50 decoded.
```

### lspci -tv
```
-[0000:00]-+-00.0  Intel Corporation 4th Gen Core Processor DRAM Controller
           +-01.0-[01]--+-00.0  Advanced Micro Devices, Inc. [AMD/ATI] Tonga XT / Amethyst XT [Radeon R9 380X / R9 M295X]
           |            \-00.1  Advanced Micro Devices, Inc. [AMD/ATI] Tonga HDMI Audio [Radeon R9 285/380]
           +-14.0  Intel Corporation 8 Series/C220 Series Chipset Family USB xHCI
           +-16.0  Intel Corporation 8 Series/C220 Series Chipset Family MEI Controller #1
           +-1b.0  Intel Corporation 8 Series/C220 Series Chipset High Definition Audio Controller
           +-1c.0-[02]----00.0  Samsung Electronics Co Ltd S4LN053X01 AHCI SSD Controller(Apple slot)
           +-1c.2-[03]----00.0  Broadcom Inc. and subsidiaries BCM4360 802.11ac Dual Band Wireless Network Adapter
           +-1c.3-[04]--+-00.0  Broadcom Inc. and subsidiaries NetXtreme BCM57766 Gigabit Ethernet PCIe
           |            \-00.1  Broadcom Inc. and subsidiaries BCM57765/57785 SDXC/MMC Card Reader
           +-1c.4-[05-9b]----00.0-[06-6b]--+-00.0-[07]----00.0  Intel Corporation DSL5520 Thunderbolt 2 NHI [Falcon Ridge 4C 2013]
           |                               +-03.0-[08-38]--
           |                               +-04.0-[39]--
           |                               +-05.0-[3a-6a]--
           |                               \-06.0-[6b]--
           +-1f.0  Intel Corporation Z87 Express LPC Controller
           \-1f.3  Intel Corporation 8 Series/C220 Series Chipset Family SMBus Controller
```

### lsusb -t
```
/:  Bus 001.Port 001: Dev 001, Class=root_hub, Driver=xhci_hcd/14p, 480M
    |__ Port 002: Dev 002, If 0, Class=Human Interface Device, Driver=usbhid, 12M
    |__ Port 002: Dev 002, If 1, Class=Human Interface Device, Driver=usbhid, 12M
    |__ Port 006: Dev 121, If 0, Class=Human Interface Device, Driver=usbhid, 1.5M
    |__ Port 006: Dev 121, If 1, Class=Human Interface Device, Driver=usbhid, 1.5M
    |__ Port 007: Dev 005, If 0, Class=Video, Driver=uvcvideo, 480M
    |__ Port 007: Dev 005, If 1, Class=Video, Driver=uvcvideo, 480M
    |__ Port 007: Dev 005, If 2, Class=Vendor Specific Class, Driver=[none], 480M
    |__ Port 008: Dev 006, If 0, Class=Hub, Driver=hub/3p, 12M
        |__ Port 003: Dev 009, If 0, Class=Vendor Specific Class, Driver=btusb, 12M
        |__ Port 003: Dev 009, If 1, Class=Wireless, Driver=btusb, 12M
        |__ Port 003: Dev 009, If 2, Class=Vendor Specific Class, Driver=btusb, 12M
        |__ Port 003: Dev 009, If 3, Class=Application Specific Interface, Driver=[none], 12M
/:  Bus 002.Port 001: Dev 001, Class=root_hub, Driver=xhci_hcd/6p, 5000M
```

