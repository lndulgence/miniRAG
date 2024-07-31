import subprocess
import time    

def check_dns_resolution(pod_name, count=5):
    while True:
        if count == 0:
            raise Exception(f"DNS resolution for {pod_name} failed after multiple retries")
        try:
            # Run nslookup command to check DNS resolution
            subprocess.run(["nslookup", f"{pod_name}"], check=True)
            print(f"DNS resolution for {pod_name} successful")
            break  # Break the loop if DNS resolution is successful
        except subprocess.CalledProcessError:
            print(f"DNS resolution for {pod_name} failed. Retrying...")
            time.sleep(5)  # Wait for 5 seconds before retrying
            count -= 1