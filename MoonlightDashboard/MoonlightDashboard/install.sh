sudo add-apt-repository ppa:dotnet/backports
sudo apt-get update && sudo apt-get install -y dotnet-sdk-8.0

#change the path in the service file if you dont have this under /root/...
cp moonlightdashboard.service /etc/systemd/system/moonlightdashboard.service
systemctl daemon-reload
systemctl enable moonlightdashboard.service
systemctl start moonlightdashboard.service