# 3.1 抓包分析（Wireshark / xcap）

## 抓包环境搭建（三种方式）

按《抓包工具wireshark常用方法介绍》（测试部 易秋兰）：

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

知识库《wireshark和xcap使用分享》（周鹏）给出完整工作流：用 Wireshark 协助构造需要的报文 → 用 xcap 从指定网卡发送出去。适用场景：需要发送特定报文给网关而没有现成设备能发（实例：测试 dhcpd option 60 校验功能）。xcap 依赖 winpcap，报版本错误时装高版本 winpcap（《xcap发包工具使用方法》- 罗琪）。

## 分析产出要求

抓包分析的产出不是 pcap 文件本身，而是**结论 + 证据**：关键报文截图、时序说明、与标准/预期的差异点。缺陷提报时作为证据链附件（见 [4.3 缺陷证据链](/4-defects/evidence)）。

## 验收 checklist（导师签核项）

- [ ] 用镜像交换机抓到一次完整 DHCP 四步，逐包讲解
- [ ] 用 tcpdump 在设备侧抓包并导出分析
- [ ] 用过滤式定位一次 TCP 重传问题
- [ ] 用 xcap 构造并发送一个带指定 Option 的 DHCP 报文
- [ ] 产出一份「结论 + 证据」的抓包分析记录

## 扩展阅读（ima 测试知识库）

- 《Wireshark 抓包.pdf》- 王琰琳 —— 部门标准教程
- 《抓包工具wireshark常用方法介绍.ppt》- 易秋兰；《wireshark介绍.ppt》- 罗君
- 《wireshark和xcap使用分享》- 周鹏；《xcap发包工具使用方法》- 罗琪
- 《Win7 设置PC抓取带vlan数据包设置》—— VLAN 环境抓包配置
