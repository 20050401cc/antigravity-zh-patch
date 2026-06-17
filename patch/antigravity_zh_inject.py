import json
import pathlib
import sys
import time
import urllib.request

import websocket


USER_DATA = pathlib.Path.home() / "AppData" / "Roaming" / "Antigravity"
PORT_FILE = USER_DATA / "DevToolsActivePort"

TRANSLATOR_JS = r"""

(() => {
  const exact = new Map(Object.entries({
    "File": "文件",
    "View": "视图",
    "Window": "窗口",
    "Edit": "编辑",
    "Help": "帮助",
    "New Window": "新建窗口",
    "Docs": "文档",
    "New Conversation": "新建对话",
    "Conversation History": "对话历史",
    "Scheduled Tasks": "计划任务",
    "Projects": "项目",
    "No conversations yet": "暂无对话",
    "Conversations": "对话",
    "Conversation": "对话",
    "Starting The Conversation": "开始对话",
    "Ask anything, @ to mention, / for actions": "输入消息，@ 提及，/ 执行动作",
    "Ask anything, @ to mention": "输入消息，@ 提及",
    "Start first conversation": "开始第一个对话",
    "Add context": "添加上下文",
    "Message input": "消息输入",
    "User message": "用户消息",
    "Agent response": "智能体回复",
    "Typeahead menu": "快捷菜单",
    "Record voice memo": "录制语音备忘录",
    "Record Audio": "录制音频",
    "Toggle Voice Recording": "切换语音录制",
    "Cancel (Ctrl+D)": "取消 (Ctrl+D)",
    "Worked for": "已执行",
    "See less": "收起",
    "Working": "工作中",
    "Working...": "工作中...",
    "Edited": "已编辑",
    "Ran": "已运行",
    "Run": "运行",
    "Review": "审阅",
    "Walkthrough": "操作指引",
    "Task": "任务",
    "Pending messages": "待处理消息",
    "The conversation was compacted while generating this response.": "在生成此回复时对话已被压缩。",
    "Sidebar": "侧边栏",
    "Toggle Sidebar": "切换侧边栏",
    "Select model, current:": "选择模型，当前：",
    "Toggle Model Selector": "切换模型选择器",
    "Verbose agent chat": "详细智能体对话",
    "Display and preserve intermediate thinking steps": "显示并保留中间思考步骤",
    "Go Back": "后退",
    "Go Forward": "前进",
    "Display Options": "显示选项",
    "Toggle Auxiliary Pane": "切换辅助面板",
    "Navigation": "导航",
    "Layout Controls": "布局控制",
    "Focus Input": "聚焦输入",
    "Find in Pane": "在面板中查找",
    "Open Conversation Picker": "打开对话选择器",
    "Select Next Conversation": "选择下一个对话",
    "Select Previous Conversation": "选择上一个对话",
    "Selection Actions": "选中操作",
    "Show Selection Actions": "显示选中操作",
    "Zoom In": "放大",
    "Zoom Out": "缩小",
    "Reset Zoom": "重置缩放",
    "Copy": "复制",
    "Copy code": "复制代码",
    "At mention code block": "引用代码块",
    "Good response": "回答不错",
    "Bad response": "回答不好",
    "Settings": "设置",
    "Open Settings": "打开设置",
    "General": "通用",
    "Account": "账户",
    "Permissions": "权限",
    "Appearance": "外观",
    "Models": "模型",
    "Customizations": "自定义",
    "Default Customizations": "默认自定义",
    "Customize Global Skills": "自定义全局技能",
    "Custom Agents": "自定义智能体",
    "MCP Servers": "MCP 服务器",
    "Notifications": "通知",
    "App": "应用",
    "Security": "安全",
    "Browser": "浏览器",
    "Editor": "编辑器",
    "Terminal": "终端",
    "Commands": "命令",
    "Files": "文件",
    "Quota": "额度",
    "Shortcuts": "快捷键",
    "Provide Feedback": "提供反馈",
    "Not in Project": "不在项目中",
    "Outside of Project": "项目之外",
    "Manage your plan, credentials, and general preferences.": "管理您的套餐、凭据和常规偏好设置。",
    "Enable Telemetry": "启用遥测",
    "When toggled on, Antigravity collects usage data to help Google enhance performance and features.": "开启后，Antigravity 将收集使用数据以帮助 Google 提升性能和功能。",
    "Marketing Emails": "营销邮件",
    "Receive product updates, tips, and promotions from Google Antigravity via email.": "通过电子邮件接收来自 Google Antigravity 的产品更新、提示和促销信息。",
    "Your Plan:": "您的套餐：",
    "Your Plan: Google AI Pro": "您的套餐：Google AI Pro",
    "Your Plan: Google AI Ultra": "您的套餐：Google AI Ultra",
    "You can upgrade to a Google AI Ultra plan to receive the highest rate limits.": "您可以升级至 Google AI Ultra 套餐以获得最高的使用额度。",
    "Upgrade": "升级",
    "Email": "电子邮件",
    "Sign Out": "退出登录",
    "Sign In": "登录",
    "Auth and Billing": "认证与计费",
    "By using this app, you agree to its": "使用本应用即表示您同意其",
    "Terms of Service": "服务条款",
    "Learn more": "了解更多",
    "Learn more about": "了解更多关于",
    "Manage project folders, agent settings, and permissions.": "管理项目文件夹、智能体设置和权限。",
    "No folders added yet.": "暂无添加文件夹。",
    "Add Folder": "添加文件夹",
    "+ Add Folder": "+ 添加文件夹",
    "Configure global allowed and denied resource permissions.": "配置全局允许和拒绝的资源权限。",
    "Project-Specific Settings": "项目特定设置",
    "Modify scoped permissions, folders, and agent settings like Sandbox and Terminal Command Execution.": "修改作用域权限、文件夹以及智能体设置（如沙盒和终端命令执行）。",
    "Go to Projects": "前往项目",
    "File Permissions": "文件权限",
    "File Access Rules": "文件访问规则",
    "Configure allowed and denied paths for file reads and writes.": "配置允许和拒绝读写的文件路径。",
    "Open": "打开",
    "Network Permissions": "网络权限",
    "Network Access Rules": "网络访问规则",
    "Configure allowed and denied URLs for reading.": "配置允许和拒绝读取的 URL。",
    "Terminal & Tooling Permissions": "终端和工具权限",
    "Terminal Commands": "终端命令",
    "Configure allowed terminal commands.": "配置允许执行的终端命令。",
    "Commands Outside Sandbox": "沙盒外命令",
    "Configure allowed commands outside the sandbox.": "配置允许在沙盒外执行的命令。",
    "MCP Tools": "MCP 工具",
    "Mcp Tools": "MCP 工具",
    "Configure external tools via Model Context Protocol.": "通过模型上下文协议配置外部工具。",
    "Local Permissions": "本地权限",
    ". Local permissions have higher priority.": "。本地权限优先级更高。",
    "Inherits from": "继承自",
    "Actuation Permissions": "操控权限",
    "Browser Actuation Rules": "浏览器操控规则",
    "Configure allowed and denied URLs for browser actuation.": "配置允许和拒绝的浏览器操控 URL。",
    "Configure the agent's visual theme and display preferences.": "配置智能体的视觉主题和显示偏好。",
    "Accent": "强调色",
    "Foreground": "前景色",
    "Background": "背景色",
    "Dark Theme": "深色主题",
    "Light Theme": "浅色主题",
    "Default Dark": "默认深色",
    "Default Light": "默认浅色",
    "Select light, dark, or inherit system settings.": "选择浅色、深色或继承系统设置。",
    "Configure AI models and view your quota.": "配置 AI 模型并查看您的额度。",
    "Model Quota": "模型额度",
    "Model Credits": "模型积分",
    "Token Usage": "Token 用量",
    "AI Credits Used to Generate Response": "生成回复所用的 AI 积分",
    "Enable AI Credit Overages": "启用 AI 积分超额",
    "When toggled on, Antigravity will use your AI credits to fulfill model requests once you're out of model quota. Antigravity will always use your model quota first before using AI credits.": "开启后，当您的模型额度用完时，Antigravity 将使用您的 AI 积分来满足模型请求。Antigravity 将始终优先使用模型额度，然后再使用 AI 积分。",
    "Get More AI Credits": "获取更多 AI 积分",
    "Available AI Credits:": "可用 AI 积分：",
    "Refresh": "刷新",
    "Refresh quota and credits data": "刷新额度和积分数据",
    "View your available model quota and AI credits. Model quota refreshes periodically based on your plan. Enable AI Credit Overages to continue using models when your quota is exhausted.": "查看您可用的模型额度和 AI 积分。模型额度会根据您的套餐定期刷新。启用 AI 积分超额以在额度用完后继续使用模型。",
    "% of the customization budget is available.": "% 的自定义预算可用。",
    "The breakdown below shows token usage from customizations like skills, rules, and MCP. If the budget is exceeded, large customizations will be truncated automatically.": "以下分项显示了来自自定义配置（如技能、规则和 MCP）的 Token 使用情况。如果超出预算，较大的自定义配置将被自动截断。",
    "Recommended": "推荐",
    "Configure default behaviors, skills, and MCP servers.": "配置默认行为、技能和 MCP 服务器。",
    "No customizations found for this workspace.": "未找到此工作区的自定义配置。",
    "Customize": "自定义",
    "Installed MCP Servers": "已安装的 MCP 服务器",
    "Add MCP": "添加 MCP",
    "global settings": "全局设置",
    "Browser Settings": "浏览器设置",
    "Configure the browser subagent. It requires": "配置浏览器子智能体。它需要",
    "to be installed. The browser subagent can be invoked by typing /browser in the conversation input box.": "已安装。可以在对话输入框中输入 /browser 来调用浏览器子智能体。",
    "Browser Javascript Execution Policy": "浏览器 JavaScript 执行策略",
    "Controls whether the agent can run custom JavaScript to automate complex browser actions.": "控制智能体是否可以运行自定义 JavaScript 以自动执行复杂的浏览器操作。",
    "Install IDE": "安装 IDE",
    "Google Chrome": "Google Chrome",
    "App Settings": "应用设置",
    "Manage application settings.": "管理应用程序设置。",
    "Keep In Menu Bar": "保留在菜单栏",
    "The app will be accessible from the menu bar and will keep running in the background when all windows are closed.": "应用将可从菜单栏访问，并在所有窗口关闭后继续在后台运行。",
    "Prevent Sleep": "阻止休眠",
    "Prevent the computer from sleeping while the app is running.": "在应用运行时阻止计算机进入休眠。",
    "Marketplace": "应用市场",
    "Marketplace Gallery URL": "应用市场页面 URL",
    "Marketplace Item URL": "应用市场项目 URL",
    "Changes the base URL for marketplace search results. You must restart Antigravity to use the new marketplace after changing this value.": "更改应用市场搜索结果的基础 URL。更改此值后需重启 Antigravity 才能使用新的应用市场。",
    "Changes the base URL on each extension page. You must restart Antigravity to use the new marketplace after changing this value.": "更改每个扩展页面的基础 URL。更改此值后需重启 Antigravity 才能使用新的应用市场。",
    "Build With Google Plugins": "使用 Google 插件构建",
    "Google Drive integration not available": "Google Drive 集成不可用",
    "Security Preset": "安全预设",
    "Preset": "预设",
    "Choose a predefined security preset for the agent. This controls terminal auto-execution policy, and file access policy.": "为智能体选择预定义的安全预设。这控制终端自动执行策略和文件访问策略。",
    "Agent Settings": "智能体设置",
    "Agent Behavior": "智能体行为",
    "Agent settings and permissions for conversations outside of projects.": "项目外对话的智能体设置和权限。",
    "Chat Settings": "聊天设置",
    "Artifact Review Policy": "工件审阅策略",
    "Specifies Agent's behavior when asking for review on artifacts, which are documents it creates to enable a richer conversation experience.": "指定智能体在请求审阅工件时的行为。工件是智能体创建的文档，用于实现更丰富的对话体验。",
    "Always Ask": "始终询问",
    "Disabled": "已禁用",
    "Editor Settings": "编辑器设置",
    "Configure editor-specific behaviors and shortcuts.": "配置编辑器特定的行为和快捷键。",
    "Show \"Edit\" and \"Chat\" buttons when selecting text in the editor.": "在编辑器中选中文本时显示\"编辑\"和\"聊天\"按钮。",
    "Open Editor Settings": "打开编辑器设置",
    "To modify editor settings, open Settings within the editor window.": "要修改编辑器设置，请在编辑器窗口中打开设置。",
    "Notification Settings": "通知设置",
    "Manage your notification preferences.": "管理您的通知偏好设置。",
    "To modify notification settings, open your operating system's system preferences.": "要修改通知设置，请打开操作系统的系统偏好设置。",
    "Open System Preferences": "打开系统偏好设置",
    "Keyboard shortcuts for quick navigation and control.": "用于快速导航和控制的键盘快捷键。",
    "No scheduled tasks configured.": "未配置计划任务。",
    "Add scheduled task": "添加计划任务",
    "See Activity": "查看活动",
    "Feedback Type": "反馈类型",
    "Bug Report": "错误报告",
    "Feature Request": "功能请求",
    "General Feedback": "常规反馈",
    "Description": "描述",
    "Describe the bug you encountered...": "描述您遇到的错误...",
    "Steps to Reproduce": "重现步骤",
    "Steps to reproduce the issue": "问题重现步骤",
    "Please list the steps to reproduce the issue": "请列出重现该问题的步骤",
    "Expected behavior": "预期行为",
    "Actual behavior": "实际行为",
    "Any error messages": "任何错误信息",
    "Any relevant information": "任何相关信息",
    "Please describe the issue in detail. The more actionable your feedback, the quicker our team can address your request. Some helpful information includes:": "请详细描述问题。您的反馈越具体可操作，我们的团队就能越快处理您的请求。以下信息会有帮助：",
    "Attach Antigravity server logs": "附加 Antigravity 服务器日志",
    "Attach a screenshot (optional)": "附加截图（可选）",
    "We recommend attaching logs. Attaching logs will help the Antigravity team act on and prioritize your feedback.": "我们建议附加日志。附加日志将帮助 Antigravity 团队处理和优先排列您的反馈。",
    "New Project": "新建项目",
    "Quick Start": "快速开始",
    "Create New Project": "创建新项目",
    "Create Project": "创建项目",
    "Select Project": "选择项目",
    "Open File Search": "打开文件搜索",
    "File Picker": "文件选择器",
    "Filter": "筛选",
    "Create a new project. You can add folders to it now or later.": "创建一个新项目。你可以现在或稍后添加文件夹。",
    "Instantly create a new project and folder to start building.": "立即创建一个新项目和文件夹并开始构建。",
    "Search conversations...": "搜索对话...",
    "Search tasks...": "搜索任务...",
    "New": "新建",
    "Fork": "分支",
    "Create fork": "创建分支",
    "Command Palette": "命令面板",
    "Submit": "提交",
    "Cancel": "取消",
    "Save": "保存",
    "Close": "关闭",
    "Delete": "删除",
    "Clear": "清空",
    "Send": "发送",
    "Stop generating": "停止生成",
    "Regenerate": "重新生成",
    "Loading...": "加载中...",
    "Search": "搜索",
    "Allow": "允许",
    "Ask": "询问",
    "Deny": "拒绝",
    "Add": "添加",
    "Allow/deny agent command execution outside the sandbox.": "允许/拒绝智能体在沙盒外执行命令。",
    "Block all browser JavaScript execution.": "阻止所有浏览器 JavaScript 执行。",
    "Request Review": "请求审阅",
    "Prompt for approval before running browser scripts.": "在运行浏览器脚本前提示审批。",
    "Always Proceed": "始终继续",
    "Allow full browser script execution without prompting.": "允许完整的浏览器脚本执行而无需提示。",
    "Waiting for user input.": "等待用户输入。",
    "Allow running this command?": "允许运行此命令吗？",
    "Yes, allow this time": "是，允许本次运行",
    "No (tell the agent what to do instead)": "否（告诉智能体下一步做什么）",
    "Skip": "跳过",
    "Overview": "概览",
    "File Reads": "读取文件",
    "Allow/deny agent read access to specific files or directories.": "允许/拒绝智能体对特定文件或目录的读取访问权限。",
    "File Writes": "写入文件",
    "Allow/deny agent write access to specific files or directories.": "允许/拒绝智能体对特定文件或目录的写入访问权限。",
    "Browser Actuation Permissions": "浏览器操控权限",
    "Execute URLs": "执行 URL",
    "Allow/deny agent browser actuation access to specific URLs.": "允许/拒绝智能体对特定 URL 的浏览器操控权限。",
    "Useful for tasks that require file access across your full machine. The agent has full read and write access to all local files, but all proposed terminal commands require manual review and approval before running.": "适用于需要在整台机器上访问文件的任务。智能体对所有本地文件具有完全的读写权限，但在运行所有提议的终端命令前都需要手动审批。",
    "Default": "默认",
    "Requires manual review for all terminal commands and file accesses outside of the working folders.": "要求对工作目录外的所有终端命令和文件访问进行手动审查。",
    "Full Machine": "完整机器",
    "All terminal commands require review. The agent can read or write to any file in the machine.": "所有终端命令均需审查。智能体可读写机器上的任意文件。",
    "Turbo Mode": "极速模式",
    "Disables all safety barriers for maximal iteration velocity.": "禁用所有安全限制以获得最高迭代速度。",
    "Custom": "自定义",
    "Manually customize individual settings.": "手动自定义各个设置项。",
    "No": "否",
    "(tell the agent what to do instead)": "（告诉智能体下一步做什么）",
    "Read URLs": "读取 URL",
    "Allow/deny agent read access to specific URLs or domains.": "允许/拒绝智能体对特定 URL 或域名的读取访问权限。",
    "Build with Antigravity Plugins": "使用 Antigravity 插件构建",
    "Plugins are packaged collections of skills and MCPs to help the Agent in Antigravity work with Google developer products. You can always change your choices in Settings.": "插件是技能和 MCP 的打包集合，用于帮助智能体使用 Google 开发者产品。您随时可以在设置中更改选择。",
    "External tools the agent can call via Model Context Protocol.": "智能体可以通过模型上下文协议（MCP）调用的外部工具。",
    "Outside of folders file access policy": "工作目录外文件访问策略",
    "Configures how the agent tries to access files outside of its working folders.": "配置智能体如何尝试访问其工作目录外的文件。",
    "Terminal Command Auto Execution": "终端命令自动执行",
    "Controls whether terminal commands require your approval before running.": "控制终端命令在运行前是否需要您的批准。",
    "Require Review": "需要审查",
    "Model": "模型",
    "Fast": "快速",
    "Undo changes up to this point": "撤销到此处的更改",
    "Run until the specified goal is completely finished": "运行直到指定的目标完全完成",
    "Run an instruction on a recurring schedule or as a one-time timer": "按定期计划或一次性定时器运行指令",
    "Invoke a browser agent for web tasks": "调用浏览器智能体执行网络任务",
    "Interview me to align on a plan": "通过访谈与我沟通以确认计划",
    "Search for code symbols": "搜索代码符号",
    "Search git history": "搜索 Git 历史",
    "Search the web": "搜索网络",
    "Search all convos...": "搜索所有对话...",
    "Recent": "最近",
    "to navigate": "导航",
    "to select": "选择",
    "Search for files in the project...": "在项目中搜索文件...",
    "No items found": "未找到项目",
    "Type to search...": "输入以搜索...",
    "Open Launchpad": "打开启动台",
    "Open Keyboard Shortcuts": "打开快捷键设置",
    "Provide feedback": "提供反馈",
    "Toggle Project Selector": "切换项目选择器",
    "Open Command Palette": "打开命令面板",
    "Open Project Picker": "打开项目选择器",
    "Close Tab": "关闭标签页",
    "New Editor Window": "新建编辑器窗口",
    "Open Conversation History": "打开对话历史",
    "Remote Debugging Required": "需要远程调试",
    "To use browser tools, you need to enable remote debugging:": "要使用浏览器工具，您需要启用远程调试：",
    "Navigate to": "导航到",
    "Enable \"Allow remote debugging for this browser instance\".": "启用“允许此浏览器实例的远程调试”。",
    "Proceed Anyways": "仍然继续",
    "Check again": "再次检查",
    "Minimize": "最小化",
    "Maximize": "最大化",
    "Toggle Developer Tools": "切换开发者工具",
    "Copy conversation markdown": "复制对话 Markdown",
    "Recent Files": "最近使用的文件",
    "Useful for typical development with an emphasis on security. It prioritizes safety over speed by requiring manual approval for all terminal commands and files outside the project directory.": "适用于强调安全性的典型开发。它优先考虑安全而不是速度，要求对所有终端命令和项目目录之外的文件访问进行手动审核。",
    "A high-risk mode that disables all safety barriers. The agent operates with full system access, auto-executes all terminal commands, and reads or writes to all local files without review prompts.": "禁用所有安全屏障的高风险模式。智能体以完整的系统访问权限运行，自动执行所有终端命令，并在没有审核提示的情况下读取或写入所有本地文件。",
    "Copy Content": "复制内容",
    "View Diff": "查看差异",
    "Viewing Diff": "正在查看差异",
    "Subagents": "子智能体",
    "Files Changed": "更改的文件",
    "Background Tasks": "后台任务",
    "Review Changes": "审阅更改",
    "Gemini Models": "Gemini 模型",
    "Claude and GPT models": "Claude 及 GPT 模型",
    "Weekly Limit": "周度额度",
    "Five Hour Limit": "5 小时额度",
    "Within each group, models share a weekly limit and a 5-hour limit. Quota is consumed proportionally to the cost of the tokens. Thus, limits will last longer with shorter tasks or using more cost-effective models. The 5-hour limit smooths out aggregate demand to fairly distribute global capacity across all users, while your weekly limit is tied directly to your individual tier.": "在每个分组中，模型共享周度额度和 5 小时额度。额度会根据 Token 的成本按比例消耗。因此，使用更具成本效益的模型或执行较短的任务时，额度将更加耐用。5 小时额度可以平滑总体需求，以便在所有用户之间公平地分配全局算力，而您的周度额度则直接与您的个人等级挂钩。",
    "You have not used any of your weekly limit.": "您尚未使用任何周度额度。",
    "You have not used any of your 5-hour limit.": "您尚未使用任何 5 小时额度。"
  }));

  const rewriters = [
    [/^Worked for\s+(.+)$/i, "已执行 $1"],
    [/^See all\s*\((\d+)\)$/i, "查看全部 ($1)"],
    [/^(\d+)\s*m$/i, "$1 分钟"],
    [/^(\d+)\s*h$/i, "$1 小时"],
    [/^(\d+)\s*d$/i, "$1 天"],
    [/^You have used some of your weekly limit, it will fully refresh in (.+)\.$/i, "您已使用了部分周度额度，将在 $1 后完全刷新。"],
    [/^You have used some of your 5-hour limit, it will fully refresh in (.+)\.$/i, "您已使用了部分 5 小时额度，将在 $1 后完全刷新。"],
    [/^You have hit your 5-hour limit, so the weekly limit does not currently apply\. Your 5-hour limit will refresh in (.+)\.$/i, "您已用尽了 5 小时额度，因此周度额度暂不适用。您的 5 小时额度将在 $1 后刷新。"],
    [/^You have hit your 5-hour limit, it will refresh in (.+)\. If on a supported paid plan, you can use AI credits in the interim\.$/i, "您已用尽了 5 小时额度，将在 $1 后刷新。如果您订阅了支持的付费计划，期间可以使用 AI 积分。"],
    [/^(\d+)\s*s$/i, "$1 秒"],
    [/^(\d+)\s*w$/i, "$1 周"],
    [/^(\d+)\s*mo$/i, "$1 个月"],
    [/^(\d+)\s*y$/i, "$1 年"],
    [/^Thought for (\d+)s$/i, "思考了 $1 秒"],
    [/^Thought for (\d+)m$/i, "思考了 $1 分钟"],
    [/^(\d+)\s*files?\s*changed\s*(.*)$/i, "$1 个文件已更改 $2"],
    [/^(\d+) tools? enabled$/i, "$1 个工具已启用"],
    [/^(\d+) tasks?$/i, "$1 个任务"],
    [/^(\d+) tasks? running$/i, "$1 个任务运行中"],
    [/^Refreshes in (.+)$/i, "将在 $1 后刷新"],
    [/^Available AI Credits: (\d+)$/i, "可用 AI 积分：$1"],
    [/^Show (\d+) breakdowns?$/i, "显示 $1 个分项"],
    [/^(\d+) breakdowns?$/i, "$1 个分项"],
    [/^Select model, current: (.+)$/i, "选择模型，当前：$1"],
    [/^Mcp Tools: (\d+) tokens$/i, "MCP 工具：$1 tokens"],
    [/^Send feedback as (.+)$/i, "以 $1 身份发送反馈"],
    [/^Version ([\d\.]+)$/i, "版本 $1"],
    [/^Allow$/i, "允许"],
    [/^Ask$/i, "询问"],
    [/^Deny$/i, "拒绝"],
    [/^Add$/i, "添加"],
    [/^Default$/i, "默认"],
    [/^Full Machine$/i, "完整机器"],
    [/^Turbo Mode$/i, "极速模式"],
    [/^Custom$/i, "自定义"],
    [/^No$/i, "否"],
    [/^Yes, and always allow '(.+)' when not in a project$/i, "是，当不在项目中时始终允许 '$1'"],
    [/^Yes, and always allow '(.+)'$/i, "是，始终允许 '$1'"],
    [/^Files$/i, "文件"],
    [/^Folders$/i, "文件夹"],
    [/^Code$/i, "代码"],
    [/^Git$/i, "Git"],
    [/^Web$/i, "网络"],
    [/^Context$/i, "上下文"],
    [/^Rules$/i, "规则"],
    [/^Media \(Today (.+)\)$/i, "媒体 (今天 $1)"],
    [/^Media \(Yesterday (.+)\)$/i, "媒体 (昨天 $1)"],
    [/^Media \((.+)\)$/i, "媒体 ($1)"],
    [/^Show (\d+) more\.\.\.$/i, "显示更多 $1 个..."],
    [/^(\d+)\s*mins?\s*ago$/i, "$1 分钟前"],
    [/^(\d+)\s*hrs?\s*ago$/i, "$1 小时前"],
    [/^(\d+)\s*days?\s*ago$/i, "$1 天前"],
    [/^(\d+)\s*weeks?\s*ago$/i, "$1 周前"],
    [/^(\d+)\s*months?\s*ago$/i, "$1 个月前"],
    [/^(\d+)\s*years?\s*ago$/i, "$1 年前"]
  ];

  function translateText(raw) {
    if (!raw) return raw;
    const trimmed = raw.trim();
    if (!trimmed) return raw;
    let translated = exact.get(trimmed);
    if (!translated) {
      for (const [pattern, replacement] of rewriters) {
        if (pattern.test(trimmed)) {
          translated = trimmed.replace(pattern, replacement);
          break;
        }
      }
    }
    if (!translated || translated === trimmed) return raw;
    
    // Post-process time units for things like "将在 2 hours, 9 minutes 后刷新"
    translated = translated.replace(/(\d+)\s+hours?/gi, "$1 小时");
    translated = translated.replace(/(\d+)\s+minutes?/gi, "$1 分钟");
    translated = translated.replace(/(\d+)\s+seconds?/gi, "$1 秒");
    translated = translated.replace(/(\d+)\s+days?/gi, "$1 天");
    
    const leading = raw.match(/^\s*/)?.[0] ?? "";
    const trailing = raw.match(/\s*$/)?.[0] ?? "";
    return leading + translated + trailing;
  }

  function shouldSkipNode(node) {
    const parent = node.parentElement;
    if (!parent) return true;
    return parent.closest("pre, code, textarea, input, [contenteditable='true']");
  }

  function translateAttributes(element) {
    for (const attr of ["aria-label", "title", "placeholder", "data-placeholder"]) {
      const value = element.getAttribute?.(attr);
      if (!value) continue;
      const next = translateText(value);
      if (next !== value) element.setAttribute(attr, next);
    }
  }

  function translateOne(node) {
    if (!node) return;
    if (node.nodeType === Node.TEXT_NODE) {
      if (shouldSkipNode(node)) return;
      const next = translateText(node.nodeValue);
      if (next !== node.nodeValue) node.nodeValue = next;
      return;
    }
    if (node.nodeType === Node.ELEMENT_NODE) translateAttributes(node);
  }

  function translateTree(root) {
    if (!root) return;
    translateOne(root);
    if (root.nodeType !== Node.ELEMENT_NODE && root.nodeType !== Node.DOCUMENT_NODE) return;
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    for (const node of nodes) translateOne(node);
  }

  if (window.__antigravityZhObserver) {
    window.__antigravityZhObserver.disconnect();
  }
  translateTree(document.documentElement);
  window.__antigravityZhObserver = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
      if (mutation.type === "characterData") {
        translateOne(mutation.target);
      } else if (mutation.type === "attributes") {
        translateOne(mutation.target);
      } else {
        for (const node of mutation.addedNodes) translateTree(node);
      }
    }
  });
  window.__antigravityZhObserver.observe(document.documentElement, {
    childList: true,
    subtree: true,
    characterData: true,
    attributes: true,
    attributeFilter: ["aria-label", "title", "placeholder", "data-placeholder"]
  });
  return {
    language: navigator.language,
    title: document.title,
    body: document.body ? document.body.innerText.slice(0, 500) : ""
  };
})()
"""


def read_targets():
    port = PORT_FILE.read_text(encoding="utf-8").splitlines()[0].strip()
    proxy_handler = urllib.request.ProxyHandler({})
    opener = urllib.request.build_opener(proxy_handler)
    with opener.open(f"http://127.0.0.1:{port}/json", timeout=3) as response:
        return port, json.load(response)


def send(ws, seq, method, params=None):
    seq += 1
    ws.send(json.dumps({"id": seq, "method": method, "params": params or {}}))
    while True:
        message = json.loads(ws.recv())
        if message.get("id") == seq:
            return seq, message


def main():
    # Wait for the auto-restart to finish.
    time.sleep(4)
    deadline = time.time() + 45
    last_error = None
    while time.time() < deadline:
        try:
            if not PORT_FILE.exists():
                time.sleep(0.5)
                continue
            _, targets = read_targets()
            matching_targets = [
                item
                for item in targets
                if item.get("type") == "page"
                and str(item.get("url", "")).startswith("https://127.0.0.1")
                and item.get("webSocketDebuggerUrl")
            ]
            if not matching_targets:
                time.sleep(0.5)
                continue
            
            success_count = 0
            for target in matching_targets:
                try:
                    ws = websocket.create_connection(
                        target["webSocketDebuggerUrl"], timeout=5, suppress_origin=True
                    )
                    seq = 0
                    seq, _ = send(ws, seq, "Runtime.enable")
                    seq, _ = send(ws, seq, "Page.enable")
                    seq, _ = send(
                        ws,
                        seq,
                        "Page.addScriptToEvaluateOnNewDocument",
                        {"source": TRANSLATOR_JS},
                    )
                    seq, result = send(
                        ws,
                        seq,
                        "Runtime.evaluate",
                        {"expression": TRANSLATOR_JS, "returnByValue": True},
                    )
                    ws.close()
                    success_count += 1
                except Exception as e:
                    last_error = e
            
            if success_count > 0:
                print(f"Successfully injected into {success_count} targets")
                return 0
        except Exception as exc:
            last_error = exc
            time.sleep(0.75)
    print(f"Failed to inject zh patch: {last_error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
