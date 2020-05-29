
dev:
	export HUGO_VERSION=0.19
	hugo server -FD

prod:
	export HUGO_VERSION=0.19
	hugo server -FD --config config.toml,config/prod.toml
