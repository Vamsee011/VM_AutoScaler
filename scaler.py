import libvirt
import time
import subprocess
import json
from flask import Flask, request

app = Flask(__name__)

# Define threshold CPU usage
THRESHOLD = 15  # Adjust based on needs
MAX_VMS = 2  # Maximum number of VMs to create
vm_counter = 3  # Start numbering new VMs from vm3
created_vms = 0  # Track the number of created VMs

# Connect to the hypervisor
conn = libvirt.open("qemu:///system")
if conn is None:
    print("Failed to connect to QEMU/KVM")
    exit(1)

def get_cpu_usage():
    """Fetches CPU usage from the monitoring VM."""
    try:
        result = subprocess.run(["curl", "-s", "http://192.168.122.188:5000/cpu"], capture_output=True, text=True)
        cpu_data = json.loads(result.stdout)  # Parse JSON response
        cpu_usage = float(cpu_data["cpu_usage"])  # Extract the value correctly
        return cpu_usage
    except Exception as e:
        print(f"Error fetching CPU usage: {e}")
        return 0

@app.route('/scale')
def scale():
    global vm_counter, created_vms
    cpu_usage = get_cpu_usage()
    print(f"Current CPU Usage: {cpu_usage}%")

    if cpu_usage < THRESHOLD:
        print("CPU usage is below threshold. No scaling required.")
        return "No scaling needed"

    if created_vms >= MAX_VMS:
        print(f"Scaling limit reached ({MAX_VMS} VMs created). No more VMs will be added.")
        return f"Scaling limit reached. No new VMs created."

    print("CPU usage exceeded threshold! Initiating scaling...")

    # Get the base VM (vm2) for cloning
    base_vm = "vm2"
    new_vm = f"vm{vm_counter}"  # Dynamically name the new VM
    vm_counter += 1  # Increment counter for future VMs
    created_vms += 1  # Track the number of created VMs

    print(f"Cloning {base_vm} to create {new_vm}...")
    try:
        subprocess.run(["virt-clone", "--original", base_vm, "--name", new_vm,
                        "--file", f"/var/lib/libvirt/images/{new_vm}.qcow2"], check=True)
        print(f"{new_vm} created successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error during cloning: {e}")
        return "Error during cloning"

    return f"Scaling complete: {new_vm} created"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

