# simplest makefile possible with way too much hardcoded
# this should hijack more stuff from the fedora package
# git stuff so that we can get the source files, srpm filename, etc dynamically

source:
	[ -d collectd-$(VERSION).git ] && rm -rf collectd-$(VERSION).git || true # return true so we don't error out because the test condition fails
	# this is run from inside our collectd fork so we clone a clean copy to work off of
	git clone ../../ collectd-$(VERSION).git
	pushd collectd-$(VERSION).git ; \
	./clean.sh && ./build.sh && git commit -a -m "Clean and build" ; \
	git archive --format tar --prefix=collectd-$(VERSION)/ HEAD | gzip > ../collectd-$(VERSION).tar.gz  ; \
	popd

vendor:
	[ -f curl-7.34.0.tar.bz2 ] || curl -O https://curl.haxx.se/download/curl-7.34.0.tar.bz2
	sha1sum -c curl.sha1

srpm: source vendor
	rpmbuild --define "_source_filedigest_algorithm md5" --define "_sourcedir $$(pwd)" --define "_srcrpmdir $$(pwd)" --define "collectd_version $(VERSION)" --define "build_num $(BUILD_NUM)" -bs stackdriver-agent.spec

MOCK_ROOT="$(DISTRO)-$(ARCH)"
ifeq ($(MOCK_ROOT), "-")
	MOCK_ROOT="default"
endif
ARCH ?= `uname -m`

build: srpm vendor-rpms
	rm -rf result
	mock --arch $(ARCH) -r $(MOCK_ROOT) --install flex bison ;
	if [[ $(DISTRO) != "epel-7" ]]; then \
	    mock --arch $(ARCH) -r $(MOCK_ROOT) --install vendor-*/$(ARCH)/hiredis*-0.10.1-3.*.rpm ; \
	fi ;
	if [[ $(DISTRO) == "amzn-2014.03" ]]; then \
	    mock --arch $(ARCH) -r $(MOCK_ROOT) --install vendor-*/$(ARCH)/yajl*-1.0.7-3.el6.$(ARCH).rpm ; \
	fi ;
	mock --arch $(ARCH) -r $(MOCK_ROOT) --no-clean --define "collectd_version $(VERSION)" --define "build_num $(BUILD_NUM)" --resultdir result $$(pwd)/*.src.rpm

OUTPUT_DIR ?= result
sign:
	KEYID="7B190BD2" expect signer.exp vendor-el6/*/*rpm  vendor-el7/*/*rpm
	KEYID="7B190BD2" expect signer.exp $(OUTPUT_DIR)/*el-6*/stackdriver/result/*rpm $(OUTPUT_DIR)/*el-6*/result/*rpm
	KEYID="7B190BD2" expect signer.exp $(OUTPUT_DIR)/*amzn*/stackdriver/result/*rpm $(OUTPUT_DIR)/*amzn*/result/*rpm
	KEYID="7B190BD2" expect signer.exp $(OUTPUT_DIR)/*el-7*/stackdriver/result/*rpm $(OUTPUT_DIR)/*el-7*/result/*rpm

vendor-dirs:
	mkdir -p vendor-el6/i386 vendor-el6/x86_64 vendor-el6/src
# amazon linux 2014.03 can use el6 packages
	rm -f vendor-amzn-2014.03 && ln -s vendor-el6 vendor-amzn-2014.03
	mkdir -p vendor-el7/x86_64 vendor-el7/src

# download yajl packages for our repo
# these are from stock centos6
get-yajl: vendor-dirs
	pushd vendor-el6/i386 && curl -O http://testrepo.stackdriver.com/vendor/yajl/i386/yajl-1.0.7-3.el6.i686.rpm
	pushd vendor-el6/i386 && curl -O http://testrepo.stackdriver.com/vendor/yajl/i386/yajl-devel-1.0.7-3.el6.i686.rpm
	pushd vendor-el6/x86_64 && curl -O http://testrepo.stackdriver.com/vendor/yajl/x86_64/yajl-1.0.7-3.el6.x86_64.rpm
	pushd vendor-el6/x86_64 && curl -O http://testrepo.stackdriver.com/vendor/yajl/x86_64/yajl-devel-1.0.7-3.el6.x86_64.rpm
	pushd vendor-el6/src && curl -O http://testrepo.stackdriver.com/vendor/yajl/x86_64/yajl-1.0.7-3.el6.src.rpm

# these are from epel
get-hiredis: vendor-dirs
	pushd vendor-el6/i386 && curl -O http://testrepo.stackdriver.com/vendor/hiredis/i386/hiredis-0.10.1-3.el6.i686.rpm
	pushd vendor-el6/i386 && curl -O http://testrepo.stackdriver.com/vendor/hiredis/i386/hiredis-devel-0.10.1-3.el6.i686.rpm
	pushd vendor-el6/x86_64 && curl -O http://testrepo.stackdriver.com/vendor/hiredis/x86_64/hiredis-0.10.1-3.el6.x86_64.rpm
	pushd vendor-el6/x86_64 && curl -O http://testrepo.stackdriver.com/vendor/hiredis/x86_64/hiredis-devel-0.10.1-3.el6.x86_64.rpm
	pushd vendor-el6/src && curl -O http://testrepo.stackdriver.com/vendor/hiredis/x86_64/hiredis-0.10.1-3.el6.src.rpm

# these are from epel
get-psutil: vendor-dirs
	pushd vendor-el6/i386 && curl -O http://testrepo.stackdriver.com/vendor/psutil/python-psutil-0.6.1-1.el6.i686.rpm
	pushd vendor-el6/x86_64 && curl -O http://testrepo.stackdriver.com/vendor/psutil/python-psutil-0.6.1-1.el6.x86_64.rpm
	pushd vendor-el6/src && curl -O http://testrepo.stackdriver.com/vendor/psutil/python-psutil-0.6.1-1.el6.src.rpm
	pushd vendor-el7/x86_64 && curl -O http://testrepo.stackdriver.com/vendor/psutil/python-psutil-0.6.1-3.el7.x86_64.rpm
	pushd vendor-el7/src && curl -O http://testrepo.stackdriver.com/vendor/psutil/python-psutil-0.6.1-3.el7.src.rpm

# these are from epel
get-netifaces: vendor-dirs
	pushd vendor-el6/i386 && curl -O http://testrepo.stackdriver.com/vendor/netifaces/python-netifaces-0.5-1.el6.i686.rpm
	pushd vendor-el6/x86_64 && curl -O http://testrepo.stackdriver.com/vendor/netifaces/python-netifaces-0.5-1.el6.x86_64.rpm
	pushd vendor-el6/src && curl -O http://testrepo.stackdriver.com/vendor/netifaces/python-netifaces-0.5-1.el6.src.rpm
	pushd vendor-el7/x86_64 && curl -O http://testrepo.stackdriver.com/vendor/netifaces/python-netifaces-0.5-4.el7.x86_64.rpm
	pushd vendor-el7/src && curl -O http://testrepo.stackdriver.com/vendor/netifaces/python-netifaces-0.5-4.el7.src.rpm

# download packages which aren't necessarily in base repos
vendor-rpms: get-yajl get-hiredis get-psutil get-netifaces

repo:
	@mkdir repo
	@for distro in el6 el7 amzn-2014.03 ; do \
		for arch in i386 x86_64 src ; do \
			if [[ $$distro == "amzn-2014.03" && $$arch == "i386" ]]; then continue ; fi ; \
			if [[ $$distro == "el7" && $$arch == "i386" ]]; then continue ; fi ; \
			if [ $$distro == "amzn-2014.03" ]; then disttag="amzn1" ; else disttag=$$distro ; fi ; \
			mkdir -p repo/$$distro/$$arch ; \
			find $(OUTPUT_DIR) -name "*$$disttag*$$arch*.rpm" -exec cp -vl {} repo/$$distro/$$arch \; ; \
			find $(OUTPUT_DIR) -name "*$$disttag*noarch*.rpm" -exec cp -vl {} repo/$$distro/$$arch \; ; \
			find vendor-$$distro/$$arch -name '*rpm' -exec cp -vl {} repo/$$distro/$$arch \; ; \
			createrepo -d repo/$$distro/$$arch ; \
		done ; \
                if [ $$distro == "el6" ]; then ln -s $$distro repo/$$distro"Server" ; fi ; \
	done

# would love to use the jenkins s3 artifact uploader for this but it doesn't preserve
# the directory structure
# consider --delete-removed
# also, figure out how to make this put the repo config + gpg key + readme in place
# and don't use an s3 config file in /tmp
syncrepo: repo
	s3cmd -c /etc/s3cmd.cfg sync --follow-symlinks repo/ s3://testrepo.stackdriver.com/repo/

syncalpharepo: repo
	s3cmd -c /etc/s3cmd.cfg sync --follow-symlinks repo/ s3://alpharepo.stackdriver.com/repo/

syncgrepo: repo
	export BOTO_CONFIG=/etc/boto.cfg
	gsutil -m rsync -c -r repo/ gs://gtestrepo.stackdriver.com/repo/

clean:
	rm -rf result *rpm collectd-5.3.0 *.tar.bz2 collectd-5.3.0.git *.tar.gz
