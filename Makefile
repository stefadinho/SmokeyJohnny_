HUGO_VERSION=0.72.0
HUGO_PLATFORM=Linux-64bit.deb
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
	# https://api.github.com/repos/gohugoio/hugo/releases/
	rm -f hugo*_$(HUGO_PLATFORM)
	curl -s url -s https://api.github.com/repos/gohugoio/hugo/releases/tags/v$(HUGO_VERSION) \
	| jq '.assets' \
	| jq '.[] | select(.name=="hugo_extended_$(HUGO_VERSION)_$(HUGO_PLATFORM)")' \
	| jq '.url' \
	| xargs curl -s \
	| grep  browser_download_url \
	| grep $(HUGO_PLATFORM) \
	| grep extended \
	| cut -d '"' -f 4 \
	| wget -i -
	sudo dpkg -i hugo*_$(HUGO_PLATFORM)
	rm hugo*_$(HUGO_PLATFORM)
	hugo version
