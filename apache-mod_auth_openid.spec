#Module-Specific definitions
%define mod_name mod_auth_openid
%define mod_conf A88_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	An OpenID authentication module for Apache 2
Name:		apache-%{mod_name}
Version:	0.5
Release:	%mkrel 3
Group:		System/Servers
License:	MIT
URL:		http://trac.butterfat.net/public/mod_auth_openid
Source0:	%{mod_name}-%{version}.tar.gz
Source1:	%{mod_conf}
Patch0:		mod_auth_openid-dbdir.diff
Patch1:		mod_auth_openid-0.4-fix-linkage.patch
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	apache-mpm-prefork >= 2.2.0
BuildRequires:	pkgconfig
BuildRequires:	autoconf2.5
BuildRequires:	automake1.8
BuildRequires:	libtool
BuildRequires:	konforka-devel >= 0.0.1
BuildRequires:	opkele-devel >= 2.0
BuildRequires:	sqlite3-devel >= 3.3.0
BuildRequires:	curl-devel
BuildRequires:	pcre-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_auth_openid is an authentication module for the Apache 2 Web server. It
handles the functions of an OpenID consumer as specified in the OpenID 1.1
specification. Once installed, a simple configuration directive can secure a
directory or application on your Web server and require a valid OpenID
identity. You can configure trusted/untrusted identity providers along with a
number of other options.

%prep
%setup -q -n %{mod_name}-%{version}
%patch0 -p0
%patch1 -p0 -b .linkage

cp %{SOURCE1} %{mod_conf}

%build
%serverbuild
autoreconf -fi
%configure2_5x --disable-static \
    --localstatedir=/var/lib \
    --with-apxs=%{_sbindir}/apxs \
    --with-apr-config=%{_bindir}/apr-1-config \
    --with-sqlite3=%{_prefix} \
    --with-pcre=%{_prefix}

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}/var/lib/%{mod_name}

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}
install -m0755 db_info %{buildroot}%{_sbindir}/%{mod_name}-db_info

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
 %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
 if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
 fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%attr(0755,root,root) %{_sbindir}/%{mod_name}-db_info
%attr(0755,apache,apache) %dir /var/lib/%{mod_name}
