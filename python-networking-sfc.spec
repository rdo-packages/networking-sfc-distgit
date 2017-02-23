%global pypi_name networking-sfc
%global module networking_sfc
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        API and implementations to support Service Function Chaining in Neutron

License:        ASL 2.0
URL:            https://launchpad.net/%{pypi_name}
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-sphinx
# Test requirements
BuildRequires:  python-mock
BuildRequires:  python-requests-mock
BuildRequires:  python-oslotest
BuildRequires:  python-testrepository
BuildRequires:  python-testresources
BuildRequires:  python-testscenarios
BuildRequires:  python-neutron-lib-tests
BuildRequires:  python-neutron-tests
BuildRequires:  openstack-neutron
# To remove when code has moved to python-openstackclient
BuildRequires:  python2-osc-lib-tests

%description
This project provides APIs and implementations to support Service Function
Chaining in Neutron.

Service Function Chaining is a mechanism for overriding the basic destination
based forwarding that is typical of IP networks. It is conceptually related to
Policy Based Routing in physical networks but it is typically thought of as a
Software Defined Networking technology. It is often used in conjunction with
security functions although it may be used for a broader range of features.
Fundamentally SFC is the ability to cause network packet flows to route through
a network via a path other than the one that would be chosen by routing table
lookup on the packet's destination IP address. It is most commonly used in
conjunction with Network Function Virtualization when recreating in a virtual
environment a series of network functions that would have traditionally been
implemented as a collection of physical network devices connected in series by
cables.

%package -n python2-%{pypi_name}
Summary:        API and implementations to support Service Function Chaining in Neutron
%{?python_provide:%python_provide python2-%{pypi_name}}

Requires:       python-alembic
Requires:       python-eventlet
Requires:       python-netaddr
Requires:       python-neutron
Requires:       python-neutron-lib
Requires:       python-neutronclient
Requires:       python-oslo-config
Requires:       python-oslo-i18n
Requires:       python-oslo-log
Requires:       python-oslo-messaging
Requires:       python-oslo-serialization
Requires:       python-oslo-utils
Requires:       python-six
Requires:       python-sqlalchemy
Requires:       python-stevedore
# To remove when code has moved to python-openstackclient
Requires:       python-openstackclient

%description -n python2-%{pypi_name}
This project provides APIs and implementations to support Service Function
Chaining in Neutron.

Service Function Chaining is a mechanism for overriding the basic destination
based forwarding that is typical of IP networks. It is conceptually related to
Policy Based Routing in physical networks but it is typically thought of as a
Software Defined Networking technology. It is often used in conjunction with
security functions although it may be used for a broader range of features.
Fundamentally SFC is the ability to cause network packet flows to route through
a network via a path other than the one that would be chosen by routing table
lookup on the packet's destination IP address. It is most commonly used in
conjunction with Network Function Virtualization when recreating in a virtual
environment a series of network functions that would have traditionally been
implemented as a collection of physical network devices connected in series by
cables.


%package -n python-%{pypi_name}-doc
Summary:        Documentation for networking-sfc
%description -n python-%{pypi_name}-doc
Documentation for networking-sfc

%package -n python2-%{pypi_name}-tests
Summary:        Tests for networking-sfc
Requires:       python2-%{pypi_name} = %{version}-%{release}
Requires:       python-mock
Requires:       python-requests-mock
Requires:       python-oslotest
Requires:       python-testrepository
Requires:       python-testresources
Requires:       python-testscenarios
Requires:       python-neutron-lib-tests
Requires:       python-neutron-tests
Requires:       openstack-neutron
# To remove when code has moved to python-openstackclient
Requires:       python2-osc-lib-tests


%description -n python2-%{pypi_name}-tests
Networking-sfc set of tests


%prep
%autosetup -n %{pypi_name}-%{upstream_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# FIXME(bcafarel): require neutronclient.tests.unit (python-neutronclient-tests package was dropped)
rm -rf %{module}/tests/unit/cli

%build
%py2_build
%{__python2} setup.py build_sphinx


%install
%py2_install


%check
# FIXME(bcafarel): random unit test failures, apparently CentOS-specific
# Currently being tracked in https://bugs.launchpad.net/networking-sfc/+bug/1666568 
%{__python2} setup.py testr || :


%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{module}
%{python2_sitelib}/%{module}-*.egg-info
%exclude %{python2_sitelib}/%{module}/tests

%files -n python-%{pypi_name}-doc
%doc doc/build/html/*
%license LICENSE

%files -n python2-%{pypi_name}-tests
%license LICENSE
%{python2_sitelib}/%{module}/tests
%exclude %{python2_sitelib}/%{module}/tests/contrib


%changelog
