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
	DEBEMAIL="engineering@stackdriver.com" DEBFULLNAME="Stackdriver Engineering" dch --package stackdriver-agent --distribution $(DISTRO) -v $(VERSION)-$(BUILD_NUM).$(DISTRO) "Automated build" ; \
	cat debian/changelog ; \
	if [ -f debian/control.$(DISTRO) ]; then cp debian/control.$(DISTRO) debian/control ; else cp debian/control.base debian/control ; fi ; \
	DEB_BUILD_OPTIONS=nostrip,noopt dpkg-source -b . ; \
	popd ; \
	rm -rf collectd-$(VERSION)

BASETGZ=$(DISTRO)-$(ARCH).tgz
ifeq ($(BASETGZ), "-.tgz")
    BASETGZ=base.tgz
endif
BASETGZ_PATH=/var/cache/pbuilder/$(BASETGZ)
DISTRO?=`lsb_release -a 2>/dev/null |grep Codename |awk {'print $2;'}`
ARCH?=`uname -i`

ifeq ($(DISTRO),wheezy)
DEBIAN = 1
endif
ifeq ($(DISTRO),jessie)
DEBIAN=1
endif
ifeq ($(DISTRO),stretch)
DEBIAN=1
endif

ifeq (1,$(DEBIAN))
DEBIAN_OPTS = --mirror ftp://ftp.us.debian.org/debian/ --debootstrapopts "--keyring=/usr/share/keyrings/debian-archive-keyring.gpg"
COMPONENTS = "main contrib non-free"
else
COMPONENTS = "main restricted universe multiverse"
endif

setup-root:
	sudo pbuilder create --basetgz $(BASETGZ_PATH) --components $(COMPONENTS) --distribution $(DISTRO) --architecture $(ARCH) $(DEBIAN_OPTS)

build: srcpkg
	[ -f $(BASETGZ_PATH) ] || make setup-root
	rm -rf result ; mkdir result
	sudo pbuilder build --buildresult result --basetgz $(BASETGZ_PATH) stackdriver-agent_$(VERSION)-$(BUILD_NUM).$(DISTRO).dsc

OUTPUT_DIR ?= result

vendor-debs:

repo:
	@rm -rf apt
	@mkdir -p apt/conf
	@cp distributions apt/conf/distributions
	@for distro in precise trusty xenial wheezy jessie stretch; do \
		find $(OUTPUT_DIR)/*$$distro* -name "*.deb" -exec reprepro --export=never -Vb apt includedeb $$distro {} \; ;\
		find $(OUTPUT_DIR)/*$$distro* -name "*.dsc" -exec reprepro --export=never -Vb apt includedsc $$distro {} \; ; \
	done

# would love to use the jenkins s3 artifact uploader for this but it doesn't preserve
# the directory structure
syncrepo: repo
	s3cmd -c /etc/s3cmd.cfg sync --follow-symlinks apt/ s3://testrepo.stackdriver.com/apt/

syncalpharepo: repo
	s3cmd -c /etc/s3cmd.cfg sync --follow-symlinks apt/ s3://alpharepo.stackdriver.com/apt/

# The default permissions for the repo is set to public-read
syncgrepo: repo
	export BOTO_CONFIG=/etc/boto.cfg
	gsutil -m rsync -c -r apt/ gs://gtestrepo.stackdriver.com/apt/

sign:
	# need to do this after adding packages so that the repo is properly signed. and yay expect
	expect signer.exp

clean:
	rm -rf *.dsc *.deb *.tar.gz *.tar.bz2 collectd-$(VERSION) result apt
