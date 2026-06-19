# 许可边界 · 歸藏家族（Licensing Notice — guizang clean-typography family）

本仓库**整体以 MIT 授权**（见根目录 [`LICENSE`](../../LICENSE)）。**但下面列出的文件例外**——
它们的视觉设计系统（字号字重耦合纪律、预设调色板、组件库）提炼自设计师 **歸藏**
的 **[guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill)**，该上游项目以
**AGPL-3.0** 授权。为尊重其 copyleft，本目录下这些「歸藏家族」文件同样以
**AGPL-3.0** 分发：

```
references/styles/guizang-dna.md          # 家族宪法（字阶纪律 + 预设调色板 + 组件目录）
references/styles/guizang-clean.css        # 组件库（stat-card / callout / pipeline / timeline / bar-chart …）
references/styles/guizang-checklist.md     # 交付质检门
```

**衍生提醒**：以下文件**内嵌**了 `guizang-clean.css` 的作用域副本 / 使用其预设调色板，
因此就「歸藏家族视觉系统」这一部分而言，同样受 AGPL-3.0 约束（文件其余的视频卡片
脚手架、动效声明属本仓库 MIT 部分）：

```
references/styles/swiss.html  ·  minimal.html  ·  terminal.html
references/styles/editorial-print.html  ·  pastel-aura.html
scripts/validate-clean-card.mjs            # 校验脚本，内嵌预设调色板 allowlist
```

AGPL-3.0 全文见同目录 [`LICENSE.AGPL-3.0.txt`](LICENSE.AGPL-3.0.txt)，或
<https://www.gnu.org/licenses/agpl-3.0.html>。

## 这对你意味着什么

- **个人 / 学习 / 内部非商用** —— 随便用。
- **商用 / 对外网络服务** —— AGPL-3.0 是「传染性」copyleft：你用到上述歸藏家族部分时，
  通常需要把对应衍生作品也以 AGPL-3.0 开源、并向用户提供完整源码。**商用前请通读
  AGPL-3.0 并确认合规**，或联系歸藏（[@op7418](https://github.com/op7418)）获取另行授权。
- 不想受 AGPL 约束？**换掉歸藏家族那 5 款风格**（改用「视觉特效类」风格，它们不依赖
  歸藏 DNA），其余部分仍是干净的 MIT。

> 颜色 hex 值、间距数字、排版规则本身属事实 / idea 不受版权保护；本边界出于对原作者
> 创作（组件选择与编排、设计系统策展）的尊重与谨慎，主动标注，而非法律意见。
