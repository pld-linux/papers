# TODO: use gtk4-update-icon-cache
#
# Conditional build:
%bcond_without	apidocs		# gi-docgen based API documentation
%bcond_without	nautilus	# Nautilus extension

Summary:	Document viewer for multiple document formats
Summary(pl.UTF-8):	Przeglądarka dokumentów w wielu formatach
Name:		papers
Version:	46.0
Release:	1
License:	GPL v2+
Group:		X11/Applications/Graphics
Source0:	https://download.gnome.org/sources/papers/46/%{name}-%{version}.tar.xz
# Source0-md5:	d7feddef42e506ae26a64db71b2d10c2
URL:		https://gitlab.gnome.org/GNOME/papers
BuildRequires:	appstream-glib
BuildRequires:	cairo-devel >= 1.14.0
BuildRequires:	cargo
BuildRequires:	dbus-devel
BuildRequires:	djvulibre-devel >= 3.5.22
BuildRequires:	exempi-devel >= 2.0
BuildRequires:	gdk-pixbuf2-devel >= 2.40.0
%{?with_apidocs:BuildRequires:	gi-docgen >= 2021.1}
BuildRequires:	glib2-devel >= 1:2.75.0
BuildRequires:	gobject-introspection-devel >= 1.0
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	gtk4-devel >= 4.13.8
BuildRequires:	libadwaita-devel >= 1.5.0
BuildRequires:	libarchive-devel >= 3.6.0
BuildRequires:	libgxps-devel >= 0.2.1
BuildRequires:	libsecret-devel >= 0.5
BuildRequires:	libspectre-devel >= 0.2.0
BuildRequires:	libtiff-devel >= 4.0
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	meson >= 0.59
%{?with_nautilus:BuildRequires:	nautilus-devel >= 43}
BuildRequires:	ninja >= 1.5
#BuildRequires:	pango-devel >= 1:1.52.0
BuildRequires:	poppler-glib-devel >= 22.05.0
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.029
BuildRequires:	rust >= 1.70
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib2 >= 1:2.75.0
Requires(post,postun):	gtk-update-icon-cache
Requires:	cairo >= 1.14.0
Requires:	hicolor-icon-theme
Requires:	libarchive >= 3.6.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debugsource packages don't support rust (or require adding some flags to rust/cargo)
%define		_debugsource_packages	0

%description
Papers is a document viewer for multiple document formats like pdf,
postscript, and many others.

%description -l pl.UTF-8
Papers jest przeglądarką dokumentów w wielu formatach takich jak pdf,
postscript i wielu innych.

%package libs
Summary:	Papers shared libraries
Summary(pl.UTF-8):	Biblioteki współdzielone Papers
Group:		X11/Libraries
Requires:	gdk-pixbuf2 >= 2.40.0
Requires:	glib2 >= 1:2.75.0
Requires:	gtk4 >= 4.13.8
Requires:	libadwaita >= 1.5.0

%description libs
Papers shared libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone Papers.

%package devel
Summary:	Header files for Papers
Summary(pl.UTF-8):	Pliki nagłówkowe Papers
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.75.0
Requires:	gtk4-devel >= 4.13.8

%description devel
Header files for Papers.

%description devel -l pl.UTF-8
Pliki nagłówkowe Papers.

%package apidocs
Summary:	Papers API documentation
Summary(pl.UTF-8):	Dokumentacja API aplikacji Papers
Group:		Documentation
BuildArch:	noarch

%description apidocs
Evince API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API aplikacji Evince.

%package backend-djvu
Summary:	View DjVu documents with Papers
Summary(pl.UTF-8):	Przeglądanie dokumentów DjVu przy użyciu Papers
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	djvulibre >= 3.5.22

%description backend-djvu
View DjVu documents with Papers.

%description backend-djvu -l pl.UTF-8
Przeglądanie dokumentów DjVu przy użyciu Papers.

%package backend-pdf
Summary:	View PDF documents with Papers
Summary(pl.UTF-8):	Przeglądanie dokumentów PDF przy użyciu Papers
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	cairo >= 1.14.0
Requires:	libxml2 >= 1:2.6.31
Requires:	poppler-glib >= 22.05.0

%description backend-pdf
View PDF documents with Papers.

%description backend-pdf -l pl.UTF-8
Przeglądanie dokumentów PDF przy użyciu Papers.

%package backend-ps
Summary:	View PostScript documents with Papers
Summary(pl.UTF-8):	Przeglądanie dokumentów PostScript przy użyciu Papers
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	libspectre >= 0.2.0

%description backend-ps
View PostScript documents with Papers.

%description backend-ps -l pl.UTF-8
Przeglądanie dokumentów PostScript przy użyciu Papers.

%package backend-xps
Summary:	View XPS documents with Papers
Summary(pl.UTF-8):	Przeglądanie dokumentów XPS przy użyciu Papers
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	libgxps >= 0.2.1

%description backend-xps
View XPS documents with Papers.

%description backend-xps -l pl.UTF-8
Przeglądanie dokumentów XPS przy użyciu Papers.

%package -n nautilus-extension-papers
Summary:	Papers extension for Nautilus
Summary(pl.UTF-8):	Rozszerzenie Papers dla Nautilusa
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	nautilus >= 43
Obsoletes:	nautilus-extension-papers < 43

%description -n nautilus-extension-papers
This extension shows Papers document properties in Nautilus.

%description -n nautilus-extension-papers -l pl.UTF-8
To rozszerzenie pokazuje właściwości dokumentu Papers w Nautilusie.

%prep
%setup -q -n %{name}-%{version}

%build
%meson build \
	%{!?with_apidocs:-Dgtk_doc=false} \
	%{!?with_nautilus:-Dnautilus=false} \
	-Dps=enabled

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/libpps* $RPM_BUILD_ROOT%{_gidocdir}
%endif

# not supported by glibc (as of 2.39)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang papers --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor
%glib_compile_schemas

%postun
%update_desktop_database
%update_icon_cache hicolor
%glib_compile_schemas

%files -f papers.lang
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_bindir}/papers
%attr(755,root,root) %{_bindir}/papers-previewer
%attr(755,root,root) %{_bindir}/papers-thumbnailer
%dir %{_libdir}/papers
%dir %{_libdir}/papers/5
%dir %{_libdir}/papers/5/backends
%attr(755,root,root) %{_libdir}/papers/5/backends/libcomicsdocument.so
%{_libdir}/papers/5/backends/comicsdocument.papers-backend
%attr(755,root,root) %{_libdir}/papers/5/backends/libtiffdocument.so
%{_libdir}/papers/5/backends/tiffdocument.papers-backend
%{_datadir}/glib-2.0/schemas/org.gnome.Papers.gschema.xml
%{_datadir}/metainfo/org.gnome.Papers.metainfo.xml
%{_datadir}/metainfo/papers-comicsdocument.metainfo.xml
%{_datadir}/metainfo/papers-tiffdocument.metainfo.xml
%{_datadir}/thumbnailers/papers.thumbnailer
%{_desktopdir}/org.gnome.Papers.desktop
%{_desktopdir}/org.gnome.Papers-previewer.desktop
%{_iconsdir}/hicolor/scalable/apps/org.gnome.Papers.svg
%{_iconsdir}/hicolor/symbolic/apps/org.gnome.Papers-symbolic.svg
%{_mandir}/man1/papers.1*
%{_mandir}/man1/papers-previewer.1*
%{_mandir}/man1/papers-thumbnailer.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libppsdocument-4.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libppsdocument-4.0.so.5
%attr(755,root,root) %{_libdir}/libppsshell-4.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libppsshell-4.0.so.4
%attr(755,root,root) %{_libdir}/libppsview-4.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libppsview-4.0.so.4
%{_libdir}/girepository-1.0/PapersDocument-4.0.typelib
%{_libdir}/girepository-1.0/PapersView-4.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libppsdocument-4.0.so
%attr(755,root,root) %{_libdir}/libppsshell-4.0.so
%attr(755,root,root) %{_libdir}/libppsview-4.0.so
%{_includedir}/papers
%{_datadir}/gir-1.0/PapersDocument-4.0.gir
%{_datadir}/gir-1.0/PapersView-4.0.gir
%{_pkgconfigdir}/papers-document-4.0.pc
%{_pkgconfigdir}/papers-view-4.0.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/libppsdocument
%{_gidocdir}/libppsview
%endif

%files backend-djvu
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/papers/5/backends/libdjvudocument.so
%{_libdir}/papers/5/backends/djvudocument.papers-backend
%{_datadir}/metainfo/papers-djvudocument.metainfo.xml

%files backend-pdf
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/papers/5/backends/libpdfdocument.so
%{_libdir}/papers/5/backends/pdfdocument.papers-backend
%{_datadir}/metainfo/papers-pdfdocument.metainfo.xml

%files backend-ps
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/papers/5/backends/libpsdocument.so
%{_libdir}/papers/5/backends/psdocument.papers-backend
%{_datadir}/metainfo/papers-psdocument.metainfo.xml

%files backend-xps
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/papers/5/backends/libxpsdocument.so
%{_libdir}/papers/5/backends/xpsdocument.papers-backend
%{_datadir}/metainfo/papers-xpsdocument.metainfo.xml

%if %{with nautilus}
%files -n nautilus-extension-papers
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nautilus/extensions-4/libpapers-document-properties.so
%endif
