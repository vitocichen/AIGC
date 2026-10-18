---
name: chenyu-minimax-submit
description: >-
  把 MiniMax H3 的融合Ref｜8步用 HTTP 提交到用户当次确认仍在线的晨羽智云 ComfyUI，不控制鼠标、不点击网页。
  用户要在晨羽、Chenyu、ComfyUI 云上生成 MiniMax，或提到融合Ref｜8步、ref 8步，或别的 Agent 说没有云接口、想点网页代生成时使用。
---

# 晨羽 ComfyUI 提交 MiniMax H3

网页上的「生成」背后就是这几个 HTTP 接口。别的 Agent 没有浏览器权限时，用同一套接口提交。不要控制鼠标，不要点击 ComfyUI 页面，不要叫用户自己去网页点生成。

不调用 Toonflow 的 `generateVideo`、`node:generateVideo`。不把旧地址当成还活着。

## 地址

只用用户在当次对话里确认仍在线的 Pod 根地址，形如 `https://<id>.gz15.chenyu.cn`。地址末尾不要多余斜杠。

先请求 `GET /queue`。

- 返回 `404` 且正文含「未获取到Pod地址」：机器已关。停下，说明地址失效，不换地址重交，不重试。
- `queue_running` 或 `queue_pending` 非空：停下，不插队。
- `502`、`503`、`504` 或短暂断连：最多重试 6 次，每次间隔 8 秒。
- 目标成片文件已经存在：不重复提交。

## 提示词

正文按 `workflow` 的 Seedance 2.5 A9.2，并先通过 `validate_seedance_prompt.py --model 2.5`。

发给模型的字符串必须：

- 去掉 `【制片交接卡｜不发送给模型】` 及其后全部内容。交接卡留在磁盘文件里。
- 把参考图行里的文件名换成 `- 参考图`。可用 `(?m)^- \S+\.(?:png|jpg|jpeg|webp)` 替换。磁盘上的提示词仍保留真实路径。
- 确认发出的字符串里没有交接卡、图片文件名和 `first_frame`。

## 上传参考图

`POST /upload/image`，`multipart/form-data`。

- 字段 `overwrite` 为 `true`。
- 字段 `image` 为文件。远程文件名只用英文和数字，例如 `g01_face.png`。中文文件名会烧到画面上。
- 响应里的 `name` 就是工作流 `LoadImage` 要用的名字。

## 工作流

云上只用这一套，简写是 **融合Ref｜8步**。别的 Agent 看到「融合Ref｜8步」「融合 Ref 8 步」或「ref 8步」，就是下面这个工作流，不要换成 FL2VA、25 步或 Wan。

`POST /prompt`，JSON 为 `{"prompt": <下图>, "client_id": <随机>}`。`1344×768`，24fps，不加 FL2VA，不接 `first_frame`。参考图从 `reference_image_0` 往后接，每张一个 `LoadImage`。

时长帧数用 `max(5, round(秒 × 24))`，再补到能被当前融合步长接受的长度：`帧 + (5 - 帧 % 17) % 17`。一次不超过规则里的上限。当前上限是 8 秒、192 帧。更长不要提交。

节点：

- `UNETLoader`：`MiniMax/minimax_h3_fused_refdelta_r1024_turbo8_mystic07_int8_convrot.safetensors`，`weight_dtype` 为 `default`
- `MiniMaxLowVRAMAttention`：`head_chunks` 为 8
- 视频 VAE：`minimax-h3/minimax_h3_video_vae_fp16.safetensors`
- 音频 VAE：`minimax-h3/minimax_h3_audio_vae_fp32.safetensors`
- `CLIPLoader`：`minimax-h3/qwen3vl_32b_minimax_h3_int8_convrot.safetensors`，`type` 为 `minimax`
- `MiniMaxH3DirectorConditioning`：`width` 1344，`height` 768，`ref_image_size` 为 `match`，`latent` 取该节点输出 1
- `MiniMaxH3SigmaShift`：`shift_video` 6，`shift_audio` 3
- `KSamplerSelect`：`euler`
- `BasicScheduler`：`simple`，`steps` 8，`denoise` 1
- `RandomNoise` 写入当次种子。已用过的种子不复用
- `VAEDecode` 接视频 VAE，`VAEDecodeAudio` 接音频 VAE
- `CreateVideo`：`fps` 24，`bit_depth` 8
- `SaveVideo`：`format` 为 `mp4`，`codec` 为 `auto`。`filename_prefix` 只用英文

`node_errors` 非空则停止，不自动再交一次。

## 取回

用返回的 `prompt_id` 轮询 `GET /history/{prompt_id}`，直到 `status_str` 为 `success` 或 `error`。轮询间隔约 12 秒，单次任务不超过 30 分钟。

`error` 时记下消息并停止，不换同一套参数自动重交。

成功后从输出里找 `.mp4`，用 `GET /view?filename&subfolder&type` 下载到项目里的人类可读路径。记录 `prompt_id`、`execution_start`、`execution_success`、本地文件路径和字节数。生成成功不等于采用。

可参考的实现：`信光/生成素材/视频/G01_半写实工作文件/G01_按新规则连续提交.py`。那里的 Pod 地址只对那一次有效，下次必须用用户新确认的地址。
