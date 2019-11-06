include VERSION

source:
	[ -d collectd-pristine.git ] && rm -rf collectd-pristine.git || true # return true so we don't error out because the test condition fails
	# this is run from inside our collectd fork so we clone a clean copy to work off of
	git clone ../../ collectd-pristine.git
	pushd collectd-pristine.git ; \
	git archive --format tar --prefix=collectd-pristine/ HEAD | gzip > ../stackdriver-agent-$(PKG_VERSION).orig.tar.gz  ; \
	popd

# $(filter) will return all matching entries from the first list, or empty if none match.
ifneq ($(filter epel-6 amzn-%,$(DISTRO)),)  # If DISTRO is epel-6 or amzn-*.
CURL_VERSION=7.34.0
else
ifeq ($(filter sles%,$(DISTRO)),)  # If DISTRO is not sles*.
CURL_VERSION=7.52.1
endif
endif

ifeq ($(filter sles%,$(DISTRO)),)  # If DISTRO is not sles*.
vendor:
	[ -f curl-$(CURL_VERSION).tar.bz2 ] || curl -O https://curl.haxx.se/download/curl-$(CURL_VERSION).tar.bz2
	sha1sum -c curl-$(CURL_VERSION).sha1
else
vendor:;true
endif

TOPDIR=/root/rpmbuild

build: source vendor vendor-rpms
	[ -n "$(DIR_TO_RM)" ] && rm -rf "$(DIR_TO_RM)" || true # return true so we don't error out because the test condition fails
	if [[ $(DISTRO) == "epel-6" || $(DISTRO) == amzn-* ]]; then \
	  yum install -y vendor-$(DISTRO)/$(ARCH)/hiredis*-0.10.1-3.*.rpm; \
	fi
	if [[ "$(DISTRO)" == "amzn-2016.09" ]]; then \
	  # Stagger installs as libyajl needs to be installed before yajl-devel. \
	  yum install -y vendor-$(DISTRO)/$(ARCH)/yajl-1*.rpm; \
	  yum install -y vendor-$(DISTRO)/$(ARCH)/yajl-devel*.rpm; \
	fi
	rpmbuild --define "_topdir $(TOPDIR)" --define "_source_filedigest_algorithm md5" --define "_sourcedir $$(pwd)" --define "_srcrpmdir $$(pwd)" --define "package_version $(PKG_VERSION)" --define "build_num $(PKG_BUILD)" -ba stackdriver-agent.spec
	mkdir -p $(OUTPUT_DIR)
	cp $(TOPDIR)/RPMS/$(ARCH)/stackdriver-agent-*.rpm $(OUTPUT_DIR)/

ARCH ?= `uname -m`

OUTPUT_DIR ?= result

ifneq ($(findstring $(abspath $(OUTPUT_DIR)),$(CURDIR)),)
DIR_TO_RM :=  # Avoid trying to rm any prefix of the current directory.
else
DIR_TO_RM := $(OUTPUT_DIR)
endif

ifeq ($(filter sles%,$(DISTRO)),)  # If DISTRO is not sles*.
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
else
vendor-rpms:; true
endif

clean:
	rm -rf $(DIR_TO_RM) *rpm collectd-pristine *.tar.bz2 collectd-pristine.git *.tar.gz
