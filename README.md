
# VM Auto-Scaler Using CPU Monitoring with Libvirt & Python

This project implements an automatic virtual machine (VM) scaling system using Python, Flask, and KVM/libvirt. It dynamically clones new VMs when CPU usage exceeds a configured threshold, simulating cloud-style autoscaling behavior in a local virtualized environment.


## Requirements

- Host OS with libvirt + KVM/QEMU
- At least one base VM template (e.g., vm2)
- Python 3.6+
- pip packages: Flask, psutil, requests
- CLI tools: virt-clone, virsh


## Components

- monitor.py — Runs inside VM1, monitors CPU load and exposes a `/cpu` API via Flask.
- scaler.py — Runs on the host, polls CPU stats and triggers VM cloning using libvirt tools.


## Features

- Real-time CPU monitoring from VM1 via REST API
- Auto-scaling of VMs by cloning a base template (vm2) using virt-clone
- Configurable threshold & max VM count to prevent resource overuse
- Clean integration with libvirt APIs and subprocess automation


## Setup & Usage

### 1️⃣ Install Dependencies (Host & VM)

  pip install -r requirements.txt

- Ensure libvirt & virt-clone are installed on the host:

  sudo apt install libvirt-clients virt-manager virtinst

### 2️⃣ Run the Monitor (Inside VM1)
- Edit monitor.py to set the correct host IP:

  HOST_IP = "<host-ip>"

- Then run:

  python3 monitor.py

### 3️⃣ Run the Scaler (On Host)
- Ensure that vm2 exists and is shut off (not running).
- Then start the scaler service:

  python3 scaler.py

### 4️⃣ Trigger Load (From Host)
- Use ApacheBench or any load generator to simulate CPU spike:

  ab -n 5000 -c 50 http://<vm1-ip>:5000/cpu


## Sample Output
Current CPU Usage: 42.0%

CPU usage exceeded threshold! Initiating scaling...

Cloning vm2 to create vm3...

Scaling complete: vm3 created

