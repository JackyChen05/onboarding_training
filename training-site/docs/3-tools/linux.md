# 3.4 Linux 常用命令

## 目标

设备 shell（串口/Telnet/ADB）上独立完成日常观测与操作。嵌入式 Linux 多为 BusyBox 精简环境，命令以实用为准。

## 高频命令速查

| 场景 | 命令 | 说明 |
| --- | --- | --- |
| 运行时长 | `uptime` | 长稳测试起点记录 |
| 内存观测 | `free`、`cat /proc/meminfo` | 趋势判据：持续上升 = 泄漏嫌疑 |
| 进程 | `ps`、`top` | 定位异常进程与 CPU 占用 |
| 端口与连接 | `netstat -nap` | 对外服务进程清点（安全测试也用它，见《联通FTTR进程权限最小化测试方法》） |
| 网卡状态 | `ifconfig` / `ip addr`、`ethtool` | 协商速率核对 |
| 抓包 | `tcpdump -s0 -w /data/xx.cap` | 设备侧抓包 |
| 日志 | `logread`、`dmesg`、`cat /var/log/messages` | 系统日志与内核消息 |
| 文件系统 | `df -h`、`du`、`ls -l /data` | 存储写满是常见失效 |
| 闪存/分区 | `cat /proc/mtd` | 升级、烧录相关 |
| 进程权限 | `capsh --print` | 权限最小化测试 |
| 无线 | `iwconfig`、`iw dev`、`wl`（博通） | 无线状态与参数 |

## 长稳观测套路（配合手册练习 2-9）

连续多天定时记录 `uptime` + 内存占用 + 连接终端数，画折线看单调趋势——**判据是趋势斜率，不是绝对阈值**（手册 2.5 要点 4）。

## Windows 侧 CMD 基本诊断

测试 PC 侧（非设备 shell）常用 CMD 命令做链路诊断：

| 命令 | 用途 |
| --- | --- |
| `ping <IP> -t` / `-l <大小>` | 连通性与长ping；大包测分片/MTU |
| `arp -a` | 查看 ARP 缓存表（IP↔MAC 映射） |
| `ipconfig /all` `/flushdns` | 网卡配置全览；清 DNS 缓存（排查解析异常） |
| `tracert <IP>` | 路由跳数追踪，定位断点在哪一跳 |
| `netstat -ano` | PC 本机端口与连接占用 |
| `nslookup <域名>` | DNS 解析验证 |

这些是「环境问题还是设备问题」分层定位的第一刀——先用 PC 侧命令确认链路通不通、解析对不对，再上设备 shell。

## 验收 checklist（导师签核项）

- [ ] 不看文档完成：登 shell → 查 uptime/内存/进程 → 抓包 1 分钟 → 导出日志
- [ ] 用 `netstat -nap` 清点一台网关的全部对外服务进程
- [ ] 说出 `top` 中 load average 与单核 CPU 的关系（嵌入式单核/多核）
- [ ] 找到日志轮转配置并说明覆盖风险

## 扩展阅读（ima 测试知识库）

- 《24、电信TN接口linux环境搭建指导》—— Linux 测试环境搭建
- 《联通FTTR进程权限最小化测试方法及说明》—— netstat + capsh 实战
- 《嵌入式产品测试（外网链接）》—— OpenWrt netifd/ubus/procd 等进阶阅读

### 本地经验文档（D:\WorkbuddySpace\Testwiki\经验文档）

- 《中兴微方案常用指令集V1.0》—— 中兴微平台 shell 命令速查（13 组内总结）
- 《联通智能相关命令》—— 联通平台设备命令集（006/网关/45）
- 《DBUS接口命令集》—— 电信 DBUS 接口命令（006/网关/43）
- 《OSGITest工具命令集》—— OSGI 插件测试命令（006/网关/51）
- 《Ubuntu下使用Kea搭建DHCP服务器》《Ubuntu下搭建Speedtest测速服务器》—— Linux 服务器搭建（006/网关/57、58）
- 《CMD基本诊断指令》—— Windows 侧 ping/arp/ipconfig/tracert 诊断（07 常用测试工具）
