import os
import time
import subprocess
import requests

BLUE_URL = "http://blue"
GREEN_URL = "http://green"
NGINX_CONF = "/etc/nginx/nginx.conf"
NGINX_CONTAINER = "nginx_reverse_proxy"

def is_healthy(url):
    try:
        response = requests.get(url, timeout=3)
        return response.status_code == 200
    except:
        return False

def switch_to(active_color):
    print(f"Switching traffic to {active_color.upper()}...")
    new_conf = f"""
events {{}}

http {{
    upstream app_backend {{
        server {active_color}:80;
    }}

    server {{
        listen 80;
        location / {{
            proxy_pass http://app_backend;
        }}
    }}
}}
"""
    # Write to a local temp file
    with open("nginx.conf", "w") as f:
        f.write(new_conf)

    # Copy new config into nginx container
    subprocess.run([
        "docker", "cp", "nginx.conf", f"{NGINX_CONTAINER}:/etc/nginx/nginx.conf"
    ])

    # Reload nginx inside the container
    subprocess.run([
        "docker", "exec", NGINX_CONTAINER, "nginx", "-s", "reload"
    ])
    print("✅ Switched and reloaded NGINX configuration.")

def main():
    current = "blue"
    while True:
        blue_healthy = is_healthy(BLUE_URL)
        green_healthy = is_healthy(GREEN_URL)

        if green_healthy and not blue_healthy:
            if current != "green":
                switch_to("green")
                current = "green"
        elif blue_healthy and not green_healthy:
            if current != "blue":
                switch_to("blue")
                current = "blue"
        else:
            print("Both healthy or both down — no switch.")

        time.sleep(10)

if __name__ == "__main__":
    main()
