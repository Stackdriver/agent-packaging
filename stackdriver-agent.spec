%global _hardened_build 1
%global __provides_exclude_from .*/collectd/.*\\.so$

# we have some references to the buildroot in the binaries for the include path
%define __arch_install_post %{nil}

%define programprefix stackdriver-

# a little unorthodox but let's get basically everything under /opt
%define _prefix /opt/stackdriver/collectd
%define _sysconfdir %{_prefix}/etc
%define _mandir %{_prefix}/man
%define _initddir /etc/rc.d/init.d

# some things that we enable or not based on distro version
%define has_yajl 0
%define has_hiredis 0
%define mongo 0
%define varnish 0
%define java_plugin 0
%define dep_filter 0
%define java_version 1.7.0

%if 0%{?rhel} >= 6
%define has_yajl 1
%define has_hiredis 1
%define mongo 1
%define varnish 1
%define java_plugin 1
%define dep_filter 1
%endif

%if 0%{?rhel} <= 6
%define java_version 1.6.0
%endif

%if 0%{?amzn} >= 1
%define has_yajl 1
%define has_hiredis 1
%define mongo 1
%define varnish 1
%define java_plugin 1
%define dep_filter 1
%endif

%if %{has_hiredis}
%define redis_flag --enable-redis --with-libhiredis
%endif

%if %{has_yajl}
%define curl_json_flag --enable-curl_json
%define gcm_flag --enable-write_gcm
%endif

%if %{mongo}
%define mongo_flag  --enable-mongodb
%endif

%if %{varnish}
%define varnish_flag --enable-varnish
%endif

%if %{java_plugin}
%define java_flag --enable-java --with-java=/usr/lib/jvm/java
%endif



Summary: Stackdriver system metrics collection daemon
Name: stackdriver-agent
Version: %{collectd_version}
Release: %{build_num}%{?dist}
License: GPLv2
Group: System Environment/Daemons
URL: http://www.stackdriver.com/

Source: collectd-%{version}.tar.gz
# embed libcurl so we know it's linked against openssl instead of
# nss. this avoids problems of nss leaking with libcurl. sigh.
%define curl_version 7.34.0
Source1: curl-%{curl_version}.tar.bz2
Source200: stackdriver-agent
Source201: stackdriver-collectd.conf
Source202: stackdriver.sysconfig
Source203: stackdriver-collectd-gcm.conf
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(ExtUtils::Embed)
BuildRequires: python-devel
BuildRequires: libgcrypt-devel
BuildRequires: autoconf, automake
BuildRequires: mysql-devel
# this is in the main mysql package sometimes but -devel ends up
# just depending on libs.
BuildRequires: /usr/bin/mysql_config
BuildRequires: postgresql-devel
BuildRequires: git
BuildRequires: openssl-devel

%if %{java_plugin}
BuildRequires: java-%{java_version}-openjdk-devel
BuildRequires: java-%{java_version}-openjdk
BuildRequires: java-devel
%endif

%if %{has_hiredis}
BuildRequires: hiredis-devel
%endif
%if %{has_yajl}
BuildRequires: yajl-devel
Requires: yajl
%endif
%if %{mongo}
BuildRequires: varnish-libs-devel
%endif
Requires: curl
Requires: sed
Requires(preun): /sbin/chkconfig
Requires(post): /sbin/chkconfig
Requires(post): /bin/grep
Requires: stackdriver-extractor >= 94
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%define    _use_internal_dependency_generator 0

# NOTE: this will only work for EL6.  If we want to support EL5, we'll
# have to do some more work
%if %{dep_filter}
%filter_requires_in mysql
%filter_requires_in postgresql
%filter_requires_in redis
%filter_requires_in curl_json
%filter_requires_in varnish
%filter_requires_in write_gcm
%filter_requires_in java
%filter_setup
%endif

%description
The Stackdriver system metrics daemon collects system statistics and
sends them to the Stackdriver service.

Currently includes collectd.

%prep
# update for aarch64
%setup -q -n collectd-%{version} -a 1

%build
# build libcurl first
pushd curl-%{curl_version}
./configure --prefix=%{buildroot}%{_prefix} --with-ssl --disable-threaded-resolver --enable-ipv6 \
    --with-libidn --disable-shared --enable-static --disable-manual \
    --with-ca-bundle=/etc/pki/tls/certs/ca-bundle.crt
%{__make} %{?_smp_mflags}
%{__make} install
popd
export PATH=%{buildroot}/%{_prefix}/bin:$PATH

# install mongo-c-driver into mongodb-mongo-c-driver/build
%configure CFLAGS="%{optflags} -DLT_LAZY_OR_NOW='RTLD_NOW|RTLD_GLOBAL' -Icurl-%{curl_version}/include" \
    --program-prefix=stackdriver- \
    --disable-all-plugins \
    --disable-static \
    --disable-perl --without-libperl  --without-perl-bindings \
    --with-libiptc \
    --with-libmongoc=own \
    --with-libcurl=%{buildroot}/%{_prefix} \
    --with-python \
    --enable-cpu \
    --enable-curl \
    --enable-df \
    --enable-disk \
    --enable-load \
    --enable-logfile \
    --enable-logging-metrics \
    --enable-memory \
    --enable-swap \
    --enable-syslog \
    --enable-interface \
    --enable-tcpconns \
    --enable-write_http \
    --enable-aggregation \
    --enable-csv \
    --enable-nginx \
    --enable-apache \
    --enable-memcached \
    --enable-mysql \
    --enable-protocols \
    --enable-postgresql \
    --enable-plugin_mem \
    --enable-processes \
    --enable-ntpd \
    --enable-nfs \
    --enable-zookeeper \
    --enable-stackdriver_agent \
    --enable-exec \
    --enable-tail \
    --enable-statsd \
    --enable-network \
    --enable-match_regex --enable-target_set \
    --enable-target_replace --enable-target_scale \
    --enable-match_throttle_metadata_keys \
    --enable-write_log \
    --enable-unixsock \
    --with-useragent="stackdriver_agent/%{version}-%{release}" \
    %{java_flag} \
    %{redis_flag} \
    %{curl_json_flag} \
    %{mongo_flag} \
    %{varnish_flag} \
    %{gcm_flag} \
    --enable-debug

%{__make} %{?_smp_mflags}


%install
# we have to reinstall as %%install cleans the buildroot
pushd curl-%{curl_version}
%{__make} install
# now remove things to avoid unpackaged files
rm -rf %{buildroot}/%{_prefix}/bin %{buildroot}/%{_prefix}/man
rm -rf %{buildroot}/%{_prefix}/share %{buildroot}/%{_prefix}/lib*/pkgconfig
popd

%{__rm} -rf contrib/SpamAssassin
%{__make} install DESTDIR="%{buildroot}"

%{__install} -Dp -m0755 %{SOURCE200} %{buildroot}/%{_initddir}/stackdriver-agent
%{__install} -Dp -m0644 %{SOURCE201} %{buildroot}%{_sysconfdir}/collectd.conf.tmpl
%{__install} -Dp -m0644 %{SOURCE202} %{buildroot}/etc/sysconfig/stackdriver
%{__install} -Dp -m0644 %{SOURCE203} %{buildroot}%{_sysconfdir}/collectd-gcm.conf.tmpl

%{__install} -d -m0755 %{buildroot}/%{_datadir}/collectd/collection3/

find contrib/ -type f -exec %{__chmod} a-x {} \;

# Remove Perl hidden .packlist files.
find %{buildroot} -name .packlist -exec rm {} \;
# Remove Perl temporary file perllocal.pod
find %{buildroot} -name perllocal.pod -exec rm {} \;

# Move config contribs
mkdir -p %{buildroot}%{_sysconfdir}/collectd.d/

# *.la files shouldn't be distributed.
rm -f %{buildroot}%{_libdir}/{collectd/,}*.la

# now remove more libcurl stuff that was needed to finish the install
rm -rf %{buildroot}%{_prefix}/include/curl %{buildroot}%{_prefix}/lib/libcurl*

# remove libmongoc and libbson includes and doc files
%{__rm} -rf %{buildroot}%{_prefix}/include/libmongoc-1.0
%{__rm} -rf %{buildroot}%{_prefix}/include/libbson-1.0

%{__rm} -rf %{buildroot}%{_prefix}/share/doc/mongo-c-driver
%{__rm} -rf %{buildroot}%{_prefix}/share/doc/libbson

%{__rm} -f %{buildroot}%{_prefix}/bin/stackdriver-mongoc-stat

# Remove files that are laying about that rpmbuild is complaining about.
%{__rm} -f %{buildroot}%{_prefix}/man/man5/%{programprefix}collectd-email.5*
%{__rm} -f %{buildroot}%{_prefix}/man/man5/%{programprefix}collectd-java.5*
%{__rm} -f %{buildroot}%{_prefix}/man/man5/%{programprefix}collectd-lua.5*
%{__rm} -f %{buildroot}%{_prefix}/man/man5/%{programprefix}collectd-perl.5*
%{__rm} -f %{buildroot}%{_prefix}/man/man5/%{programprefix}collectd-snmp.5*
%{__rm} -f %{buildroot}%{_prefix}/bin/stackdriver-utils_vl_lookup_test

%post
/sbin/ldconfig
/sbin/chkconfig --add stackdriver-agent
if [ $(grep -c 'STACKDRIVER_API_KEY=""' /etc/sysconfig/stackdriver) -eq 0 ] ; then
    echo Please edit /etc/sysconfig/stackdriver to supply your API key.
fi

%preun
if [ $1 -eq 0 ]; then
    /sbin/service stackdriver-agent stop &>/dev/null || :
    /sbin/chkconfig --del stackdriver-agent
fi

%postun
/sbin/ldconfig
/sbin/service stackdriver-agent condrestart &>/dev/null || :

%files
%defattr(-, root, root, -)
%ghost %{_sysconfdir}/collectd.conf
%config %{_sysconfdir}/collectd.conf.tmpl
%config %{_sysconfdir}/collectd-gcm.conf.tmpl
%config(noreplace) %{_sysconfdir}/collectd.d/

%{_bindir}/%{programprefix}collectd-nagios
%{_bindir}/%{programprefix}collectdctl
%{_bindir}/%{programprefix}collectd-tg
%{_bindir}/%{programprefix}read_agent_logging
%{_sbindir}/%{programprefix}collectd
%{_sbindir}/%{programprefix}collectdmon

%dir %{_libdir}/collectd
%{_libdir}/collectd/*.so

%{_datadir}/collectd/types.db
%{_datadir}/collectd/postgresql_default.conf

# collectdclient - TBD reintroduce -devel subpackage?
%{_libdir}/libcollectdclient.so
%{_libdir}/libcollectdclient.so.1
%{_libdir}/libcollectdclient.so.1.0.0
%{_libdir}/pkgconfig/libcollectdclient.pc
%{_includedir}/collectd/client.h
%{_includedir}/collectd/lcc_features.h
%{_includedir}/collectd/network.h
%{_includedir}/collectd/network_buffer.h

%{_libdir}/libbson-1.0.*
%{_libdir}/libmongoc-1.0.*
%{_libdir}/libmongoc-priv.*
%{_libdir}/pkgconfig/*

%if %{java_plugin}
%dir %{_datadir}/collectd/java
%{_datadir}/collectd/java/collectd-api.jar
%{_datadir}/collectd/java/generic-jmx.jar
%endif

%doc AUTHORS ChangeLog COPYING README
%doc %{_mandir}/man1/%{programprefix}collectd.1*
%doc %{_mandir}/man1/%{programprefix}collectdctl.1*
%doc %{_mandir}/man1/%{programprefix}collectd-nagios.1*
%doc %{_mandir}/man1/%{programprefix}collectd-tg.1*
%doc %{_mandir}/man1/%{programprefix}collectdmon.1*
%doc %{_mandir}/man5/%{programprefix}collectd.conf.5*
%doc %{_mandir}/man5/%{programprefix}collectd-exec.5*
%doc %{_mandir}/man5/%{programprefix}collectd-python.5*
%doc %{_mandir}/man5/%{programprefix}collectd-threshold.5*
%doc %{_mandir}/man5/%{programprefix}collectd-unixsock.5*
%doc %{_mandir}/man5/%{programprefix}types.db.5*

# Stackdriver.
%{_initddir}/stackdriver-agent
%config(noreplace) /etc/sysconfig/stackdriver


%changelog
* Thu Jan 16 2014 Jeremy Katz <jeremy@stackdriver.com> 5.3.0-122
- Build libcurl against openssl and use that instead of system libcurl to avoid leaks

* Thu Jul 18 2013 John (J5) Palmieri <j5@stackdriver.com>
- Move to automated builds from jenkins

* Mon Jul 15 2013 John (J5) Palmieri <j5@stackdriver.com> 5.3.0-19
- start of refactor

* Thu Jul 11 2013 John (J5) Palmieri <j5@stackdriver.com> 5.3.0-18
- bump for authentication fixes in collectd

* Thu Jul 11 2013 John (J5) Palmieri <j5@stackdriver.com> 5.3.0-17
- bump for collectd fixes

* Fri Jul 05 2013 John (J5) Palmieri <j5@stackdriver.com> 5.3.0-16
- install the postgresql_default.conf default query files

* Tue Jul 02 2013 John (J5) Palmieri <j5@stackdriver.com> 5.3.0-15
- bump to grab invalid free fix

* Mon Jul 01 2013 John (J5) Palmieri <j5@stackdriver.com> 5.3.0-14
- bump for upstream becaue we don't yet have auto version builders inplace

* Sun Jun 30 2013 John (J5) Palmieri <j5@stackdriver.com> 5.3.0-13
- Get rid of patches
- Build new collectd from our repo

* Thu Jun 28 2013 John (J5) Palmieri <j5@stackdriver.com> 5.3.0-12
- use our forked copy of collectd

* Thu Jun 27 2013 John (J5) Palmieri <j5@stackdriver.com> 5.3.0-11
- fix typo s/LD_LIBRARY_DIR/LD_LIBRARY_PATH

* Thu Jun 27 2013 John (J5) Palmieri <j5@stackdriver.com> 5.3.0-10
- init file now sets LD_LIBRARY_PATH when running collectd so the mongo plugi
  can find its support libs

* Wed Jun 26 2013 John (J5) Palmieri <j5@stackdriver.com> 5.3.0-9
- looks like we still dynamically link to the mongo drivers so install them

* Wed Jun 26 2013 John (J5) Palmieri <j5@stackdriver.com> 5.3.0-8
- make path to the mongo driver absolute

* Wed Jun 26 2013 John (J5) Palmieri <j5@stackdriver.com> - 5.3.0-7
- add bits for building mongodb plugin

* Mon Jun  3 2013 Jeremy Katz <katzj@fedoraproject.org>
- Add plugins for mysql, postgresql and redis

* Fri May 31 2013 Jeremy Katz <katzj@fedoraproject.org>
- Add memcached, nginx and apache plugins

* Mon May 28 2013 Jeremy Katz <katzj@fedoraproject.org>
- Restart nightly

* Wed May 23 2013 Jeremy Katz <katzj@fedoraproject.org>
- Enable aggregation plugin
- Set up to send rates to new endpoint + use aggregates
- Bump buffer size for write_http so we send all data at once

* Wed May 23 2013 Jeremy Katz <katzj@fedoraproject.org>
- Minor fixes

* Wed May  8 2013 Jeremy Katz <katzj@fedoraproject.org>
- Initial build of Stackdriver agent package based on Fedora collectd 5.3.0 package
