
run:
	export HUGO_VERSION=0.19
	hugo server -FD

install-hugo:
	# https://api.github.com/repos/gohugoio/hugo/releases
	rm hugo*_Linux-64bit.deb
	curl -s https://api.github.com/repos/gohugoio/hugo/releases/assets/15877575 \
  | grep  browser_download_url \
  | grep Linux-64bit.deb \
  | grep extended \
  | cut -d '"' -f 4 \
  | wget -i -
	sudo dpkg -i hugo*_Linux-64bit.deb
	hugo version
	rm hugo*_Linux-64bit.deb
