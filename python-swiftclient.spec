%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname swiftclient

%if 0%{?fedora}
%global with_python3 1
%endif

%global common_desc \
Client library and command line utility for interacting with Openstack \
Object Storage API.

Name:       python-swiftclient
Version:    3.5.1
Release:    1%{?dist}
Summary:    Client Library for OpenStack Object Storage API
License:    ASL 2.0
URL:        http://launchpad.net/python-swiftclient/
Source0:    https://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz

BuildArch:  noarch

%description
%{common_desc}

%package -n python2-%{sname}
Summary:    Client Library for OpenStack Object Storage API
%{?python_provide:%python_provide python2-swiftclient}

BuildRequires: python2-devel
BuildRequires: python2-setuptools
BuildRequires: python2-pbr

Requires:      python2-requests
Requires:      python2-six
Requires:      python2-keystoneclient
Requires:      python2-futures

%description -n python2-%{sname}
%{common_desc}

%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:    Client Library for OpenStack Object Storage API
%{?python_provide:%python_provide python3-swiftclient}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr

Requires:      python3-requests
Requires:      python3-six
Requires:      python3-keystoneclient

%description -n python3-%{sname}
%{common_desc}
%endif

%package doc
Summary:    Documentation for OpenStack Object Storage API Client
Group:      Documentation

BuildRequires: python2-sphinx
BuildRequires: python2-oslo-sphinx
BuildRequires: openstack-macros
BuildRequires: python2-futures

%description doc
Documentation for the client library for interacting with Openstack
Object Storage API.

%prep
%setup -q -n %{name}-%{upstream_version}

# Let RPM handle the dependencies
%py_req_cleanup

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/swift %{buildroot}%{_bindir}/swift-%{python3_version}
ln -s ./swift-%{python3_version} %{buildroot}%{_bindir}/swift-3
# Delete tests
rm -fr %{buildroot}%{python3_sitelib}/swiftclient/tests
%endif

%py2_install
mv %{buildroot}%{_bindir}/swift %{buildroot}%{_bindir}/swift-%{python2_version}
ln -s ./swift-%{python2_version} %{buildroot}%{_bindir}/swift-2

ln -s ./swift-2 %{buildroot}%{_bindir}/swift

# Delete tests
rm -fr %{buildroot}%{python2_sitelib}/swiftclient/tests

%{__python2} setup.py build_sphinx -b html
rm -rf doc/build/html/.{doctrees,buildinfo}

%{__python2} setup.py build_sphinx -b man
install -p -D -m 644 doc/build/man/*.1 %{buildroot}%{_mandir}/man1/

%files -n python2-%{sname}
%doc README.rst
%license LICENSE
%{python2_sitelib}/swiftclient
%{python2_sitelib}/*.egg-info
%{_bindir}/swift
%{_bindir}/swift-2
%{_bindir}/swift-%{python2_version}
%{_mandir}/man1/*

%if 0%{?with_python3}
%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sname}
%{python3_sitelib}/*.egg-info
%{_bindir}/swift-3
%{_bindir}/swift-%{python3_version}
%endif

%files doc
%doc doc/build/html
%license LICENSE

%changelog
* Mon Oct 28 2019 RDO <dev@lists.rdoproject.org> 3.5.1-1
- Update to 3.5.1

* Sat Feb 10 2018 RDO <dev@lists.rdoproject.org> 3.5.0-1
- Update to 3.5.0

