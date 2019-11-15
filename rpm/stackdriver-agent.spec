%global _hardened_build 1
# Not all platforms support __provides_exclude_from; see dep_filter below.
%global __provides_exclude_from .*/collectd/.*\\.so$

%if 0%{?suse_version} > 0
# we expect the distro suffix
%if 0%{?suse_version} < 1500
%global dist .sles12
%endif
%if 0%{?suse_version} >= 1500
%global dist .sles15
%endif
%endif

# we have some references to the buildroot in the binaries for the include path
%define __arch_install_post %{nil}

%define programprefix stackdriver-

# Everything lives under /opt/ except config files which live in /etc/stackdriver/
%define _prefix /opt/stackdriver/collectd
%define _sysconfdir %{_prefix}/etc
%define _confdir /etc/stackdriver
%define _mandir %{_prefix}/man
%if 0%{?suse_version} > 0
%define _initddir /etc/init.d
%else
%define _initddir /etc/rc.d/init.d
%endif

# some things that we enable or not based on distro version
%define docker_flag --disable-docker
%define has_yajl 1
%define bundle_yajl 0
%define has_hiredis 1
%define mongo 1
%define bundle_mongo 1
%define varnish 1
%define java_plugin 1
%define bundle_curl 1
%define curl_version 7.34.0
%define java_version 1.6.0
%define java_lib_location /usr/lib/jvm/java
%define has_python36 0
# Enabled for systems that don't support the __provides_exclude_from global.
%define dep_filter 1

%if 0%{?rhel} >= 7
%define java_version 1.7.0
%define curl_version 7.52.1
%define docker_flag --enable-docker
%define dep_filter 0
%endif

%if 0%{?rhel} >= 8
%define java_version 1.8.0
%define has_python36 1
%define dep_filter 0
%endif

%if 0%{?amzn} >= 1
%define bundle_yajl 1
%define dep_filter 0
%endif

%if 0%{?suse_version} > 0
%define bundle_curl 0
%define java_lib_location /usr/lib64/jvm/java
%if 0%{?suse_version} < 1500
%define java_version 1.7.0
%endif
%if 0%{?suse_version} >= 1500
# Yes, SLES really has underscores.
%define java_version 1_8_0
%define dep_filter 0
%endif
%endif

%if %{has_hiredis}
%define redis_flag --enable-redis --with-libhiredis
%endif

%if %{bundle_curl}
%define curl_include -Icurl-%{curl_version}/include
%define libcurl_flag --with-libcurl=%{buildroot}/%{_prefix}
%endif

%if %{has_yajl}
%define curl_json_flag --enable-curl_json
%define gcm_flag --enable-write_gcm
%endif

%if %{mongo}
%define mongo_flag  --enable-mongodb
%if %{bundle_mongo}
%define libmongoc_flag --with-libmongoc=own --with-libbson=bundled
%else
%define libmongoc_flag --with-libmongoc=yes
%endif
%endif

%if %{varnish}
%define varnish_flag --enable-varnish
%endif

%if %{java_plugin}
%define java_flag --enable-java --with-java=%{java_lib_location}
%endif

Summary: Stackdriver system metrics collection daemon
Name: stackdriver-agent
Version: %{package_version}
Release: %{build_num}%{?dist}
License: GPLv2
Group: System Environment/Daemons
URL: http://www.stackdriver.com/

Source: stackdriver-agent-%{version}.orig.tar.gz
%if %{bundle_curl}
# embed libcurl so we know it's linked against openssl instead of
# nss. this avoids problems of nss leaking with libcurl. sigh.
Source1: curl-%{curl_version}.tar.bz2
%endif
Source200: stackdriver-agent
Source201: collectd.conf
Source202: stackdriver.sysconfig
%if 0%{?suse_version} == 0
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(ExtUtils::Embed)
%endif
%if ! %{has_python36}
BuildRequires: python-devel
%else
BuildRequires: python36-devel
%endif
BuildRequires: libgcrypt-devel
BuildRequires: autoconf, automake
%if 0%{?suse_version} > 0
BuildRequires: bison
BuildRequires: flex
BuildRequires: libtool
BuildRequires: rpm-build
%endif
%if ! %{bundle_curl}
BuildRequires: libcurl-devel
%endif
%if 0%{?suse_version} > 0
BuildRequires: libmysqlclient-devel
%else
BuildRequires: mysql-devel
%endif
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
%if 0%{?suse_version} > 0
BuildRequires: libyajl-devel
%else
BuildRequires: yajl-devel
%endif
%if ! %{bundle_yajl}
%if 0%{?suse_version} > 0
Requires: libyajl2
%else
Requires: yajl
%endif
%endif
%endif
%if %{varnish}
%if 0%{?suse_version} > 0
BuildRequires: varnish-devel
%else
BuildRequires: varnish-libs-devel
%endif
%endif
%if %{mongo}
%if ! %{bundle_mongo}
BuildRequires: mongo-c-driver-devel, cyrus-sasl-devel
Requires: mongo-c-driver-libs
%endif
%endif
Requires: curl
Requires: sed
Requires(preun): /sbin/chkconfig
Requires(post): /sbin/chkconfig
Requires(post): /bin/grep
%if 0%{?suse_version} > 0
Requires(post): %insserv_prereq
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%define _use_internal_dependency_generator 0

%if 0%{?suse_version} > 0
##### This section has been copied from redhat/macros.
# prevent anything matching from being scanned for provides
%define filter_provides_in(P) %{expand: \
%global __filter_prov_cmd %{?__filter_prov_cmd} %{__grep} -v %{-P} '%*' | \
}

# prevent anything matching from being scanned for requires
%define filter_requires_in(P) %{expand: \
%global __filter_req_cmd %{?__filter_req_cmd} %{__grep} -v %{-P} '%*' | \
}

# actually set up the filtering bits
%define filter_setup %{expand: \
%global _use_internal_dependency_generator 0 \
%global __deploop() while read FILE; do echo "${FILE}" | /usr/lib/rpm/rpmdeps -%{1}; done | /bin/sort -u \
%global __find_provides /bin/sh -c "%{?__filter_prov_cmd} %{__deploop P} %{?__filter_from_prov}" \
%global __find_requires /bin/sh -c "%{?__filter_req_cmd}  %{__deploop R} %{?__filter_from_req}" \
}
##### End section
%endif

%if %{dep_filter}
%filter_provides_in .*/collectd/.*\.so$
%endif

%filter_requires_in mysql
%filter_requires_in postgresql
%filter_requires_in redis
%filter_requires_in curl_json
%filter_requires_in varnish
%filter_requires_in write_gcm
%filter_requires_in java
%filter_requires_in python
%filter_setup

%description
The Stackdriver system metrics daemon collects system statistics and
sends them to the Stackdriver service.

Currently includes collectd.

%prep
%setup -q -n collectd-pristine
# update for aarch64
%if %{bundle_curl}
%setup -q -n collectd-pristine -a 1
%endif

%build
%if %{bundle_curl}
# build libcurl first
pushd curl-%{curl_version}
./configure --prefix=%{buildroot}%{_prefix} --with-ssl --disable-threaded-resolver --enable-ipv6 \
    --with-libidn --disable-shared --enable-static --disable-manual \
    --with-ca-bundle=/etc/pki/tls/certs/ca-bundle.crt
%{__make} %{?_smp_mflags}
%{__make} install
popd
%endif
export PATH=%{buildroot}/%{_prefix}/bin:$PATH

# re-generate build files
./clean.sh && ./build.sh

# install mongo-c-driver into mongodb-mongo-c-driver/build
%configure CFLAGS="%{optflags} -DLT_LAZY_OR_NOW='RTLD_NOW|RTLD_GLOBAL' %{?curl_include}" \
    --program-prefix=stackdriver- \
    --disable-all-plugins \
    --disable-static \
    --disable-perl --without-libperl  --without-perl-bindings \
    --with-libiptc \
    %{?libcurl_flag} \
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
    --enable-python \
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
    %{docker_flag} \
    %{java_flag} \
    %{redis_flag} \
    %{curl_json_flag} \
    %{libmongoc_flag} \
    %{mongo_flag} \
    %{varnish_flag} \
    %{gcm_flag} \
    --enable-debug

%{__make} %{?_smp_mflags}


%install
# we have to reinstall as %%install cleans the buildroot
%if %{bundle_curl}
pushd curl-%{curl_version}
%{__make} install
# now remove things to avoid unpackaged files
rm -rf %{buildroot}/%{_prefix}/bin %{buildroot}/%{_prefix}/man
rm -rf %{buildroot}/%{_prefix}/share %{buildroot}/%{_prefix}/lib*/pkgconfig
popd
%endif

%{__rm} -rf contrib/SpamAssassin
%{__make} install DESTDIR="%{buildroot}"

%{__install} -Dp -m0755 %{SOURCE200} %{buildroot}/%{_initddir}/stackdriver-agent
%{__install} -Dp -m0644 %{SOURCE201} %{buildroot}/%{_confdir}/collectd.conf
%{__install} -Dp -m0644 %{SOURCE202} %{buildroot}/etc/sysconfig/stackdriver

%{__install} -d -m0755 %{buildroot}/%{_datadir}/collectd/collection3/

find contrib/ -type f -exec %{__chmod} a-x {} \;

# Remove Perl hidden .packlist files.
find %{buildroot} -name .packlist -exec rm {} \;
# Remove Perl temporary file perllocal.pod
find %{buildroot} -name perllocal.pod -exec rm {} \;

# Move config contribs
mkdir -p %{buildroot}%{_sysconfdir}/collectd.d/
mkdir -p %{buildroot}%{_confdir}/collectd.d/

# *.la files shouldn't be distributed.
rm -f %{buildroot}%{_libdir}/{collectd/,}*.la
rm -f %{buildroot}%{_sysconfdir}/collectd.conf
rm -f %{buildroot}%{_sysconfdir}/collectd.conf.pkg-orig

# now remove more libcurl stuff that was needed to finish the install
rm -rf %{buildroot}%{_prefix}/include/curl %{buildroot}%{_prefix}/lib/libcurl*

%if %{bundle_mongo}
# remove libmongoc and libbson includes and doc files
%{__rm} -rf %{buildroot}%{_prefix}/include/libmongoc-1.0
%{__rm} -rf %{buildroot}%{_prefix}/include/libbson-1.0

%{__rm} -rf %{buildroot}%{_prefix}/share/doc/mongo-c-driver
%{__rm} -rf %{buildroot}%{_prefix}/share/doc/libbson

%{__rm} -f %{buildroot}%{_prefix}/bin/stackdriver-mongoc-stat
%endif

# Remove files that are laying about that rpmbuild is complaining about.
%{__rm} -f %{buildroot}%{_prefix}/man/man5/%{programprefix}collectd-email.5*
%{__rm} -f %{buildroot}%{_prefix}/man/man5/%{programprefix}collectd-java.5*
%{__rm} -f %{buildroot}%{_prefix}/man/man5/%{programprefix}collectd-lua.5*
%{__rm} -f %{buildroot}%{_prefix}/man/man5/%{programprefix}collectd-perl.5*
%{__rm} -f %{buildroot}%{_prefix}/man/man5/%{programprefix}collectd-snmp.5*
%{__rm} -f %{buildroot}%{_prefix}/bin/stackdriver-utils_vl_lookup_test

%if %{bundle_yajl}
mkdir -p %{buildroot}%{_libdir}/yajl/
cp /usr/lib64/libyajl.so.1 %{buildroot}%{_libdir}/yajl/
ln -s -t %{buildroot}%{_libdir} yajl/libyajl.so.1
cp /usr/share/doc/yajl-1.0.7/COPYING yajl.COPYING
%endif

%post
/sbin/ldconfig
/sbin/chkconfig --add stackdriver-agent
%if 0%{?suse_version} > 0
# Enable the service by default.
%{fillup_and_insserv -f -y stackdriver-agent}
%endif

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
%config %{_confdir}/collectd.conf
%config(noreplace) %{_sysconfdir}/collectd.d/
%config(noreplace) %{_confdir}/collectd.d/

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
%{_libdir}/libcollectdclient.so*
%{_libdir}/pkgconfig/libcollectdclient.pc
%{_includedir}/collectd/*.h

%if %{bundle_mongo}
%{_libdir}/libbson-1.0.*
%{_libdir}/libmongoc-1.0.*
%{_libdir}/libmongoc-priv.*
%endif
%{_libdir}/pkgconfig/*

%if %{bundle_yajl}
%dir %{_libdir}/yajl/
%{_libdir}/yajl/libyajl.so.1
%{_libdir}/libyajl.so.1
%endif

%if %{java_plugin}
%dir %{_datadir}/collectd/java
%{_datadir}/collectd/java/collectd-api.jar
%{_datadir}/collectd/java/generic-jmx.jar
%endif

%doc AUTHORS ChangeLog COPYING README

%if %{bundle_yajl}
%doc yajl.COPYING
%endif

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
* Mon Oct 16 2017 Stackdriver Agents <stackdriver-agents@google.com> 5.5.2-372
- Make --write-gcm the default.
