# recruitment-system
基于Vue.js、Flask、mysql搭建的招聘系统。

### 后端部分

1. 新建back-end/.env

  ```python
  FLASK_APP=recsys.py
  
  SQLALCHEMY_DATABASE_URI='' # 数据库链接
  
  MAIL_SERVER='' # 地址
  MAIL_PORT= # 端口
  MAIL_USE_SSL= # 是否启用SSL
  MAIL_USERNAME='' # 邮件服务器用户名
  MAIL_PASSWORD='' # 邮件服务器密码
  MAIL_SENDER='' # 发送方
  
  SECRET_KEY='' # 密钥
  ```

2. 安装依赖

  ```python
  # [./back-end] pip(pip3) install -r requirements.txt
  ```

3. 数据库迁移

  ```python
  # [./back-end] flask db upgrade
  ```

4. 运行Flask

  ```python
  # [./back-end] flask run -h 0.0.0.0 -p 5000
  ```

  
