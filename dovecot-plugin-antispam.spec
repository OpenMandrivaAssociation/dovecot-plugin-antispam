Name:		dovecot-plugin-antispam
Version:	51
Release:	3
Summary:	Spam filter teaching plugin for the Dovecot IMAP server
Group:		System/Servers

# BSD License (two clause)
# http://www.freebsd.org/copyright/freebsd-license.html
License:	BSD-2-Clause
URL:		https://wiki2.dovecot.org/Plugins/Antispam
BuildRequires:  dovecot-devel
BuildRequires:  autoconf automake
Requires:	rspamd dovecot

# Taken from http://hg.dovecot.org/dovecot-antispam-plugin
Source0:	dovecot-antispam-plugin-%{version}.tar.xz

%description
A dovecot plugin for training rspamd's Bayes filter.
Any message moved to the Junk folder will be trained as spam.

%prep
%setup -qn dovecot-antispam-plugin-%{version}
./autogen.sh
%configure --with-dovecot=%{_libdir}/dovecot

%build
%make

%install
%make install DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/dovecot/conf.d
cat >%{buildroot}%{_sysconfdir}/dovecot/conf.d/90-antispam.conf <<'EOF'
mail_plugins = $mail_plugins antispam
plugin {
	antispam_mail_spam = learn_spam
	antispam_mail_notspam = learn_ham
	antispam_mail_sendmail = /usr/bin/rspamc
}
EOF

%files
%{_libdir}/dovecot/modules/lib90_antispam_plugin.so
%{_mandir}/man7/dovecot-antispam.7*
%{_sysconfdir}/dovecot/conf.d/90-antispam.conf
