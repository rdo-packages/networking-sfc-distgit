%global pypi_name networking-sfc
%global module networking_sfc
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global docpath doc/build/html
%global with_doc 1


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
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
# Test requirements
BuildRequires:  python3-mock
BuildRequires:  python3-oslotest
BuildRequires:  python3-stestr
BuildRequires:  python3-testresources
BuildRequires:  python3-testscenarios
BuildRequires:  python3-neutron-lib-tests
BuildRequires:  python3-neutron-tests
BuildRequires:  python3-requests-mock
BuildRequires:  openstack-neutron

%description
%{common_desc}

%package -n python3-%{pypi_name}
Summary:        API and implementations to support Service Function Chaining in Neutron
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       python3-pbr >= 2.0.0
Requires:       openstack-neutron-common
Requires:       openstack-neutron >= 1:13.0.0
Requires:       python3-alembic >= 0.8.10
Requires:       python3-eventlet >= 0.18.2
Requires:       python3-netaddr >= 0.7.18
Requires:       python3-neutronclient >= 6.7.0
Requires:       python3-oslo-config >= 2:5.2.0
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-log >= 3.36.0
Requires:       python3-oslo-messaging >= 5.29.0
Requires:       python3-oslo-serialization >= 2.18.0
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-six >= 1.10.0
Requires:       python3-sqlalchemy >= 1.2.0
Requires:       python3-stevedore >= 1.20.0
Requires:       python3-neutron
Requires:       python3-neutron-lib >= 1.18.0

%description -n python3-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:        Documentation for networking-sfc

BuildRequires:  python3-openstackdocstheme
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinxcontrib-rsvgconverter

%description -n python-%{pypi_name}-doc
%{common_desc}

This package contains documentation.
%endif

%package -n python3-%{pypi_name}-tests
Summary:        Tests for networking-sfc
Requires:       python3-%{pypi_name} = %{version}-%{release}
Requires:       python3-mock
Requires:       python3-oslotest
Requires:       python3-stestr
Requires:       python3-testresources
Requires:       python3-testscenarios
BuildRequires:  python3-neutron-lib-tests
BuildRequires:  python3-neutron-tests
BuildRequires:  python3-requests-mock

%description -n python3-%{pypi_name}-tests
Networking-sfc set of tests

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Let RPM handle the dependencies
%py_req_cleanup

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# FIXME(bcafarel): require neutronclient.tests.unit (python-neutronclient-tests package was dropped)
rm -rf %{module}/tests/unit/cli

%build
%py3_build

%if 0%{?with_doc}
sphinx-build-3 -W -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

# generate the configuration file
PYTHONPATH=. oslo-config-generator-3 --config-file etc/oslo-config-generator/networking-sfc.conf

%install
%py3_install

# The generated config files are not moved automatically by setup.py
mkdir -p %{buildroot}%{_sysconfdir}/neutron/conf.d/neutron-server
mv etc/networking-sfc.conf.sample %{buildroot}%{_sysconfdir}/neutron/conf.d/neutron-server/networking-sfc.conf

%check
export PATH=$PATH:$RPM_BUILD_ROOT/usr/bin
PYTHON=python3 stestr-3 run

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-*.egg-info
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/conf.d/neutron-server/networking-sfc.conf
%exclude %{python3_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%doc doc/build/html/*
%license LICENSE
%endif

%files -n python3-%{pypi_name}-tests
%{python3_sitelib}/%{module}/tests
%exclude %{python3_sitelib}/%{module}/tests/contrib

%changelog
