# I don't know how to use Docker very well, but a friend suggested that I use it... 🙃
FROM python:3
WORKDIR /src/
RUN pip install --no-cache-dir -r requirements.txt

# If you get an error saying `command not found: lolcat` or something like that on MacOS, then remove `| lolcat -f`
# ./Makefile, or install it (https://formulae.brew.sh/formula/lolcat).
CMD [ "make" ]
