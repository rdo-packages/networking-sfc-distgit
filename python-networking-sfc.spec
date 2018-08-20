%global milestone .0rc1
%global pypi_name networking-sfc
%global module networking_sfc
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

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
Version:        7.0.0
Release:        0.1%{?milestone}%{?dist}
Summary:        API and implementations to support Service Function Chaining in Neutron

License:        ASL 2.0
URL:            https://launchpad.net/%{pypi_name}
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

#
# patches_base=7.0.0.0rc1
#

BuildArch:      noarch

BuildRequires:  openstack-macros
BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python2-openstackdocstheme
BuildRequires:  python2-sphinx
# Test requirements
BuildRequires:  python2-mock
BuildRequires:  python-requests-mock
BuildRequires:  python2-oslotest
BuildRequires:  python2-stestr
BuildRequires:  python2-testresources
BuildRequires:  python2-testscenarios
BuildRequires:  python-neutron-lib-tests
BuildRequires:  python-neutron-tests
BuildRequires:  openstack-neutron

%description
%{common_desc}

%package -n python2-%{pypi_name}
Summary:        API and implementations to support Service Function Chaining in Neutron
%{?python_provide:%python_provide python2-%{pypi_name}}

Requires:       python2-pbr >= 2.0.0
Requires:       openstack-neutron-common
Requires:       openstack-neutron
Requires:       python2-alembic
Requires:       python2-eventlet
Requires:       python2-netaddr
Requires:       python-neutron
Requires:       python-neutron-lib >= 1.18.0
Requires:       python2-neutronclient >= 6.7.0
Requires:       python2-oslo-config >= 2:5.2.0
Requires:       python2-oslo-i18n >= 3.15.3
Requires:       python2-oslo-log >= 3.36.0
Requires:       python2-oslo-messaging >= 5.29.0
Requires:       python2-oslo-serialization >= 2.18.0
Requires:       python2-oslo-utils >= 3.33.0
Requires:       python2-six
Requires:       python2-sqlalchemy
Requires:       python2-stevedore >= 1.20.0

%description -n python2-%{pypi_name}
%{common_desc}

%package -n python-%{pypi_name}-doc
Summary:        Documentation for networking-sfc
%description -n python-%{pypi_name}-doc
Documentation for networking-sfc

%package -n python2-%{pypi_name}-tests
Summary:        Tests for networking-sfc
Requires:       python2-%{pypi_name} = %{version}-%{release}
Requires:       python2-mock
Requires:       python-requests-mock
Requires:       python2-oslotest
Requires:       python2-stestr
Requires:       python2-testresources
Requires:       python2-testscenarios
Requires:       python-neutron-lib-tests
Requires:       python-neutron-tests

%description -n python2-%{pypi_name}-tests
Networking-sfc set of tests

%package -n python2-%{pypi_name}-tests-tempest
Summary:    Tempest plugin for %{name}

Requires:       python2-%{pypi_name} = %{version}-%{release}
Requires:       python2-tempest

%description -n python2-%{pypi_name}-tests-tempest
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
%py2_build
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
# generate the configuration file
PYTHONPATH=. oslo-config-generator --config-file etc/oslo-config-generator/networking-sfc.conf


%install
%py2_install

# Create a fake tempest plugin entrypoint
%py2_entrypoint %{module} %{pypi_name}

# The generated config files are not moved automatically by setup.py
mkdir -p %{buildroot}%{_sysconfdir}/neutron/conf.d/neutron-server
mv etc/networking-sfc.conf.sample %{buildroot}%{_sysconfdir}/neutron/conf.d/neutron-server/networking-sfc.conf

%check
export OS_TEST_PATH='./networking_sfc/tests/functional'
export PATH=$PATH:$RPM_BUILD_ROOT/usr/bin
stestr run

%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{module}
%{python2_sitelib}/%{module}-*.egg-info
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/conf.d/neutron-server/networking-sfc.conf
%exclude %{python2_sitelib}/%{module}/tests

%files -n python-%{pypi_name}-doc
%doc doc/build/html/*
%license LICENSE

%files -n python2-%{pypi_name}-tests
%{python2_sitelib}/%{module}/tests
%exclude %{python2_sitelib}/%{module}/tests/contrib
%exclude %{python2_sitelib}/%{module}/tests/tempest_plugin

%files -n python2-%{pypi_name}-tests-tempest
%{python2_sitelib}/%{module}_tests.egg-info
%{python2_sitelib}/%{module}/tests/tempest_plugin
%{python2_sitelib}/%{module}/tests/__init__.py*

%changelog
* Mon Aug 20 2018 RDO <dev@lists.rdoproject.org> 7.0.0-0.1.0rc1
- Update to 7.0.0.0rc1

