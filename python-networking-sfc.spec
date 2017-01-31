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

BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-sphinx
BuildRequires:  python2-devel

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
%{?python_provide:%python_provide python2-%{library}}

Requires:       python-neutron

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
Requires:   python2-%{pypi_name} = %{version}-%{release}

%description -n python2-%{pypi_name}-tests
Networking-sfc set of tests


%prep
%autosetup -n %{pypi_name}-%{upstream_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%{__python2} setup.py build_sphinx


%install
%py2_install


%check
%{__python2} setup.py testr


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
