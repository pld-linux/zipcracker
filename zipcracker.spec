%define zlib_v	1.1.3
Summary:	program that helps users recover their files from password protected zip archives
Summary(pl):	program pozwalaj�cy na odzyskiwanie plik�w z archiw�w zip zabezpieczonych has�em
Name:		zipcracker
Version:	0.1.1
Release:	3
License:	GPL
Group:		Applications/Archiving
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	53eff1305484cb1fd08516023e6123fe
# DO NOT USE SYSTEM SHARED ZLIB --misiek
Source1:	http://www.gzip.org/zlib/zlib-%{zlib_v}.tar.gz
# Source1-md5:	ada18615d2a66dee4d6f5ff916ecd4c6
Patch0:		%{name}-gettext.patch
Patch1:		%{name}-zlib.patch
Patch2:		http://zipcracker.sourceforge.net/zlib-%{zlib_v}.patch.gz
URL:		http://zipcracker.sourceforge.net/
BuildRequires:	ORBit-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gnome-libs-devel >= 1.0.0
BuildRequires:	gtk+-devel >= 1.2.0
BuildRequires:	libtool
BuildRequires:	pvm-devel >= 3.4.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/X11/GNOME

%description
ZipCracker is a program that helps users recover their files from
password protected zip archives, when the user has forgotten the
password. ZipCracker uses brute force to find the password.

%description -l pl
ZipCracker to program pozwalaj�cy na odzyskiwanie plik�w z archiw�w
zip zabezpieczonych has�em w przypadkach gdy u�ytkownik zapomnia�
has�a. ZipCracker do znalezienia has�a u�ywa metody brute force.

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1
cd zlib-%{zlib_v}
%patch2 -p0

%build
rm -f missing
%{__libtoolize}
%{__gettextize}
%{__aclocal} -I %{_aclocaldir}/gnome
%{__autoconf}
%{__automake}
ln -s zlib-%{zlib_v} zlib
cd zlib-%{zlib_v}
CFLAGS="-D_REENTRANT -fPIC %{rpmcflags}"
CC="%{__cc}"
export CFLAGS CC
./configure
%{__make} libz.a
cd ..
unset CFLAGS CC
CPPFLAGS="-I$PWD/zlib-%{zlib_v}"
export CPPFLAGS
%configure \
	--with-gnome \
	--with-pvm
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README* TODO
%attr(755,root,root) %{_bindir}/*