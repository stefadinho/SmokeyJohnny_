
HUGO_VERSION=0.72.0

run:
	export HUGO_VERSION=$(HUGO_VERSION)
	hugo server -FD

install-hugo:
	# https://api.github.com/repos/gohugoio/hugo/releases
	rm -f hugo*_Linux-64bit.deb
	curl -s url -s https://api.github.com/repos/gohugoio/hugo/releases \
	| jq '.[] | select(.name=="v$(HUGO_VERSION)") | .assets' \
	| jq '.[] | select(.name=="hugo_extended_$(HUGO_VERSION)_Linux-64bit.deb")' \
	| jq '.url' \
	| xargs curl -s \
	| grep  browser_download_url \
	| grep Linux-64bit.deb \
	| grep extended \
	| cut -d '"' -f 4 \
	| wget -i -
	sudo dpkg -i hugo*_Linux-64bit.deb
	rm hugo*_Linux-64bit.deb
	hugo version
