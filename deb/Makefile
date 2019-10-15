# this assumes it is being built from inside the stackdriver collectd git fork
SHELL=/bin/bash
source:
	[ -d collectd-5.8.1.git ] && rm -rf collectd-5.8.1.git || true # return true so we don't error out because the test condition fails
	git clone ../../ collectd-5.8.1.git
	PKG_VERSION=$(shell cat VERSION)
	pushd collectd-5.8.1.git ; \
	git archive --format tar --prefix=collectd-5.8.1/ HEAD | gzip > ../stackdriver-agent_$(PKG_VERSION).orig.tar.gz  ; \
	popd

srcpkg: source debian/rules
	tar -xf stackdriver-agent_$(PKG_VERSION).orig.tar.gz
	pushd collectd-5.8.1 ; \
	cp -r ../debian . ; \
	DEBEMAIL="stackdriver-agents@google.com" DEBFULLNAME="Stackdriver Agents" dch --package stackdriver-agent --distribution $(DISTRO) -v $(PKG_VERSION)-1.$(DISTRO) "Automated build" ; \
	cat debian/changelog ; \
	pushd debian ; \
	if [ -f controls/control.$(DISTRO) ]; then cp controls/control.$(DISTRO) control ; else cp controls/control.base control ; fi ; \
	popd ; \
	popd ; \

build: srcpkg
	pushd collectd-5.8.1 ; \
	debuild -us -uc; \
	popd ; \
	rm -rf collectd-5.8.1

DISTRO?=`lsb_release -a 2>/dev/null |grep Codename |awk {'print $2;'}`
ARCH?=`uname -i`

OUTPUT_DIR ?= result

vendor-debs:

clean:
	rm -rf *.dsc *.deb *.tar.gz *.tar.bz2 collectd-5.8.1 collectd-5.8.1.git result apt
