---
name: vidu-q2-video-prompt
description: 为 Vidu Q2 系列的文生、图生、首尾帧和参考生接口编写型号匹配的正式提示词，重点支持低成本 Q2 Pro Fast。
---

# Vidu Q2 视频提示词

仅在 Vidu 总路由已经锁定为 Q2 时使用。

主要来源：

- [Vidu Q2 文生视频](https://platform.vidu.com/docs/api-reference/video-models/vidu-q2/text-to-video)
- [Vidu Q2 图生视频](https://platform.vidu.com/docs/api-reference/video-models/vidu-q2/image-to-video)
- [Vidu Q2 首尾帧](https://platform.vidu.com/docs/api-reference/video-models/vidu-q2/start-end-to-video)
- [Vidu Q2 参考生视频](https://platform.vidu.com/docs/api-reference/video-models/vidu-q2/reference-to-video)
- [Vidu 官方更新公告](https://platform.vidu.com/docs/api-reference/updates)
- [阿里云 Q2 Pro Fast](https://help.aliyun.com/zh/model-studio/viduq2-pro-fast-img2video)
- [阿里云 Vidu 图生视频 API](https://help.aliyun.com/zh/model-studio/vidu-image-to-video-api-reference)
- [阿里云 Vidu Prompt 指南](https://help.aliyun.com/zh/model-studio/vidu-video-generation-prompt-guide)

## 型号能力路由

### Q2 Pro Fast

官方 ID：

- Vidu 直连：`viduq2-pro-fast`
- 阿里云：`vidu/viduq2-pro-fast_img2video`

只用于：

- 图生视频；
- 首尾帧生视频。

不得用于 Reference-to-Video，不得写 `[@角色]`、多参考主体或“图1场景、图2角色、图3道具”的独立参考绑定。需要角色、场景、道具时，先把它们合成一张完整首帧；需要严格终点时再提供尾帧。

常见能力：

- 图生时长：1–10 秒；
- 首尾帧时长在不同渠道文档中存在 1–8 与 1–10 秒差异，必须读取实际接口；
- 分辨率：720p / 1080p，默认通常 720p；
- 阿里云 Q2 Pro Fast 不提供 Q3 的原生音频开关，默认按无声视频处理，除非当前节点明确返回支持；
- 图生可使用 `movement_amplitude=auto|small|medium|large`；
- 设置自动推荐提示词时可能忽略手写 prompt，因此正式制作默认 `is_rec=false`。

### Q2 Pro

常见 ID：

- Vidu 直连：`viduq2-pro`
- 阿里云图生：`vidu/viduq2-pro_img2video`
- 阿里云参考生：`vidu/viduq2-pro_reference2video`

支持图生、首尾帧和参考生。参考生可使用图片主体；Vidu 官方文档显示，无视频参考时可上传 1–7 张图片，带视频参考时通常为 1–4 张图片，并支持 1–2 个参考视频。实际数量服从当前供应商接口。

### Q2 Turbo

常见 ID：

- Vidu 直连：`viduq2-turbo`
- 阿里云：`vidu/viduq2-turbo_img2video`

主要用于图生和首尾帧。不得因为名字含 Q2 就假设支持 Q2 Pro 的视频参考或多主体能力。

### Q2 基础模型

`viduq2` 可用于文生视频和对应参考生能力；文生通常支持 1–10 秒及 540p/720p/1080p。使用参考生时按当前接口选择图片列表或 subject 调用，不能借用 Pro Fast ID。

## 选择规则

- 最低成本、已有完整首帧：优先 Q2 Pro Fast 图生。
- 需要锁定结尾：Q2 Pro Fast 首尾帧。
- 需要角色、场景、道具分别作为参考：Q2 Pro Reference，不得选择 Fast。
- 没有图片：使用支持文生的 Q2 型号，不把空图片请求伪装成图生。
- 用户指定型号与所需输入冲突时，展示冲突和可选型号，由用户决定，不自动升级。

## Q2 Pro Fast 首帧制作要求

首帧已经承担身份、服装、场景、道具、站位、构图和画幅：

- 角色脸、体型和服装必须正确；
- 所需道具已经出现在正确手或位置；
- 画面是视频真实起点，不使用角色设定拼版；
- 多人镜头先在首帧完成空间关系；
- 输入图画幅就是输出画幅依据。

提示词不要重复大段身份描述与首帧竞争，重点控制动作、表情、环境运动、摄影和结束状态。

## 图生视频正文

结构：

1. 风格、景别、机位、构图、运镜和动态幅度；
2. 明确“从输入首帧开始”；
3. 按时间顺序写一个主要动作链；
4. 写环境次级运动和光线；
5. 写结束姿态及无字幕、无多余人物、无畸形等可见限制。

适合 Q2 Fast 的提示词应单镜头、主体少、动作明确。不要在 10 秒内塞多次切镜、大幅换景和多个复杂事件。

## 首尾帧正文

- 输入1是首帧，输入2是尾帧；
- 两帧宽高比一致，分辨率接近，角色、服装、道具和场景连续；
- 正文只写中间如何自然过渡，不重复要求与尾帧冲突的结束状态；
- 明确镜头是否固定、推进或移动，避免同时要求互斥运镜；
- 尾帧变化过大时拆段，不靠提示词强行瞬移。

## Q2 Reference 正文

仅用于真正支持 Reference-to-Video 的型号：

- Vidu subject 接口使用 `[@主体名]`；
- 阿里云顺序媒体接口按实际顺序使用“图1为……；图2为……”；
- 不同时输出两套绑定语法，除非调用层真实建立了两套映射；
- 身份由参考素材控制，正文主要写动作、环境、灯光、镜头和交互；
- 提示词外貌描述不得与参考图冲突。

## 字符与参数

不同 Q2 页面曾出现 1500、2000、5000 字符上限。规则如下：

1. 优先读取当前供应商和当前接口返回的限制；
2. 直连图生按不超过 2000 字符；
3. 未能确认时，提交正文控制在 1500 个字符以内；
4. 不为填满上限堆叠同义词。

`is_rec=true` 时部分接口会忽略手写 prompt，且可能额外计费。正式手写提示词默认记录：

```text
is_rec：false
```

## 正式文件模板

```text
# G01 Vidu Q2 提示词

供应商：<Vidu 官方 / 阿里云百炼 / 实际渠道>
系列：Q2
模型：<精确模型 ID>
模式：<文生视频 / 图生视频 / 首尾帧 / 参考生视频>
时长：<真实支持值>
画幅：<输入图画幅或真实参数>
分辨率：<真实配置>
音频：<支持 / 不支持 / 关闭>
运动幅度：<auto / small / medium / large / 不适用>
is_rec：<false / 不适用>

输入素材：
1. <首帧、尾帧或参考素材> — <唯一用途>

## 提交正文

<可直接提交给当前 Q2 接口的自然语言正文>
```

交付前运行：

```text
python .cursor/skills/vidu-q2-video-prompt/scripts/validate_vidu_q2_prompt.py <提示词文件>
```

校验通过不等于生成授权。
