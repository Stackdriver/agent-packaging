source:
	[ -d collectd-$(VERSION).git ] && rm -rf collectd-$(VERSION).git || true # return true so we don't error out because the test condition fails
	# this is run from inside our collectd fork so we clone a clean copy to work off of
	git clone ../../ collectd-$(VERSION).git
	pushd collectd-$(VERSION).git ; \
	git archive --format tar --prefix=collectd-$(VERSION)/ HEAD | gzip > ../collectd-$(VERSION).tar.gz  ; \
	popd

ARCH ?= `uname -m`

build: source
	rm -rf result
	rpmbuild --define "_source_filedigest_algorithm md5" --define "_sourcedir $$(pwd)" --define "_srcrpmdir $$(pwd)" --define "collectd_version $(VERSION)" --define "build_num $(BUILD_NUM)" -ba stackdriver-agent.spec
	mkdir result
	cp /usr/src/packages/RPMS/$(ARCH)/stackdriver-agent-*.rpm result/

clean:
	rm -rf result *rpm collectd-5.5.2 *.tar.bz2 collectd-5.5.2.git *.tar.gz
