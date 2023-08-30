TARGET	:=	api

all: $(TARGET)

$(TARGET):
	v -o "$(TARGET)" .

.PHONY: $(TARGET)

$(TARGET)-prod-linux:
	v -os linux -o "$(TARGET)" -skip-unused -show-timings -ldflags '-static -lm' -prod .

$(TARGET)-prod-macos:
	v -os macos -o "$(TARGET)" -skip-unused -show-timings -prod .

$(TARGET)-prod-windows:
	v -os windows -o "$(TARGET)" -skip-unused -show-timings -ldflags '-static -lm' -prod .

fclean:
	rm -f $(TARGET)

format:
	v fmt -w src/

re: fclean all
