%{!?tcp_wrappers:%define tcp_wrappers 1}

Summary: vsftpd - Very Secure Ftp Daemon
Name: vsftpd
Version: 2.0.5
Release: 6
License: GPL
Group: System Environment/Daemons
URL: http://vsftpd.beasts.org/
Source: ftp://vsftpd.beasts.org/users/cevans/%{name}-%{version}.tar.gz
Source1: vsftpd.xinetd
Source2: vsftpd.pam
Source3: vsftpd.ftpusers
Source4: vsftpd.user_list
Source5: vsftpd.init
Source6: vsftpd_conf_migrate.sh
Patch1: vsftpd-1.1.3-rh.patch
Patch2: vsftpd-1.0.1-missingok.patch
Patch3: vsftpd-2.0.1-tcp_wrappers.patch
Patch4: vsftpd-1.5.1-libs.patch
Patch5: vsftpd-2.0.2-signal.patch
Patch6: vsftpd-1.2.1-conffile.patch
Patch7: vsftpd-2.0.1-build_ssl.patch
Patch8: vsftpd-2.0.1-server_args.patch
Patch9: vsftpd-2.0.1-dir.patch
Patch10: vsftpd-2.0.1-use_localtime.patch
Patch11: vsftpd-1.2.1-nonrootconf.patch
Patch13: vsftpd-2.0.3-background.patch
Patch14: vsftpd-2.0.3-daemonize_fds.patch
Patch15: vsftpd-2.0.1-kickline.patch
Patch16: vsfptd-2.0.3-user_config.patch
Patch17: vsftpd-2.0.3-pam_hostname.patch
Patch18: vsftpd-close-std-fds.patch
Patch19: vsftpd-2.0.5-default_ipv6.patch
Patch20: vsftpd-2.0.5-add_ipv6_option.patch
Patch21: vsftpd-2.0.5-correct_comments.patch
Patch22: vsftpd-2.0.5-man.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
%if %{tcp_wrappers}
BuildPrereq: tcp_wrappers
%endif
BuildRequires: pam-devel
Requires: pam
Requires: /%{_lib}/security/pam_loginuid.so
BuildRequires: libcap-devel
Requires: libcap
BuildRequires: openssl-devel
Requires: openssl
# for -fpie
BuildPrereq: gcc > gcc-3.2.3-13, binutils > binutils-2.14.90.0.4-24, glibc-devel >= 2.3.2-45
Requires: logrotate
Prereq: /sbin/chkconfig, /sbin/service, /usr/sbin/usermod
Obsoletes: anonftp
Provides: ftpserver

%description
vsftpd is a Very Secure FTP daemon. It was written completely from
scratch.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1 -b .rh
%patch2 -p1 -b .mok
%if %{tcp_wrappers}
%patch3 -p1 -b .tcp_wrappers
%endif
%patch4 -p1 -b .libs
cp %{SOURCE1} .
%patch5 -p1 -b .signal
%patch6 -p1
%patch7 -p1 -b .build_ssl
%patch8 -p1 -b .server_args
%patch9 -p1 -b .dir
%patch10 -p1 -b .use_localtime
%patch11 -p1 -b .nonrootconf
%patch13 -p1 -b .background
%patch14 -p1 -b .fds
%patch15 -p1 -b .kickline
%patch16 -p1 -b .user_config
%patch17 -p1 -b .old-pam
%patch18 -p1 -b .close-fds
%patch19 -p1 -b .ipv6
%patch20 -p1 -b .ipv6opt
%patch21 -p1 -b .comments
%patch22 -p1 -b .manp

%build
%ifarch s390x
make CFLAGS="$RPM_OPT_FLAGS -fPIE -pipe" \
%else
make CFLAGS="$RPM_OPT_FLAGS -fpie -pipe" \
%endif
	LINK="-pie -lssl" \
	%{?_smp_mflags}

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/sbin
mkdir -p $RPM_BUILD_ROOT/etc
mkdir -p $RPM_BUILD_ROOT/etc/{vsftpd,pam.d,logrotate.d,rc.d/init.d}
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man{5,8}
install -m 755 vsftpd  $RPM_BUILD_ROOT/usr/sbin/vsftpd
install -m 600 vsftpd.conf $RPM_BUILD_ROOT/etc/vsftpd/vsftpd.conf
install -m 644 vsftpd.conf.5 $RPM_BUILD_ROOT/%{_mandir}/man5/
install -m 644 vsftpd.8 $RPM_BUILD_ROOT/%{_mandir}/man8/
install -m 644 RedHat/vsftpd.log $RPM_BUILD_ROOT/etc/logrotate.d/vsftpd.log
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/vsftpd
install -m 600 %{SOURCE3} $RPM_BUILD_ROOT/etc/vsftpd/ftpusers
install -m 600 %{SOURCE4} $RPM_BUILD_ROOT/etc/vsftpd/user_list
install -m 755 %{SOURCE5} $RPM_BUILD_ROOT/etc/rc.d/init.d/vsftpd
install -m 744 %{SOURCE6} $RPM_BUILD_ROOT/etc/vsftpd/vsftpd_conf_migrate.sh
                            
mkdir -p $RPM_BUILD_ROOT/var/ftp/pub

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add vsftpd
#/usr/sbin/usermod -d /var/ftp ftp >/dev/null 2>&1 || :

%preun
if [ $1 = 0 ]; then
 /sbin/service vsftpd stop > /dev/null 2>&1
 /sbin/chkconfig --del vsftpd
fi
  

%files
%defattr(-,root,root)
/usr/sbin/vsftpd
/etc/rc.d/init.d/vsftpd
#%config(noreplace) /etc/vsftpd.*
%dir /etc/vsftpd
%config(noreplace) /etc/vsftpd/*
%config(noreplace) /etc/pam.d/vsftpd
%config(noreplace) /etc/logrotate.d/vsftpd.log
%doc FAQ INSTALL BUGS AUDIT Changelog LICENSE README README.security REWARD SPEED TODO BENCHMARKS COPYING SECURITY/ EXAMPLE/ TUNING SIZE vsftpd.xinetd
%{_mandir}/man5/vsftpd.conf.*
%{_mandir}/man8/vsftpd.*
/var/ftp

%changelog
* Tue Aug 22 2006 Maros Barabas <mbarabas@redhat.com> - 2.0.5-7
- correct paths of configuration files on man pages

* Tue Aug 15 2006 Maros Barabas	<mbarabas@redhat.com> - 2.0.5-6
- correct comments

* Tue Aug 08 2006 Maros Barabas	<mbarabas@redhat.com> - 2.0.5-5
- option to change listening to IPv6 protocol

* Thu Aug 01 2006 Maros Barabas <mbarabas@redhat.com> - 2.0.5-4
- listen to IPv4 connections in default conf file

* Mon Jul 17 2006 Radek Vokal <rvokal@redhat.com> - 2.0.5-3
- listen to IPv6 connections in default conf file

* Thu Jul 13 2006 Radek Vokal <rvokal@redhat.com> - 2.0.5-2
- add keyinit instructions to the vsftpd PAM script (#198637)

* Wed Jul 12 2006 Radek Vokal <rvokal@redhat.com> - 2.0.5-1
- upgrade to 2.0.5
- IE should now show the login dialog again (#191147)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.0.4-1.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.0.4-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.0.4-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Jan 12 2006 Radek Vokal <rvokal@redhat.com> 2.0.4-1
- upgrade to 2.0.4
- vsftpd now lock files for simultanous up/downloads (#162511)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 09 2005 Radek Vokal <rvokal@redhat.com> 2.0.3-12
- rebuilt against new openssl
- close std file descriptors

* Tue Oct 04 2005 Radek Vokal <rvokal@redhat.com> 2.0.3-11
- use include instead of pam_stack in pam config

* Fri Sep 09 2005 Radek Vokal <rvokal@redhat.com> 2.0.3-10
- vsfptd.log as a default log file has to be rotated (#167359)
- vsftpd does dns reverse before passing hosts to pam_access.so (#159745)

* Wed Aug 31 2005 Radek Vokal <rvokal@redhat.com> 2.0.3-9
- don't die when no user config file is present (#166986)

* Tue Aug 09 2005 Radek Vokal <rvokal@redhat.com> 2.0.3-8
- removed additional cmd line for ftp (#165083)

* Thu Aug 04 2005 Radek Vokal <rvokal@redhat.com> 2.0.3-7
- daemonize with file descriptors (#164998)

* Thu Jun 30 2005 Radek Vokal <rvokal@redhat.com> 2.0.3-6
- start in background as default, init script changed (#158714)

* Mon Jun 27 2005 Radek Vokal <rvokal@redhat.com> 2.0.3-5
- fixed requires for 64bit libs

* Thu Jun 23 2005 Radek Vokal <rvokal@redhat.com> 2.0.3-4
- fixed requires for pam_loginuid

* Wed Jun 01 2005 Radek Vokal <rvokal@redhat.com> 2.0.3-3
- vsftpd update for new audit system (#159223)

* Fri May 27 2005 Radek Vokal <rvokal@redhat.com> 2.0.3-2
- timezone fix, patch from suse.de (#158779)

* Wed Mar 23 2005 Radek Vokal <rvokal@redhat.com> 2.0.3-1
- new release, fixes #106416 and #134541 

* Mon Mar 14 2005 Radek Vokal <rvokal@redhat.com> 2.0.3-pre2
- prerelease, fixes IPv6 issues

* Mon Mar 14 2005 Radek Vokal <rvokal@redhat.com> 2.0.2-1
- update to new release, several bug fixes

* Wed Mar 02 2005 Radek Vokal <rvokal@redhat.com> 2.0.1-10
- rebuilt against gcc4 and new openssl

* Mon Feb 07 2005 Radek Vokal <rvokal@redhat.com> 2.0.1-9
- don't allow to read non-root config files (#145548)

* Mon Jan 10 2005 Radek Vokal <rvokal@redhat.com> 2.0.1-8
- use localtime also in logs (#143687)

* Tue Dec 14 2004 Radek Vokal <rvokal@redhat.com> 2.0.1-7
- fixing directory in vsftpd.pam file (#142805)

* Mon Nov 11 2004 Radek Vokal <rvokal@redhat.com> 2.0.1-6
- vsftpd. files moved to /etc/vsftpd
- added vsftpd_conf_migrate.sh script for moving conf files

* Fri Oct 01 2004 Radek Vokal <rvokal@redhat.com> 2.0.1-5
- vsftpd under xinetd reads its config file (#134314)

* Thu Sep 16 2004 Radek Vokal <rvokal@redhat.com> 2.0.1-4
- spec file changed, ftp dir change commented (#130119)
- added doc files (#113056)

* Wed Sep 08 2004 Jan Kratochvil <project-vsftpd@jankratochvil.net>
- update for 2.0.1 for SSL

* Fri Aug 27 2004 Radek Vokal <rvokal@redhat.com> 2.0.1-2
- vsftpd.conf file changed, default IPv6 support

* Fri Aug 20 2004 Radek Vokal <rvokal@redhat.com> 2.0.1-1
- tcp_wrapper patch updated, signal patch updated
- upgrade to 2.0.1, fixes several bugs, RHEL and FC builds

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 19 2004 Bill Nottingham <notting@redhat.com> 1.2.1-6
- fix the logrotate config (#116253) 

* Mon May  3 2004 Bill Nottingham <notting@redhat.com> 1.2.1-5
- fix all references to vsftpd.conf to be /etc/vsftpd/vsftpd.conf,
  including in the binary (#121199, #104075)

* Thu Mar 25 2004 Bill Nottingham <notting@redhat.com> 1.2.1-4
- don't call malloc()/free() in signal handlers (#119136,
  <olivier.baudron@m4x.org>)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Nov 24 2003 Karsten Hopp <karsten@redhat.de> 1.2.1-1
- update to 1.2.1, which fixes #89765 and lot of other issues
- remove manpage patch, it isn't required anymore
- clean up init script
- don't use script to find libs to link with (lib64 issues)

* Sun Oct 12 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- allow compiling without tcp_wrappers support

* Mon Sep 15 2003 Bill Nottingham <notting@redhat.com> 1.2.0-4
- fix errant newline (#104443)

* Fri Aug  8 2003 Bill Nottingham <notting@redhat.com> 1.2.0-3
- tweak man page (#84584, #72798)
- buildprereqs for pie (#99336)
- free ride through the build system to fix (#101582)

* Thu Jun 26 2003 Bill Nottingham <notting@redhat.com> 1.2.0-2
- update to 1.2.0

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Apr 28 2003 Bill Nottingham <notting@redhat.com> 1.1.3-9
- fix tcp_wrappers usage (#89765, <dale@riyescott.com>)

* Fri Feb 28 2003 Nalin Dahyabhai <nalin@redhat.com> 1.1.3-8
- enable use of tcp_wrappers

* Tue Feb 11 2003 Bill Nottingham <notting@redhat.com> 1.1.3-7
- provide /var/ftp & /var/ftp/pub. obsolete anonftp.

* Mon Feb 10 2003 Bill Nottingham <notting@redhat.com> 1.1.3-6
- clean up comments in init script (#83962)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Dec 30 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- change to /etc/rc.d/init.d for better compatibility

* Mon Dec 16 2002 Bill Nottingham <notting@redhat.com> 1.1.3-3
- fix initscript perms
- fix typo in initscript (#76587)

* Fri Dec 13 2002 Bill Nottingham <notting@redhat.com> 1.1.3-2
- update to 1.1.3
- run standalone, don't run by default
- fix reqs
 
* Fri Nov 22 2002 Joe Orton <jorton@redhat.com> 1.1.0-3
- fix use with xinetd-ipv6; add flags=IPv4 in xinetd file (#78410)

* Tue Nov 12 2002 Nalin Dahyabhai <nalin@redhat.com> 1.0.1-9
- remove absolute paths from PAM configuration so that the right modules get
  used for whichever arch we're built for on multilib systems

* Thu Aug 15 2002 Elliot Lee <sopwith@redhat.com> 1.0.1-8
- -D_FILE_OFFSET_BITS=64
- smp make
- remove forced optflags=-g for lack of supporting documentation
 
* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

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
