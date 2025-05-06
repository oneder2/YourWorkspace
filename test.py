import os


env_vars = os.environ

# 输出所有环境变量
print(env_vars["DEV_DATABASE_URL"])
# for key, value in env_vars.items():
#     print(f"{key}: {value}")