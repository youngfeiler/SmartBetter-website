import os
print(os.environ.get("API_KEY"))

#[ec2-user@ip-172-31-37-33 SmartBetter-website]$ echo $API_KEY
# sk_live_51Nm0vBHM5Jv8uc5M6uWD1Ax9oHXnfo9IhhfqVSa05tG9Mvj8H92jBW
# [ec2-user@ip-172-31-37-33 SmartBetter-website]$ git pull
# remote: Enumerating objects: 4, done.
# remote: Counting objects: 100% (4/4), done.
# remote: Compressing objects: 100% (1/1), done.
# remote: Total 3 (delta 1), reused 3 (delta 1), pack-reused 0
# Unpacking objects: 100% (3/3), 290 bytes | 290.00 KiB/s, done.
# From https://github.com/youngfeiler/SmartBetter-website
#    7b4e02f..b8da1e9  master     -> origin/master
# Merge made by the 'ort' strategy.
#  test.py | 2 ++
#  1 file changed, 2 insertions(+)
#  create mode 100644 test.py
# [ec2-user@ip-172-31-37-33 SmartBetter-website]$ python test.py
# -bash: python: command not found
# [ec2-user@ip-172-31-37-33 SmartBetter-website]$ python3 test.py
# sk_live_51Nm0vBHM5Jv8uc5M6uWD1Ax9oHXnfo9IhhfqVSa05tG9Mvj8H92jBW
# [ec2-user@ip-172-31-37-33 SmartBetter-website]$ 
