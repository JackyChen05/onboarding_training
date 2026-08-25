# 3.7 平台调试命令速查

本页全量收录《应届生试用期能力建设与签核手册》Sheet3、《中兴微平台调试Debug指令大全》《国内路由器平台WiFi性能测试常用命令集》的调试命令，按平台/方案分组。标注说明：

- ⭐ **常用**：日常测试高频使用，要求熟练掌握
- 🔧 **进阶**：问题定位/深度调试用，需要时查阅

::: warning 敏感信息说明
中兴微/ECONET 各平台的默认账号密码属公开信息（2.14 节列出）；但**隐藏页面 URL（含一次性时戳 Telnet 开关）、内网服务器地址**仍按规范剔除，需要时向导师索取并遵守保密要求。
:::

## 一、ADB 调试（中屏音箱/安卓设备）

### 设备管理 ⭐

| 命令 | 功能 |
| --- | --- |
| `adb devices` | 查看当前连接的设备列表，确认在线 |
| `adb install <apk路径>` | 安装指定 APK，用于固件验证或应用部署 |
| `adb uninstall <package>` | 卸载指定包名应用，用于测试清理或版本替换 |
| `adb shell pm list packages` | 列出所有已安装应用包名，可配合 `\| grep xxx` 模糊查找 |
| `adb shell pm list packages -3` | 仅列第三方应用（排除系统预置） |
| `adb shell pm list packages -s` | 仅列系统应用 |
| `adb shell am start -n <package>/<activity>` | 通过包名+Activity 直接启动应用特定页面（如设置页） |
| `adb shell am force-stop <package>` | 强制停止应用进程，模拟应用被杀后的状态恢复 |
| `adb shell input text "hello"` | 模拟键盘输入，用于自动化填充表单或搜索框 |
| `adb shell input keyevent KEYCODE_BACK` | 模拟遥控器返回键，用于 UI 自动化导航 |
| `adb shell screenrecord /sdcard/demo.mp4` | 录制屏幕操作视频，用于复现 Bug 或制作演示 |
| `adb exec-out screencap -p > screen.png` | 截取当前屏幕保存本地，用于问题截图取证 |
| `adb push <本地文件> <设备路径>` | 推送文件到设备（测试包、配置文件） |
| `adb pull <设备文件> <本地路径>` | 从设备拉取文件（日志、截图） |
| `adb shell monkey -p <package> -v 1000` | Monkey 随机压力测试（1000 次随机事件），验证稳定性 |

### 日志与性能分析 ⭐

| 命令 | 功能 |
| --- | --- |
| `adb logcat -v time \| grep -i "error\|crash"` | 实时查看 error/crash 日志，快速定位崩溃 |
| `adb logcat -v time -s TagName` | 按 Tag 过滤带时间戳日志，追踪特定模块 |
| `adb shell dumpsys meminfo <package>` | 查看应用内存详情（Java Heap、Native Heap、Graphics） |
| `adb shell dumpsys cpuinfo` | 查看 CPU 各核心及进程实时占用率 |
| `adb shell top -n 1 \| grep <包名>` | 查看指定应用瞬时 CPU 占用 |
| `adb shell cat /proc/meminfo` | 系统整体内存（MemTotal/MemFree/Cached/Swap） |
| `adb shell cat /proc/cpuinfo` | CPU 架构、核心数、型号及硬件信息 |

## 二、中兴微方案接入网产品 ⭐

中兴微（ZTE Micro / Sanechips）平台用 **sendcmd / sidbg** 两大命令族操作底层数据库，**sismac / sk_test** 负责写号。不同芯片版本（ZX279127/128/131/133 等）命令略有差异，先用 `cat /proc/zxic/softVersion` 确认版本。

### 2.1 系统信息查看 ⭐

| 命令 | 功能 |
| --- | --- |
| `cat /proc/version` | 查看软件版本时间 |
| `cat /proc/zxic/softVersion` | 查看软件版本号 |
| `cat /proc/zxic/hardVersion` | 查看硬件版本号 |
| `cat /proc/zxic/bootVersion` | 查看 boot 软件时间 |
| `cat /proc/zxic/versionstates` | 查看软件分区情况 |
| `siupgrade switchver 0/1` | 版本分区切换（重启生效） |
| `cat /proc/cpuusage` | 查看 CPU 使用率 |
| `cat /proc/meminfo` | 查看 RAM 使用情况（需自行计算） |
| `cat /userconfig/flag_type` | 查看地区码 |
| `cat /proc/pon/upmode` | 查看 PON 上行模式 |
| `ifconfig` | 查看所有网络接口状态 |
| `iwconfig apcli0` / `iwconfig apcli1` | 查看 Mesh Agent 连接状态（2.4G/5G 回传） |
| `cat /var/iproute2/wan_mark_map.conf` | 查看 WAN 连接的 mark 值映射 |
| `opticalst -getpara` | 获取发送/接收光功率 |
| `echo 0 128 > /sys/devices/platform/ponmac/gmac/bwMap` + `cat .../allocTab` | 获取 OLT 下发参数 🔧 |
| `ifconfig mirror add pon0 eth0` | 设置 PON 口镜像（eth0=LAN1，eth1=LAN2，eth2=LAN3，eth3=LAN4） |
| `ifconfig mirror del pon0 eth0` / `ifconfig mirror show` | 删除 / 查看 PON 口镜像 |
| `sidbg log -l <级别>` | 管理模块打印级别：None(0)~Debug(8) |

### 2.2 sendcmd 命令族（数据库操作）⭐

| 命令 | 功能 |
| --- | --- |
| `sendcmd 1 DB p DevAuthInfo` | 查看设备认证信息（账号密码） |
| `sendcmd 1 DB printall 1` | 打印数据库全部内容 |
| `sendcmd 1 DB save` / `sendcmd 1 DB reset` | 保存修改 / 恢复出厂 |
| `sendcmd 1 DB p WLANAD` | 查看下挂设备信息 |
| `sendcmd 1 DB p WLANBase` / `WLANCfg` / `WLANGUEST` | WiFi 网卡 / SSID / 访客网络配置 |
| `sendcmd 1 DB p WLANPSK` / `WLANWEP` / `WLANWAPI` | PSK / WEP / WAPI 密钥配置 |
| `sendcmd 1 DB p WLANWMM` / `WLANWPS` | WMM / WPS 配置 |
| `sendcmd 1 DB p ForwardRule` / `MirrorRule` / `DetailProcess` | 数据流重定向 / 镜像 / 精细流处理规则 🔧 |
| `sendcmd 1 DB p CMCCApiRight` | 查看网关插件权限 |
| `sendcmd 1 DB p PPPTimePlc` | 查看 PPPoE 重拨时间策略 |
| `sendcmd 1 DB set <表名> <行号> <字段> <值>` | 修改数据库字段值 |
| `sendcmd 1 DB set TelnetCfg 0 Lan_Enable 1` / `TS_Enable 1` | 开启 Telnet（LAN 侧 / TS 侧） |
| `sendcmd 1 DB set PDTCTUSERINFO 0 Status 0` + `Result 1` | 关闭 DNS 欺骗 🔧 |
| `sendcmd 1 DB set PPPTimePlc 0 IntervalCnt <值>` / `TimePlc "间隔"` | 设置 PPPoE 重拨次数 / 时间间隔 🔧 |
| `sendcmd 1 DB set CMCCOSGIInfo 0 AccDefault 1` / `CMCCBundleInfo 0 InstallFirst 0` | OSGI 插件默认权限 / 安装首选项 🔧 |
| `sendcmd 1 DB set NetWorkingPlugin 0 DBGFlag 1` | 开启平台交互报文日志 |
| `sendcmd 1 DB set EasyMeshConfig 0 MapEnable 0` | 关闭 Mesh |

### 2.3 sendcmd 二级进程调试日志 🔧

格式：`sendcmd <进程号> <模块> -1 <级别>`（8=Debug 开，0/5=关）。

| 命令 | 功能 |
| --- | --- |
| `sendcmd 1 wlan_config -1 8` / `wlan_mgr -1 8` / `wlan adapter -1 8` | wlan 配置/管理/adapter 调试日志 |
| `sendcmd 1 upgrade_mgr -1 8` / `fm_mgr -1 8` | 升级管理 / 文件管理模块日志 |
| `sendcmd 3 webd -1 8` / `-1 0` | 开 / 关 Web 调试日志 |
| `sendcmd 3 tr069 -1 8` / `-1 5` | 开 / 关 RMS(TR069) 日志 |
| `sendcmd 3 tr069 showsoap 1` / `0` | 开 / 关 SOAP 报文打印 |
| `sendcmd 3 webd printenv` | 查看 Web 环境变量 |
| `sendcmd 73 -1 8` / `73 plugm_cmdtype dbgall 1` / `dbgjson 1` | 插件日志 / 全部调试 / JSON 调试 |
| `sendcmd 73 rm_mgr quickboot 1` | 快速发起连接（代替插拔光纤调试） |
| `sendcmd 74 osgid logctr 1` / `0` / `shutdown` / `install name=.. url=.. fsize=..` | Java 日志开关 / 关 OSGI 框架 / 安装 OSGI 插件 |
| `sendcmd 2 -1 8` / `2 BoardControl set 34008 0 10` / `0 20` | 语音调试日志 / 开 / 关语音口测试（产测） |

### 2.4 sidbg 命令族 ⭐

| 命令 | 功能 |
| --- | --- |
| `sidbg 1 DB printall 1` | 打印数据库全部内容 |
| `sidbg 1 DB p DevAuthInfo` | 查看设备认证信息（账号密码） |
| `sidbg 1 DB p DevInfo` | 查看设备基本信息 |
| `sidbg 1 DB set TelnetCfg 0 Lan_Enable 1` / `TS_Enable 1` | 开启 Telnet（需重启生效） |
| `sidbg 1 DB save` / `sidbg 1 DB reset` | 保存 / 恢复出厂 |
| `sidbg 1 DB set VoIPLineCfg 0 BufferUnderflows 0` 等 | 语音 Buffer/Overruns/Underruns 参数 🔧 |
| `sidbg 1 DB set NetWorkingPlugin 0 DBGFlag 1` | 开启平台交互日志 |

### 2.5 OMCI 与 GPON 调试 🔧

| 命令 | 功能 |
| --- | --- |
| `sendcmd 132 omcidebug setprintlevel 5 0 0` | 开 OMCI 5 级日志（详细调试） |
| `sendcmd 132 omcidebug setprintlevel 3 0 0` | 开 OMCI 3 级日志（升级时用） |
| `sendcmd 132 omcidebug setprintlevel 0 0 0` | 关 OMCI 日志 |
| `gponsdk_test -s_print_dbg 2` / `0` | 开 / 关 GPON SDK PLoAM 消息打印（断电不保存） |
| `gpontest -gpondncounters` | 下行接收错误统计，判断链路质量 |

### 2.6 写号/生产指令（sismac / sk_test）⭐

| 命令 | 功能 |
| --- | --- |
| `sismac show` | 查看所有参数 |
| `sismac 1 2176 SKYW` | 写入设备 OUI（厂商 ID） |
| `sismac 1 2177 <8位>` / `sismac 1 768 <6位>` / `sismac 1 256 <MAC>` | 写入 MAC 后 8 位 / 前 6 位 / 完整 MAC |
| `sismac 1 512 <标识>` | 写入设备标识 |
| `sismac 1 1024 <SSID>` / `sismac 1 1312 <密码>` | 写入 2.4G SSID / 密码 |
| `sismac 1 1028 <SSID-5G>` / `sismac 1 1316 <密码>` | 写入 5G SSID / 密码 |
| `sismac 1 1793 <密码>` | 写入 Web 登录密码 |
| `sismac 2 512` | 查看 SN 值（转 ascii 即 root 密码） 🔧 |
| `sk_test set_ethernet_mac <MAC>` | 写入 br0 MAC |
| `sk_test set_sn <sn>` / `set_cmei <cmei>` | 写入 SN / CMEI |
| `sk_test set_2g_ssid <ssid>` / `set_2g_password <pwd>` | 2.4G SSID / 密钥 |
| `sk_test set_5g_ssid <ssid>` / `set_5g_password <pwd>` | 5G SSID / 密钥 |
| `sk_test set_web_user_name <name>` / `set_web_user_password <pwd>` | Web 普通用户账号 / 密码 |
| `sk_test set_region_id 299` | 设置地区码（299=全国） |
| `sk_test set_xponsn <12位SN>` | 写入 GPON SN |
| `sk_test set_device_model <型号>` / `set_hardware_version <ver>` | 改设备型号 / 硬件版本（重启生效） |
| `sk_test save_wifi_calibration_2g` / `_5g` | 保存 2G/5G WiFi 校准数据 |
| `siupgrade sdefconf 199` | 设置地区码（199=全国） |
| `nand scrub.chip` | 手动清除 FLASH（切换运营商时，**慎用**） 🔧 |

> 写完号必须恢复出厂（`sidbg 1 DB reset` 或页面操作）才生效。

### 2.7 WiFi 调试（MTK，中兴微路由平台）🔧

| 命令 | 功能 |
| --- | --- |
| `iwpriv wlan0 e2p` / `iwpriv wlan4 e2p` | 读 2.4G / 5G 校准值 |
| `cd /wlan` + `tftp -pl MT7603E.bin <IP>` / `MT7613E_EEPROM.bin` | 备份 2.4G / 5G 校准文件 |
| `tftp -gr MT7915_EEPROM.bin <IP>` | 写入校准文件 |
| `iwpriv wlan0 e2p 191=4852; e2p 193=0148; set bufferWriteBack=4` | 切 2 天线 |
| `iwpriv wlan0 e2p 191=485B; e2p 193=014C; set bufferWriteBack=4` | 切 3 天线 |
| `iwpriv wlan0/wlan4 show stainfo` | 查看无线终端列表 |
| `iwpriv wlan0/wlan4 set Debug=3` | 无线 debug；循环抓日志 `while true;do iwpriv wlan0 show stainfo;sleep 1;iwpriv wlan4 stat;done` |
| `iwpriv wlan4 show radio_stat` / `sta_stat` / `mbss_stat` / `stat` / `mbss=1` / `set ResetCounter` | wifi 接口信息 / 计数清零 |
| `iwpriv wlan4 show manual_txop` / `txopinfo` / `tmacinfo` / `agginfo` | txop 相关 |
| `iwpriv ra1 set TxBurst=0; iwpriv ra1 mac 820F4014=ffff0000` | 调 TXOP 提高发包时间 |
| `iwpriv wlan4 show mibinfo=1` | 收发包数统计 |
| `iwpriv wlan4 show driverinfo` | 无线驱动版本 |
| `iwpriv wlan0/wlan4 set SiteSurvey=1` + `set PartialScan=1` + `get_site_survey` | 无线扫描及查看 |
| `nvram show wapi` | 查看黑白名单 |
| `nvram set wapi MacFilterEnable 1` + `MacFilterPolicy 0/1` + `set MacFilterEntries` | 黑白名单（0=黑名单 / 1=白名单） |
| `echo watchdog=disable > /proc/watchdog/ctrl` | 关闭看门狗（长稳测试防自动重启） |

### 2.8 Mesh 调试（mapd_cfg / mapd_cli）🔧

| 命令 | 功能 |
| --- | --- |
| `sendcmd 1 DB set EasyMeshConfig 0 MapEnable 0` + `sendcmd 1 DB save` | 关闭 Mesh |
| `iwconfig apcli0` / `apcli1` | 查看 Agent 连接状态 |
| `mapd_cfg` | 查看/修改漫游策略（`CentralizedSteering=1` 默认集中式，controller 决定漫游） |
| `cat /wlan/mapd_cfg` | 查看当前漫游策略（含 bss_config_priority/DualBH/BHSteerTimeout 等） |
| `mapd_cli /tmp/mapd_ctrl get steeringparams` | 漫游参数全表（CU 阈值、RSSI 边缘、MCS/RSSI Crossing、BTM/Force 超时与禁时等） |
| `mapd_cli /tmp/mapd_ctrl get steeringparams \| LowRSSIAPSteerEdge_root` / `_RE` | Apsteering 阈值 |
| `mapd_cli /tmp/mapd_ctrl set log_level 2` 后看 log `[mapd][wlanif_deauth_sta]` | 判断是否走进 force steering（强制漫游） |
| `mapd_cli /tmp/mapd_ctrl get RSSIThreshold` / `RSSIThreshold5G` | Bandsteering 阈值（2.4G→5G / 5G→2.4G） |
| `mapd_cli /tmp/mapd_ctrl set RSSIThreshold -50` / `set RSSIThreshold5G -60` | 修改 Bandsteering 阈值 |
| `mapd_cli /tmp/mapd_ctrl set log_level 2`（开）/ `6`（关） | mapd 日志（值越小 log 越多） |
| `1905ctrl agent log_level 3`（开）/ `1`（关） | 1905 daemon 日志（值越大 log 越多） |

### 2.9 加速开关与 WAN 镜像 ⭐

性能测试前必做——关加速排除硬件转发干扰：

| 命令 | 功能 |
| --- | --- |
| `echo 0 > /proc/ffe/hff_enable` | 关闭硬加速 |
| `echo 0 > /proc/ffe/ffe_enable` | 关闭软加速 |
| `ifconfig mirror add nbif0 eth0` | 设置 WAN 口镜像 |

### 2.10 网络与防火墙调试 🔧

| 命令 | 功能 |
| --- | --- |
| `iptables -nL` / `-t nat` / `-t mangle` | 三层防火墙 / NAT / Mangle 规则 |
| `ebtables -L` | 二层防火墙规则 |
| `cat /proc/net/mirror_rule` / `detail_process_rule` | 镜像 / 精细流处理内核规则 |
| `cat /proc/net/dev` | 网络设备统计 |
| `cat /proc/filesystems \| grep cifs` | 是否支持 CIFS |

### 2.11 DBUS / ubus 接口速览 🔧

运营商平台对接（电信 com.ctc.igd1、联通 com.cuc.igd1）走 DBUS。掌握通用格式即可，具体路径随项目查接口文档：

```bash
# 监控 DBUS 信号
dbus-monitor --system --monitor "type='signal'"
# 查看接口方法（Introspect）
dbus-send --system --print-reply --dest=com.ctc.igd1 <路径> org.freedesktop.DBus.Introspectable.Introspect
# 读属性 Get / GetAll
dbus-send --system --type=method_call --print-reply --dest=com.ctc.igd1 <路径> com.ctc.igd1.Properties.Get string:'<接口>' string:'<属性>'
# 写属性 Set
dbus-send --system --type=method_call --print-reply --dest=com.ctc.igd1 <路径> com.ctc.igd1.Properties.Set string:'<接口>' string:'<属性>' variant:<类型>:'<值>'
```

常用路径：`/com/ctc/igd1/Info/{Device,Network,PON,WiFi,VoIP}`（信息查询）、`/com/ctc/igd1/Diagnostics/{Ping,TraceRoute,HttpDownload}`（诊断测试，调 `StartTest`）。联通侧把 `com.ctc` 换成 `com.cuc`，另可用 `gdbus call -y -d com.cuc.igd1 -o <路径> -m <方法>`。

ubus（电信 elink 场景）：`ubus monitor` 开日志；`ubus call ctcapd serverinfo set '{...}'` 设注册测试平台地址；`ubus call ctcapd.appd stop/run '{"appname":"elinkclt"}'` 启停 elink 插件。

### 2.12 联通中间件与 App 管理速览 🔧

```bash
lxc-attach -n ufw -P /opt/cu/framework   # 进入中间件
ufwmg -v                                  # 中间件版本
cu_pkg.sh List / Install <pkg.ipk> / Uninstall / Stop / Run / stat   # 插件管理
```

App 管理经 `com.cuc.appframework1` DBUS 接口（List/Install/Uninstall/Upgrade/Run/Stop/GetStatus）。

### 2.13 文件传输（tftp）⭐

| 命令 | 功能 |
| --- | --- |
| `tftp -pl <文件> <IP>` | 设备上传文件到 PC（put） |
| `tftp -gr <文件> <IP>` | 从 PC 下载文件到设备（get） |
| `mount -t cifs //IP/share /mnt -o username=..,password=..` | 挂载 CIFS/SMB 共享 |

### 2.14 运营商默认账号（公开信息）

| 设备 | 运营商 | 串口 | telnet |
| --- | --- | --- | --- |
| 路由器-中兴微 | 移动 | `root/aDm8H%MdA` | `CMCCAdmin / wifi密码+web登录密码` |
| 路由器-中兴微 | 电信 | `root/aDm8H%MdA` | `telecomadmin / wifi密码+web登录密码` |
| 路由器-中兴微 | 联通 | `root/aDm8H%MdA` | `user / web登录密码` |
| 网关-中兴微 | 电信 | `root/Zxic521` | 一级 `telnetadmin/nE7jA%5m`，二级 `su/网关SN` |
| 网关-中兴微 | 移动 | `root/aDm8H%MdA` | 一级 `root/wifi密码+管理员密码`，二级 `su/aDm8H%MdA` |
| 网关-中兴微 | 联通 | `root/Zxic521` | 一级 `user/Pon521`，二级 `su/Pon521` |

> Telnet 开启方式（隐藏页面 + 一次性时戳）属敏感操作，向导师索取，不进本站。

### 2.15 常用调试组合 ⭐

```bash
# ① 快速查看账号密码（串口登录后）
sidbg 1 DB printall 1            # 或 sendcmd 1 DB p DevAuthInfo

# ② 开启 Telnet（重启生效）
sidbg 1 DB set TelnetCfg 0 Lan_Enable 1
sidbg 1 DB set TelnetCfg 0 TS_Enable 1
sidbg 1 DB save && reboot

# ③ 写号后恢复出厂（写完号必须恢复出厂才生效）
sk_test set_ethernet_mac <MAC>; sk_test set_sn <sn>
sk_test set_2g_ssid <ssid>; sk_test set_2g_password <pwd>
sk_test set_5g_ssid <ssid>; sk_test set_5g_password <pwd>
sk_test set_web_user_name <name>; sk_test set_web_user_password <pwd>
sk_test set_region_id 299
sidbg 1 DB reset

# ④ 查看软件版本/分区
cat /proc/zxic/softVersion; cat /proc/zxic/hardVersion; cat /proc/zxic/versionstates

# ⑤ 开 OMCI 调试日志（注册问题定位，插光纤前执行）
gponsdk_test -s_print_dbg 2
sendcmd 132 omcidebug setprintlevel 5 0 0
# ... 插光纤抓日志后关闭 ...
gponsdk_test -s_print_dbg 0
sendcmd 132 omcidebug setprintlevel 0 0 0

# ⑥ 关加速（性能测试前）
echo 0 > /proc/ffe/hff_enable; echo 0 > /proc/ffe/ffe_enable
```

## 三、BCM 无线驱动调试

### 驱动/radio 信息 ⭐

| 命令 | 功能 |
| --- | --- |
| `wl -i wl1 ver` | 查看驱动版本 |
| `wl -i wl1 revinfo` | 查看当前频段无线芯片信息 |
| `wl -i wl1 msglevel error assoc` | 开启无线驱动打印等级（需编译开启 BCMDBG，wl.mk 加 `WLFLAGS += -DBCMDBG`） |
| `nvram set hapd_dbg=1; nvram restart; hostapd_cli -i wl1.1 LOG_LEVEL DEBUG` | hostapd 调试打印 🔧 |
| `cat /proc/kmsg &` | telnet 时打开驱动打印 🔧 |

### STA 客户端管理 ⭐

| 命令 | 功能 |
| --- | --- |
| `wl -i wl1.1 sta_info all` / `wl -i wl1.1 sta_info <mac>` | 查看全部/指定客户端关联信息 |
| `wl -i wl1.1 bs_data` | 查看发送给客户端的流量、空口占用率、重传率、协商速率 |
| `wl -i wl1.1 dpstats a:` / `wl -i wl1.1 pktq_stats A:+` | 发送方向包队列优先级、流量与包统计、协商速率、空口占用率 🔧 |
| `wl -i wl1.1 rx_report` | 接收方向统计 🔧 |
| `wl -i wl1.1 disassoc <mac>` | 踢掉客户端 |
| `wl -i wl1 macmode <0/1/2>` + `wl -i wl1.1 mac <mac>` | MAC 过滤（0 关闭 / 1 黑名单 / 2 白名单） |

### 无线接口与射频配置 🔧

| 命令 | 功能 |
| --- | --- |
| `wl -i wl1.1 bss` | 查看接口 down/up 状态 |
| `wl -i wl1 phy_tempsense` | 无线芯片温度 |
| `wl -i wl1 phy_tempthresh` | 温度截温（超过会减少天线数量） |
| `wl -i wl1 curpower` | 功率表（需开启 WLTEST） |
| `wl -i wl1 country list` / `wl -i wl1 country US` | 查看/配置国家码（配置需先 down 后 up） |
| `wl -i wl1 chanspecs` / `wl -i wl1 chanspec 60l` | 查看支持信道频宽 / 配置信道频宽 |
| `wl -i wl1 csa 0 5 36/80` | 通过 CSA 切换信道 |
| `wl -i wl1.1 status` | 接口信道频宽、网络模式、信道利用率、天线数 |
| `wl -i wl1 rateset` | 当前频段支持的速率集 |
| `wl -i wl1 chanim_stats` | radio 统计的空口信息 |
| `wl -i wl1 wme_ac ap/sta [be ecwmax 6]` | 查看/配置 AP/STA 的 WME 参数 |
| `wl -i wl1 dfs_status` | DFS 信道状态 |
| `wl -i wl1.1 assoclist` | 接口下挂设备 |
| `wl -i wl1 scan` + `wl -i wl1 scanresults` | 邻居扫描及结果 |
| `wl -i wl1 obss_coex` | 自动信道状态 |
| `wl -i wl1.1 if_counters` | 接口数据包统计 |
| `wl -i wl1 maxassoc [64]` | 查看/配置最大连接数 |
| `wl -i wl1.1 closednet <0/1>` | 隐藏 SSID |
| `wl -i wl1 taf` / `wl -i wl1 atf` | TAF / ATF 开关 |
| `wl -i wl1 txchain` / `wl -i wl1 rxchain` | TX/RX 天线数（1/2/4/8 按位或，如 7=三根天线） |
| `wl -i wl1 sgi_tx` | TX shortGI 模式（-1 AUTO，0~5 各档 GI） |
| `wl -i wl1 ampdu_resp_timeout` | AMPDU timeout |
| `wl -i wl1 rxchain_pwrsave_enable` / `radio_pwrsave_enable` | 天线省电 |
| `wl -i wl1 wme_apsd` | WMM 自动省电 |
| `wl -i wl1.1 pspretend_retry_limit` | PS pretend 机制 |
| `wl -i wl1 he features` | OFDMA、MU-MIMO 配置 |

### 无线网络模式切换 🔧

统一套路：`wl -i wl1 down` → 设置 he/vhtmode/nmode/nreqd/mode_reqd 组合 → `wl -i wl1 up`。

| 目标模式 | 参数组合（mode_reqd 关键值） |
| --- | --- |
| 11ax | he enab 1; vhtmode 1; nmode 1; nreqd 0; **mode_reqd 4** |
| 11ac | he enab 0; vhtmode 1; nmode 1; nreqd 0; **mode_reqd 3** |
| 11n | he enab 0; vhtmode 0; nmode 1; nreqd 1; **mode_reqd 2** |
| 11a | he enab 0; vhtmode 0; nmode 0; nreqd 0; **mode_reqd 0**（需 nmode=1 且 nreqd 才能配置） |
| 11a/n/ac | he enab 0; vhtmode 1; nmode 1; nreqd 0; mode_reqd 0 |
| 11a/n | he enab 0; vhtmode 0; nmode 1; nreqd 0; mode_reqd 0 |

### Smartmesh 漫游调试（steering/BTM）🔧

| 命令 | 功能 |
| --- | --- |
| `wbd_weak_sta_cfg_bh=1000 -75 3 50 200 0x001c` | weak backhaul sta 阈值 |
| `wbd_bkt_weak_sta_cfg_2g/5g=1000 -60 3 100 20 0x0000c` | controller 端 weak sta 发现阈值 |
| `wl0.1/wl1.1_wbd_weak_sta_cfg=1000 -60 3 100 20 0x0000c` | agent 端 weak sta 发现阈值 |
| `wbd_tbss_thld_2g=-62 1 10 36 0x7F 0` / `wbd_tbss_thld_5g=-65 ...` | control 漫游阈值 |
| `wbd_tbss_thld_bh=-70 1 10 36 0x7F 0` | weak backhaul sta 漫游阈值（wbd_tbss_algo=0 时） |
| `wl0.1_bsd_steering_policy=0 5 3 -53 0 0x3` / `wl1.1_bsd_steering_policy=0 5 3 -74 0 0x1` | 漫游阈值配置（period/cnt/chan_busy_max/rssi/phyrate/flags 六参） |
| `wl0.1_bsd_if_qualify_policy=0 0x0 0` | 接口是否有资格接受新 STA（默认不启用） |
| `bsd_steer_no_deauth` | 0=不支持 BTM 的老设备会 deauth；1=不支持的 stop steering |
| `nvram get steer_resp_timeout` | BTM_req 超时未回应归为 unknown（默认 5s），触发强踢 |
| `bsd_block_sta_timeout` / `bsd_block_sta_2g_timeout` / `wbd_tm_blk_sta` 设 0 | 漫游后短暂黑名单时间清零 |
| `wbd_steer_retry_config`（默认 "4 5"） | btm_req timeout 4s、retry 5 次 |
| `nvram set steering_msglevel=1; nvram set wbd_msglevel=0x5; nvram commit; nvram restart` | ap steer 开 log（重启仍生效） |
| `wb_cli -m msglevel -l 0x5` / `nvram set bsd_msglevel=0x4011` | 无需重启开 log |
| `bsd -l` | 查看 sta 漫游记录 |
| `wbd_ignr_maclst` | 空格分隔的 mac 不漫游 |
| `wbd_band_steer`（默认 1） | bandsteer by smartmesh 开关 |
| `nvram set bsd_ifnames=""; nvram commit; nvram restart` | 移除漫游无线接口 |
| `wb_cli -m info` / `nvram get bsd_steer_no_deauth` / `nvram get wbd_band_steer` | 查看组网设备情况 |

**weak sta 六参说明**：`(data rate阈值, rssi阈值, 上次rssi-本次rssi, txrate阈值, tx fail阈值, flags)`。flags 位：0x1 logic AND / 0x2 Active STA / 0x4 RSSI & Hysteresis / 0x8 Tx Rate / 0x10 Tx Fail，如 0xc = RSSI + Tx rate。
**steer_flags**：0x1 = BTM_rsp unknown 不强踢；0x2 = BTM_rsp reject 强踢。

## 四、ECONET 平台

### 常用操作 ⭐

| 命令 | 功能 |
| --- | --- |
| `prolinecmd serialnum/ssid/wpakey/ssidac/wpakeyac set <值>` | 写号（序列号、2.4G/5G SSID 与密钥） |
| `sys mac <mac>` | 写设备 MAC（非原厂默认 MAC 必须写） |
| `tcapi show account` | 查看账号信息（默认凭据向导师索取，注意保密，非客户需求不要变更） |
| `tcapi set Account_Entry Active Yes; tcapi save; tcapi commit Account_Entry` | 打开超级用户 🔧 |
| `sys wan2lan on 15` / `sys wan2lan off` | WAN2LAN 镜像抓包（每个 bit 对应一个 LAN 口；**实际业务时一定不要开**，会影响 WAN 业务） |
| `prolinecmd restore default` | 恢复出厂 |
| `/userfs/bin/mtd write /userfs/ctromfile_f.cfg romfile -r` | 恢复到工厂模式（romfile_f=工厂配置，romfile=非工厂配置） 🔧 |
| `tcapi show sysinfo` | ResetFlag=0 用户模式 / 1 工厂模式 |
| `cat /proc/tc3162/skyvid` / `cat /proc/tc3162/skycapability` | VID 查询 |

Telnet 开启方式为隐藏页面 URL（已剔除，向导师索取）。

### TR069 ⭐

| 命令 | 功能 |
| --- | --- |
| `tcapi show cwmp` | TR069 配置查看 |
| `tcapi set syslog_entry LogEnable Yes` + `advancedLogEnable 1` + `WriteLevel 2,0,4,1,1` + `moduleType 0,0,1,0,0` + `Cwmp_Entry dbgflag 4` + commit/save | 开启 TR069 日志 🔧 |
| `tcapi set cwmp_entry acsUrl "<ACS地址>"` + conReqUserName/conReqPassword + commit | 配置 ACS（实验室地址向导师索取） |
| `sys wan2lan on 15` + Wireshark 过滤 `ip.addr` 和 `tcp.port` | TR069 抓包 |
| `ps -ef \| grep tr69` | 查看 TR069 进程 |

### VOIP 🔧

| 命令 | 功能 |
| --- | --- |
| `tcapi show VoIPBasic` / `tcapi show VoIPAdvanced` | VOIP 配置查看 |
| `sys wan2lan on 15` + 操作电话 + Wireshark 抓 SIP | SIP 抓包 |
| `sipclient -v "0xff 0xf"` / `"0xff 0x0"` | 开/关 sipclient 日志（log 量大，可能影响正常通话振铃） |
| `insmod /lib/modules/pcmDump.ko` → `echo "0 2 1 15 <PC_IP> 3000" > /proc/vdsp/debug/pcmdump` | pcmdump 抓取 raw data（注意不要重复加载驱动） |

### OMCI & PON ⭐

| 命令 | 功能 |
| --- | --- |
| `tcapi show XPON` / `tcapi show GPON_ONU` | GPON 配置查看 |
| `prolinecmd mt7570bob display` / `echo flash_dump > /proc/pon_phy/debug` | 校准数据查看 |
| `tftp -g -r 7570_bob.conf <IP>` + `prolinecmd mt7570bob save` | 导入 bob 光参（display 全 FF 时才需导入） 🔧 |
| `echo Phy_Rogue_PRBS 1 > /proc/pon_phy/debug` + `cat /proc/pon_phy/rogue` | 长发光状态（**非必要不要用**；7529 上此验证指令无效） 🔧 |
| `ponmgr gpon get info` | PON 查询 SN、status |
| `echo msg oam/err/int/act 1 > /proc/gpon/debug`（pon_phy 同理） | 查看 activation 的 PLOAM 交互报文 |
| `echo show pwan_drop 1 > /proc/gpon/debug` / `echo show xpon_print 1 > /proc/gpon/debug` | 丢包位置查看 |
| `echo bip_cnt show > /proc/gpon/debug` | CRC 错误查看 |
| `echo pon_phy_status > /proc/pon_phy/debug` / `echo show_BoB_information > /proc/pon_phy/debug` | 确认 phy 状态与接收光功率（Rx power 正常范围 **-8 ~ -28 dBm**） ⭐ |
| `tcapi show GPON_LOIDAuth` | LOID 认证状态（Authstatus 值符合电信规范） |
| `echo gpon startup 1 > /proc/gpon/debug` | 手动 PON 重新上线 |

**对接 IOP 常用参数修改**（EN7529/EN7528）🔧：VendorID（`tcapi set GPON_ONU VendorId SKYW`）、GPON SN（`sk_test set_xponsn`，重启生效）、设备型号（`sk_test set_device_model`）、软件版本号（`tcapi set GPON_SoftImage0/1 Version`，杀 omci 进程生效）、硬件版本号（`sk_test set_hardware_version`，重启生效）。7529 还可 `selfDefVD Yes` 随配置变化。

**OMCI 抓包**⭐：OMCI 是以太网 88b5 二层报文，Wireshark 需安装 lua 插件（init.lua、omci.lua、BinDecHex.lua，覆盖安装目录，附件向导师索取）→ `sys wan2lan on 15` 开镜像 → 抓包过滤 omci。

**sniffer mode** 🔧：`dbgmgr gpon set sniffer gtc enable <0/1>`（注意各 LAN 口互相覆盖）；无 dbgmgr 的版本用寄存器 `sys memwl bfb6438c/bfb64370/bfb64390/bfb6436c/bfb6439c/bfb64368` 按 LAN port 配置。

**寄存器命令** 🔧：`sys memrl bfb640bc` 查 ONT Ox 状态（0x5=O5）；`sys memrl bfaf0130` PHY Ready 与光纤连接；`sys memrl bfaf05e0` PHY LOS；`sys memrl bfaf021c` RX SYNC（0x4a=GPON online）；`sys memrl bfb00070` WAN Mode；`sys memrl bfaf0124` PHY Mode。

### WiFi ⭐

| 命令 | 功能 |
| --- | --- |
| `tcapi show wlan`（2G）/ `tcapi show wlan11ac`（5G） | 无线配置查看 |
| `tcapi set wlan_entry2 OriginalEnableSSID 1` | 开启 SSID（EnableSSID 会自动转 StartSSID，故用此指令） |
| `iwpriv ra1/rai1 show driverinfo` | 无线驱动版本 |
| `iwpriv ra1/rai1 set Debug=3` + `iwpriv ra1/rai1 stat` | 无线 debug；循环抓日志：`while true;do iwpriv rai0 show stainfo;sleep 1;iwpriv rai0 stat;done` |
| `iwpriv ra1/rai1 show stainfo` / `tcapi show wifiMacTab` | 无线终端列表 |
| `iwpriv rai1 set ACLShowAll=1` | 驱动黑白名单（Debug level: Trace） |
| `tcapi show wifineighbortab` / `wifineighbortabweb` | 无线邻居列表 |
| `iwpriv ra1/rai1 set SiteSurvey=1` + `get_site_survey` | 无线扫描 |
| `iwpriv ra0 e2p` | 读取校准值 |
| `iwpriv rai0 set AutoChannelDisable=1/0` + `True_ACSCheckTime=900` | 自动信道检测开关与周期 |
| `iwpriv rai0 set AutoChannelSel=3/4` | AutoChannelSel=4 开启 wifi hopping（泰国 true 适配） 🔧 |
| `iwpriv rai1/ra1 show apcfginfo` / `iwpriv ra0 show SCSInfo` / EDCCA 系列 | 无线其他调试 🔧 |
| `iwpriv ra1 set FixedRate=[WCID]-[Mode]-[BW]-[MCS]-[VhtNss]-[SGI]-[Preamble]-[STBC]-[LDPC]-[SPE_EN]` | 固定速率（7613 5G 示例见原文） 🔧 |

**WiFi 校准数据操作**（EN7529 AX3000/AX3600、EN7528 AX1800）🔧：保存 `iwpriv rai1 set bufferWriteBack=4` + `sk_test save_wifi_calibration_<2g/5g>`；导出/导入用 `mtd readflash/writeflash` 操作 reservearea 分区（offset 因机型而异：AX3000 208896/311296，AX3600 131072，AX1800 4096/307200），经 tftp 传输。

**MT7916 芯片确认**⭐：版本号高于 20220803 支持新晶圆；`iwpriv ra0 mac 70010210` 返回值 0=E1、2=E2（原厂建议用 E2，E1 样机不要关注无线稳定性）。

**抗干扰调试**（7613/7603 5G/2.4G）🔧：Peak T-Put 不符预期时调 TxPower（`iwpriv wlan4 set PercentageCtrl=1; PowerDropCtrl=<值>`）；RTS/CTS 与 CTS2Self 开关（`HtProtect=0` + mac 820F2058/820F205C 四组组合）；TXOP（`TxBurst=0` + mac 820F4014）；CWmax/CWmin/AIFSN（mac 802f31a4）；SCS 档位（M/L 档 mac 值）；EDCCA 开关（`ed_chk=0`）。套路：先 Cable 后 OTA，先单 STA 定位是抗干扰还是多用户问题。

### MESH 🔧

| 命令 | 功能 |
| --- | --- |
| `tcapi show mesh` | MESH 配置查看 |
| `iwconfig rai0/ra0` + `tcapi get mesh_common MeshStatus` + `tcapi show mesh_apclibh` | Agent 当前连接信息 |
| `cat /etc/wts_bss_info_config` / `cat /etc/mapd_cfg.txt` | 服务参数 |
| `wappctrl ra0 wps_pbc` | wifi onboarding trigger |
| `mapd_cli /tmp/mapd_ctrl dump_topology_v1` / `cat /tmp/dump.txt` | 查看拓扑 |
| `mapd_cli /tmp/mapd_ctrl set log_level 3/5` | mapd debug（值越小 log 越多）；1905 daemon 用 `1905ctrl agent log_level 3`、`wappctrl /tmp/wapp_ctrl set log_level 3`（值越大越多） |
| `tcapi set mesh_common core_dump 1` + tftp 取 core 文件 | 开启 coredump |
| `mapd_cli /tmp/mapd_ctrl mib` / `mib sta <client_id>` | client id / 终端能力集与漫游统计 / Channel Utilization |
| `wappctrl ra0 map reset_default` / `tcapi unset mesh_apclibh_entry0/1` + save + commit | 清除 agent 已配置 bss |
| `tcapi show MeshRoleExchange` / `tcapi set MeshRoleExchange_Entry MeshRole 1` + commit | 自适应角色查看/设置 Controller |
| `iwpriv rai1 set no_bcn=1` | 5G 不发 beacon（测 bandsteering 到 5G；7529/7916 下指令后仍可连 5G，7528/7615 会落到 2.4G） |

### WAN & LAN ⭐

| 命令 | 功能 |
| --- | --- |
| `tcapi show wan` / `tcapi show wan.pvc.1` | WAN 配置查看 |
| `tcapi show lan` | LAN 配置查看 |

### 2.5G PHY（GPY211）🔧

排查顺序：Serdes 配置（boot: `printenv`；系统: `sys serdes`）→ PHY ko 加载（`cat /proc/modules`，LAN=hsgmii_lan.ko / WAN=ae_wan.ko）→ interface up（WAN=ae_wan，LAN=eth1 客制化）→ HSGMII 与 PHY link 状态 → gpy211_init 进程（未插网线不退出，link up 后重新初始化寄存器并退出）。

| 命令 | 功能 |
| --- | --- |
| `cat /proc/tc3162/hsgmii_lan_gphy211_link_status` / `hsgmii_lan_link_status` | 网卡/SOC HSGMII 连接状态 |
| `tce emiir 1 0x00 0x01` | PHY HSGMII 状态（0x796D bit2=1 为 link up） |
| `tce emiir 1 0x00 0x18` | 速率（bit[2:0]：000=10M / 001=100M / 010=1000M / 011=ANEG / 100=2.5G） |
| `tce emiiw 1 0 1b 0f00/0e01/0e00` | 恢复正常 / 2.5G 灯强制点亮 / 强制关闭 |
| `echo ... > /proc/tc3162/pseudo_mdio_test` + `cat /proc/tc3162/pseudo_mdio_get_value` | Iskratel GPIO 模拟 MDIO 读寄存器（SGMII 控制/状态、0.1、0.18） |

### 数据转发 🔧

| 命令 | 功能 |
| --- | --- |
| `cat /proc/tc3162/fe_debug_reg` / `fe_reg` | FE 丢包统计（打流前 `sys memwl 1fb50018 1` 清零，前后对比） |
| `cat /proc/tc3162/hsgmii_pcie0_mac_dbg` + `echo cnt clear > ...` | MAC 掉包查看/清零 |
| `ponmgr gpon get gemport` / `gponmapcmd showGemPortRule` / `echo show tcont/gem > /proc/gpon/debug` | GEM port mapping 问题排查（counter 清零 20000、Tx/Rx 10000） |
| `ponvlancmd show <11/12/13/14/0/40>` | VLAN 映射规则（LAN1~4→WAN / VEIP / 默认规则集） |
| `ponvlancmd dispfilterrule` | Filter 表查询 |
| diag.ko 加载 + `echo start/stop > /proc/tc3162/diag` | diag-onu 掉包日志（串口出现 "Diag tools inmod!" 表示加载成功） |
| `insmod /lib/modules/hw_nat.ko` / `hw_nat -g/-!/-c [n]/-U` | 硬件加速模块（加载/查看/清空/Show Foe Entry） |
| `qdmamgr_lan/wan set rxratelimit/txratelimit ...` | qdma 限速（含解除 wan 限速、关 cpu 保护） |
| `echo dbgcntr ring/clear/dump > /proc/qdma_lan/debug` | qdma Channel 0~31 TX CPU & FWD Counter |
| `ethphxcmd gsww 200c 10`（等 6 口） / `arl mactbl-disp` / `arl mactbl-clr` | 关 mac learning / 查看 / 清空 switch mac table |

### 网络层及系统 ⭐

| 命令 | 功能 |
| --- | --- |
| `top` / `mpstat -P ALL 1` | CPU 使用率 |
| `ifconfig nas0_0 down; ifconfig nas0_0 hw ether <mac>; ifconfig nas0_0 up` | 修改网络接口 MAC |
| `ip route delete/add default via <gw> dev <if> table main` | IPv4 路由 🔧 |
| `ip -6 addr add/del <addr>/64 dev <if>` | IPv6 地址 🔧 |
| `ip -6 route show/add/del` / `route -A inet6 add default gw <gw> dev <if>` | IPv6 路由 🔧 |
| `ip rule show` / `ip route show table <表>` | 策略路由 🔧 |
| `tftp -g/-p -r <file> <IP>` | tftp 下载/上传 |
| `tcpdump -i <if> [-w file.pcap] ['过滤表达式']` | 设备侧抓包（如 `'udp and port 67 and port 68'` 抓 DHCP） ⭐ |
| `cat /proc/net/nf_conntrack` | 连接跟踪表 |
| `cat /proc/tc3162/gsw_stats` / `eth_port_status` / `eth_portmap` / `gsw_link_st` | 网口状态 |
| `ethphxcmd portmirror enable 1 X` + `portmirror port-based Y 1 1 0 0 0` | LAN port Y 镜像到 X |
| `sys memrl/wl bfa20104 ...` / `echo active 3 0/1 > /proc/tc3162/gpio_output` / `echo ... > /proc/tc3162/led_def` | 点灯寄存器与 GPIO 强制操作 🔧 |
| `echo 1/2/3 > /proc/sys/vm/drop_caches` / `cat /proc/meminfo \| grep Cached` | 释放 pagecache/dentries/inodes 🔧 |
| boa debug：`cp /boaroot/* /tmp/boaroot -arf; killall -9 boa; /userfs/bin/boa -c /tmp/boaroot -f ... -d &` | BOA Debug 页面 🔧 |

IPv6 测试 DNS：百度 `2400:da00::6666`、谷歌 `2001:4860:4860::8888`。

### 常见问题解决方案 ⭐

| 现象 | 原因与对策 |
| --- | --- |
| Mesh Controller SSID 变为 MAP-UNCONF | ① SSID 中存在空格；② SSID 已开启但 /etc/wts_bss_info_config 未写入 |
| SSID 同步异常（Controller ra0→Agent ra0+ra1） | br0 MAC 第一字节第 7/8 bit 需为 0：mac 第二个字符必须是 0/4/8/C（如 20/24/28/2C 开头） |
| 页面首页出现方块乱码（写号错误） | `prolinecmd clear 1` 清空写号（**现网已写号设备不要运行！**）→ `sys mac` 重写 → `prolinecmd restore default` |
| 组播升级失败（不接收文件直接重启） | `sk_test set_multicast_upgrade_magic [0x15691358]` |
| 串口卡死 | 在 skyw_cmder.asp 页面下发 `/sbin/getty -L ttyS0 115200 vt100` |
| 高低温 PON-LAN 下行丢包（WIFI 不限速跑吞吐量） | 启动完成后 `ethphxcmd dstq mode 3; sys memwl 1fa80040 700030` |
| 2.4G 信令测试 ping 速率问题 | ping 报文默认走 1M 速率，测试需 `iwpriv ra0 set IcmpRateMode=1` |
| TestCenter 打流异常 | 加速学习需要时间，需预跑设置 |
| WiFi 2.4G+5G 同时 TX 打流重启 | 1A 电源适配器功率不够，换大功率电源 |
| 信而泰 TeleATT 打流 3/4 口几乎不通 | LAN 口终端 IP 太小（1.2~1.5）导致，改大（如 .20/.30/.40/.50）；或 `echo 0 > /proc/tc3162/hwnat_ethtype` |

### 其他 🔧

| 命令 | 功能 |
| --- | --- |
| `ethphxcmd gsww2 1 7d04/7d10/7d14 66666/77777` + `7d18` | 7526G LAN 侧 LED：先解除硬件控制（每个 6/7 代表一个口），再控制亮灭（读用 gswr2） |
| `iwpriv ra1 set be_to_vo=1; TxBurst=0; HtRdg=0; manual_txop=1` + mac 60130014/60130010=ffffffff（或 tcapi WLan_Common Aifsn/Cwmin/Cwmax 组合） | 无线 Ping 优化 |

## 原文出处

- 《应届生试用期能力建设与签核手册.xlsx》Sheet3 —— 经验文档/07 常用测试工具（隐藏页面、内网地址已剔除，向导师索取）
- 《中兴微平台调试Debug指令大全.md》—— 经验文档/07 常用测试工具（第二节 2.1~2.15 主要来源）
- 《国内路由器平台WiFi性能测试常用命令集》—— 经验文档/06 性能测试相关总结（写号/WiFi/Mesh/中兴微128R/运营商默认账号）
