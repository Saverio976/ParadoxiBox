all:
	mkdir -p ./api/bin
	make -C ./musicplayer
	cp ./musicplayer/musicplayer ./api/bin
	make -C ./musicplayer-cli
	cp ./musicplayer-cli/musicplayer-cli ./api/bin

all-prod-linux:
	mkdir -p ./api/bin
	make -C ./musicplayer musicplayer-prod-linux
	cp ./musicplayer/musicplayer ./api/bin
	make -C ./musicplayer-cli musicplayer-cli-prod-linux
	cp ./musicplayer-cli/musicplayer-cli ./api/bin

all-prod-windows:
	mkdir -p ./api/bin
	make -C ./musicplayer musicplayer-prod-windows
	cp ./musicplayer/musicplayer ./api/bin
	make -C ./musicplayer-cli musicplayer-cli-prod-windows
	cp ./musicplayer-cli/musicplayer-cli ./api/bin

all-prod-macos:
	mkdir -p ./api/bin
	make -C ./musicplayer musicplayer-prod-macos
	cp ./musicplayer/musicplayer ./api/bin
	make -C ./musicplayer-cli musicplayer-cli-prod-macos
	cp ./musicplayer-cli/musicplayer-cli ./api/bin

fclean:
	rm -rf ./api/bin
	make -C ./musicplayer fclean
	make -C ./musicplayer-cli fclean

re: fclean all
