from settings import config

print("VK settings:")
print(f"VK object: {config.vk}")
if config.vk:
    print(f"Access token: {config.vk.access_token}")
    print(f"Group domains: {config.vk.group_domains}")
    print(f"Version: {config.vk.version}")
    print(f"Check interval: {config.vk.check_interval}")
else:
    print("VK settings not loaded")
