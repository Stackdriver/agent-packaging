include VERSION

source:
	[ -d collectd-$(VERSION).git ] && rm -rf collectd-$(VERSION).git || true # return true so we don't error out because the test condition fails
	# this is run from inside our collectd fork so we clone a clean copy to work off of
	git clone ../../ collectd-$(VERSION).git
	pushd collectd-$(VERSION).git ; \
	git archive --format tar --prefix=collectd-$(VERSION)/ HEAD | gzip > ../stackdriver-agent-$(PKG_VERSION).orig.tar.gz  ; \
	popd

ifneq ($(filter epel-6 amzn-%,$(DISTRO)),)
CURL_VERSION=7.34.0
else
CURL_VERSION=7.52.1
endif

vendor:
	[ -f curl-$(CURL_VERSION).tar.bz2 ] || curl -O https://curl.haxx.se/download/curl-$(CURL_VERSION).tar.bz2
	sha1sum -c curl-$(CURL_VERSION).sha1

ARCH ?= `uname -m`

build: source vendor vendor-rpms
	rm -rf result
	if [[ $(DISTRO) == "epel-6" || $(DISTRO) == amzn-* ]]; then \
	  yum install -y vendor-$(DISTRO)/$(ARCH)/hiredis*-0.10.1-3.*.rpm; \
	fi
	if [[ "$(DISTRO)" == "amzn-2016.09" ]]; then \
	  # Stagger installs as libyajl needs to be installed before yajl-devel. \
	  yum install -y vendor-$(DISTRO)/$(ARCH)/yajl-1*.rpm; \
	  yum install -y vendor-$(DISTRO)/$(ARCH)/yajl-devel*.rpm; \
	fi
	rpmbuild --define "_source_filedigest_algorithm md5" --define "_sourcedir $$(pwd)" --define "_srcrpmdir $$(pwd)" --define "collectd_version $(VERSION)" --define "package_version $(PKG_VERSION)" --define "build_num $(PKG_BUILD)" -ba stackdriver-agent.spec
	mkdir result
	cp /root/rpmbuild/RPMS/$(ARCH)/stackdriver-agent-*.rpm result/

OUTPUT_DIR ?= result
vendor-dirs:
	mkdir -p vendor-epel-6/x86_64 vendor-epel-6/src
	# Amazon Linux 2016.09 can use el6 packages.
	rm -f vendor-amzn-2016.09 && ln -s vendor-epel-6 vendor-amzn-2016.09
	mkdir -p vendor-epel-7/x86_64 vendor-epel-7/src

# Download yajl packages for our repo;
# TODO(dhrupadb): See if all these downloads are necessary now that we are not building our own repo.
# These are from stock centos6.
get-yajl: vendor-dirs
	pushd vendor-epel-6/x86_64 && curl -O http://testrepo.stackdriver.com/vendor/yajl/x86_64/yajl-1.0.7-3.el6.x86_64.rpm
	pushd vendor-epel-6/x86_64 && curl -O http://testrepo.stackdriver.com/vendor/yajl/x86_64/yajl-devel-1.0.7-3.el6.x86_64.rpm
	pushd vendor-epel-6/src && curl -O http://testrepo.stackdriver.com/vendor/yajl/x86_64/yajl-1.0.7-3.el6.src.rpm

# These are from epel.
get-hiredis: vendor-dirs
	pushd vendor-epel-6/x86_64 && curl -O http://testrepo.stackdriver.com/vendor/hiredis/x86_64/hiredis-0.10.1-3.el6.x86_64.rpm
	pushd vendor-epel-6/x86_64 && curl -O http://testrepo.stackdriver.com/vendor/hiredis/x86_64/hiredis-devel-0.10.1-3.el6.x86_64.rpm
	pushd vendor-epel-6/src && curl -O http://testrepo.stackdriver.com/vendor/hiredis/x86_64/hiredis-0.10.1-3.el6.src.rpm

# These are from epel.
get-psutil: vendor-dirs
	pushd vendor-epel-6/x86_64 && curl -O http://testrepo.stackdriver.com/vendor/psutil/python-psutil-0.6.1-1.el6.x86_64.rpm
	pushd vendor-epel-6/src && curl -O http://testrepo.stackdriver.com/vendor/psutil/python-psutil-0.6.1-1.el6.src.rpm
	pushd vendor-epel-7/x86_64 && curl -O http://testrepo.stackdriver.com/vendor/psutil/python-psutil-0.6.1-3.el7.x86_64.rpm
	pushd vendor-epel-7/src && curl -O http://testrepo.stackdriver.com/vendor/psutil/python-psutil-0.6.1-3.el7.src.rpm

# These are from epel.
get-netifaces: vendor-dirs
	pushd vendor-epel-6/x86_64 && curl -O http://testrepo.stackdriver.com/vendor/netifaces/python-netifaces-0.5-1.el6.x86_64.rpm
	pushd vendor-epel-6/src && curl -O http://testrepo.stackdriver.com/vendor/netifaces/python-netifaces-0.5-1.el6.src.rpm
	pushd vendor-epel-7/x86_64 && curl -O http://testrepo.stackdriver.com/vendor/netifaces/python-netifaces-0.5-4.el7.x86_64.rpm
	pushd vendor-epel-7/src && curl -O http://testrepo.stackdriver.com/vendor/netifaces/python-netifaces-0.5-4.el7.src.rpm

# Download packages which aren't necessarily in base repos.
vendor-rpms: get-yajl get-hiredis get-psutil get-netifaces

clean:
	rm -rf result *rpm collectd-$(VERSION) *.tar.bz2 collectd-$(VERSION).git *.tar.gz
