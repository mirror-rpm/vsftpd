%define optflags -g
Summary: vsftpd - Very Secure Ftp Daemon
Name: vsftpd
Version: 1.0.1
Release: 5
License: GPL
Group: System Environment/Daemons
URL: ftp://ferret.lmh.ox.ac.uk/pub/linux/
Source: %{name}-%{version}.tar.gz
Source1: vsftpd.xinetd
Source2: vsftpd.pam
Source3: vsftpd.ftpusers
Source4: vsftpd.user_list
Patch1: vsftpd-1.0.1-rh.patch
Patch2: vsftpd-1.0.1-missingok.patch
Patch3: vsftpd-1.0.1-anon.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: xinetd, logrotate
Provides: ftpserver

%description
vsftpd is a Very Secure FTP daemon. It was written completely from
scratch.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1 -b .rh
%patch2 -p1 -b .mok
%patch3 -p1 -b .anon

%build
make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/sbin
mkdir -p $RPM_BUILD_ROOT/etc
mkdir -p $RPM_BUILD_ROOT/etc/pam.d
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
mkdir -p $RPM_BUILD_ROOT/etc/xinetd.d
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man5
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man8
install -m 755 vsftpd  $RPM_BUILD_ROOT/usr/sbin/vsftpd
install -m 600 vsftpd.conf $RPM_BUILD_ROOT/etc/vsftpd.conf
install -m 644 vsftpd.conf.5 $RPM_BUILD_ROOT/%{_mandir}/man5/
install -m 644 vsftpd.8 $RPM_BUILD_ROOT/%{_mandir}/man8/
install -m 644 RedHat/vsftpd.log $RPM_BUILD_ROOT/etc/logrotate.d/vsftpd.log
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/xinetd.d/vsftpd
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/vsftpd
install -m 600 %{SOURCE3} $RPM_BUILD_ROOT/etc/vsftpd.ftpusers
install -m 600 %{SOURCE4} $RPM_BUILD_ROOT/etc/vsftpd.user_list

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/sbin/vsftpd
%config(noreplace) /etc/vsftpd.*
%config(noreplace) /etc/pam.d/vsftpd
%config(noreplace) /etc/logrotate.d/vsftpd.log
%config(noreplace) /etc/xinetd.d/vsftpd
%doc INSTALL BUGS AUDIT Changelog LICENSE README README.security REWARD SPEED TODO SECURITY/ TUNING SIZE
%{_mandir}/man5/vsftpd.conf.*
%{_mandir}/man8/vsftpd.*

%changelog
* Wed Apr 10 2002 Bill Nottingham <notting@redhat.com> 1.0.1-5
- don't spit out ugly errors if anonftp isn't installed (#62987)
- fix horribly broken userlist setup (#62321)

* Thu Feb 28 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.0.1-4
- s/Copyright/License/
- add "missingok" to the logrotate script, so we don't get errors
  when nothing has happened

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Nov 28 2001 Bill Nottingham <notting@redhat.com>
- initial packaging for RHL, munge included specfile

* Thu Mar 22 2001 Seth Vidal <skvidal@phy.duke.edu>
- updated to 0.0.15
- added entry for vsftpd.8 man page
- added entry for vsftpd.log logrotate file
- added TUNING file to docs list

* Wed Mar 7 2001 Seth Vidal <skvidal@phy.duke.edu>
- Updated to 0.0.14
- made %files entry for man page

* Wed Feb 21 2001 Seth Vidal <skvidal@phy.duke.edu>
- Updated to 0.0.13

* Mon Feb 12 2001 Seth Vidal <skvidal@phy.duke.edu>
- Updated to 0.0.12

* Wed Feb 7 2001 Seth Vidal <skvidal@phy.duke.edu>
- updated to 0.0.11

* Fri Feb 1 2001 Seth Vidal <skvidal@phy.duke.edu>
- Update to 0.0.10

* Fri Feb 1 2001 Seth Vidal <skvidal@phy.duke.edu>
- First RPM packaging
- Stolen items from wu-ftpd's pam setup
- Separated rh 7 and rh 6.X's packages
- Built for Rh6
