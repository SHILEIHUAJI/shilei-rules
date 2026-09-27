# Proc Alias 映射表管理与自动校验

维护 Android 应用包名（`Package Name`）到目录别名（`Alias`）的映射关系文件 `proc-alias.yaml`。

## 📁 文件说明

* `proc-alias.yaml`: 包名与别名映射表（修改此文件触发自动统计）。
* `check_proc_alias.py`: 云端自动检测与统计脚本。
* `.github/workflows/check-alias.yml`: GitHub Actions 云端工作流配置。

---

<!-- STATS_START -->
## 📊 包名数据可视化统计大屏

### 📈 概览
- **配置文件总行数**: `276` 条
- **独立有效应用数**: `276` 个
- **重复包名状态**: ✅ **校验通过 (无重复)**


### 🎨 应用分类分布饼图

```mermaid
pie title 包名分类占比统计
    "vivo 厂商应用" : 122
    "其他第三方应用" : 61
    "Google 系应用" : 54
    "GitHub/开源极客工具" : 9
    "开源组织应用" : 9
    "Android 系统组件" : 7
    "主流电商与服务" : 5
    "字节跳动系" : 4
    "百度系" : 2
    "微软系" : 2
    "腾讯系" : 1
```

### 📋 分类列表明细
<details><summary><b>vivo 厂商应用</b> （包含 122 个应用）</summary>

| 包名 (Package Name) | 目录别名 (Alias) | 备注 |
| :--- | :--- | :--- |
| `com.vivo.SmartKey` | `quick-launch` | 快捷启动 |
| `com.vivo.abe` | `smart-engine` | 智慧引擎 |
| `com.vivo.accessibility` | `accessibility` | 无障碍 |
| `com.vivo.accessibilityenhance` | `accessibility-enhance` | 无障碍增强 |
| `com.vivo.agent` | `jovi-voice` | Jovi语音 |
| `com.vivo.ai.copilot` | `blueheart-v` | 蓝心小V |
| `com.vivo.aiengine` | `ai-engine` | 智慧服务 |
| `com.vivo.aiservice` | `ai-service` | AIService |
| `com.vivo.alldocuments` | `all-documents-viewer` | vivo万能查看器 |
| `com.vivo.alphacamera` | `alpha-camera` | AlphaCamera |
| `com.vivo.android.connectivity.mainline.common.resources.overlay` | `conn-common-overlay` | 连接通用覆盖层 |
| `com.vivo.android.connectivity.mainline.manufacturer.resources.overlay` | `connectivity-overlay` | 连接资源覆盖层 |
| `com.vivo.android.wifi.common.resources.overlay` | `wifi-common-overlay` | WiFi通用资源覆盖层 |
| `com.vivo.android.wifi.mainline.manufacturer.resources.overlay` | `wifi-mainline-overlay` | WiFi主线路资源覆盖层 |
| `com.vivo.android.wifi.mainline.platform.resources.overlay` | `wifi-mainline-platform-overlay` | WiFi主线平台覆盖层 |
| `com.vivo.android.wifi.manufacturer.resources.overlay` | `wifi-mfg-overlay` | WiFi厂商资源覆盖层 |
| `com.vivo.android.wifi.platform.resources.overlay` | `wifi-platform-overlay` | WiFi平台资源覆盖层 |
| `com.vivo.appfilter` | `pull-up-prevent-service` | 防拉起服务 |
| `com.vivo.assistant` | `important-notification` | 重要通知 |
| `com.vivo.audiofx` | `audio-effects` | 音效设置 |
| `com.vivo.base.player` | `system-audio-player` | 系统音频播放器 |
| `com.vivo.bsptest` | `bsp-test` | BSP测试 |
| `com.vivo.car.launcher` | `car-launcher` | 车载launcher |
| `com.vivo.car.networking` | `smart-car-networking` | 智能车载 |
| `com.vivo.card` | `super-card-wallet` | 超级卡包 |
| `com.vivo.cipherchain` | `cipher-vault` | 密码保险箱 |
| `com.vivo.compass` | `compass` | 指南针 |
| `com.vivo.connbase` | `multi-device-connect` | 多设备互联 |
| `com.vivo.connbase.sysui` | `control-center` | ControlCenter |
| `com.vivo.cota` | `cota` | COTA升级 |
| `com.vivo.countdownwidget` | `countdown-widget` | 计时器组件 |
| `com.vivo.daemonService` | `vivo-service-daemon` | vivo服务 |
| `com.vivo.defaultPlayer` | `default-player` | 视频播放器 |
| `com.vivo.desktopstickers` | `desktop-stickers` | 贴纸 |
| `com.vivo.devicepower` | `device-power` | 设备电量 |
| `com.vivo.devicereg` | `device-management` | 设备管理 |
| `com.vivo.doubleinstance` | `app-clone` | 应用分身 |
| `com.vivo.doubletimezoneclock` | `dual-clock-widget` | i挂件 |
| `com.vivo.easyshare` | `easyshare` | 互传 |
| `com.vivo.faceui` | `face-ui` | FaceUI |
| `com.vivo.faceunlock` | `face-unlock` | 面部识别 |
| `com.vivo.familycare.local` | `familycare-local` | 健康使用设备 |
| `com.vivo.favorite` | `favorite` | 收藏 |
| `com.vivo.findphone` | `find-phone` | 查找 |
| `com.vivo.fingerprint` | `fingerprint-unlock` | 指纹与密码 |
| `com.vivo.fingerprintui` | `fingerprint-ui` | 指纹UI组件 |
| `com.vivo.fingerprintvit` | `fingerprint-vit` | 指纹组件 |
| `com.vivo.floatingball` | `floating-ball` | 悬浮球 |
| `com.vivo.gallery` | `vivo-gallery` | vivo相册 |
| `com.vivo.gamecube` | `gamecube` | 游戏魔盒 |
| `com.vivo.gametrain` | `sound-position-train` | 听音辨位训练场 |
| `com.vivo.globalanimation` | `global-animation` | 全局动效 |
| `com.vivo.globalanimation.resources` | `global-animation-res` | 全局动画资源 |
| `com.vivo.globalsearch` | `global-search` | 全局搜索 |
| `com.vivo.health` | `vivo-health` | vivo健康 |
| `com.vivo.healthservice` | `health-service` | 健康服务 |
| `com.vivo.healthwidget` | `health-widget` | 健康组件 |
| `com.vivo.hiboard` | `smart-desktop` | 智慧桌面 |
| `com.vivo.hybrid` | `quick-app-framework` | 快应用框架服务 |
| `com.vivo.iotserver` | `iot-engine` | IoT服务引擎 |
| `com.vivo.launchercopilot` | `blueheart-v-widget` | 蓝心小V组件 |
| `com.vivo.livewallpaper.box` | `live-wallpaper-box` | 动态壁纸盒子 |
| `com.vivo.magazine` | `lockscreen-magazine` | 阅图锁屏 |
| `com.vivo.minscreen` | `mini-screen` | 小屏 |
| `com.vivo.moodcube` | `morph-engine` | 变形器 |
| `com.vivo.motionrecognition` | `motion-recognition` | 智能体感 |
| `com.vivo.multinlp` | `location-service` | 定位服务 |
| `com.vivo.musicwidgetmix` | `atom-music-widget` | 原子随身听 |
| `com.vivo.networkimprove` | `network-improve` | 网络优化 |
| `com.vivo.networkstate` | `network-state` | 网络状态 |
| `com.vivo.nightpearl` | `night-pearl` | 熄屏显示 |
| `com.vivo.numbermark` | `number-mark` | 陌电识别 |
| `com.vivo.pay` | `multi-scene-secure-pay` | 多场景安全支付服务 |
| `com.vivo.pcsuite` | `pc-suite` | vivo办公套件 |
| `com.vivo.pem` | `power-guard` | 电量守护 |
| `com.vivo.permissionmanager` | `permission-manager` | 权限管理 |
| `com.vivo.phonehandoff` | `phone-handoff` | 通话接力 |
| `com.vivo.privacylauncher` | `privacy-launcher` | 隐私桌面 |
| `com.vivo.pushservice` | `push-service` | 推送引擎 |
| `com.vivo.quickpay` | `quick-pay` | 快捷支付 |
| `com.vivo.remotassistant` | `remote-assistant` | 远程协助 |
| `com.vivo.remotemplugin` | `vivo-remote` | 客服协助 ✅ 修正：原com.vivo.remotepass |
| `com.vivo.safecenter` | `safe-center` | 安全中心 |
| `com.vivo.screenagent` | `v-note-helper` | 小V帮记 |
| `com.vivo.sda` | `vivo-sda` | 售后诊断助手 ✅ 修正：原com.vivo.ada |
| `com.vivo.sdkplugin` | `service-secure-plugin` | vivo服务安全插件 |
| `com.vivo.seservice` | `digital-car-key` | 数字车钥匙服务 |
| `com.vivo.setupwizard` | `setup-wizard` | 开机引导 |
| `com.vivo.share` | `vivo-share` | vivo互传 |
| `com.vivo.sim.contacts` | `sim-contacts-service` | SIM卡联系人服务 |
| `com.vivo.simpleiconthemeres` | `simple-icon-theme-res` | 简约图标主题资源 |
| `com.vivo.singularity` | `vivo-webview` | vivo系统WebView |
| `com.vivo.smartanswer` | `smart-answer` | 电话秘书 |
| `com.vivo.smartmultiwindow` | `smart-multiwindow` | 多任务 |
| `com.vivo.smartshot` | `smart-screenshot` | 超级截屏 |
| `com.vivo.smartunlock` | `smart-unlock` | 智能解锁 |
| `com.vivo.sos` | `sos-emergency` | 紧急呼叫 |
| `com.vivo.space` | `vivo-official-site` | vivo官网 |
| `com.vivo.sps` | `super-process-system` | SuperProcessSystem |
| `com.vivo.symmetry` | `vivo-camera` | vivo摄影 |
| `com.vivo.systemblur.server` | `system-blur-server` | SystemBlur |
| `com.vivo.systemuiplugin` | `system-ui-plugin` | 系统界面组件 |
| `com.vivo.third.numbermark` | `third-number-mark` | 陌生电话识别组件 |
| `com.vivo.translator` | `translator` | 翻译机 |
| `com.vivo.upnp.server` | `dlna-server` | 投屏 |
| `com.vivo.upslide` | `interaction-pool` | 交互池 |
| `com.vivo.vdfs` | `cross-device-share` | 跨设备使用 |
| `com.vivo.vhomeguide` | `v-home-guide` | VHome指引 |
| `com.vivo.vibrator4d` | `vibrator-4d` | 4D振感 |
| `com.vivo.video.floating` | `video-beauty` | 视频通话美颜 |
| `com.vivo.videoservice` | `video-editor` | 视频编辑 |
| `com.vivo.vivo3rdalgoservice` | `image-algo-service` | ImageAlgoService |
| `com.vivo.vms` | `vivo-mobile-service` | vivo移动服务 |
| `com.vivo.voicerecognition` | `voice-recognition` | 声音识别 |
| `com.vivo.voicewakeup` | `voice-wakeup` | 语音唤醒 |
| `com.vivo.vtouch` | `scan-assistant` | 扫描 |
| `com.vivo.wallet` | `vivo-wallet` | vivo 钱包 |
| `com.vivo.weather.provider` | `weather-provider` | 天气存储 |
| `com.vivo.widget.calendar` | `calendar-widget` | 日历组件 |
| `com.vivo.widget.cleanspeed` | `clean-speed` | 清理加速组件 |
| `com.vivo.widget.healthcare` | `healthcare-widget` | 健康关怀 |
| `com.vivo.xspace` | `atom-privacy-system` | 原子隐私系统 |

</details>

<details><summary><b>其他第三方应用</b> （包含 61 个应用）</summary>

| 包名 (Package Name) | 目录别名 (Alias) | 备注 |
| :--- | :--- | :--- |
| `ai.perplexity.app.android` | `perplexity` | Perplexity ✅ 修正：原com.perplexity.perplexity |
| `android.overlay.vivoresrro` | `vivo-res-overlay` | vivo资源覆盖层 |
| `app.intra` | `intra` | Intra |
| `cn.wps.moffice_eng` | `wps-office` | WPS Office |
| `com.aliyun.tongyi` | `tongyi` | 千问 |
| `com.anthropic.claude` | `claude` | Claude |
| `com.apkpure.aegon` | `apkpure` | APKPure ✅ 修正：原com.apkpure.aframe |
| `com.bbk.account` | `bbk-account` | vivo账号 |
| `com.bbk.theme.resources` | `wallpaper-res` | vivo壁纸资源 |
| `com.bd.nproject` | `lemon8` | Lemon8 ✅ 修正：原com.lumi.lemon8 |
| `com.browser2345` | `browser2345` | 2345浏览器 |
| `com.cctv.yangshipin.app.androidp` | `yangshipin` | 央视频 |
| `com.coolapk.market` | `coolapk` | 酷安 |
| `com.ct.client` | `chinatelecom` | 中国电信 |
| `com.ddm.iptools` | `ip-tools` | IP Tools |
| `com.deepl.mobiletranslator` | `deepl` | DeepL ✅ 修正：多了点→连写 |
| `com.fitbit.FitbitMobile` | `health-mobile` | Health ✅ 修正：原com.health.mobile |
| `com.hp.printercontrol` | `hp-smart` | HP |
| `com.huawei.smarthome` | `huawei-smarthome` | 智慧生活 |
| `com.icbc` | `icbc` | 中国工商银行 |
| `com.jincheng.supercaculator` | `super-calculator` | 全能计算器 ✅ 修正：故意少l→caculator |
| `com.kwai.video` | `kwai` | Kwai |
| `com.kwai.videoeditor` | `kwai-videoeditor` | 快影 |
| `com.larus.wolf` | `dola` | Dola(字节海外AI) ✅ 补充 |
| `com.lenovo.safecenter` | `lenovo-safecenter` | 联想智能设备安全组件 |
| `com.lonelycatgames.Xplore` | `x-plore` | X-plore |
| `com.lovebizhi.wallpaper` | `lovebizhi` | 爱壁纸 |
| `com.luna.music` | `luna-music` | 汽水音乐 |
| `com.meizu.flyme.calculator` | `meizu-calculator` | 魅族计算器 |
| `com.mmbox.xbrowser` | `xbrowser` | X浏览器 |
| `com.nasoft.socmark` | `socmark` | 手机性能排行 |
| `com.nebula.clashmi` | `clash-mi` | Clash Mi ✅ 补充 |
| `com.niksoftware.snapseed` | `snapseed` | Snapseed |
| `com.ookla.speedtest` | `speedtest` | Speedtest |
| `com.openai.chatgpt` | `chatgpt` | ChatGPT |
| `com.payoneer.mobile` | `payoneer` | 派安盈 |
| `com.pikcloud.pikpak` | `pikpak` | PikPak网盘 ✅ 补充 |
| `com.pinterest` | `pinterest` | Pinterest ✅ 补充 |
| `com.pranavpandey.rotation` | `rotation` | Rotation |
| `com.rhmsoft.edit` | `quickedit` | QuickEdit |
| `com.sgcc.wsgw.cn` | `wsgw` | 网上国网 |
| `com.tailscale.ipn` | `tailscale` | Tailscale ✅ 补充 |
| `com.termux` | `termux` | Termux |
| `com.tiktok.lite.go` | `tiktok-lite` | TikTok Lite |
| `com.twitter.android` | `twitter` | Twitter / X |
| `com.v2ray.ang` | `v2rayng` | v2rayNG |
| `com.v2ray.ang.fdroid` | `v2rayng-fdroid` | v2rayNG(F-Droid版) ✅ 补充变体 |
| `com.waze` | `waze` | Waze 导航 |
| `com.wirelessalien.zipxtract` | `zipxtract` | ZipXtract ✅ 修正：saleri→alien |
| `com.xiaomi.smarthome` | `mijia` | 米家 |
| `com.xtc.originwidget` | `xtc-widget` | 小天才组件 ✅ 修正：少i→originwidget |
| `com.yozo.vivo.office` | `vivo-document` | vivo文档 |
| `com.zhiliaoapp.musically` | `tiktok` | TikTok国际版 ✅ 修正+补充 |
| `com.zidongdianji` | `auto-clicker` | 自动点击器 |
| `com.zoho.notebook` | `zoho-notebook` | Notebook |
| `info.muge.appshare` | `appshare` | AppShare ✅ 修正：myapp→muge |
| `jp.ddo.hotmist.unicodepad` | `unicodepad` | UnicodePad ✅ 修正：pakutoma→hotmist |
| `mark.via.gp` | `via-browser` | Via浏览器 |
| `sz.szsmk.citizencard` | `szsmk` | 智慧苏州 |
| `tw.nekomimi.nekogram` | `nekogram` | Nekogram ✅ 补充 |
| `xxx.pornhub.fuck` | `javdb` | JavDB ✅ 修正：xio→xxx |

</details>

<details><summary><b>Google 系应用</b> （包含 54 个应用）</summary>

| 包名 (Package Name) | 目录别名 (Alias) | 备注 |
| :--- | :--- | :--- |
| `com.google.android.GoogleCamera` | `google-camera` | Google 相机 |
| `com.google.android.apps.adm` | `google-find-my-device` | 查找我的设备 |
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
| `com.google.android.apps.labs.language.tailwind` | `google-notebook` | Google笔记本 |
| `com.google.android.apps.magazines` | `google-news` | Google 新闻 |
| `com.google.android.apps.maps` | `google-maps` | 地图 |
| `com.google.android.apps.messaging` | `google-messages` | Google 信息 |
| `com.google.android.apps.nbu.files` | `google-files` | Google Files / 文件极客 |
| `com.google.android.apps.photos` | `google-photos` | Google 相册 |
| `com.google.android.apps.photosgo` | `photos-go` | 相册(Go版) |
| `com.google.android.apps.podcasts` | `google-podcasts` | Google 播客 |
| `com.google.android.apps.tachyon` | `google-meet` | Google Meet |
| `com.google.android.apps.tasks` | `google-tasks` | Google Tasks |
| `com.google.android.apps.translate` | `google-translate` | Google 翻译 |
| `com.google.android.apps.walletnfcrel` | `google-wallet` | Google 钱包 |
| `com.google.android.apps.wallpaper` | `google-wallpapers` | Google 壁纸 |
| `com.google.android.apps.wellbeing` | `digital-wellbeing` | 数字健康 |
| `com.google.android.apps.youtube.creator` | `youtube-studio` | YouTube Studio |
| `com.google.android.apps.youtube.kids` | `youtube-kids` | YouTube Kids |
| `com.google.android.apps.youtube.music` | `youtube-music` | YouTube Music |
| `com.google.android.as.oss` | `private-compute-services` | Private Compute Services ✅ 补全.oss |
| `com.google.android.authenticator` | `google-authenticator` | 身份验证器 |
| `com.google.android.calculator` | `google-calculator` | Google 计算器 |
| `com.google.android.calendar` | `google-calendar` | Google 日历 |
| `com.google.android.contactkeys` | `android-keyverifier` | Android密钥验证 ✅ 修正包名 |
| `com.google.android.contacts` | `google-contacts` | 通讯录 |
| `com.google.android.deskclock` | `google-clock` | Google 时钟 |
| `com.google.android.dialer` | `google-dialer` | 电话 |
| `com.google.android.gm` | `gmail` | Gmail |
| `com.google.android.gms` | `google-gms` | 谷歌服务 |
| `com.google.android.googlequicksearchbox` | `google-app` | Google搜索/助理 ✅ 建议更准确 |
| `com.google.android.ims` | `carrier-services` | Carrier Services |
| `com.google.android.inputmethod.latin` | `gboard` | Gboard |
| `com.google.android.keep` | `google-keep` | Google Keep 记事 |
| `com.google.android.play.games` | `google-play-games` | Google Play 游戏 |
| `com.google.android.projection.gearhead` | `android-auto` | Android Auto |
| `com.google.android.recorder` | `google-recorder` | Google 录音机 |
| `com.google.android.safetycore` | `android-safetycore` | Android System SafetyCore |
| `com.google.android.tts` | `google-tts` | Google 语音服务(TTS) |
| `com.google.android.videos` | `google-tv` | Google TV |
| `com.google.android.youtube` | `youtube` | YouTube |
| `com.google.ar.lens` | `google-lens` | 智能镜头 |
| `com.google.earth` | `google-earth` | Google 地球 |

</details>

<details><summary><b>GitHub/开源极客工具</b> （包含 9 个应用）</summary>

| 包名 (Package Name) | 目录别名 (Alias) | 备注 |
| :--- | :--- | :--- |
| `bin.mt.plus` | `mt-file-manager` | - |
| `bin.mt.termex` | `mt-terminal-extension-pack` | MT终端扩展包 ✅ 修正：原bin.mt.plus |
| `com.github.android` | `github` | GitHub |
| `com.github.nrfr` | `nrfr` | Nrfr |
| `io.github.InfinityLoop1309.NewPipeEnhanced` | `pipepipe` | PipePipe ✅ 修正：原com.pipepipe.app |
| `io.github.samolego.canta` | `canta` | Canta |
| `li.songe.gkd` | `gkd` | GKD |
| `moe.shizuku.privileged.api` | `shizuku` | Shizuku |
| `org.fdroid.fdroid` | `fdroid` | F-Droid |

</details>

<details><summary><b>开源组织应用</b> （包含 9 个应用）</summary>

| 包名 (Package Name) | 目录别名 (Alias) | 备注 |
| :--- | :--- | :--- |
| `org.breezyweather` | `breezy-weather` | Breezy Weather |
| `org.chromium.webapk.a71da6c439749dd60_v2` | `google-pwa` | Google PWA ✅ 补充 |
| `org.chromium.webapk.ac00537baef003203_v2` | `wikipedia-pwa` | Wikipedia(PWA) ✅ 修正：org.wikipedia |
| `org.localsend.localsend_app` | `localsend` | LocalSend |
| `org.mozilla.firefox` | `firefox` | Firefox |
| `org.telegram.messenger` | `telegram` | Telegram |
| `org.torproject.torbrowser` | `tor-browser` | Tor Browser |
| `org.videolan.vlc` | `vlc` | VLC |
| `org.videolan.vlc.debug` | `vlc-debug` | VLC测试版 ✅ 补充变体 |

</details>

<details><summary><b>Android 系统组件</b> （包含 7 个应用）</summary>

| 包名 (Package Name) | 目录别名 (Alias) | 备注 |
| :--- | :--- | :--- |
| `com.android.bbkcalculatos` | `vivo-calculator` | vivo计算器 ✅ 修正：原com.vivo.calculator |
| `com.android.chrome` | `chrome` | Chrome |
| `com.android.documentsui` | `vivo-file` | vivo 文件 |
| `com.android.filemanager` | `vivo-file-management` | vivo 文件管理 |
| `com.android.vending` | `google-play-store` | Google Play 商店 |
| `com.android.vendors.bridge.softsim` | `b-sim` | SIM/虚拟SIM相关 |
| `com.android.vivo.tws.vivotws` | `vivo-tws` | vivo TWS |

</details>

<details><summary><b>主流电商与服务</b> （包含 5 个应用）</summary>

| 包名 (Package Name) | 目录别名 (Alias) | 备注 |
| :--- | :--- | :--- |
| `com.eg.android.AlipayGphone` | `zhifubao` | 支付宝 |
| `com.sankuai.meituan` | `meituan` | 美团 |
| `com.taobao.idlefish` | `idlefish` | 闲鱼 |
| `com.taobao.taobao` | `taobao` | 淘宝 |
| `com.xunmeng.pinduoduo` | `pinduoduo` | 拼多多 |

</details>

<details><summary><b>字节跳动系</b> （包含 4 个应用）</summary>

| 包名 (Package Name) | 目录别名 (Alias) | 备注 |
| :--- | :--- | :--- |
| `com.bytedance.android.ludao.online` | `ludao` | 笨包路人谈 |
| `com.ss.android.article.news` | `toutiao` | 头条搜索 |
| `com.ss.android.ugc.aweme` | `aweme` | 抖音 |
| `com.ss.android.ugc.trill` | `tiktok-in` | TikTok(印度/旧版) |

</details>

<details><summary><b>百度系</b> （包含 2 个应用）</summary>

| 包名 (Package Name) | 目录别名 (Alias) | 备注 |
| :--- | :--- | :--- |
| `com.baidu.dict` | `baidu-dict` | 百度汉语 |
| `com.baidu.tieba` | `baidu-tieba` | 百度贴吧 |

</details>

<details><summary><b>微软系</b> （包含 2 个应用）</summary>

| 包名 (Package Name) | 目录别名 (Alias) | 备注 |
| :--- | :--- | :--- |
| `com.microsoft.copilot` | `copilot` | Copilot |
| `com.microsoft.emmx` | `edge` | Edge |

</details>

<details><summary><b>腾讯系</b> （包含 1 个应用）</summary>

| 包名 (Package Name) | 目录别名 (Alias) | 备注 |
| :--- | :--- | :--- |
| `com.tencent.mm` | `wechat` | 微信 |

</details>

<!-- STATS_END -->
