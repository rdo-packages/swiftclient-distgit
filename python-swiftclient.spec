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
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global with_doc 1

%global sname swiftclient

%global common_desc \
Client library and command line utility for interacting with Openstack \
Object Storage API.

Name:       python-swiftclient
Version:    XXX
Release:    XXX
Summary:    Client Library for OpenStack Object Storage API
License:    ASL 2.0
URL:        http://launchpad.net/python-swiftclient/
Source0:    https://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz

BuildArch:  noarch

%description
%{common_desc}

%package -n python%{pyver}-%{sname}
Summary:    Client Library for OpenStack Object Storage API
%{?python_provide:%python_provide python%{pyver}-swiftclient}
%if %{pyver} == 3
Obsoletes: python2-%{sname} < %{version}-%{release}
%endif

BuildRequires: python%{pyver}-devel
BuildRequires: python%{pyver}-setuptools
BuildRequires: python%{pyver}-pbr
BuildRequires: openstack-macros

Requires:      python%{pyver}-requests
Requires:      python%{pyver}-six
Requires:      python%{pyver}-keystoneclient
# Handle python2 exception
%if %{pyver} == 2
Requires:      python%{pyver}-futures
%endif

%description -n python%{pyver}-%{sname}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:    Documentation for OpenStack Object Storage API Client
Group:      Documentation

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-openstackdocstheme
# Handle python2 exception
%if %{pyver} == 2
BuildRequires: python%{pyver}-futures
%endif

%description doc
Documentation for the client library for interacting with Openstack
Object Storage API.
%endif

%prep
%setup -q -n %{name}-%{upstream_version}

# Let RPM handle the dependencies
%py_req_cleanup

%build
%{pyver_build}

%install
%{pyver_install}
# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s swift %{buildroot}%{_bindir}/swift-%{pyver}

# Delete tests
rm -fr %{buildroot}%{pyver_sitelib}/swiftclient/tests

%if 0%{?with_doc}
%{pyver_bin} setup.py build_sphinx -b html
rm -rf doc/build/html/.{doctrees,buildinfo}

%{pyver_bin} setup.py build_sphinx -b man
install -p -D -m 644 doc/build/man/*.1 %{buildroot}%{_mandir}/man1/
%endif

%files -n python%{pyver}-%{sname}
%doc README.rst
%license LICENSE
%{pyver_sitelib}/swiftclient
%{pyver_sitelib}/*.egg-info
%{_bindir}/swift
%{_bindir}/swift-%{pyver}
%{_mandir}/man1/*

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%license LICENSE
%endif
%changelog
