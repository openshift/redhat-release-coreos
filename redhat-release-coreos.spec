# This package was forked from fedora-release into redhat-release-server into
# redhat-release-atomic-host, then into redhat-release-coreos.
# Be sure to look at changes upstream!

%define debug_package %{nil}
%define product_family Red Hat
%define variant_titlecase CoreOS
%define variant_titlecase_concat CoreOS
%define variant_lowercase coreos
%define release_pkg_version 20180515.0
%define base_release_version 3
%define full_release_version 3.10
%define dist_release_version 3
# Fake this out; we need at least 7, since e.g. systemd has a dependency
# on system-release > 7.2, etc.
%define os_version 7.99
#define beta %{nil}
%define dist .el%{dist_release_version}

Name:           redhat-release%{?variant_lowercase:-%{variant_lowercase}}
Version:        %{full_release_version}
Release:        %{release_pkg_version}.atomic%{?dist}.0
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
%{product_family}%{?variant_titlecase: %{variant_titlecase}} release files

%prep
%setup -q -n redhat-release-%{base_release_version}

%build
echo OK

%install
rm -rf %{buildroot}

# create /etc
mkdir -p %{buildroot}/etc
mkdir -p %{buildroot}/usr/lib/

mkdir -p %{buildroot}/etc/pki/product

# create /etc/system-release and /etc/redhat-release
echo "%{product_family}%{?variant_titlecase: %{variant_titlecase}} release %{full_release_version}%{?beta: %{beta}}" > %{buildroot}/usr/lib/redhat-release
ln -s ../usr/lib/redhat-release %{buildroot}/etc/system-release
ln -s ../usr/lib/redhat-release %{buildroot}/etc/redhat-release

# create /etc/os-release
cat << EOF >>%{buildroot}/usr/lib/os-release
NAME="%{product_family}%{?variant_titlecase: %{variant_titlecase}}"
VERSION="%{full_release_version}"
ID="coreos"
ID_LIKE="rhel fedora"
VARIANT="CoreOS"
VARIANT_ID=coreos
VERSION_ID="%{full_release_version}"
PRETTY_NAME="%{product_family}%{?variant_titlecase: %{variant_titlecase}} %{full_release_version}"
ANSI_COLOR="0;31"
CPE_NAME="cpe:/o:redhat:enterprise_linux:%{full_release_version}:%{?beta:beta}%{!?beta:GA}%{?variant_lowercase::%{variant_lowercase}}"
HOME_URL="https://www.redhat.com/"
BUG_REPORT_URL="https://bugzilla.redhat.com/"

REDHAT_BUGZILLA_PRODUCT="%{product_family} %{base_release_version}"
REDHAT_BUGZILLA_PRODUCT_VERSION="%{full_release_version}"
REDHAT_SUPPORT_PRODUCT="%{product_family}"
REDHAT_SUPPORT_PRODUCT_VERSION="%{full_release_version}"
EOF
ln -s ../usr/lib/os-release %{buildroot}/etc/os-release
# write cpe to /etc/system/release-cpe
echo "cpe:/o:redhat:enterprise_linux:%{full_release_version}:%{?beta:beta}%{!?beta:GA}%{?variant_lowercase::%{variant_lowercase}}" | tr [A-Z] [a-z] > %{buildroot}/usr/lib/system-release-cpe
ln -s ../usr/lib/system-release-cpe %{buildroot}/etc/system-release-cpe

# create /etc/issue and /etc/issue.net
echo '\S' > %{buildroot}/etc/issue
echo 'Kernel \r on an \m' >> %{buildroot}/etc/issue
cp %{buildroot}/etc/issue %{buildroot}/etc/issue.net
echo >> %{buildroot}/etc/issue

# combine GPG keys
cat RPM-GPG-KEY-redhat-release-2 RPM-GPG-KEY-redhat-auxiliary > RPM-GPG-KEY-redhat-release
rm RPM-GPG-KEY-redhat-release-2 RPM-GPG-KEY-redhat-auxiliary
cat RPM-GPG-KEY-redhat-beta-2 RPM-GPG-KEY-redhat-legacy-beta > RPM-GPG-KEY-redhat-beta
rm RPM-GPG-KEY-redhat-beta-2 RPM-GPG-KEY-redhat-legacy-beta

# copy GPG keys
mkdir -p -m 755 %{buildroot}/etc/pki/rpm-gpg
mkdir -p -m 755 %{buildroot}/%{_datadir}/ostree/trusted.gpg.d
for file in RPM-GPG-KEY* ; do
    install -m 644 $file %{buildroot}/etc/pki/rpm-gpg
    gpg --dearmor < $file > %{buildroot}/%{_datadir}/ostree/trusted.gpg.d/$file.gpg
done

# set up the dist tag macros
install -d -m 755 %{buildroot}/etc/rpm
cat >> %{buildroot}/etc/rpm/macros.dist << EOF
# dist macros.

%%rhel %{base_release_version}
%%dist %dist
%%el%{base_release_version} 1
EOF

# use unbranded datadir
mkdir -p -m 755 %{buildroot}/%{_datadir}/redhat-release
install -m 644 EULA %{buildroot}/%{_datadir}/redhat-release

# use unbranded docdir
mkdir -p -m 755 %{buildroot}/%{_docdir}/redhat-release
install -m 644 GPL %{buildroot}/%{_docdir}/redhat-release

# copy systemd presets
mkdir -p %{buildroot}/%{_prefix}/lib/systemd/system-preset/
for x in *.preset; do install -m 0644 ${x} %{buildroot}/%{_prefix}/lib/systemd/system-preset/; done

# let systemd handle core dumps
# https://bugzilla.redhat.com/show_bug.cgi?id=1191045
mkdir -p %{buildroot}%{_prefix}/lib/sysctl.d/
install -m 0644 49-coredump.conf %{buildroot}%{_prefix}/lib/sysctl.d/

# https://bugzilla.redhat.com/show_bug.cgi?id=1204194
mkdir -p %{buildroot}/etc/systemd/system
ln -s /dev/null %{buildroot}/etc/systemd/system/brandbot.path

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
/etc/redhat-release
/etc/system-release
%{_prefix}/lib/os-release
%{_prefix}/lib/redhat-release
%{_prefix}/lib/system-release-cpe
%config /etc/os-release
%config /etc/system-release-cpe
%config(noreplace) /etc/issue
%config(noreplace) /etc/issue.net
%config(noreplace) /etc/systemd/system/brandbot.path
/etc/pki/rpm-gpg/
%{_datadir}/ostree/trusted.gpg.d/*.gpg
/etc/rpm/macros.dist
%{_docdir}/redhat-release/*
%{_datadir}/redhat-release/*
%{_prefix}/lib/systemd/system-preset/*
%{_prefix}/lib/sysctl.d/*
