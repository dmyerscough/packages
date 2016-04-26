Name:           consul
Version:        0.6.4
Release:        1
Summary:        Consul has multiple components, but as a whole, it is a tool for discovering and configuring services in your infrastructure.

License:        Mozilla Public License, version 2.0
URL:            www.consul.io
Source0:        https://releases.hashicorp.com/consul/0.6.4/%{name}_%{version}_linux_amd64.zip
#Source0:        %{name}_%{version}_linux_amd64.zip

Requires(pre):  shadow-utils

%description
Consul is a tool for service discovery and configuration.
Consul is distributed, highly available, and extremely scalable.

Consul provides several key features:

* Service Discovery - Consul makes it simple for services to register
themselves and to discover other services via a DNS or HTTP interface.
External services such as SaaS providers can be registered as well.

* Health Checking - Health Checking enables Consul to quickly alert operators
about any issues in a cluster. The integration with service discovery prevents
routing traffic to unhealthy hosts and enables service level circuit breakers.

* Key/Value Storage - A flexible key/value store enables storing dynamic configuration,
feature flagging, coordination, leader election and more. The simple HTTP API makes it
easy to use anywhere.

* Multi-Datacenter - Consul is built to be datacenter aware, and can support any number
of regions without complex configuration.

%pre
%{_bindir}/getent passwd consul >/dev/null || %{_sbindir}/useradd -r \
-d /home/consul -c "consul service" -s /sbin/nologin consul

%prep
%setup -c

%install
mkdir -p ${RPM_BUILD_ROOT}/etc/consul.d/{bootstrap,server,client}
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}/var/consul

install -m 755 %{_builddir}/%{name}-%{version}/consul ${RPM_BUILD_ROOT}%{_sbindir}

for config in %{_sourcedir}/consul.d/* ; do
    cfg=${config##*/}
    install -m 600 ${config} ${RPM_BUILD_ROOT}/etc/consul.d/${cfg%.*}/config.json
done

#install -m 600 %{_sourcedir}/consul.d/bootstrap.json ${RPM_BUILD_ROOT}/etc/consul.d/bootstrap/config.json
#install -m 600 %{_sourcedir}/consul.d/client.json ${RPM_BUILD_ROOT}/etc/consul.d/client/config.json
#install -m 600 %{_sourcedir}/consul.d/server.json ${RPM_BUILD_ROOT}/etc/consul.d/server/config.json

%files
%attr(755, -, root) %{_sbindir}/consul
%attr(755, -, root) %{_sysconfdir}/consul.d
%attr(700, -, root) %{_sysconfdir}/consul.d/server
%attr(700, -, root) %{_sysconfdir}/consul.d/client
%attr(600, -, root) %{_sysconfdir}/consul.d/bootstrap/config.json
%attr(600, -, root) %{_sysconfdir}/consul.d/client/config.json
%attr(600, -, root) %{_sysconfdir}/consul.d/server/config.json
%attr(755, -, root) %{_localstatedir}/consul


%changelog
* Thu Apr 21 2016 Damian Myerscough <Damian dot Myerscough at gmail dot com> - 0.6.4
- Initial Consul build
