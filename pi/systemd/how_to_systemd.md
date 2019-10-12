How to handle systems services:
===============================

Create a 'foo.service' file for the service and place it into /etc/systemd/system/


start the service foo:
sudo systemctl start foo.service
of just
sudo systemctl start foo


stop the service foo:
sudo systemctl stop foo


restart service foo:
sudo systemctl restart foo


get status of service foo:
sudo systemctl status foo


start service foo on startup (autostart):
sudo systemctl enable foo


do not start service foo on startup anymore:
sudo systemctl disable foo
