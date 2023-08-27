TARGET	:=	paradoxibox-cli

all: $(TARGET)

$(TARGET):
	v -o "$(TARGET)" .

$(TARGET)-prod:
	v -o "$(TARGET)" -prod .

fclean:
	rm -f $(TARGET)

format:
	v fmt -w src/

re: fclean all
