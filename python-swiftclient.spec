%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname swiftclient

%if 0%{?fedora}
%global with_python3 1
%endif

Name:       python-swiftclient
Version:    XXX
Release:    XXX
Summary:    Client Library for OpenStack Object Storage API
License:    ASL 2.0
URL:        http://launchpad.net/python-swiftclient/
Source0:    http://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz

BuildArch:  noarch

%description
Client library and command line utility for interacting with Openstack
Object Storage API.

%package -n python2-%{sname}
Summary:    Client Library for OpenStack Object Storage API
%{?python_provide:%python_provide python2-swiftclient}

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr

Requires:      python-futures
Requires:      python-requests
Requires:      python-six
Requires:      python-keystoneclient

%description -n python2-%{sname}
Client library and command line utility for interacting with Openstack
Object Storage API.

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
Client library and command line utility for interacting with Openstack
Object Storage API.
%endif

%package doc
Summary:    Documentation for OpenStack Object Storage API Client
Group:      Documentation

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx
BuildRequires: python-futures

%description doc
Documentation for the client library for interacting with Openstack
Object Storage API.

%prep
%setup -q -n %{name}-%{upstream_version}

# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

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


export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html
sphinx-build -b man doc/source man

install -p -D -m 644 doc/manpages/swift.1 %{buildroot}%{_mandir}/man1/swift.1

%files -n python2-%{sname}
%doc README.rst
%license LICENSE
%{python2_sitelib}/swiftclient
%{python2_sitelib}/*.egg-info
%{_bindir}/swift
%{_bindir}/swift-2
%{_bindir}/swift-%{python2_version}
%{_mandir}/man1/swift.1.gz

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
%doc html
%license LICENSE

%changelog
