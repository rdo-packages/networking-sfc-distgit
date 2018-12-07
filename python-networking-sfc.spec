%global pypi_name networking-sfc
%global module networking_sfc
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global docpath doc/build/html

# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif

%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
%global pyver_entrypoint %py%{pyver}_entrypoint %{module} %{pypi_name}
# End of macros for py2/py3 compatibility

%global common_desc \
This project provides APIs and implementations to support Service Function \
Chaining in Neutron. \
\
Service Function Chaining is a mechanism for overriding the basic destination \
based forwarding that is typical of IP networks. It is conceptually related to \
Policy Based Routing in physical networks but it is typically thought of as a \
Software Defined Networking technology. It is often used in conjunction with \
security functions although it may be used for a broader range of features. \
Fundamentally SFC is the ability to cause network packet flows to route through \
a network via a path other than the one that would be chosen by routing table \
lookup on the packet's destination IP address. It is most commonly used in \
conjunction with Network Function Virtualization when recreating in a virtual \
environment a series of network functions that would have traditionally been \
implemented as a collection of physical network devices connected in series by \
cables.

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        API and implementations to support Service Function Chaining in Neutron

License:        ASL 2.0
URL:            https://launchpad.net/%{pypi_name}
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  openstack-macros
BuildRequires:  git
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-sphinx
# Test requirements
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-stestr
BuildRequires:  python%{pyver}-testresources
BuildRequires:  python%{pyver}-testscenarios
BuildRequires:  python%{pyver}-neutron-lib-tests
BuildRequires:  python%{pyver}-neutron-tests
%if %{pyver} == 2
BuildRequires:  python-requests-mock
%else
BuildRequires:  python%{pyver}-requests-mock
%endif
BuildRequires:  openstack-neutron

%description
%{common_desc}

%package -n python%{pyver}-%{pypi_name}
Summary:        API and implementations to support Service Function Chaining in Neutron
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}

Requires:       python%{pyver}-pbr >= 2.0.0
Requires:       openstack-neutron-common
Requires:       openstack-neutron
Requires:       python%{pyver}-alembic
Requires:       python%{pyver}-eventlet
Requires:       python%{pyver}-netaddr
Requires:       python%{pyver}-neutronclient >= 6.7.0
Requires:       python%{pyver}-oslo-config >= 2:5.2.0
Requires:       python%{pyver}-oslo-i18n >= 3.15.3
Requires:       python%{pyver}-oslo-log >= 3.36.0
Requires:       python%{pyver}-oslo-messaging >= 5.29.0
Requires:       python%{pyver}-oslo-serialization >= 2.18.0
Requires:       python%{pyver}-oslo-utils >= 3.33.0
Requires:       python%{pyver}-six
Requires:       python%{pyver}-sqlalchemy
Requires:       python%{pyver}-stevedore >= 1.20.0
Requires:       python%{pyver}-neutron
Requires:       python%{pyver}-neutron-lib >= 1.18.0

%description -n python%{pyver}-%{pypi_name}
%{common_desc}

%package -n python-%{pypi_name}-doc
Summary:        Documentation for networking-sfc
%description -n python-%{pypi_name}-doc
Documentation for networking-sfc

%package -n python%{pyver}-%{pypi_name}-tests
Summary:        Tests for networking-sfc
Requires:       python%{pyver}-%{pypi_name} = %{version}-%{release}
Requires:       python%{pyver}-mock
Requires:       python%{pyver}-oslotest
Requires:       python%{pyver}-stestr
Requires:       python%{pyver}-testresources
Requires:       python%{pyver}-testscenarios
BuildRequires:  python%{pyver}-neutron-lib-tests
BuildRequires:  python%{pyver}-neutron-tests
%if %{pyver} == 2
BuildRequires:  python-requests-mock
%else
BuildRequires:  python%{pyver}-requests-mock
%endif

%description -n python%{pyver}-%{pypi_name}-tests
Networking-sfc set of tests

%package -n python%{pyver}-%{pypi_name}-tests-tempest
Summary:    Tempest plugin for %{name}

Requires:       python%{pyver}-%{pypi_name} = %{version}-%{release}
Requires:       python%{pyver}-tempest

%description -n python%{pyver}-%{pypi_name}-tests-tempest
It contains the tempest plugin for %{name}.

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Let RPM handle the dependencies
%py_req_cleanup

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# FIXME(bcafarel): require neutronclient.tests.unit (python-neutronclient-tests package was dropped)
rm -rf %{module}/tests/unit/cli

%build
%pyver_build
%{pyver_bin} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
# generate the configuration file
PYTHONPATH=. oslo-config-generator-%{pyver} --config-file etc/oslo-config-generator/networking-sfc.conf


%install
%pyver_install

# Create a fake tempest plugin entrypoint
%pyver_entrypoint

# The generated config files are not moved automatically by setup.py
mkdir -p %{buildroot}%{_sysconfdir}/neutron/conf.d/neutron-server
mv etc/networking-sfc.conf.sample %{buildroot}%{_sysconfdir}/neutron/conf.d/neutron-server/networking-sfc.conf

%check
export PATH=$PATH:$RPM_BUILD_ROOT/usr/bin
stestr-%{pyver} run

%files -n python%{pyver}-%{pypi_name}
%license LICENSE
%doc README.rst
%{pyver_sitelib}/%{module}
%{pyver_sitelib}/%{module}-*.egg-info
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/conf.d/neutron-server/networking-sfc.conf
%exclude %{pyver_sitelib}/%{module}/tests

%files -n python-%{pypi_name}-doc
%doc doc/build/html/*
%license LICENSE

%files -n python%{pyver}-%{pypi_name}-tests
%{pyver_sitelib}/%{module}/tests
%exclude %{pyver_sitelib}/%{module}/tests/contrib
%exclude %{pyver_sitelib}/%{module}/tests/tempest_plugin

%files -n python%{pyver}-%{pypi_name}-tests-tempest
%{pyver_sitelib}/%{module}_tests.egg-info
%{pyver_sitelib}/%{module}/tests/tempest_plugin
%{pyver_sitelib}/%{module}/tests/__init__.py*

%changelog
