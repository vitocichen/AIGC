---
name: vidu-q3-video-prompt
description: 为 Vidu Q3 系列的文生、图生、首尾帧、通用参考生、Mix、Drama 和 Ad 模型编写匹配其长时长、智能切镜、多参考和声画能力的正式提示词。
---

# Vidu Q3 视频提示词

仅在 Vidu 总路由已经锁定为 Q3 时使用。

主要来源：

- [Vidu Q3 文生视频](https://platform.vidu.com/docs/api-reference/video-models/vidu-q3/text-to-video)
- [Vidu Q3 首尾帧](https://platform.vidu.com/docs/api-reference/video-models/vidu-q3/start-end-to-video)
- [Vidu Q3 参考生视频](https://platform.vidu.com/docs/api-reference/video-models/vidu-q3/reference-to-video)
- [阿里云 Q3 图生视频 API](https://help.aliyun.com/zh/model-studio/vidu-image-to-video-api-reference)
- [阿里云 Q3 Reference](https://help.aliyun.com/zh/model-studio/viduq3-reference2video)
- [阿里云 Q3 Mix](https://help.aliyun.com/zh/model-studio/viduq3-mix-reference2video)
- [阿里云 Q3 Drama](https://help.aliyun.com/zh/model-studio/viduq3-drama-reference2video)
- [阿里云 Q3 Ad](https://help.aliyun.com/zh/model-studio/viduq3-ad-reference2video)
- [阿里云 Vidu Prompt 指南](https://help.aliyun.com/zh/model-studio/vidu-video-generation-prompt-guide)

## 型号能力路由

### Q3 Pro

常见 ID：

- Vidu 直连：`viduq3-pro`
- 阿里云图生：`vidu/viduq3-pro_img2video`

适合高质量文生、图生和首尾帧，支持更长剧情、智能切镜和声画同步。常见时长 1–16 秒；阿里云图生支持 540p/720p/1080p。

### Q3 Pro Fast

常见 ID：

- Vidu 直连：`viduq3-pro-fast`
- 阿里云：`vidu/viduq3-pro-fast_img2video`

用于成本和速度优先的 Q3 图生或首尾帧。常见时长 1–16 秒，常用 720p/1080p，并支持 Q3 音频能力。它不是 Q3 多参考型号；多参考必须选择 Reference 系列。

### Q3 Turbo

常见 ID：

- Vidu 直连：`viduq3-turbo`
- 阿里云：`vidu/viduq3-turbo_img2video`

适合快速图生、文生或首尾帧。不得假定它具有 Q3 Mix/Drama 的 1–7 张多参考能力。

### Q3 Reference

常见 ID：

- Vidu 直连：`viduq3`
- 阿里云：`vidu/viduq3_reference2video`

支持 1–7 张参考图片、智能切镜、多机位一致性和声画同出，适合通用短剧、漫剧、影视与广告。

### Q3 Mix

常见 ID：

- Vidu 直连：`viduq3-mix`
- 阿里云：`vidu/viduq3-mix_reference2video`

支持 1–7 张参考图片，强调画面质感、动态效果、智能转场和综合均衡。用于角色、场景、道具、风格等多种参考同时参与的复杂镜头。

### Q3 Drama

常见 ID：

- Vidu 直连：`viduq3-drama`
- 阿里云：`vidu/viduq3-drama_reference2video`

面向精品剧与 AI 漫剧，强调人物一致性、情绪、动效和细节。官方与供应商页面对最长 15/16 秒存在差异，必须读取实际接口；通常支持 1–7 张图片和 720p/1080p。

### Q3 Ad

常见阿里云 ID：

```text
vidu/viduq3-ad_reference2video
```

面向商品广告，强调营销切镜、智能运镜和音效。只在项目目标确为商品/TVC/投放广告时选择，不用于普通剧情只因为它会自动切镜。

## 让用户选择

用户只说“Q3”时，根据真实需求展示可用候选，不替用户决定：

- 低成本快速图生：Q3 Pro Fast；
- 高质量单首帧、长剧情或音画同步：Q3 Pro；
- 快速通用：Q3 Turbo；
- 通用 1–7 图参考：Q3 Reference；
- 多种参考混合和综合质感：Q3 Mix；
- AI 漫剧、短剧表演与情绪：Q3 Drama；
- 商品广告：Q3 Ad。

只展示当前节点/API真实存在的型号。用户选定后锁存，除非能力冲突或用户主动修改。

## Q3 提示词共同结构

Q3 可处理比 Q2 Fast 更长的动作和有限多镜头，但仍应控制复杂度：

1. **目标与风格**：媒介、题材、主情绪和最终观感；
2. **参考绑定**：角色、场景、道具、商品或风格参考的真实顺序/主体名；
3. **时序画面**：按时间顺序描述动作、表演、机位、切镜和转场；
4. **声音**：仅在模型和调用参数真实开启音频时写对白、环境、拟音和音乐；
5. **结束状态与限制**：明确最后画面、连续性和无字幕/无多余人物等可见要求。

正文保持连续自然语言，不使用 Seedance 的 `Objective / Timeline / Preserve / Avoid` 顶层字段。需要多个镜头时可以写清“先……随后切到……最后……”，或使用少量时间段；不要建立与真实时长不符的密集镜头表。

## 多参考规则

- 只上传本段真实需要的 1–7 张图片；
- 角色图负责身份，场景图负责空间，道具图负责外形，风格图只负责整体视觉；不得让一张图承担矛盾职责；
- Vidu subject 调用使用 `[@主体名]`；阿里云顺序媒体接口使用“图1为……；图2为……”；
- 同一角色有多视图时明确它们属于同一角色；
- 参考图的服装、道具状态和正文不得冲突；
- 图片顺序或主体名变化后必须重写正文绑定。

## 剧情与切镜

- Q3 支持智能切镜不等于允许任意改剧情；
- 每次切镜必须服务于已确认事件、反应或信息揭示；
- 16 秒内通常控制在 1–3 个主要镜头；对白密集、多人互动或复杂动作应拆段；
- Q3 Drama 可强化情绪和表演，但不得补写原剧本没有的台词、前史或动作；
- Q3 Ad 可以强化商品展示，但不得用于普通剧情时擅自改成广告片。

## 音频

- 只有当前模型和接口明确支持且 `audio=true` 时，正文才写原生声音；
- 对白逐句明确说话人和内容，避免多个角色同段重叠长句；
- 环境声、动作拟音和情绪音乐分清层次；
- 用户计划外部配音时设置 `audio=false`，正文不要求模型生成台词声音；
- 节点不支持声音参考时不得编造 `voice_id` 或声音素材绑定。

## 字符与参数

Q3 不同接口和区域文档存在 5000 与 20000 字符上限差异。必须使用当前供应商实际限制；无法确认时把提交正文控制在 5000 字符以内。长上限不等于应该写满。

常见能力：

- 文生/图生：通常 1–16 秒；
- Reference/Mix：通常最长 16 秒；
- Drama：供应商可能为 2–15 或 2–16 秒；
- Ad：供应商可能为 3–15 或面向 16 秒广告；
- 分辨率及画幅服从具体型号和渠道；
- 音频默认值不同，必须显式记录。

## 正式文件模板

```text
# G01 Vidu Q3 提示词

供应商：<Vidu 官方 / 阿里云百炼 / 实际渠道>
系列：Q3
模型：<精确模型 ID>
模式：<文生 / 图生 / 首尾帧 / 参考生>
用途：<通用 / Mix / Drama / Ad / Pro / Pro Fast / Turbo>
时长：<真实支持值>
画幅：<真实配置>
分辨率：<真实配置>
音频：<true / false / 不支持>
运动幅度：<真实配置或不适用>

输入素材：
1. <图片/主体名> — <唯一用途>
2. <图片/主体名> — <唯一用途>

## 提交正文

<可直接提交给当前 Q3 接口的自然语言正文>
```

交付前运行：

```text
python .cursor/skills/vidu-q3-video-prompt/scripts/validate_vidu_q3_prompt.py <提示词文件>
```

校验通过不等于生成授权。
