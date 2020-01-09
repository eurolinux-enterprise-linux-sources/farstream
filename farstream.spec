%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define gst_ver 0.10.33
%define gst_plugins_base_ver 0.10.33

Name:           farstream
Version:        0.1.2
Release:        8%{?dist}
Summary:        Libraries for videoconferencing

License:        LGPLv2+
URL:            http://www.freedesktop.org/wiki/Software/Farstream
Source0:        http://freedesktop.org/software/%{name}/releases/%{name}/%{name}-%{version}.tar.gz
Patch0:         farstream-prefer-vp8.patch
Patch1:         0001-Gtk-doc-tags-belong-after-the-description.patch

BuildRequires:  libnice-devel >= 0.1.0
BuildRequires:  gstreamer-devel >= %{gst_ver}
BuildRequires:  gstreamer-plugins-base-devel >= %{gst_plugins_base_ver}
BuildRequires:  gupnp-igd-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  python-devel
BuildRequires:  gstreamer-python-devel
BuildRequires:  pygobject2-devel

Requires:       gstreamer-plugins-good >= 0.10.29
Requires:       gstreamer-plugins-bad-free >= 0.10.23

## Obsolete farsight2 with Fedora 17.
Provides:       farsight2 = %{version}
Obsoletes:      farsight2 < 0.0.32


%description
%{name} is a collection of GStreamer modules and libraries for
videoconferencing.


%package        python
Summary:        Python binding for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

## Obsolete farsight2 with Fedora 17.
Provides:       farsight2-python = %{version}
Obsoletes:      farsight2-python < 0.0.32


%description    python
Python bindings for %{name}.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-python = %{version}-%{release}
Requires:       gstreamer-devel  >= %{gst_ver}
Requires:       gstreamer-plugins-base-devel >= %{gst_plugins_base_ver}
Requires:       pkgconfig

## Obsolete farsight2 with Fedora 17.
Provides:       farsight2-devel = %{version}
Obsoletes:      farsight2-devel < 0.0.32

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1 -b .vp8
%patch1 -p1


%build
%configure                                                              \
  --with-package-name='Fedora Farstream package'                        \
  --with-package-origin='http://download.fedoraproject.org'             \
  --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc COPYING NEWS AUTHORS
%{_libdir}/*.so.*
%dir %{_libdir}/%{name}-0.1
%{_libdir}/%{name}-0.1/libmulticast-transmitter.so
%{_libdir}/%{name}-0.1/libnice-transmitter.so
%{_libdir}/%{name}-0.1/librawudp-transmitter.so
%{_libdir}/%{name}-0.1/libshm-transmitter.so
%{_libdir}/gstreamer-0.10/libfsfunnel.so
%{_libdir}/gstreamer-0.10/libfsmsnconference.so
%{_libdir}/gstreamer-0.10/libfsrawconference.so
%{_libdir}/gstreamer-0.10/libfsrtcpfilter.so
%{_libdir}/gstreamer-0.10/libfsrtpconference.so
%{_libdir}/gstreamer-0.10/libfsvideoanyrate.so
%{_libdir}/girepository-1.0/Farstream-0.1.typelib
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/0.1
%dir %{_datadir}/%{name}/0.1/fsrtpconference
%dir %{_datadir}/%{name}/0.1/fsrawconference
%{_datadir}/%{name}/0.1/fsrtpconference/default-codec-preferences
%{_datadir}/%{name}/0.1/fsrtpconference/default-element-properties
%{_datadir}/%{name}/0.1/fsrawconference/default-element-properties


%files python
%{python_sitearch}/farstream.so


%files devel
%{_libdir}/libfarstream-0.1.so
%{_libdir}/pkgconfig/%{name}-0.1.pc
%{_includedir}/%{name}-0.1/%{name}/
%{_datadir}/gir-1.0/Farstream-0.1.gir
%{_datadir}/gtk-doc/html/%{name}-libs-0.10/
%{_datadir}/gtk-doc/html/%{name}-plugins-0.1/


%changelog
* Fri Feb 28 2014 Matthias Clasen <mclasen@redhat.com> - 0.1.2-8
- Rebuild
Resolves: #1070804

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.1.2-7
- Mass rebuild 2014-01-24
  Related: #1056145

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.1.2-6
- Mass rebuild 2013-12-27

* Thu Apr 18 2013 Debarshi Ray <rishi@fedoraproject.org> - 0.1.2-5
- Fix build failure due broken annotations.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 24 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.1.2-2
- Add patch to prefer vp8. Thanks, Debarshi.

* Fri Mar 23 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.1.2-1
- Update to 0.1.2.
- Drop patch to ignore config while comparing send codecs. Fixed upstream.

* Thu Mar 22 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.1.1-6
- Build gobject-introspection.

* Tue Mar 13 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.1.1-5
- Add provides/obsoletes for python subpackage.

* Mon Mar  5 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.1.1-4
- Use version macro in provides.

* Sat Mar  3 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.1.1-3
- Backport patch to ignore config while comparing send codecs.

* Tue Feb 28 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.1.1-2
- Appended isa macro to name in devel subpackage.
- Add obsolete/provide to devel subpackage.
- Correct package origin url.

* Sat Feb 25 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.1.1-1
- Initial Fedora spec.

