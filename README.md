# 使用指南
一人签到，全寝不愁  
```bash
pip install -r request.txt # 下载使用的第三方的库    
vi config.json  # 增加签到用户  
nohup python3 socketSever.py &  # 后台挂起运行  
```
# 关于config.json
```python
usr:"zhangsan"  # 可爱的昵称  
usrdata:"zhangsan_token"  # token值  
```
你可以在[上课啦](https://skl.hduhelp.com/?type=2&v=3)登陆后根据Url获得账户的token
