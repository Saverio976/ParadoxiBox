TARGET	:=	paradoxibox-cli

all: $(TARGET)

$(TARGET):
	v -o "$(TARGET)" .

.PHONY: $(TARGET)

$(TARGET)-prod-linux:
	v -os linux -o "$(TARGET)" -skip-unused -show-timings -ldflags '-static' -prod .

$(TARGET)-prod-windows:
	v -os windows -o "$(TARGET)" -skip-unused -show-timings -prod .

fclean:
	rm -f $(TARGET)

format:
	v fmt -w src/

re: fclean all
