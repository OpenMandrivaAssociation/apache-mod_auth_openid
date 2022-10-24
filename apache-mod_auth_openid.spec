#Module-Specific definitions
%define mod_name mod_auth_openid
%define mod_conf A88_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	An OpenID authentication module for Apache 2
Name:		apache-%{mod_name}
Version:	0.8
Release:	1
Group:		System/Servers
License:	MIT
URL:		http://findingscience.com/mod_auth_openid/
Source0:	https://github.com/bmuller/mod_auth_openid/releases/download/v%{version}/mod_auth_openid-%{version}.tar.gz
Source1:	%{mod_conf}
Patch0:		mod_auth_openid-dbdir.diff
Patch1:		mod_auth_openid-fix-linkage.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	apache-mpm-event >= 2.2.0
BuildRequires:	pkgconfig
BuildRequires:	autoconf automake libtool
BuildRequires:	konforka-devel >= 0.0.1
BuildRequires:	opkele-devel >= 2.0
BuildRequires:	sqlite3-devel >= 3.3.0
BuildRequires:	curl-devel
BuildRequires:	pcre-devel

%description
mod_auth_openid is an authentication module for the Apache 2 Web server. It
handles the functions of an OpenID consumer as specified in the OpenID 1.1
specification. Once installed, a simple configuration directive can secure a
directory or application on your Web server and require a valid OpenID
identity. You can configure trusted/untrusted identity providers along with a
number of other options.

%prep
%autosetup -p0 -n %{mod_name}-%{version}
sed -e 's,@LIBDIR@,%{_libdir},g' %{SOURCE1} >%{mod_conf}

%build
%serverbuild
autoreconf -fi
%configure --disable-static \
    --localstatedir=/var/lib \
    --with-apxs=%{_bindir}/apxs \
    --with-apr-config=%{_bindir}/apr-1-config \
    --with-sqlite3=%{_prefix} \
    --with-pcre=%{_prefix}

%make SQLITE3_LDFLAGS='-lsqlite3'

%install
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}/var/lib/%{mod_name}

install -m0755 src/.libs/*.so %{buildroot}%{_libdir}/apache/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}
install -m0755 src/db_info %{buildroot}%{_sbindir}/%{mod_name}-db_info

%files
%doc AUTHORS COPYING ChangeLog NEWS README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache/%{mod_so}
%attr(0755,root,root) %{_sbindir}/%{mod_name}-db_info
%attr(0755,apache,apache) %dir /var/lib/%{mod_name}
