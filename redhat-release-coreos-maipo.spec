# This package was forked from fedora-release into redhat-release-server into
# redhat-release-atomic-host, then into redhat-release-coreos.
# Be sure to look at changes upstream!

%define debug_package %{nil}
# Fake this out; we need at least 7, since e.g. systemd has a dependency
# on system-release > 7.2, etc.
%define os_version 7.99
%define dist .el%{version}

Name:           redhat-release-coreos-maipo
Version:        47
Release:        0%{?dist}
Summary:        %{product_family}%{?variant_titlecase: %{variant_titlecase}} release file
Group:          System Environment/Base
License:        GPLv2
Provides:       redhat-release = %{os_version}-%{release}
Provides:       system-release = %{os_version}-%{release}
# We need to use Server, since there's no RPM content set for anything else
Provides:       system-release(releasever) = %{base_release_version}Server
# This doesn't exist today, I committed the data to git
Source0:        redhat-release-%{variant_lowercase}-%{base_release_version}-4.tar.gz

%description
%{summary}

%prep
%setup -q -n redhat-release-%{base_release_version}

%build
make fs-maipo

%install
rm -rf %{buildroot}
cp -a --reflink=auto fs-maipo %{buildroot}

(cd %{buildroot} && find . -maxdepth 1 -type d | sed -e 's,^.,/,') > files.list

%files -f files.list
