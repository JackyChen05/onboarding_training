import { defineConfig } from 'vitepress'

export default defineConfig({
  title: '嵌入式产品测试 · 应届生培训',
  description: '软件测试工程师入职培训学习站',
  lang: 'zh-CN',
  cleanUrls: true,
  lastUpdated: true,
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '培训路径', link: '/path' },
      { text: '1 产品知识', link: '/1-access/' },
      { text: '2 多媒体产品', link: '/2-multimedia/' },
      { text: '3 常用工具', link: '/3-tools/' },
      { text: '4 缺陷库', link: '/4-defects/' },
      { text: '5 典型案例', link: '/5-cases/' },
      { text: '维护规范', link: '/maintenance' }
    ],
    sidebar: {
      '/1-access/': [
        {
          text: '1. 产品知识（接入产品）',
          items: [
            { text: '模块总览', link: '/1-access/' },
            { text: '1.1 PON 架构（OLT/ONU/ODN）', link: '/1-access/pon' },
            { text: '1.2 注册与 OMCI', link: '/1-access/omci' },
            { text: '1.3 DBA 带宽分配', link: '/1-access/dba' },
            { text: '1.4 TR-069 / TR-369 远程管理', link: '/1-access/tr069' },
            { text: '1.5 关键协议（DHCP/PPPoE/NAT/TCP/UDP/IP）', link: '/1-access/protocols' },
            { text: '1.6 Wi-Fi 关键指标', link: '/1-access/wifi' },
            { text: '1.7 测试环境搭建与验收标准', link: '/1-access/env' }
          ]
        }
      ],
      '/2-multimedia/': [
        {
          text: '2. 多媒体产品',
          items: [
            { text: '模块总览', link: '/2-multimedia/' },
            { text: '2.1 系统架构', link: '/2-multimedia/arch' },
            { text: '2.2 关键协议（IGMP/RTSP/HLS/DASH）', link: '/2-multimedia/protocols' },
            { text: '2.3 CAS / DRM 与 HDMI / HDCP', link: '/2-multimedia/drm' },
            { text: '2.4 核心业务功能', link: '/2-multimedia/features' },
            { text: '2.5 测试环境搭建与验收标准', link: '/2-multimedia/env' }
          ]
        }
      ],
      '/3-tools/': [
        {
          text: '3. 常用工具（可独立操作）',
          items: [
            { text: '模块总览与验收方式', link: '/3-tools/' },
            { text: '3.1 抓包分析（Wireshark / xcap）', link: '/3-tools/wireshark' },
            { text: '3.2 串口与系统日志抓取', link: '/3-tools/serial' },
            { text: '3.3 码流 / 媒体分析', link: '/3-tools/stream' },
            { text: '3.4 Linux 常用命令', link: '/3-tools/linux' },
            { text: '3.5 版本与缺陷管理工具', link: '/3-tools/defect-tools' }
          ]
        }
      ],
      '/4-defects/': [
        {
          text: '4. 缺陷库',
          items: [
            { text: '模块总览', link: '/4-defects/' },
            { text: '4.1 缺陷生命周期与提报规范', link: '/4-defects/lifecycle' },
            { text: '4.2 缺陷模式分类', link: '/4-defects/patterns' },
            { text: '4.3 缺陷证据链要求', link: '/4-defects/evidence' }
          ]
        }
      ],
      '/5-cases/': [
        {
          text: '5. 典型案例',
          items: [
            { text: '模块总览', link: '/5-cases/' },
            { text: '5.1 运营商入库测试经验', link: '/5-cases/operator' },
            { text: '5.2 现网问题复盘', link: '/5-cases/field' },
            { text: '5.3 环境搭建典型案例', link: '/5-cases/env-cases' }
          ]
        }
      ]
    },
    search: {
      provider: 'local',
      options: {
        locales: {
          root: {
            translations: {
              button: { buttonText: '搜索', buttonAriaLabel: '搜索' },
              modal: {
                noResultsText: '未找到相关结果',
                resetButtonTitle: '清除',
                footer: { selectText: '选择', navigateText: '切换', closeText: '关闭' }
              }
            }
          }
        }
      }
    },
    outline: { level: [2, 3], label: '本页目录' },
    docFooter: { prev: '上一页', next: '下一页' },
    lastUpdatedText: '最后更新',
    returnToTopLabel: '回到顶部',
    sidebarMenuLabel: '菜单',
    darkModeSwitchLabel: '外观'
  }
})
