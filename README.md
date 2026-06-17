# Antigravity 中文化补丁

这是一个给 Google Antigravity 2.0 桌面端使用的运行时中文化补丁。它不会修改 Antigravity 安装包本体，而是在应用启动后通过本机 DevTools 调试端口把常见英文界面文案替换为中文。

## 本 Fork 的专属增强特性

由于原版仓库已久未维护，此 Fork 版本包含了多项重要改进以确保兼容最新版 AG 并提升汉化覆盖率：

1. **更全面的汉化覆盖**：大幅扩展了字典词条（原 PR #1），补充了正则表达式重写规则、侧边栏、命令面板、设置选项、提示框等几乎所有新生界面的汉化，并应原需求移除了 Artifact 的直译。
2. **最新版 AG 启动兼容**：最新版 AG 出于安全策略默认禁用了远程调试端口，本版本在 `Antigravity.zh.ps1` 启动参数中强制补齐了 `--remote-debugging-port=0`，解决新版无法注入的问题（原 PR #3）。
3. **修复系统代理拦截**：显式绕过了本地代理连接 DevTools WebSocket，彻底解决开启 Clash 等科学上网工具后引起的 `502 Bad Gateway` 报错和脚本闪退。
4. **多级目标智能注入**：针对最新版 AG 引入的各种弹窗和 Splash 等多 Target 并存的情况，改为遍历匹配所有页面，确保精准命中主窗口。

## 包含内容

- `patch/antigravity_zh_inject.py`：中文化注入脚本。
- `patch/Antigravity.zh.ps1`：Windows 启动器脚本，启动 Antigravity 后自动注入中文化补丁。
- `rules/GEMINI.example.md`：让 AI 默认用简体中文回复的规则示例。

## 使用方式

1. 将 `patch/antigravity_zh_inject.py` 和 `patch/Antigravity.zh.ps1` 放到 Antigravity 安装目录。
2. 右键桌面快捷方式，打开“属性”。
3. 将目标改为类似下面的命令，路径按你的实际安装目录调整：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "D:\Apps\Google\Antigravity\Antigravity.zh.ps1"
```

4. 之后从这个快捷方式启动 Antigravity。

## 说明

这个项目是运行时 UI 文案替换补丁，不是 Google 官方语言包。若 Antigravity 更新后界面文案变化，可以在 `antigravity_zh_inject.py` 的词表中继续补充。

## 隐私

本公开包已移除个人电脑路径、快捷方式备份、Preferences 备份、订阅链接、密钥和其他本机私有信息。
