# Cloudflare DDNS for Docker

A simple docker app that runs on a set interval to check and update the specified DNS record in a YAML config file.

* [Running with docker](#running-with-docker)
	* [AMD64](#amd64)
	* [ARM64v8](#arm64v8)
* [Docker Tags](#docker-tags)
	* [Platform Tags](#platform-tags)
	* [Image Tags](#image-tags)
* [Configuration](#configuration)
	* [Configurable Options](#configurable-options)
	* [Configuring Domains](#configuring-domains)
	* [Configuring Records](#configuring-records)
* [Building from source](#building-from-source)
* [License](#license)


## Running with docker

Use the docker run command below to pull the pre-built container from the repository and start updating your DNS records dynamically!

### AMD64
```
docker run -d \
	--name cloudflare_ddns
	--restart=on-failure \
	-v "$PWD:/code/config" \
	docker pull ghcr.io/shrunbr/cloudflare-ddns:stable
```

### ARM64v8
```
docker run -d \
	--name cloudflare_ddns
	--restart=on-failure \
	-v "$PWD:/code/config" \
	docker pull ghcr.io/shrunbr/cloudflare-ddns:stable-arm64v8
```

## Docker Tags

#### **Platform Tags**

* `-arm64v8` - Raspberry PI 4 Supported

#### **Image Tags**

* `stable` - Current working, stable image based upon release
* `stable-rc` - Latest master branch commit, most of these images wil come from pull request merges which have been confirmed working. There will be times where the `stable` and `stable-rc` image do match. May still contain minimal issues, use at your own risk.
* `unstable` - DANGER: These images come from the dev branch, you may or may not break things in your cloudflare environment or system if you run this image. Use at your own risk!

## Configuration

You'll need to first setup a `config.yml` file within a directory to mount within the container. You can find an example file located at [config/example.yml](config/example.yml)

### Configurable Options

All variables are currently **REQUIRED** for the container to run.

|    Variable   	| Description                                                                      	|
|:-------------:	|----------------------------------------------------------------------------------	|
|     token     	| Cloudflare Global API Key                                                        	|
|     email     	| Cloudflare account email address                                                 	|
|    use_ipv6   	| AAA records? (True/False)                                                        	|
|  use_cf_proxy 	| Proxy traffic though Cloudflare? (True/False)                                    	|
| logging_level 	| Sets container logging level (DEBUG/INFO; default is INFO)                       	|
|     timer     	| How often (in seconds) you want to check your IP and update the specified record 	|
|    domains:   	| List of domains to update records under (currently only supports 1 domain)       	|
|    records    	| List of records under the domains to update (currently only supports 1 record)   	|
<br>

### Configuring domains

The current stable branch only supports 1 domain per container. However, the YAML config has been positioned to be able to support more than 1 in the future. For both current and future state you'll need to configure the domains in a list format.

```
domains:
    - "example.com"
```
Hopefully in the near-ish future, the time can be allocated to start development on multi-domain support.

### Configuring records

Just like the domains, today the current stable branch only supports 1 domain per container. For both current and future state you'll need to configure the records in a list format.

```
records:
    - name: "RECORD NAME"
```
Also, hopefully in the near-ish future, the time can be allocated to start development on multi-record support.

## Building from source

Feel free to clone/fork the repo and build the container from source. All you'll need to do is build and run the image.

```
docker build -t cloudflare-ddns-python .
```
Running the docker command above will build the image and tag it as `cloudflare-ddns-python`. Once you have the image built you can run it using the same command above in the [running with docker](#Running-with-docker) section.

## License
[LICENSE](LICENSE)