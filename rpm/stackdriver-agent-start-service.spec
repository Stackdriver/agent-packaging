# Build with "rpmbuild -bb stackdriver-agent-start-service.spec".
Summary: Service auto-start helper for the Stackdriver system metrics collection daemon
Name: stackdriver-agent-start-service
Version: 0.0.1
Release: 1%{?dist}
BuildArch: noarch
License: ASL 2.0
Group: System Environment/Daemons
URL: https://cloud.google.com/monitoring/agent
Requires: stackdriver-agent

%description
This auxiliary helper automatically starts the Stackdriver system metrics daemon when installed.

%files

%clean
exit 0

%post
/sbin/service stackdriver-agent start

%changelog
* Thu Jun 11 2020 Stackdriver Agents <stackdriver-agents@google.com> 0.0.1-1
- Initial release.
