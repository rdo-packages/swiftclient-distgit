%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

BuildRequires: git-core

%description
%{common_desc}

%package -n python3-%{sname}
Summary:    Client Library for OpenStack Object Storage API
%{?python_provide:%python_provide python3-swiftclient}
Obsoletes: python2-%{sname} < %{version}-%{release}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr
BuildRequires: openstack-macros

Requires:      python3-requests
# Upstream specify as extra requirement for auth version 2 or 3
Requires:      python3-keystoneclient

%description -n python3-%{sname}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:    Documentation for OpenStack Object Storage API Client
Group:      Documentation

BuildRequires: python3-sphinx
BuildRequires: python3-openstackdocstheme
BuildRequires: python3-keystoneauth1

%description doc
Documentation for the client library for interacting with Openstack
Object Storage API.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{name}-%{upstream_version} -S git

# Let RPM handle the dependencies
%py_req_cleanup

%build
%{py3_build}

%install
%{py3_install}
# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s swift %{buildroot}%{_bindir}/swift-3

# Delete tests
rm -fr %{buildroot}%{python3_sitelib}/swiftclient/tests

%if 0%{?with_doc}
sphinx-build -W -b html doc/source doc/build/html
rm -rf doc/build/html/.{doctrees,buildinfo}

sphinx-build -W -b man doc/source doc/build/man
install -p -D -m 644 doc/build/man/*.1 %{buildroot}%{_mandir}/man1/
%endif

%files -n python3-%{sname}
%doc README.rst
%license LICENSE
%{python3_sitelib}/swiftclient
%{python3_sitelib}/*.egg-info
%{_bindir}/swift
%{_bindir}/swift-3
%{_mandir}/man1/*

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%license LICENSE
%endif
%changelog
