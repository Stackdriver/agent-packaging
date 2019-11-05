# this assumes it is being built from inside the stackdriver collectd git fork
SHELL=/bin/bash

include VERSION

source:
	[ -d collectd-$(VERSION).git ] && rm -rf collectd-$(VERSION).git || true # return true so we don't error out because the test condition fails
	# this is run from inside our collectd fork so we clone a clean copy to work off of
	git clone ../../ collectd-$(VERSION).git
	pushd collectd-$(VERSION).git ; \
	git archive --format tar --prefix=collectd-$(VERSION)/ HEAD | gzip > ../stackdriver-agent_$(PKG_VERSION).orig.tar.gz  ; \
	popd

srcpkg: source debian/rules
	tar -xf stackdriver-agent_$(PKG_VERSION).orig.tar.gz
	pushd collectd-$(VERSION) ; \
	cp -r ../debian . ; \
	DEBEMAIL="stackdriver-agents@google.com" DEBFULLNAME="Stackdriver Agents" dch --package stackdriver-agent --distribution $(DISTRO) -v $(PKG_VERSION)-$(PKG_BUILD).$(DISTRO) "Automated build" ; \
	cat debian/changelog ; \
	pushd debian ; \
	if [ -f controls/control.$(DISTRO) ]; then cp controls/control.$(DISTRO) control ; else cp controls/control.base control ; fi ; \
	popd ; \
	popd

build: srcpkg
	[ -n "$(DIR_TO_RM)" ] && rm -rf "$(DIR_TO_RM)" || true # return true so we don't error out because the test condition fails
	pushd collectd-$(VERSION) ; \
	debuild -us -uc; \
	popd ; \
	rm -rf collectd-$(VERSION)
	mkdir -p $(OUTPUT_DIR)
	[ "$(OUTPUT_DIR)" != "." ] && mv ./stackdriver-agent_*.deb $(OUTPUT_DIR)/ || true # return true so we don't error out because the test condition fails

DISTRO?=`lsb_release -a 2>/dev/null |grep Codename |awk {'print $2;'}`
ARCH?=`uname -i`

OUTPUT_DIR ?= result

ifneq ($(findstring $(abspath $(OUTPUT_DIR)),$(CURDIR)),)
DIR_TO_RM :=  # Avoid trying to rm any prefix of the current directory.
else
DIR_TO_RM := $(OUTPUT_DIR)
endif

clean:
	rm -rf $(DIR_TO_RM) *.dsc *.deb *.tar.gz *.tar.bz2 collectd-$(VERSION) collectd-$(VERSION).git result apt
