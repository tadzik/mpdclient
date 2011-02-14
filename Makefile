all:
	plasmapkg -r ../mpdclient.zip
	zip -r ../mpdclient.zip .
	plasmapkg -i ../mpdclient.zip
