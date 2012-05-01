%define tarball xf86-video-xgi
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

%define cvsdate xxxxxxx

Summary:   Xorg X11 xgi video driver
Name:      xorg-x11-drv-xgi
Version:   1.6.0
Release:   11%{?dist}
URL:       http://www.x.org
License:   MIT
Group:     User Interface/X Hardware Support

Source0:   ftp://ftp.x.org/pub/individual/driver/%{tarball}-%{version}.tar.bz2
Source1:   xgi.xinf

Patch1: xgi-1.6.0-ulong.patch
Patch2: xgi-1.6.0-big-endian.patch
Patch3: xgi-fix.patch
Patch4: xgi-1.6.0-module-data.patch
Patch5: xgi-1.6.0-symlists.patch
Patch6: xgi-1.6.0-xorg-version-current.patch
Patch7: xgi-z9s-fix-dpms.patch

ExcludeArch: s390 s390x

BuildRequires: pkgconfig
BuildRequires: xorg-x11-server-sdk >= 1.1.0-2
BuildRequires: mesa-libGL-devel >= 6.4-4
BuildRequires: libdrm-devel >= 2.0-1

Requires:  Xorg %(xserver-sdk-abi-requires ansic)
Requires:  Xorg %(xserver-sdk-abi-requires videodrv)

%description 
X.Org X11 xgi video driver.

%prep
%setup -q -n %{tarball}-%{version}
%patch1 -p1 -b .ulong
%patch2 -p1 -b .endian
%patch3 -p1 -b .makefile
%patch4 -p1 -b .module-data
%patch5 -p1 -b .symlists
%patch6 -p1 -b .xvc
%patch7 -p1 -b .dpms

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/hwdata/videoaliases
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/hwdata/videoaliases/

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir %{moduledir}
%dir %{driverdir}
%{driverdir}/xgi_drv.so
%{_datadir}/hwdata/videoaliases/xgi.xinf
#%dir %{_mandir}/man4x
%{_mandir}/man4/xgi.4*

%changelog
* Tue Sep 13 2011 Adam Jackson <ajax@redhat.com> 1.6.0-11
- spec fix (#708157)

* Fri Aug 05 2011 Adam Jackson <ajax@redhat.com> 1.6.0-10
- xgi-z9s-fix-dpms.patch: Fix DPMS-on on XG21 chips, including Z9s and
  Z9m (#704094)

* Tue Jun 28 2011 Ben Skeggs <bskeggs@redhat.com> - 1.6.0-8
- rebuild for 6.2 server rebase

* Tue Apr 26 2011 Adam Jackson <ajax@redhat.com> 1.6.0-7
- xgi-1.6.0-xorg-version-current.patch: Yet more yet more API skew. (#631738)

* Mon Apr 25 2011 Adam Jackson <ajax@redhat.com> 1.6.0-6
- xgi-1.6.0-symlists.patch: Yet more API skew. (#631738)

* Tue Apr 05 2011 Adam Jackson <ajax@redhat.com>
- xgi-1.6.0-module-data.patch: Export loader hook. (#693652)

* Mon Mar 28 2011 Adam Jackson <ajax@redhat.com> 1.6.0-4
- s@MIT/X11@MIT@ in License tag.

* Thu Mar 17 2011 Adam Jackson <ajax@redhat.com> 1.6.0-3
- Initial RHEL build. (#631738)
