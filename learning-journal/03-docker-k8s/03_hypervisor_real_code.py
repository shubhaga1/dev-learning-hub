# ============================================================
# REAL VM CREATION — VirtualBox + AWS EC2
#
# OPTION A: VirtualBox (local)
#   - Uses VBoxManage CLI (comes with VirtualBox)
#   - If VirtualBox NOT installed → shows the command that WOULD run
#
# OPTION B: AWS EC2 (cloud)
#   - Uses boto3 with dummy keys → shows the API call that WOULD run
#   - With real keys → actually creates VM on AWS
#
# pip install boto3
# ============================================================

import subprocess
import time


# ============================================================
# HELPER — runs a shell command, shows it even if it fails
# ============================================================
def run_cmd(label, cmd):
    print(f"\n[{label}]")
    print(f"  Command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  ✅ Success: {result.stdout.strip()}")
    else:
        print(f"  ❌ Failed (VirtualBox not installed or VM doesn't exist)")
        print(f"  Error : {result.stderr.strip()[:100]}")
    return result


# ============================================================
# OPTION A — VirtualBox (local)
# ============================================================

class VirtualBoxVM:

    def __init__(self, name, ram_mb=2048, disk_mb=20000):
        self.name    = name
        self.ram_mb  = ram_mb
        self.disk_mb = disk_mb
        print(f"\n[VirtualBoxVM.__init__]")
        print(f"  name={name}, ram={ram_mb}MB, disk={disk_mb}MB")
        print(f"  → No VM created yet. Just storing config.")

    def create(self):
        # Registers a new empty VM in VirtualBox
        run_cmd("VirtualBoxVM.create",
            ["VBoxManage", "createvm", "--name", self.name, "--register"])

    def set_memory(self):
        # Allocates RAM to the VM
        run_cmd("VirtualBoxVM.set_memory",
            ["VBoxManage", "modifyvm", self.name, "--memory", str(self.ram_mb)])

    def set_os_type(self):
        # Tells VirtualBox which OS type this is (helps with defaults)
        run_cmd("VirtualBoxVM.set_os_type",
            ["VBoxManage", "modifyvm", self.name, "--ostype", "Ubuntu_64"])

    def create_disk(self):
        # Creates a .vdi virtual hard disk file on your Mac
        run_cmd("VirtualBoxVM.create_disk",
            ["VBoxManage", "createmedium", "disk",
             "--filename", f"{self.name}.vdi",
             "--size", str(self.disk_mb)])

    def add_storage_controller(self):
        # Adds a SATA controller so we can attach the disk
        run_cmd("VirtualBoxVM.add_storage_controller",
            ["VBoxManage", "storagectl", self.name,
             "--name", "SATA", "--add", "sata", "--controller", "IntelAhci"])

    def attach_disk(self):
        # Connects the .vdi disk to the VM
        run_cmd("VirtualBoxVM.attach_disk",
            ["VBoxManage", "storageattach", self.name,
             "--storagectl", "SATA", "--port", "0", "--device", "0",
             "--type", "hdd", "--medium", f"{self.name}.vdi"])

    def attach_iso(self, iso_path="/Users/shubhamgarg/Downloads/ubuntu.iso"):
        # Attaches Ubuntu ISO so the VM can install the OS on first boot
        run_cmd("VirtualBoxVM.attach_iso",
            ["VBoxManage", "storageattach", self.name,
             "--storagectl", "SATA", "--port", "1", "--device", "0",
             "--type", "dvddrive", "--medium", iso_path])

    def start(self):
        # ACTUALLY starts the VM — a VirtualBox window opens on your screen
        run_cmd("VirtualBoxVM.start",
            ["VBoxManage", "startvm", self.name, "--type", "gui"])

    def status(self):
        # Shows current state: running / stopped / paused
        run_cmd("VirtualBoxVM.status",
            ["VBoxManage", "showvminfo", self.name, "--machinereadable"])

    def stop(self):
        # Powers off the VM (hard stop, like pulling the power cable)
        run_cmd("VirtualBoxVM.stop",
            ["VBoxManage", "controlvm", self.name, "poweroff"])

    def delete(self):
        # Permanently deletes VM + all disk files
        run_cmd("VirtualBoxVM.delete",
            ["VBoxManage", "unregistervm", self.name, "--delete"])


# ============================================================
# OPTION B — AWS EC2 (cloud)
# Uses dummy keys here → will show AuthError but prints the API call
# Replace with real keys to actually create a VM
# ============================================================

class AWSEC2VM:

    # Dummy keys — shows the API call but will fail auth
    # Replace with real keys from AWS Console → IAM → Access Keys
    AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
    AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    REGION         = "us-east-1"

    def __init__(self, name, instance_type="t2.micro"):
        """
        instance_type options:
          t2.micro  → 1 vCPU, 1GB RAM   → Free tier eligible
          t2.medium → 2 vCPU, 4GB RAM   → ~$0.046/hour
          t3.large  → 2 vCPU, 8GB RAM   → ~$0.083/hour
        """
        self.name          = name
        self.instance_type = instance_type
        self.instance_id   = None
        print(f"\n[AWSEC2VM.__init__]")
        print(f"  name={name}, type={instance_type}")
        print(f"  region={self.REGION}")
        print(f"  → No VM created yet. Just storing config.")

    def _get_ec2(self):
        import boto3
        return boto3.resource(
            "ec2",
            region_name=self.REGION,
            aws_access_key_id=self.AWS_ACCESS_KEY,
            aws_secret_access_key=self.AWS_SECRET_KEY
        )

    def create(self, ami_id="ami-0c55b159cbfafe1f0"):
        """
        ami_id = which OS image to use
          ami-0c55b159cbfafe1f0 = Ubuntu 20.04 (us-east-1)
        With real keys → actual VM boots on AWS in ~2 minutes
        With dummy keys → shows AuthorizationError
        """
        import boto3
        from botocore.exceptions import ClientError

        print(f"\n[AWSEC2VM.create]")
        print(f"  Calling: ec2.create_instances(")
        print(f"    ImageId='{ami_id}',")
        print(f"    InstanceType='{self.instance_type}',")
        print(f"    MinCount=1, MaxCount=1,")
        print(f"    Tags=[{{Name: '{self.name}'}}]")
        print(f"  )")

        try:
            ec2 = self._get_ec2()
            instances = ec2.create_instances(
                ImageId=ami_id,
                InstanceType=self.instance_type,
                MinCount=1,
                MaxCount=1,
                TagSpecifications=[{
                    "ResourceType": "instance",
                    "Tags": [{"Key": "Name", "Value": self.name}]
                }]
            )
            self.instance_id = instances[0].id
            print(f"  ✅ Instance created! ID: {self.instance_id}")

        except ClientError as e:
            print(f"  ❌ AWS Error: {e.response['Error']['Message']}")
            print(f"  → Expected with dummy keys. Use real AWS keys to actually create a VM.")

    def wait_until_running(self):
        """
        Polls AWS every 15 seconds until VM state = 'running'
        With real keys takes ~2 minutes
        """
        import boto3
        from botocore.exceptions import ClientError

        print(f"\n[AWSEC2VM.wait_until_running]")
        print(f"  Calling: instance.wait_until_running()")
        print(f"  → Polls AWS every 15s until state = 'running'")

        try:
            ec2 = self._get_ec2()
            instance = ec2.Instance(self.instance_id)
            instance.wait_until_running()
            instance.reload()
            print(f"  ✅ Running! Public IP: {instance.public_ip_address}")
            return instance.public_ip_address
        except ClientError as e:
            print(f"  ❌ AWS Error: {e.response['Error']['Message']}")

    def get_status(self):
        """
        Returns current state: pending / running / stopping / stopped / terminated
        """
        import boto3
        from botocore.exceptions import ClientError

        print(f"\n[AWSEC2VM.get_status]")
        print(f"  Calling: ec2.Instance('{self.instance_id}').state")

        try:
            ec2 = self._get_ec2()
            instance = ec2.Instance(self.instance_id)
            state = instance.state["Name"]
            print(f"  ✅ State: {state}")
            return state
        except ClientError as e:
            print(f"  ❌ AWS Error: {e.response['Error']['Message']}")

    def stop(self):
        """
        Stops the VM — compute billing stops, disk billing continues
        Can be restarted later
        """
        import boto3
        from botocore.exceptions import ClientError

        print(f"\n[AWSEC2VM.stop]")
        print(f"  Calling: instance.stop()")
        print(f"  → Compute billing stops. Disk still billed.")

        try:
            ec2 = self._get_ec2()
            ec2.Instance(self.instance_id).stop()
            print(f"  ✅ Instance stopped")
        except ClientError as e:
            print(f"  ❌ AWS Error: {e.response['Error']['Message']}")

    def terminate(self):
        """
        PERMANENTLY deletes the VM — all billing stops
        Cannot be undone!
        """
        import boto3
        from botocore.exceptions import ClientError

        print(f"\n[AWSEC2VM.terminate]")
        print(f"  Calling: instance.terminate()")
        print(f"  → VM deleted permanently. All billing stops.")

        try:
            ec2 = self._get_ec2()
            ec2.Instance(self.instance_id).terminate()
            print(f"  ✅ Instance terminated")
        except ClientError as e:
            print(f"  ❌ AWS Error: {e.response['Error']['Message']}")


# ============================================================
# PRINT ORDER:
#   1.  VirtualBoxVM.__init__            → config stored
#   2.  VirtualBoxVM.create              → VBoxManage createvm
#   3.  VirtualBoxVM.set_memory          → VBoxManage modifyvm --memory
#   4.  VirtualBoxVM.set_os_type         → VBoxManage modifyvm --ostype
#   5.  VirtualBoxVM.create_disk         → VBoxManage createmedium
#   6.  VirtualBoxVM.add_storage_controller → VBoxManage storagectl
#   7.  VirtualBoxVM.attach_disk         → VBoxManage storageattach (disk)
#   8.  VirtualBoxVM.attach_iso          → VBoxManage storageattach (iso)
#   9.  VirtualBoxVM.start               → VBoxManage startvm
#   10. VirtualBoxVM.stop                → VBoxManage controlvm poweroff
#   11. VirtualBoxVM.delete              → VBoxManage unregistervm --delete
#
#   12. AWSEC2VM.__init__                → config stored
#   13. AWSEC2VM.create                  → ec2.create_instances()
#   14. AWSEC2VM.wait_until_running      → instance.wait_until_running()
#   15. AWSEC2VM.get_status              → instance.state
#   16. AWSEC2VM.stop                    → instance.stop()
#   17. AWSEC2VM.terminate               → instance.terminate()
# ============================================================

print("\n" + "="*60)
print("OPTION A: VirtualBox (local)")
print("="*60)

vbox_vm = VirtualBoxVM("Ubuntu-Test", ram_mb=2048, disk_mb=20000)
vbox_vm.create()
vbox_vm.set_memory()
vbox_vm.set_os_type()
vbox_vm.create_disk()
vbox_vm.add_storage_controller()
vbox_vm.attach_disk()
vbox_vm.attach_iso()
vbox_vm.start()
vbox_vm.stop()
vbox_vm.delete()

print("\n" + "="*60)
print("OPTION B: AWS EC2 (cloud) — dummy keys, shows API calls")
print("="*60)

aws_vm = AWSEC2VM("my-ubuntu-server", instance_type="t2.micro")
aws_vm.create()
aws_vm.instance_id = "i-1234567890abcdef0"  # dummy id for demo
aws_vm.wait_until_running()
aws_vm.get_status()
aws_vm.stop()
aws_vm.terminate()
