###
AWS部署方式
1. 安装flask
```pip install flask```
2. 安装gunicorn
```pip install gunicorn```
3. 安装nginx
```sudo apt get instal nginx```
4. 配置nginx
5. 配置aws security
6. 启动 程序
```gunicorn -w 1 -b 127.0.0.1:8000 pwdgen:app```
7. nginx配置
```
server {
        listen 80;
        server_name _; # 外部地址
 
        location / {
                proxy_pass http://127.0.0.1:8000;
                proxy_redirect     off;
                proxy_set_header   Host                 $http_host;
                proxy_set_header   X-Real-IP            $remote_addr;
                proxy_set_header   X-Forwarded-For      $proxy_add_x_forwarded_for;
                proxy_set_header   X-Forwarded-Proto    $scheme;
}```