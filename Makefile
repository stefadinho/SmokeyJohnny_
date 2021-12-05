
HUGO_VERSION=0.72.0
LOCALIP := $(shell hostname -I | awk '{print $$1}')

run:
	@echo Required Hugo Version: $(HUGO_VERSION)
	@echo Running Hugo Version: $$(hugo version)
	rm -rf content/products
	to-templates assortiment/data.csv content/products
	hugo server

serve-subnet:
	@echo Using local ip on network to host: $(LOCALIP)
	@hugo server -DF -b http://$(LOCALIP) --bind $(LOCALIP)

install-hugo:
	# https://api.github.com/repos/gohugoio/hugo/releases
	rm -f hugo*_Linux-64bit.deb
	curl -s url -s https://api.github.com/repos/gohugoio/hugo/releases?per_page=10000 \
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
