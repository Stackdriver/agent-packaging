# simple makefile to handle setting up and running
# the builds of the stackdriver agent on debian-y
# distributions
#
# this assumes it is being built from inside the stackdriver collectd git fork
SHELL=/bin/bash

source:
	[ -d collectd-$(VERSION).git ] && rm -rf collectd-$(VERSION).git || true # return true so we don't error out because the test condition fails
	git clone ../../ collectd-$(VERSION).git
	pushd collectd-$(VERSION).git ; \
	git archive --format tar --prefix=collectd-$(VERSION)/ HEAD | gzip > ../stackdriver-agent_$(VERSION).orig.tar.gz  ; \
	popd

srcpkg: source debian/rules
	tar -xf stackdriver-agent_$(VERSION).orig.tar.gz
	pushd collectd-$(VERSION) ; \
	cp -r ../debian . ; \
	DEBEMAIL="gcm-agent-dev@google.com" DEBFULLNAME="Stackdriver Agents" dch --package stackdriver-agent --distribution $(DISTRO) -v $(VERSION)-$(BUILD_NUM).$(DISTRO) "Automated build" ; \
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

DISTRO?=`lsb_release -a 2>/dev/null |grep Codename |awk {'print $2;'}`
ARCH?=`uname -i`

OUTPUT_DIR ?= result

vendor-debs:

clean:
	rm -rf *.dsc *.deb *.tar.gz *.tar.bz2 collectd-$(VERSION) result apt
