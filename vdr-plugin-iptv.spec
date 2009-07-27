
%define plugin	iptv
%define name	vdr-plugin-%plugin
%define version	0.3.0
%define rel	2

Summary:	VDR plugin: Experience the IPTV
Name:		%name
Version:	%version
Release:	%mkrel %rel
Group:		Video
License:	GPL
URL:		http://www.saunalahti.fi/~rahrenbe/vdr/iptv/
Source:		http://www.saunalahti.fi/~rahrenbe/vdr/iptv/files/vdr-%plugin-%version.tgz
BuildRoot:	%{_tmppath}/%{name}-buildroot
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

perl -pi -e 's,CHANNELS_CONF=.*$,CHANNELS_CONF=%{_vdr_cfgdir}/channels.conf,' iptv/vlc2iptv
perl -pi -e 's,CHANNEL_SETTINGS_DIR=.*/iptv,CHANNEL_SETTINGS_DIR=%{_vdr_plugin_cfgdir}/%{plugin},' iptv/vlc2iptv

%build
%vdr_plugin_build

%install
rm -rf %{buildroot}
%vdr_plugin_install
install -d -m755 %{buildroot}%{_vdr_plugin_cfgdir}/%{plugin}
install -m755 iptv/* %{buildroot}%{_vdr_plugin_cfgdir}/%{plugin}

%clean
rm -rf %{buildroot}

%post
%vdr_plugin_post %plugin

%postun
%vdr_plugin_postun %plugin

%files -f %plugin.vdr
%defattr(-,root,root)
%doc README HISTORY
%dir %{_vdr_plugin_cfgdir}/%{plugin}
%config(noreplace) %{_vdr_plugin_cfgdir}/%{plugin}/image.sh
%config(noreplace) %{_vdr_plugin_cfgdir}/%{plugin}/internetradio.sh
%config(noreplace) %{_vdr_plugin_cfgdir}/%{plugin}/iptvstream-notrap.sh
%config(noreplace) %{_vdr_plugin_cfgdir}/%{plugin}/iptvstream.sh
%config(noreplace) %{_vdr_plugin_cfgdir}/%{plugin}/linein.sh
%config(noreplace) %{_vdr_plugin_cfgdir}/%{plugin}/vlc2iptv
%config(noreplace) %{_vdr_plugin_cfgdir}/%{plugin}/webcam.sh

