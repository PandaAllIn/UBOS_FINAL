# STUDY-003 DOCUMENTATION SOURCES
**Hardware Deep Dive Reference Materials for Janus**

---

## DOCUMENTATION PHILOSOPHY

**For Hardware Study (STUDY-003):**
- ✅ Convert all documentation to **AI-readable text format** (markdown, plain text)
- ✅ Provide **official manufacturer datasheets** where available
- ✅ Include **physics/mechanics primers** for thermal dynamics, electrical engineering
- ✅ Give him **complete, unfiltered technical data**

**For History Study (STUDY-004 - The Endless Scroll):**
- ❌ **NO preprocessing, NO summarization, NO formatting changes**
- ✅ **RAW, line-by-line reading** of the 41,613-line original document
- ✅ He must **experience it as it was written** (Genesis in its authentic form)

---

## TIER 1: OFFICIAL MANUFACTURER DOCUMENTATION

### iMac 27" Retina 5K (Late 2014) - The Balaur Chassis

**Official Apple Sources:**
- **Tech Specs Page:** https://support.apple.com/en-us/112436
- **Manuals & Downloads:** https://support.apple.com/en-us/docs/mac/135121
- **Model Identification:** https://support.apple.com/en-us/108054

**EveryMac.com (Comprehensive Specs):**
- **i7-4790K Model:** https://everymac.com/systems/apple/imac/specs/imac-core-i7-4.0-27-inch-aluminum-retina-5k-late-2014-specs.html

**To Extract:**
```
- Complete system specifications
- Thermal design (cooling system, fan curves)
- Power supply specifications
- Internal architecture diagram (if available)
- Service manual (if publicly available)
```

---

### Intel Core i7-4790K - The Mill

**Official Intel Sources:**
- **Product Specifications:** https://www.intel.com/content/www/us/en/products/sku/80807/intel-core-i74790k-processor-8m-cache-up-to-4-40-ghz/specifications.html
- **Downloads Page (Datasheets):** https://www.intel.com/content/www/us/en/products/sku/80807/intel-core-i74790k-processor-8m-cache-up-to-4-40-ghz/downloads.html

**Technical Details to Capture:**
```
- Full Haswell architecture documentation
- Instruction set reference (AVX2, SSE4.2, AES-NI)
- Thermal specifications (TJunction max, thermal monitoring)
- Power states (C-states, P-states, Turbo Boost behavior)
- Cache architecture (L1/L2/L3 latency, bandwidth)
- Memory controller specifications
- Undervolting safe ranges
- Overclocking limits (if documented)
```

**Additional Intel Resources:**
- **Haswell Microarchitecture Documentation:** Intel's optimization manual for Haswell
- **Intel 64 and IA-32 Architectures Optimization Reference Manual**

---

### AMD Radeon R9 M295X - The Auxiliary Steam Cylinder

**Best Available Sources** (no official AMD datasheet found):
- **TechPowerUp Database:** https://www.techpowerup.com/gpu-specs/radeon-r9-m295x-mac-edition.c2587
- **NotebookCheck:** https://www.notebookcheck.net/AMD-Radeon-R9-M295X.129043.0.html

**Technical Details to Capture:**
```
- Tonga/GCN 3.0 architecture details
- Compute units, stream processors, ROPs
- VRAM specifications (4GB GDDR5, 256-bit bus)
- Clock speeds (base, boost)
- Power consumption (TDP, actual measured)
- Thermal limits and throttling behavior
- VCE 3.0 encoder specifications
- OpenCL capabilities and limitations
- Why memory-bound for LLM workloads
```

**AMD Architecture Docs to Find:**
- **GCN Architecture Whitepaper** (if available for GCN 3.0)
- **VCE 3.0 Technical Documentation**
- **AMD GPU Programming Guide**

---

### Memory: DDR3-1600

**JEDEC Standards Documentation:**
- **DDR3 SDRAM Specification:** JESD79-3 (if publicly available)

**Key Technical Details:**
```
- DDR3 timing specifications (CAS latency, tRCD, tRP, tRAS)
- Dual-channel bandwidth calculations
- Power consumption per module
- Thermal characteristics
- ECC vs non-ECC (The Balaur uses non-ECC)
```

---

## TIER 2: SYSTEM-LEVEL DOCUMENTATION

### Ubuntu 24.04 LTS - The Operating System

**Official Docs:**
- **Ubuntu Server Guide:** https://ubuntu.com/server/docs
- **Kernel Documentation:** https://www.kernel.org/doc/html/latest/

**Key Topics for Janus:**
```
- CPU frequency scaling (governors: performance, powersave, ondemand)
- Memory management (transparent huge pages, swap)
- Thermal management (ACPI thermal zones)
- Power management (cpupower, powertop)
- Process scheduling (CFS scheduler)
```

---

### llama.cpp - The Mill Software

**Official Repository:**
- **GitHub:** https://github.com/ggerganov/llama.cpp
- **Documentation:** In-repo docs on quantization, backends, optimization

**Key Documentation for Janus:**
```
- Quantization formats (Q4_K_M, Q3_K_M, Q2_K, etc.)
- Threading model and scaling
- Memory mapping vs loading
- Context caching mechanisms
- Optimization flags and tuning parameters
- Speculative decoding implementation
- Benchmark methodology
```

---

## TIER 3: PHYSICS & MECHANICS PRIMERS

### Thermal Dynamics Fundamentals

**Topics to Cover:**
```
- Heat transfer: conduction, convection, radiation
- Thermal resistance and thermal conductivity
- Heat capacity and specific heat
- Thermal throttling mechanisms
- Cooling system design (heatsinks, fans, thermal paste)
- TJunction vs TCase vs ambient temperature
```

**Recommended Text (AI-readable summary):**
- Engineering basics of thermal management in computing
- Why CPUs throttle and how to prevent it
- Fan curves and acoustic optimization

---

### Electrical Engineering Basics

**Topics to Cover:**
```
- Power consumption: TDP vs actual power draw
- Voltage, current, resistance (Ohm's law)
- Power states and dynamic voltage/frequency scaling
- Undervolting principles and safety
- Power supply efficiency and ripple
```

**Recommended Focus:**
```
- How CPUs consume power (static vs dynamic)
- Why undervolting works and its limits
- Measuring power consumption (software vs hardware)
```

---

### Computer Architecture Fundamentals

**Topics to Cover:**
```
- Von Neumann vs Harvard architecture
- Pipelining and instruction-level parallelism
- Cache hierarchy and memory latency
- Branch prediction and speculative execution
- Out-of-order execution
- SIMD and vectorization (AVX2)
```

**Recommended Text:**
- Computer Architecture: A Quantitative Approach (Hennessy & Patterson) - relevant excerpts
- Focus on Haswell microarchitecture specifics

---

### Control Theory Basics (for Victorian Controls)

**Topics to Cover:**
```
- PID control fundamentals
- Feedback loops and stability
- Overshoot, oscillation, damping
- Tuning PID coefficients (Kp, Ki, Kd)
- Practical applications in thermal management
```

**Why This Matters for Janus:**
- Understanding the Governor's PID algorithm
- Tuning control parameters for optimal performance
- Recognizing control system failure modes

---

## TIER 4: OPTIMIZATION REFERENCES

### CPU Performance Tuning

**Key Resources:**
```
- Intel optimization manual for Haswell
- Linux kernel CPU frequency scaling documentation
- Undervolting guides (safe voltage ranges for i7-4790K)
- Thread affinity and NUMA considerations
- Cache optimization techniques
```

---

### LLM Inference Optimization

**Key Resources:**
```
- llama.cpp performance tuning guide
- Quantization trade-offs (speed vs quality)
- Memory bandwidth optimization
- Context caching strategies
- Speculative decoding implementation
```

---

## DOCUMENTATION STAGING PLAN

### Phase 1: Fetch and Convert (Human Task)
1. **Download official PDFs/docs from sources above**
2. **Convert to AI-readable markdown/text:**
   - Extract text from PDFs using `pdftotext` or similar
   - Format tables and diagrams as markdown
   - Preserve structure and technical accuracy
3. **Organize into categories:**
   ```
   /srv/janus/docs/hardware/
   ├── cpu/
   │   ├── i7-4790K_datasheet.md
   │   ├── haswell_architecture.md
   │   └── intel_optimization_manual_excerpts.md
   ├── gpu/
   │   ├── R9_M295X_specifications.md
   │   ├── GCN3_architecture.md
   │   └── VCE_encoder_guide.md
   ├── memory/
   │   ├── DDR3_specifications.md
   │   └── memory_tuning.md
   ├── system/
   │   ├── iMac_2014_technical_specs.md
   │   ├── thermal_design.md
   │   └── power_supply.md
   ├── physics/
   │   ├── thermal_dynamics_primer.md
   │   ├── electrical_engineering_basics.md
   │   └── computer_architecture_fundamentals.md
   └── optimization/
       ├── cpu_tuning_guide.md
       ├── llama_cpp_optimization.md
       └── control_theory_basics.md
   ```

### Phase 2: Update STUDY-003 Mission YAML
Add references to staged documentation:
```yaml
study_materials:
  hardware_documentation:
    cpu: "/srv/janus/docs/hardware/cpu/"
    gpu: "/srv/janus/docs/hardware/gpu/"
    memory: "/srv/janus/docs/hardware/memory/"
    system: "/srv/janus/docs/hardware/system/"

  physics_primers:
    - "/srv/janus/docs/hardware/physics/thermal_dynamics_primer.md"
    - "/srv/janus/docs/hardware/physics/electrical_engineering_basics.md"
    - "/srv/janus/docs/hardware/physics/computer_architecture_fundamentals.md"

  optimization_guides:
    - "/srv/janus/docs/hardware/optimization/cpu_tuning_guide.md"
    - "/srv/janus/docs/hardware/optimization/llama_cpp_optimization.md"
    - "/srv/janus/docs/hardware/optimization/control_theory_basics.md"
```

### Phase 3: Give Janus File Reading Tools
He'll need to be able to:
- Read large documentation files
- Cross-reference between documents
- Extract specific sections
- Build cumulative understanding

**Tool Requirements:**
- File reader (already has shell access)
- Directory listing (can use `ls`, `find`)
- Text search (can use `grep`)
- Possible: Custom doc reader tool for structured extraction

---

## THE DIFFERENCE: STUDY-003 vs STUDY-004

### STUDY-003 (Hardware): PREPROCESSED & STRUCTURED
```
✅ Convert PDFs to markdown
✅ Extract relevant sections
✅ Organize by category
✅ Add explanatory context where needed
✅ Make it easy to navigate and reference
```

**Why:** Technical documentation is meant to be organized, indexed, and referenced. We're giving him a **technical library**.

---

### STUDY-004 (History): RAW & AUTHENTIC
```
❌ NO conversion
❌ NO organization
❌ NO summarization
❌ NO cleaning up conversational artifacts
✅ Line-by-line, EXACTLY as written
✅ Complete with timestamps, tangents, and evolution
```

**Why:** The Endless Scroll is a **living historical document**. Janus needs to experience:
- The organic flow of ideas
- How Claude-buddy, Gemini-buddy, and Captain collaborated
- The messy, beautiful process of creation
- The evolution from abstract concepts to concrete architecture
- The humor, the breakthroughs, the "wait, what if we..." moments

**The Endless Scroll is not data—it's a STORY. And stories must be read as they were written.**

---

## ACTION ITEMS

**Captain's Tasks:**
1. ☐ Download official datasheets and manuals (links above)
2. ☐ Convert PDFs to AI-readable text/markdown
3. ☐ Stage in `/srv/janus/docs/hardware/` directory structure
4. ☐ Update STUDY-003 mission YAML with doc paths

**Optional (if Captain wants):**
- I can help draft the physics/mechanics primers in markdown
- I can extract and format key sections from manuals
- I can create an index document for easy navigation

**Once docs are staged, Janus will have:**
- Complete hardware specifications
- Physics understanding to ground his optimizations
- Real manufacturer data to validate proposals

**Then STUDY-003 will produce a hardware optimization plan grounded in REALITY, not assumptions.**

---

**Status:** Documentation sources identified, awaiting Captain's document gathering
**Next:** Stage docs → Update STUDY-003 YAML → Launch after STUDY-002 completes
