# 3.1 抓包分析（Wireshark / xcap）

## 抓包环境搭建（三种方式）

按《抓包工具wireshark常用方法介绍》（测试部）：

1. **镜像交换机**（推荐）：抓包专用交换机做端口镜像。不要用 hub——速率只能到 10M。
2. **串口 tcpdump**：设备上执行 `tcpdump -s0 -w /data/xx.cap`，不方便实时查看但最贴近设备侧。
3. **串口开启镜像抓包**：路由器/网关类产品支持的镜像功能。

无线空口抓包另见 [1.6 Wi-Fi 抓包](/1-access/wifi#无线抓包)。

## 常用过滤

| 目的 | 过滤式 |
| --- | --- |
| DHCP | `bootp` |
| PPPoE | `pppoed` / `pppoes` |
| IGMP | `igmp` |
| TR-069 | `tcp.port == 7547` |
| 指定 IP | `ip.addr == 192.168.1.1` |
| TCP 重传（找丢包） | `tcp.analysis.retransmission` |

## xcap 构造与发送报文

适用场景：需要发送特定报文给网关，但没有现成设备能发（例如验证网关对带某个 Option 的 DHCP 报文的校验逻辑）。完整工作流（实例：测试 dhcpd option 60 校验功能）：

**第一步：用 Wireshark 构造报文**

1. 先抓一个同类真实报文（如 DHCP discovery）作模板。
2. 在 Frame 层右键 → 复制 → as hex string，得到报文的十六进制字符串。
3. 对照 Wireshark「分组详情」窗口点选字段时内容区的高亮，定位要修改的字节位置（如 option 60 字段）。
4. 在文本编辑器里把目标字段替换为测试值，得到构造好的完整报文 hex 串。

**第二步：用 xcap 发送**

1. 接口列表选发送网卡，右键 start interface。
2. 新建分组，导入/粘贴构造好的报文，设置发送速率。
3. 发送后在接收侧抓包，确认报文按预期到达、网关行为符合校验逻辑。

注意：xcap 依赖 winpcap，报版本错误时安装更高版本 winpcap（《xcap发包工具使用方法》）。

## 分析产出要求

抓包分析的产出不是 pcap 文件本身，而是**结论 + 证据**：关键报文截图、时序说明、与标准/预期的差异点。缺陷提报时作为证据链附件（见 [4.3 缺陷证据链](/4-defects/evidence)）。

## 验收 checklist（导师签核项）

- [ ] 用镜像交换机抓到一次完整 DHCP 四步，逐包讲解
- [ ] 用 tcpdump 在设备侧抓包并导出分析
- [ ] 用过滤式定位一次 TCP 重传问题
- [ ] 用 xcap 构造并发送一个带指定 Option 的 DHCP 报文
- [ ] 产出一份「结论 + 证据」的抓包分析记录

## 扩展阅读（ima 测试知识库）

- 《Wireshark 抓包.pdf》 —— 部门标准教程
- 《抓包工具wireshark常用方法介绍.ppt》；《wireshark介绍.ppt》
- 《wireshark和xcap使用分享》；《xcap发包工具使用方法》
- 《Win7 设置PC抓取带vlan数据包设置》—— VLAN 环境抓包配置

### 本地经验文档（D:\WorkbuddySpace\Testwiki\经验文档）

- 《wireshark和xcap使用分享》—— 构造 dhcpd option 60 报文并发送（006/根目录）
- 《WiFi6抓包指导》—— Linux+Intel 网卡替代 Omnipeek 抓 WiFi6 数据帧（006/路由器/2）
- 《Omnipeek无线抓包以及802.11报文解析》—— 无线抓包与 802.11 帧解析（07 工具）
- 《网络性能测试工具Iperf介绍》—— TCP 吞吐/UDP 丢包时延测试（07 工具）
- 《web安全扫描&nessus漏洞扫描》《Web漏洞扫描工具AWVS安装及使用方法》—— 漏洞扫描工具（07 工具、006/网关/56）
- 《使用Burp Suite暴力破解密码》 +《Brup suit 工具Web拦截测试指导》—— Web 拦截与爆破测试（006/网关/36、路由器/18）
