git clone https://github.com/certbot/certbot

cd certbot

./certbot-auto certonly --webroot --agree-tos -v -t --email 邮箱地址 -w 网站根目录 -d 网站域名

./certbot-auto certonly --webroot --agree-tos -v -t --email 

keeliizhou@gmail.com -w /path/to/your/web/root -d note.crazy4code.com
