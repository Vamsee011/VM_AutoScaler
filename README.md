# VM Auto-Scaler Using CPU Monitoring with Libvirt & Python

This project implements an automatic virtual machine scaling system using Python and KVM/libvirt. It dynamically creates new VMs when CPU usage exceeds a configured threshold.

## 🛠️ Components

- `monitor.py` — Runs inside VM1, exposes CPU usage via Flask API.
- `scaler.py` — Runs on the host system, polls VM1 and creates new VMs via `virt-clone`.

## 💡 Features

- CPU usage monitoring via REST API (Flask + psutil)
- Auto-scaling by cloning a base VM (e.g., vm2) when CPU exceeds threshold
- Scaling limit control to prevent excessive VM creation
- Libvirt + virt-clone CLI integration

## 🚀 Setup & Usage

### 1. Install dependencies

On host and VM:
```bash
pip install -r requirements.txt

