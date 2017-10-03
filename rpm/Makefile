source:
	[ -d collectd-$(VERSION).git ] && rm -rf collectd-$(VERSION).git || true # return true so we don't error out because the test condition fails
	# this is run from inside our collectd fork so we clone a clean copy to work off of
	git clone ../../ collectd-$(VERSION).git
	pushd collectd-$(VERSION).git ; \
	git archive --format tar --prefix=collectd-$(VERSION)/ HEAD | gzip > ../collectd-$(VERSION).tar.gz  ; \
	popd

vendor:
	if [ "x$(DISTRO)" == "xepel-7" ]; then \
		[ -f curl-7.52.1.tar.bz2 ] || curl -O https://curl.haxx.se/download/curl-7.52.1.tar.bz2; \
		sha1sum -c curl-7.52.1.sha1; \
	else \
		[ -f curl-7.34.0.tar.bz2 ] || curl -O https://curl.haxx.se/download/curl-7.34.0.tar.bz2; \
		sha1sum -c curl-7.34.0.sha1; \
	fi

ARCH ?= `uname -m`

build: source vendor vendor-rpms
	rm -rf result
	yum install -y vendor-*/$(ARCH)/hiredis*-0.10.1-3.*.rpm
# Stagger installs as libyajl needs to be installed before yajl-devel.
	if [[ "$(DISTRO)" == "amzn-2016.09" ]]; then \
		yum install -y vendor-*/$(ARCH)/yajl-1*.rpm; \
		yum install -y vendor-*/$(ARCH)/yajl-devel*.rpm; \
	fi
	rpmbuild --define "_source_filedigest_algorithm md5" --define "_sourcedir $$(pwd)" --define "_srcrpmdir $$(pwd)" --define "collectd_version $(VERSION)" --define "build_num $(BUILD_NUM)" -ba stackdriver-agent.spec
	cp /root/rpmbuild/RPMS/$(ARCH)/stackdriver-agent-*.rpm .
	mkdir result
	mv *.rpm result/

OUTPUT_DIR ?= result
sign:
	KEYID="7B190BD2" expect signer.exp vendor-el6/*/*rpm  vendor-el7/*/*rpm
	KEYID="7B190BD2" expect signer.exp $(OUTPUT_DIR)/*el-6*/stackdriver/result/*rpm $(OUTPUT_DIR)/*el-6*/result/*rpm
	KEYID="7B190BD2" expect signer.exp $(OUTPUT_DIR)/*amzn*/stackdriver/result/*rpm $(OUTPUT_DIR)/*amzn*/result/*rpm
	KEYID="7B190BD2" expect signer.exp $(OUTPUT_DIR)/*el-7*/stackdriver/result/*rpm $(OUTPUT_DIR)/*el-7*/result/*rpm

vendor-dirs:
	mkdir -p vendor-el6/x86_64 vendor-el6/src
# Amazon Linux 2016.09 can use el6 packages
	rm -f vendor-amzn-2016.09 && ln -s vendor-el6 vendor-amzn-2016.09
	mkdir -p vendor-el7/x86_64 vendor-el7/src

# Download yajl packages for our repo;
# These are from stock centos6.
get-yajl: vendor-dirs
	pushd vendor-el6/x86_64 && curl -O http://testrepo.stackdriver.com/vendor/yajl/x86_64/yajl-1.0.7-3.el6.x86_64.rpm
	pushd vendor-el6/x86_64 && curl -O http://testrepo.stackdriver.com/vendor/yajl/x86_64/yajl-devel-1.0.7-3.el6.x86_64.rpm
	pushd vendor-el6/src && curl -O http://testrepo.stackdriver.com/vendor/yajl/x86_64/yajl-1.0.7-3.el6.src.rpm

# These are from epel.
get-hiredis: vendor-dirs
	pushd vendor-el6/x86_64 && curl -O http://testrepo.stackdriver.com/vendor/hiredis/x86_64/hiredis-0.10.1-3.el6.x86_64.rpm
	pushd vendor-el6/x86_64 && curl -O http://testrepo.stackdriver.com/vendor/hiredis/x86_64/hiredis-devel-0.10.1-3.el6.x86_64.rpm
	pushd vendor-el6/src && curl -O http://testrepo.stackdriver.com/vendor/hiredis/x86_64/hiredis-0.10.1-3.el6.src.rpm

# These are from epel.
get-psutil: vendor-dirs
	pushd vendor-el6/x86_64 && curl -O http://testrepo.stackdriver.com/vendor/psutil/python-psutil-0.6.1-1.el6.x86_64.rpm
	pushd vendor-el6/src && curl -O http://testrepo.stackdriver.com/vendor/psutil/python-psutil-0.6.1-1.el6.src.rpm
	pushd vendor-el7/x86_64 && curl -O http://testrepo.stackdriver.com/vendor/psutil/python-psutil-0.6.1-3.el7.x86_64.rpm
	pushd vendor-el7/src && curl -O http://testrepo.stackdriver.com/vendor/psutil/python-psutil-0.6.1-3.el7.src.rpm

# These are from epel.
get-netifaces: vendor-dirs
	pushd vendor-el6/x86_64 && curl -O http://testrepo.stackdriver.com/vendor/netifaces/python-netifaces-0.5-1.el6.x86_64.rpm
	pushd vendor-el6/src && curl -O http://testrepo.stackdriver.com/vendor/netifaces/python-netifaces-0.5-1.el6.src.rpm
	pushd vendor-el7/x86_64 && curl -O http://testrepo.stackdriver.com/vendor/netifaces/python-netifaces-0.5-4.el7.x86_64.rpm
	pushd vendor-el7/src && curl -O http://testrepo.stackdriver.com/vendor/netifaces/python-netifaces-0.5-4.el7.src.rpm

# Download packages which aren't necessarily in base repos.
vendor-rpms: get-yajl get-hiredis get-psutil get-netifaces

clean:
	rm -rf result *rpm collectd-5.5.2 *.tar.bz2 collectd-5.5.2.git *.tar.gz
