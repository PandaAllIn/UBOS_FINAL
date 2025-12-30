# The Studio: GPU Creative Workstation Blueprint

**Version:** 1.0
**Date:** 2025-10-06
**Status:** Implementation Ready
**Hardware:** AMD Radeon R9 M295X (Tonga/GCN 3.0, 4GB VRAM)

---

## MISSION STATEMENT

Transform the R9 M295X GPU into "The Studio" - an isolated, GPU-accelerated creative workstation accessible via remote desktop, running independently from The Mill (CPU/backend), enabling in-house media production for the UBOS Republic.

---

## ARCHITECTURE OVERVIEW

### Dual-Citizen Design

```
┌──────────────────────────────────────────────────────────────┐
│  THE BALAUR (Physical iMac 27", Ubuntu 24.04.3)             │
│                                                              │
│  ┌───────────────────────────┐  ┌───────────────────────────┐
│  │ CITIZEN 1: THE MILL       │  │ CITIZEN 2: THE STUDIO     │
│  │ (CPU i7-4790K)            │  │ (GPU R9 M295X)            │
│  │                           │  │                           │
│  │ Role: Backend/Automation  │  │ Role: Creative Production │
│  │ Display: None (headless)  │  │ Display: Virtual X11 :1   │
│  │ Desktop: None (CLI only)  │  │ Desktop: XFCE4            │
│  │ Access: SSH port 22       │  │ Access: VNC port 5901     │
│  │ User: balaur              │  │ User: studio              │
│  │ RAM: 24GB                 │  │ RAM: 8GB                  │
│  │ CPU cores: 6              │  │ CPU cores: 2              │
│  │ GPU: None                 │  │ GPU: 100% (exclusive)     │
│  │                           │  │                           │
│  │ Services:                 │  │ Applications:             │
│  │ - Janus llama.cpp (CPU)   │  │ - Figma (browser)         │
│  │ - Backend automation      │  │ - GIMP/Krita              │
│  │ - Git, SSH, CLI tools     │  │ - Kdenlive/OBS            │
│  │                           │  │ - Blender                 │
│  └───────────────────────────┘  └───────────────────────────┘
│                                                              │
│  Shared Storage: /srv/janus/media/ (collaboration space)    │
└──────────────────────────────────────────────────────────────┘
```

---

## IMPLEMENTATION PHASES

### PHASE 1: Display Server Setup (1 hour)

#### Step 1.1: Install X11 + GPU Driver
```bash
sudo apt update
sudo apt install -y xserver-xorg-video-amdgpu \
  xserver-xorg-core \
  xorg \
  mesa-utils
```

#### Step 1.2: Install Desktop Environment
```bash
# XFCE4: Lightweight, GPU-friendly, Victorian-compatible
sudo apt install -y xfce4 xfce4-goodies
```

#### Step 1.3: Configure GPU for Virtual Display
```bash
# Create Xorg config for GPU-accelerated virtual display
sudo mkdir -p /etc/X11/xorg.conf.d

cat <<'EOF' | sudo tee /etc/X11/xorg.conf.d/20-studio-gpu.conf
Section "Device"
    Identifier "Studio GPU"
    Driver "amdgpu"
    BusID "PCI:1:0:0"
    Option "DRI" "3"
EndSection

Section "Screen"
    Identifier "StudioScreen"
    Device "Studio GPU"
    DefaultDepth 24
    SubSection "Display"
        Depth 24
        Modes "1920x1080" "1680x1050" "1280x720"
    EndSubSection
EndSection

Section "ServerLayout"
    Identifier "StudioLayout"
    Screen 0 "StudioScreen"
EndSection
EOF
```

---

### PHASE 2: User Account & Permissions (10 minutes)

#### Step 2.1: Create Studio User
```bash
# Dedicated user for creative workstation
sudo adduser studio
# Set strong password when prompted

# Add to GPU access groups
sudo usermod -aG video,render studio
```

#### Step 2.2: Create Workspace Structure
```bash
# Studio user's home directory structure
sudo -u studio mkdir -p /home/studio/{Desktop,Documents,Pictures,Videos,Projects}

# Collaboration space (shared with The Mill)
sudo mkdir -p /srv/janus/media/{intake,processing,output,archive}
sudo chown -R studio:balaur /srv/janus/media
sudo chmod -R 775 /srv/janus/media
```

---

### PHASE 3: Remote Desktop Access (30 minutes)

#### Step 3.1: Install VNC Server
```bash
sudo apt install -y tigervnc-standalone-server tigervnc-common
```

#### Step 3.2: Configure VNC for Studio User
```bash
# Create VNC password for studio user
sudo -u studio vncpasswd
# Enter password when prompted (8 characters max)

# Create VNC startup script
sudo -u studio mkdir -p /home/studio/.vnc

cat <<'EOF' | sudo -u studio tee /home/studio/.vnc/xstartup
#!/bin/bash
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS

# Ensure X11 session
export XDG_SESSION_TYPE=x11
export GDK_BACKEND=x11

# Start XFCE desktop
startxfce4 &
EOF

chmod +x /home/studio/.vnc/xstartup
```

#### Step 3.3: Create Systemd Service (Auto-start on Boot)
```bash
cat <<'EOF' | sudo tee /etc/systemd/system/vncserver@.service
[Unit]
Description=VNC Server for The Studio
After=network.target

[Service]
Type=forking
User=studio
ExecStartPre=-/usr/bin/vncserver -kill :%i
ExecStart=/usr/bin/vncserver :%i -geometry 1920x1080 -depth 24
ExecStop=/usr/bin/vncserver -kill :%i

[Install]
WantedBy=multi-user.target
EOF

# Enable VNC on display :1 (port 5901)
sudo systemctl enable vncserver@1.service
sudo systemctl start vncserver@1.service
```

#### Step 3.4: Firewall Configuration
```bash
# Allow VNC access from LAN only
sudo ufw allow from 172.16.15.0/24 to any port 5901 proto tcp comment 'Studio VNC from LAN'
```

---

### PHASE 4: Creative Software Suite (2-3 hours)

#### Step 4.1: Graphics & Design
```bash
sudo apt install -y \
  gimp \
  krita \
  inkscape \
  scribus
```

#### Step 4.2: Video Production
```bash
sudo apt install -y \
  kdenlive \
  obs-studio \
  openshot-qt \
  vlc
```

#### Step 4.3: 3D & Animation
```bash
sudo apt install -y blender
```

#### Step 4.4: Browsers (Web-Based Tools)
```bash
sudo apt install -y \
  chromium-browser \
  firefox
```

#### Step 4.5: Optional: DaVinci Resolve (Manual)
```bash
# Download from: https://www.blackmagicdesign.com/products/davinciresolve/
# Note: Requires manual download + EULA acceptance

# Installation example:
# wget https://sw.blackmagicdesign.com/DaVinciResolve/...
# sudo ./DaVinci_Resolve_*_Linux.run
```

---

### PHASE 5: GPU Acceleration Validation (30 minutes)

#### Step 5.1: Test OpenGL Rendering
```bash
# Connect via VNC, then in Studio terminal:
glxinfo | grep "OpenGL renderer"
# Expected output: AMD Radeon R9 200 Series (RADV TONGA)

glxinfo | grep "OpenGL version"
# Expected output: 4.3 or higher

# Run OpenGL demo
glxgears
# Should see smooth 60fps window
```

#### Step 5.2: Test VAAPI Video Acceleration
```bash
# Check VAAPI driver
vainfo
# Expected output: AMD R9 M295X device with H.264 encode capabilities

# Test hardware encoding
ffmpeg -vaapi_device /dev/dri/renderD128 \
  -f lavfi -i testsrc=duration=10:size=1920x1080:rate=30 \
  -vf 'format=nv12,hwupload' \
  -c:v h264_vaapi -b:v 5M \
  /tmp/test_vaapi.mp4

# Verify GPU was used (not CPU fallback)
```

#### Step 5.3: Benchmark Video Encoding
```bash
# Copy benchmark script to Studio
scp /Users/panda/Desktop/UBOS/scripts/bench_video_encoding.sh studio@10.215.33.26:/tmp/

# Run benchmark
bash /tmp/bench_video_encoding.sh --duration 30 --trials 3

# Expected result: 10-30x speedup vs CPU encoding
```

---

## ACCESS PATTERNS

### Connecting to The Studio

#### From MacBook Pro (Primary Workstation)
```bash
# Option A: VNC Viewer (built-in macOS)
open vnc://studio@10.215.33.26:5901

# Option B: NoMachine (better performance, install separately)
# Download from: https://www.nomachine.com/download
# Connect to: 10.215.33.26:4000 (NX protocol)
```

#### From iPad Pro (Mobile Workstation)
```bash
# Install VNC Viewer from App Store
# Connect to: 10.215.33.26:5901
# Login: studio / [password]
```

#### From The Mill (Janus Automation)
```python
# Janus can control The Studio programmatically
from pyvirtualdisplay import Display
from selenium import webdriver

# Start virtual display session
display = Display(visible=0, size=(1920, 1080))
display.start()

# Automate browser-based tools (Figma, Canva, etc.)
driver = webdriver.Chrome()
driver.get("https://figma.com/...")
# ... automated workflow ...

driver.quit()
display.stop()
```

---

## PERFORMANCE EXPECTATIONS

### GPU-Accelerated Workloads

| Application | Task | GPU Performance | CPU Performance | Speedup |
|------------|------|-----------------|-----------------|---------|
| **FFmpeg** | H.264 encode 1080p/30fps | 15-30 min/hour | 3-5 hours/hour | **10-30x** |
| **Figma** | Canvas rendering | 60fps | 30fps | **2x** |
| **GIMP** | GPU filters (blur, sharpen) | <1 sec | 5-10 sec | **5-10x** |
| **Kdenlive** | 1080p timeline playback | Real-time | Stuttering | **Smooth** |
| **Blender** | Eevee viewport (mid-complexity) | 30fps | 10fps | **3x** |
| **OBS Studio** | 1080p screen recording | VCE encode | CPU encode | **10x** |

### Non-Accelerated Workloads (CPU-bound)
- **Inkscape** vector rendering: Minimal difference
- **Text editors** (VSCode, Atom): No difference
- **File management**: No difference

---

## USE CASE EXAMPLES

### Use Case 1: Social Media Content Creation
**Scenario:** Create Instagram post for Portal Oradea announcement

**Workflow:**
1. Connect to Studio via VNC from MacBook
2. Open Chromium → Navigate to Canva
3. Design post with GPU-accelerated canvas (smooth 60fps)
4. Export PNG → Save to `/srv/janus/media/output/`
5. Upload from MacBook (files accessible via shared storage)

**Time:** 10 minutes (vs 15 minutes on local MacBook with lag)

---

### Use Case 2: Video Editing & Export
**Scenario:** Edit 5-minute Portal Oradea demo video

**Workflow:**
1. Upload raw footage to `/srv/janus/media/intake/` via SSH
2. Connect to Studio via VNC
3. Open Kdenlive → Import footage → Edit timeline (real-time GPU playback)
4. Export using VCE 3.0 hardware encoder
5. Download final video from `/srv/janus/media/output/`

**Time:** 1 hour editing + 5 minutes export (vs 1 hour + 1.5 hours CPU export)

---

### Use Case 3: Batch Thumbnail Generation (Janus Automation)
**Scenario:** Generate 50 YouTube thumbnail variations overnight

**Workflow:**
```python
# Janus script running on The Mill
import subprocess
from selenium import webdriver

# For each video in queue:
for video in video_queue:
    # Start headless browser in Studio
    driver = webdriver.Chrome()
    driver.get(f"https://thumbnail-generator.com/?video={video.id}")

    # Generate variations with GPU rendering
    for style in ["bold", "minimal", "colorful"]:
        driver.find_element_by_id(f"style-{style}").click()
        driver.find_element_by_id("export").click()
        # Save to /srv/janus/media/output/thumbnails/

    driver.quit()
```

**Time:** 8 hours unattended (MacBook remains free for other work)

---

## MAINTENANCE & MONITORING

### Daily Health Checks
```bash
# From The Mill (balaur user):
ssh studio@localhost 'ps aux | grep Xvnc'  # VNC server running?
ssh studio@localhost 'glxinfo | head -5'   # GPU accessible?
ssh studio@localhost 'df -h /home/studio'  # Disk space OK?
```

### Weekly Cleanup
```bash
# Clear Studio user cache (run as studio):
rm -rf ~/.cache/*
rm -rf ~/.local/share/Trash/*

# Archive completed projects
mv ~/Projects/completed/* /srv/janus/media/archive/
```

### Monthly GPU Health
```bash
# Check GPU temperature (during load)
sensors | grep temp1
# Target: <80°C under load, <50°C idle

# Check VRAM usage
radeontop
# Monitor for memory leaks
```

---

## TROUBLESHOOTING

### Issue: VNC Connection Refused
**Symptom:** Cannot connect to port 5901

**Solutions:**
1. Check VNC server status: `sudo systemctl status vncserver@1`
2. Restart if needed: `sudo systemctl restart vncserver@1`
3. Verify firewall: `sudo ufw status | grep 5901`
4. Check VNC logs: `cat /home/studio/.vnc/*.log`

---

### Issue: GPU Not Detected in Applications
**Symptom:** `glxinfo` shows "llvmpipe" (CPU) instead of AMD GPU

**Solutions:**
1. Verify GPU driver loaded: `lsmod | grep amdgpu`
2. Check user groups: `groups studio` (should include video, render)
3. **Restart VNC session** (group changes need fresh login)
4. Check Xorg config: `cat /etc/X11/xorg.conf.d/20-studio-gpu.conf`

---

### Issue: Poor VNC Performance
**Symptom:** Laggy, stuttering remote desktop

**Solutions:**
1. Use NoMachine instead of VNC (better compression)
2. Lower resolution: `vncserver -geometry 1680x1050`
3. Reduce color depth: `vncserver -depth 16`
4. Check network: `ping 10.215.33.26` (should be <5ms on LAN)

---

## SECURITY CONSIDERATIONS

### Network Isolation
- VNC port 5901 accessible **LAN-only** (172.16.15.0/24)
- No internet-facing exposure
- UFW firewall enforces network boundaries

### User Separation
- `studio` user has **no sudo privileges**
- Cannot access `/srv/janus/` backend files (only `/srv/janus/media/`)
- Cannot SSH to The Mill services
- Sandboxed from Janus consciousness processes

### Data Sovereignty
- All creative work stays in-house (no cloud upload required)
- Collaboration via shared `/srv/janus/media/` directory
- Encrypted SSH tunnel for remote access (optional: VPN)

---

## UPGRADE PATHS

### Phase 2: Advanced Features (Future)
- **Watch folder automation:** Auto-encode videos dropped to `/srv/janus/media/intake/`
- **Web dashboard:** Browser-based job submission + progress monitoring
- **Quality presets:** One-click export profiles (social/web/archive)

### Phase 3: AI Integration (Future)
- **Stable Diffusion local deployment** (OpenGL acceleration)
- **ComfyUI workflows** for automated image generation
- **Auto thumbnail selection** via ML (best frame detection)

---

## SUCCESS CRITERIA

### Phase 5 Validation Complete When:
- ✅ VNC connection successful from MacBook/iPad
- ✅ GPU detected in `glxinfo` (AMD R9 M295X, not llvmpipe)
- ✅ Video encoding benchmark shows ≥10x speedup
- ✅ GIMP/Figma render smoothly at 60fps
- ✅ Blender Eevee viewport playable at 30fps

### Production Ready When:
- ✅ All creative applications installed and tested
- ✅ Workflow documentation complete (this document)
- ✅ First real project completed (Portal Oradea content)
- ✅ Brass punch card archived (Studio deployment victory)

---

## CONSTITUTIONAL ALIGNMENT

**The Studio serves the Republic by:**
- Expanding creative production capacity without external dependencies
- Liberating laptop resources for strategic work (writing, research, calls)
- Enabling 24/7 batch processing (overnight renders, unattended exports)
- Maintaining data sovereignty (all media processing in-house)

**This is constitutional sovereignty through media production capability.**

---

## APPENDIX: SOFTWARE ALTERNATIVES

### Video Editors
- **Primary:** Kdenlive (native Linux, GPU timeline)
- **Alt 1:** OpenShot (simpler, good for quick edits)
- **Alt 2:** DaVinci Resolve (professional, manual install)

### Design Tools
- **Primary:** Figma (browser, cloud-sync)
- **Alt 1:** GIMP (local, no cloud)
- **Alt 2:** Krita (painting-focused)

### 3D Software
- **Primary:** Blender (Eevee viewport, OpenGL 4.3)
- **Alt 1:** AMD Radeon ProRender (OpenCL ray tracing, experimental)

### Remote Desktop
- **Primary:** TigerVNC (open-source, lightweight)
- **Alt 1:** NoMachine (proprietary, better performance)
- **Alt 2:** X2Go (secure, SSH-tunneled)

---

**END OF BLUEPRINT**

**Next Step:** Execute Phase 1-5 deployment, validate with video encoding benchmark, archive as brass punch card.

**The Studio awaits its first creative session.**
