
%define plugin	iptv
%define name	vdr-plugin-%plugin
%define version	0.3.2
%define rel	2

%define debug_package %{nil}

Summary:	VDR plugin: Experience the IPTV
Name:		%name
Version:	%version
Release:	%mkrel %rel
Group:		Video
License:	GPLv2
URL:		http://www.saunalahti.fi/~rahrenbe/vdr/iptv/
Source:		http://www.saunalahti.fi/~rahrenbe/vdr/iptv/files/vdr-%plugin-%version.tgz
BuildRequires:	vdr-devel >= 1.6.0
Requires:	vdr-abi = %vdr_abi
# for example helper scripts
# disabled for now as not needed by everyone and they are quite big
#Suggests:	ffmpeg
#Suggests:	vlc
#Suggests:	mplayer
#Suggests:	alsa-utils

%description
This plugin integrates multicast IPTV transport streams seamlessly into
VDR. You can use any IPTV channel like any other normal DVB channel for
live viewing, recording, etc. The plugin also features full section
filtering capabilities which allow for example EIT information to be
extracted from the incoming stream.

Currently the IPTV plugin has direct support for both multicast UDP/RTP
and unicast HTTP MPEG1/2 transport streams. Also a file input method is
supported, but a file delay must be selected individually to prevent
VDR's transfer buffer over/underflow. Therefore the file input should be
considered as a testing feature only.

IPTV plugin also features a support for external streaming applications.
With proper helper applications and configuration IPTV plugin is able to
display not only MPEG1/2 transport streams but also other formats like
MP3 radio streams, mms video streams and so on.

The example scripts require alsa-utils, ffmpeg, mplayer, vlc.

%prep
%setup -q -n %plugin-%version
%vdr_plugin_prep

%vdr_plugin_params_begin %plugin
# Number of devices to be created
var=DEVICES
param=--devices=DEVICES
%vdr_plugin_params_end

perl -pi -e 's,CHANNELS_CONF=.*$,CHANNELS_CONF=%{vdr_cfgdir}/channels.conf,' iptv/vlc2iptv
perl -pi -e 's,CHANNEL_SETTINGS_DIR=.*/iptv,CHANNEL_SETTINGS_DIR=%{vdr_plugin_cfgdir}/%{plugin},' iptv/vlc2iptv

%build
%vdr_plugin_build

%install
%vdr_plugin_install
install -d -m755 %{buildroot}%{vdr_plugin_cfgdir}/%{plugin}
install -m755 iptv/* %{buildroot}%{vdr_plugin_cfgdir}/%{plugin}

%post
%vdr_plugin_post %plugin

%postun
%vdr_plugin_postun %plugin

%files -f %plugin.vdr
%defattr(-,root,root)
%doc README HISTORY
%dir %{vdr_plugin_cfgdir}/%{plugin}
%config(noreplace) %{vdr_plugin_cfgdir}/%{plugin}/image.sh
%config(noreplace) %{vdr_plugin_cfgdir}/%{plugin}/internetradio.sh
%config(noreplace) %{vdr_plugin_cfgdir}/%{plugin}/iptvstream-notrap.sh
%config(noreplace) %{vdr_plugin_cfgdir}/%{plugin}/iptvstream.sh
%config(noreplace) %{vdr_plugin_cfgdir}/%{plugin}/linein.sh
%config(noreplace) %{vdr_plugin_cfgdir}/%{plugin}/vlc2iptv
%config(noreplace) %{vdr_plugin_cfgdir}/%{plugin}/webcam.sh



%changelog
* Sat Sep 04 2010 Anssi Hannula <anssi@mandriva.org> 0.3.2-1mdv2011.0
+ Revision: 575998
- new version
- update license tag for current policy

* Tue Jul 28 2009 Anssi Hannula <anssi@mandriva.org> 0.3.0-2mdv2011.0
+ Revision: 401088
- rebuild for new VDR

* Sat Jul 25 2009 Anssi Hannula <anssi@mandriva.org> 0.3.0-1mdv2010.0
+ Revision: 399815
- new version
- specify requirements of example scripts in description

* Fri Mar 20 2009 Anssi Hannula <anssi@mandriva.org> 0.2.0-3mdv2009.1
+ Revision: 359327
- rebuild for new vdr

* Mon Apr 28 2008 Anssi Hannula <anssi@mandriva.org> 0.2.0-2mdv2009.0
+ Revision: 197939
- rebuild for new vdr

* Sat Apr 26 2008 Anssi Hannula <anssi@mandriva.org> 0.2.0-1mdv2009.0
+ Revision: 197681
- new version
- add vdr_plugin_prep
- bump buildrequires on vdr-devel
- drop unneeded 1.4-support patch (P0)
- initial Mandriva release

