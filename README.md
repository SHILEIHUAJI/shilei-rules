# Proc Alias 映射表管理与自动校验

维护 Android 应用包名（`Package Name`）到目录别名（`Alias`）的映射关系文件 `proc-alias.yaml`。

## 📁 文件说明

* `proc-alias.yaml`: 包名与别名映射表（修改此文件触发自动统计）。
* `check_proc_alias.py`: 云端自动检测与统计脚本。
* `.github/workflows/check-alias.yml`: GitHub Actions 云端工作流配置。

---

<!-- STATS_START -->
## 📊 实时数据统计大屏

### 📈 核心指标
| 统计指标 | 数量 | 状态 |
| :--- | :---: | :---: |
| 原始配置总条数 | `149` | - |
| 去重后独立应用数 | `140` | - |
| 重复包名冲突 | `9` | ❌ **存在重复** |


### ❌ 重复包名告警
| 包名 (Package Name) | 首次出现行号 | 冲突行号 |
| :--- | :---: | :---: |
| `com.google.android.apps.docs` | `第 95 行` | `第 128 行` |
| `com.google.android.apps.docs.editors.sheets` | `第 97 行` | `第 129 行` |
| `com.google.android.apps.docs.editors.slides` | `第 98 行` | `第 130 行` |
| `com.google.android.apps.tasks` | `第 106 行` | `第 132 行` |
| `com.google.android.calendar` | `第 110 行` | `第 133 行` |
| `com.google.android.apps.translate` | `第 107 行` | `第 134 行` |
| `com.google.android.apps.photos` | `第 104 行` | `第 138 行` |
| `com.google.android.apps.youtube.music` | `第 108 行` | `第 139 行` |
| `com.google.android.apps.messaging` | `第 103 行` | `第 149 行` |

> ⚠️ **请尽快在 `proc-alias.yaml` 中清理上述重复项！**

### 📦 包名分类汇总统计
| 应用分类类别 | 包含应用数 | 占比 |
| :--- | :---: | :---: |
| **Google 系应用与服务** | `55` | `39.3%` |
| **其他第三方应用** | `50` | `35.7%` |
| **GitHub / 开源与极客工具** | `7` | `5.0%` |
| **开源软件组织 (org.*)** | `7` | `5.0%` |
| **主流电商与服务 (阿里/拼多多/美团)** | `5` | `3.6%` |
| **字节跳动系 (ByteDance)** | `4` | `2.9%` |
| **vivo 厂商应用** | `4` | `2.9%` |
| **Android 系统核心组件** | `3` | `2.1%` |
| **百度系 (Baidu)** | `2` | `1.4%` |
| **微软系 (Microsoft)** | `2` | `1.4%` |
| **腾讯系 (Tencent)** | `1` | `0.7%` |


### 📋 详细分类清单
<details><summary><b>Google 系应用与服务</b> （包含 55 个应用，点击展开）</summary>

| 包名 (Package Name) | 目录别名 (Alias) | 备注 |
| :--- | :--- | :--- |
| `com.google.android.GoogleCamera` | `google-camera` | Google 相机 / Pixel Camera |
| `com.google.android.app.keyverifier` | `android-keyverifier` | Android System Key Verifier |
| `com.google.android.apps.adm` | `google-find-my-device` | 查找我的设备 |
| `com.google.android.apps.authenticator2` | `google-authenticator` | 身份验证器 |
| `com.google.android.apps.bard` | `gemini` | Gemini |
| `com.google.android.apps.books` | `google-play-books` | Google Play 图书 |
| `com.google.android.apps.chromecast.app` | `google-home` | Google Home |
| `com.google.android.apps.classroom` | `google-classroom` | Google 课堂 |
| `com.google.android.apps.docs` | `google-drive` | Google 云端硬盘 |
| `com.google.android.apps.docs.editors.docs` | `google-docs` | Google 文档 |
| `com.google.android.apps.docs.editors.sheets` | `google-sheets` | Google 表格 |
| `com.google.android.apps.docs.editors.slides` | `google-slides` | Google 幻灯片 |
| `com.google.android.apps.dynamite` | `google-chat` | Google Chat |
| `com.google.android.apps.fitness` | `google-fit` | Google Fit |
| `com.google.android.apps.googleassistant` | `google-assistant` | Google 助理 |
| `com.google.android.apps.healthdata` | `health-connect` | 健康数据共享 |
| `com.google.android.apps.keep` | `google-keep` | Google Keep 记事 |
| `com.google.android.apps.labs.language.tailwind` | `google-Notebook` | Google-笔记本 |
| `com.google.android.apps.magazines` | `google-news` | Google 新闻 |
| `com.google.android.apps.maps` | `google-maps` | 地图 |
| `com.google.android.apps.messaging` | `google-messages` | Google 信息 |
| `com.google.android.apps.nbu.files` | `google-files` | Google Files / 文件极客 |
| `com.google.android.apps.photos` | `google-photos` | Google 相册 |
| `com.google.android.apps.photosgo` | `photos-go` | 相册 (Go版) |
| `com.google.android.apps.podcasts` | `google-podcasts` | Google 播客 |
| `com.google.android.apps.tachyon` | `google-meet` | Google Meet |
| `com.google.android.apps.tasks` | `google-tasks` | Google Tasks |
| `com.google.android.apps.translate` | `google-translate` | Google 翻译 |
| `com.google.android.apps.walletnfcrerel` | `google-wallet` | Google 钱包 (Wallet) |
| `com.google.android.apps.wallpaper` | `google-wallpapers` | Google 壁纸 |
| `com.google.android.apps.wellbeing` | `digital-wellbeing` | 数字健康 |
| `com.google.android.apps.youtube.creator` | `youtube-studio` | YouTube Studio |
| `com.google.android.apps.youtube.kids` | `youtube-kids` | YouTube Kids |
| `com.google.android.apps.youtube.music` | `youtube-music` | YouTube Music |
| `com.google.android.as` | `private-compute-services` | Private Compute Services |
| `com.google.android.calculator` | `google-calculator` | Google 计算器 |
| `com.google.android.calendar` | `google-calendar` | Google 日历 |
| `com.google.android.contacts` | `google-contacts` | 通讯录 |
| `com.google.android.deskclock` | `google-clock` | Google 时钟 |
| `com.google.android.dialer` | `google-dialer` | 电话 |
| `com.google.android.gm` | `gmail` | Gmail |
| `com.google.android.gms` | `google-gms` | 谷歌服务 |
| `com.google.android.googlequicksearchbox` | `google-search` | Google 搜索 |
| `com.google.android.ims` | `carrier-services` | Carrier Services |
| `com.google.android.inputmethod.latin` | `gboard` | Gboard |
| `com.google.android.keep` | `google-keep` | Google Keep 记事 |
| `com.google.android.play.games` | `google-play-games` | Google Play 游戏 |
| `com.google.android.projection.gearhead` | `android-auto` | Android Auto |
| `com.google.android.recorder` | `google-recorder` | Google 录音机 |
| `com.google.android.safetycore` | `android-safetycore` | Android System SafetyCore |
| `com.google.android.tts` | `google-tts` | Google 语音服务 (TTS) |
| `com.google.android.videos` | `google-tv` | Google TV / Play 影视 |
| `com.google.android.youtube` | `youtube` | YouTube |
| `com.google.ar.lens` | `google-lens` | 智能镜头 |
| `com.google.earth` | `google-earth` | Google 地球 |

</details>

<details><summary><b>其他第三方应用</b> （包含 50 个应用，点击展开）</summary>

| 包名 (Package Name) | 目录别名 (Alias) | 备注 |
| :--- | :--- | :--- |
| `app.intra` | `intra` | Intra |
| `cn.wps.moffice_eng` | `wps-office` | WPS Office |
| `com.aliyun.tongyi` | `tongyi` | 千问 |
| `com.anthropic.claude` | `claude` | Claude |
| `com.apkpure.aframe` | `apkpure` | APKPure |
| `com.browser2345` | `browser2345` | 2345浏览器 |
| `com.coolapk.market` | `coolapk` | 酷安 |
| `com.ct.client` | `chinatelecom` | 中国电信 |
| `com.ddm.iptools` | `ip-tools` | IP Tools |
| `com.deepl.mobile.translator` | `deepl` | DeepL |
| `com.energy.weather` | `energy-weather` | Energy Weather |
| `com.health.mobile` | `health` | Health |
| `com.hp.printercontrol` | `hp-smart` | HP |
| `com.huawei.smarthome` | `huawei-smarthome` | 智慧生活 |
| `com.icbc` | `icbc` | 中国工商银行 |
| `com.jincheng.supercalculator` | `super-calculator` | 全能计算器 |
| `com.kwai.video` | `kwai` | Kwai |
| `com.kwai.videoeditor` | `kwai-videoeditor` | 快影 |
| `com.lenovo.safecenter` | `lenovo-safecenter` | 联想智能设备安全组件 |
| `com.lonelycatgames.Xplore` | `x-plore` | X-plore |
| `com.lovebizhi.wallpaper` | `lovebizhi` | 爱壁纸 |
| `com.lumi.lemon8` | `lemon8` | Lemon8 |
| `com.luna.music` | `luna-music` | 汽水音乐 |
| `com.meizu.flyme.calculator` | `flyme-calculator` | 计算器 |
| `com.mmbox.xbrowser` | `xbrowser` | X浏览器 |
| `com.mt.termux` | `mt-termux` | MT终端扩展包 |
| `com.nasoft.socmark` | `socmark` | 手机性能排行 |
| `com.niksoftware.snapseed` | `snapseed` | Snapseed |
| `com.ookla.speedtest` | `speedtest` | Speedtest |
| `com.openai.chatgpt` | `chatgpt` | ChatGPT |
| `com.payoneer.mobile` | `payoneer` | Payoneer |
| `com.perplexity.perplexity` | `perplexity` | Perplexity |
| `com.pipepipe.app` | `pipepipe` | PipePipe |
| `com.pranavpandey.rotation` | `rotation` | Rotation |
| `com.rhmsoft.edit` | `quickedit` | QuickEdit |
| `com.sgcc.wsgw.cn` | `wsgw` | 网上国网 |
| `com.termux` | `termux` | Termux |
| `com.twitter.android` | `twitter` | Cash M |
| `com.v2ray.ang` | `v2rayng` | v2rayNG |
| `com.waze` | `waze` | Waze 导航 |
| `com.wirelesssaleri.zipxtract` | `zipxtract` | ZipXtract |
| `com.xtc.orginwidget` | `xtc-widget` | 小天才组件 |
| `com.zhiliaoapp.musically.go` | `tiktok-lite` | TikTok Lite |
| `com.zidongdianji` | `auto-clicker` | 自动点击器 |
| `com.zoho.notebook` | `zoho-notebook` | Notebook |
| `info.myapp.appshare` | `appshare` | AppShare |
| `jp.ddo.pakutoma.unicodepad` | `unicodepad` | UnicodePad |
| `mark.via.gp` | `via-browser` | Via浏览器 |
| `sz.szsmk.citizencard` | `szsmk` | 智慧苏州 |
| `xio.javdb.fuck` | `javdb` | JavDB |

</details>

<details><summary><b>GitHub / 开源与极客工具</b> （包含 7 个应用，点击展开）</summary>

| 包名 (Package Name) | 目录别名 (Alias) | 备注 |
| :--- | :--- | :--- |
| `bin.mt.plus` | `mt-manager` | MT管理器 |
| `com.github.android` | `github` | GitHub |
| `com.github.nrfr` | `nrfr` | Nrfr |
| `io.github.samolego.canta` | `canta` | Canta |
| `li.songe.gkd` | `gkd` | GKD |
| `moe.shizuku.privileged.api` | `shizuku` | Shizuku |
| `org.fdroid.fdroid` | `fdroid` | F-Droid |

</details>

<details><summary><b>开源软件组织 (org.*)</b> （包含 7 个应用，点击展开）</summary>

| 包名 (Package Name) | 目录别名 (Alias) | 备注 |
| :--- | :--- | :--- |
| `org.breezyweather` | `breezy-weather` | Breezy Weather |
| `org.localsend.localsend_app` | `localsend` | LocalSend |
| `org.mozilla.firefox` | `firefox` | Firefox |
| `org.telegram.messenger` | `telegram` | Telegram |
| `org.torproject.torbrowser` | `tor-browser` | Tor Browser |
| `org.videolan.vlc` | `vlc` | VLC |
| `org.wikipedia` | `wikipedia` | Wikipedia |

</details>

<details><summary><b>主流电商与服务 (阿里/拼多多/美团)</b> （包含 5 个应用，点击展开）</summary>

| 包名 (Package Name) | 目录别名 (Alias) | 备注 |
| :--- | :--- | :--- |
| `com.eg.android.AlipayGphone` | `alipay` | 支付宝 |
| `com.sankuai.meituan` | `meituan` | 美团 |
| `com.taobao.idlefish` | `idlefish` | 闲鱼 |
| `com.taobao.taobao` | `taobao` | 淘宝 |
| `com.xunmeng.pinduoduo` | `pinduoduo` | 拼多多 |

</details>

<details><summary><b>字节跳动系 (ByteDance)</b> （包含 4 个应用，点击展开）</summary>

| 包名 (Package Name) | 目录别名 (Alias) | 备注 |
| :--- | :--- | :--- |
| `com.bytedance.android.ludao.online` | `ludao` | 笨包路人谈 |
| `com.ss.android.article.news` | `toutiao` | 头条搜索 |
| `com.ss.android.ugc.aweme` | `aweme` | 抖音 |
| `com.ss.android.ugc.trill` | `tiktok` | TikTok |

</details>

<details><summary><b>vivo 厂商应用</b> （包含 4 个应用，点击展开）</summary>

| 包名 (Package Name) | 目录别名 (Alias) | 备注 |
| :--- | :--- | :--- |
| `com.vivo.ada` | `vivo-ada` | 售后诊断助手 |
| `com.vivo.calculator` | `vivo-calculator` | vivo计算器 |
| `com.vivo.gallery` | `vivo-gallery` | vivo相册 |
| `com.vivo.remotepass` | `vivo-remote` | 客服协助 |

</details>

<details><summary><b>Android 系统核心组件</b> （包含 3 个应用，点击展开）</summary>

| 包名 (Package Name) | 目录别名 (Alias) | 备注 |
| :--- | :--- | :--- |
| `com.android.calculator2` | `calculator` | 计算器 |
| `com.android.chrome` | `chrome` | Chrome |
| `com.android.vending` | `google-play-store` | Google Play 商店 |

</details>

<details><summary><b>百度系 (Baidu)</b> （包含 2 个应用，点击展开）</summary>

| 包名 (Package Name) | 目录别名 (Alias) | 备注 |
| :--- | :--- | :--- |
| `com.baidu.dict` | `baidu-dict` | 百度汉语 |
| `com.baidu.tieba` | `baidu-tieba` | 百度贴吧 |

</details>

<details><summary><b>微软系 (Microsoft)</b> （包含 2 个应用，点击展开）</summary>

| 包名 (Package Name) | 目录别名 (Alias) | 备注 |
| :--- | :--- | :--- |
| `com.microsoft.copilot` | `copilot` | Copilot |
| `com.microsoft.emmx` | `edge` | Edge |

</details>

<details><summary><b>腾讯系 (Tencent)</b> （包含 1 个应用，点击展开）</summary>

| 包名 (Package Name) | 目录别名 (Alias) | 备注 |
| :--- | :--- | :--- |
| `com.tencent.mm` | `wechat` | 微信 |

</details>

<!-- STATS_END -->
