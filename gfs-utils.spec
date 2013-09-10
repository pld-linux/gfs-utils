# TODO:
# - PLDify init script
# - finish kernel package (doesn't build with recent kernels)
#
# Conditional build:
%bcond_with	kernel	# kernel module package
#
Summary:	Tools to manipulate GFS cluster filesystem
Summary(pl.UTF-8):	Narzędzia do operacji na klastrowym systemie plików GFS
Name:		gfs-utils
Version:	3.0.6
Release:	1
License:	LGPL v2.1+ (libraries), GPL v2+ (applications)
Group:		Applications/System
Source0:	https://fedorahosted.org/releases/c/l/cluster/%{name}-%{version}.tar.gz
# Source0-md5:	83312ec664d00d5eebc554c5b5a95724
URL:		https://fedorahosted.org/cluster/wiki/HomePage
BuildRequires:	perl-base
%if %{with kernel}
BuildRequires:	kernel-module-build >= 3:2.6.31
# which is the last compatible?
BuildRequires:	kernel-module-build < 3:3
%endif
Requires:	uname(release) >= 2.6.31
Obsoletes:	gfs < 1:3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tools to manipulate GFS cluster filesystem.

%description -l pl.UTF-8
Narzędzia do operacji na klastrowym systemie plików GFS.

%prep
%setup -q

%build
./configure \
	--cc="%{__cc}" \
	--cflags="%{rpmcflags}" \
	--ldflags="%{rpmldflags}" \
	--initddir=/etc/rc.d/init.d \
	--disable_kernel_check \
	--enable_pacemaker \
	--kernel_build=%{_kernelsrcdir} \
	--kernel_src=%{_kernelsrcdir} \
	%{!?with_kernel:--without_kernel_modules}
%{__make} \
	REALSUBDIRS="gfs-kernel/src/gfs gfs doc"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	REALSUBDIRS="gfs-kernel/src/gfs gfs doc"

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/cluster

# these belong to cman in cluster3
%{__rm} $RPM_BUILD_ROOT/etc/logrotate.d/cluster
rmdir $RPM_BUILD_ROOT/etc/cluster/cman-notify.d
rmdir $RPM_BUILD_ROOT/etc/cluster
rmdir $RPM_BUILD_ROOT/var/log/cluster
# belongs to ccs in cluster3
rmdir $RPM_BUILD_ROOT/var/run/cluster

# links to gfs2_edit and mount.gfs2
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man8/{gfs_edit,mount.gfs}.8
%{__rm} $RPM_BUILD_ROOT/sbin/mount.gfs
%{__rm} $RPM_BUILD_ROOT%{_sbindir}/gfs_edit

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/{COPYRIGHT,README.licence,usage.txt}
%attr(755,root,root) /sbin/fsck.gfs
%attr(755,root,root) /sbin/mkfs.gfs
%attr(755,root,root) %{_sbindir}/gfs_debug
%attr(755,root,root) %{_sbindir}/gfs_grow
%attr(755,root,root) %{_sbindir}/gfs_jadd
%attr(755,root,root) %{_sbindir}/gfs_quota
%attr(755,root,root) %{_sbindir}/gfs_tool
%attr(754,root,root) /etc/rc.d/init.d/gfs
%{_mandir}/man8/fsck.gfs.8*
%{_mandir}/man8/gfs.8*
%{_mandir}/man8/gfs_grow.8*
%{_mandir}/man8/gfs_jadd.8*
%{_mandir}/man8/gfs_quota.8*
%{_mandir}/man8/gfs_tool.8*
%{_mandir}/man8/mkfs.gfs.8*
