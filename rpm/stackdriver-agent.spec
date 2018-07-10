%global _hardened_build 1

# we expect the distro suffix
%global dist .sles12

# we have some references to the buildroot in the binaries for the include path
%define __arch_install_post %{nil}

%define programprefix stackdriver-

# Everything lives under /opt/ except config files which live in /etc/stackdriver/
%define _prefix /opt/stackdriver/collectd
%define _sysconfdir %{_prefix}/etc
%define _confdir /etc/stackdriver
%define _mandir %{_prefix}/man
%define _initddir /etc/init.d

# some things that we enable or not based on distro version
%define docker_flag --disable-docker
%define java_version 1_7_0


Summary: Stackdriver system metrics collection daemon
Name: stackdriver-agent
Version: %{collectd_version}
Release: %{build_num}%{?dist}
License: GPLv2
Group: System Environment/Daemons
URL: http://www.stackdriver.com/

Source: collectd-%{version}.tar.gz
Source200: stackdriver-agent
Source201: collectd.conf
Source202: stackdriver.sysconfig
BuildRequires: python-devel
BuildRequires: libgcrypt-devel
BuildRequires: flex
BuildRequires: bison
BuildRequires: autoconf, automake >= 1.14
BuildRequires: libtool
BuildRequires: rpm-build
BuildRequires: libcurl-devel
BuildRequires: libyajl-devel
BuildRequires: postgresql-devel
BuildRequires: libmysqlclient-devel
# this is in the main mysql package sometimes but -devel ends up
# just depending on libs.
BuildRequires: /usr/bin/mysql_config
BuildRequires: git
BuildRequires: openssl-devel
BuildRequires: hiredis-devel
BuildRequires: java-%{java_version}-openjdk-devel
BuildRequires: java-%{java_version}-openjdk
BuildRequires: java-devel

Requires: libyajl2
Requires: curl
Requires: sed
Requires(preun): /sbin/chkconfig
Requires(post): /sbin/chkconfig
Requires(post): /bin/grep
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%define _use_internal_dependency_generator 0

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

%filter_provides_in .*/collectd/.*\.so$

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
# update for aarch64
%setup -q -n collectd-%{version}

%build
export PATH=%{buildroot}/%{_prefix}/bin:$PATH

# install mongo-c-driver into mongodb-mongo-c-driver/build
%configure CFLAGS="%{optflags} -DLT_LAZY_OR_NOW='RTLD_NOW|RTLD_GLOBAL'" \
    --program-prefix=stackdriver- \
    --disable-all-plugins \
    --disable-static \
    --disable-perl --without-libperl  --without-perl-bindings \
    --with-libiptc \
    --with-libmongoc=own \
    --enable-cpu \
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
    --enable-java --with-java=/usr/lib64/jvm/java \
    --enable-redis --with-libhiredis \
    --enable-curl \
    --enable-curl_json \
    --enable-mongodb \
    --enable-varnish \
    --enable-write_gcm \
    --enable-debug \
    %{docker_flag}

%{__make} %{?_smp_mflags}


%install
# we have to reinstall as %%install cleans the buildroot
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

%dir %{_datadir}/collectd/java
%{_datadir}/collectd/java/collectd-api.jar
%{_datadir}/collectd/java/generic-jmx.jar

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
* Mon Oct 16 2017 Stackdriver Agents <stackdriver-agents@google.com> 5.5.2-372
- Make --write-gcm the default.
