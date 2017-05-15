# Simple makefile to handle setting up and running
# the builds of the Stackdriver agent on debian-y
# distributions,
#
# This assumes it is being built from inside the Stackdriver collectd git fork.
SHELL=/bin/bash

source:
	# Return true so we don't error out because the test condition fails.
	[ -d collectd-$(VERSION).git ] && rm -rf collectd-$(VERSION).git || true
	git clone ../../ collectd-$(VERSION).git
	pushd collectd-$(VERSION).git ; \
	git archive --format tar --prefix=collectd-$(VERSION)/ HEAD | gzip > ../stackdriver-agent_$(VERSION).orig.tar.gz  ; \
	popd

srcpkg: source debian/rules
	tar -xf stackdriver-agent_$(VERSION).orig.tar.gz
	pushd collectd-$(VERSION) ; \
	cp -r ../debian . ; \
	DEBEMAIL="engineering@stackdriver.com" DEBFULLNAME="Stackdriver Engineering" dch --package stackdriver-agent --distribution $(DISTRO) -v $(VERSION)-$(BUILD_NUM).$(DISTRO) "Automated build" ; \
	cat debian/changelog ; \
	pushd debian ; \
	if [ -f controls/control.$(DISTRO) ]; then cp controls/control.$(DISTRO) control ; else cp controls/control.base control ; fi ; \
	popd ; \
	popd ; \

build: srcpkg
	pushd collectd-$(VERSION) ; \
	debuild -us -uc; \
	popd ; \
	rm -rf collectd-$(VERSION)

DISTRO?=`lsb_release -a 2>/dev/null | grep Codename |awk {'print $2;'}`
ARCH?=`uname -i`

OUTPUT_DIR ?= result

vendor-debs:

repo:
	@rm -rf apt
	@mkdir -p apt/conf
	@cp distributions apt/conf/distributions
	@for distro in precise trusty xenial wheezy jessie ; do \
		find $(OUTPUT_DIR)/*$$distro* -name "*.deb" -exec reprepro --export=never -Vb apt includedeb $$distro {} \; ;\
		find $(OUTPUT_DIR)/*$$distro* -name "*.dsc" -exec reprepro --export=never -Vb apt includedsc $$distro {} \; ; \
	done

# The default permissions for the repo is set to public-read.
syncgrepo: repo
	export BOTO_CONFIG=/etc/boto.cfg
	gsutil -m rsync -c -r apt/ gs://gtestrepo.stackdriver.com/apt/

sign:
	# Need to do this after adding packages so that the repo is properly signed.
	expect signer.exp

clean:
	rm -rf *.dsc *.deb *.tar.gz *.tar.bz2 collectd-$(VERSION) result apt
