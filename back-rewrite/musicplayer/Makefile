TARGET	:=	musicplayer

LIB_MINIAUDIO	:=	miniaudio/v.mod

all: $(TARGET)

$(TARGET): $(LIB_MINIAUDIO)
	v -o "$(TARGET)" .

.PHONY: $(TARGET)

$(TARGET)-prod-linux: $(LIB_MINIAUDIO)
	v -os linux -o "$(TARGET)" -skip-unused -show-timings -ldflags '-static' -prod .

$(TARGET)-prod-macos: $(LIB_MINIAUDIO)
	v -os macos -o "$(TARGET)" -skip-unused -show-timings -prod .

$(TARGET)-prod-windows: $(LIB_MINIAUDIO)
	v -os windows -o "$(TARGET)" -skip-unused -show-timings -ldflags '-static' -prod .

fclean:
	rm -f $(TARGET)

format:
	v fmt -w src/

re: fclean all

$(LIB_MINIAUDIO):
	git submodule update --init miniaudio
