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
- `502`、`503`、`504` 或短暂断连：最多重试 6 次，每次间隔 8 秒。
- 目标成片文件已经存在：不重复提交。
- 同一条已经在 `queue_running` 或 `queue_pending` 里：不重复提交。
- 队列里是别人的任务：不插队。

## 不让机器空转

用户选了云端 ComfyUI，并且已经授权这一批生成段时，按最省空转的顺序连续提交。不等用户逐段回来看，也不等上一段被采用。

- 换地点、闪回、时间跳，以及一场的第一段，不靠上一段结尾。这些段可以先放进 `queue_pending` 填空档。成片顺序更靠前的段优先于这些后场。
- 上一段的 `history` 一变成 `success`，立刻 `POST /queue`，正文 `{"delete": [那些尚未开算的后场 prompt_id]}`，把它们从 `queue_pending` 拿下。正在 `queue_running` 的那一条不删、不打断。然后下载并核对这一段的地点、墙面、陈设、衣服、人数、左右和持物。
- 同一场的下一段对得上：先交这一段，提交体加 `"front": true`，插到还没开算的后场前面。再把刚才拿下的后场按原来的先后排回去。不用等那些后场算完。对不上就停这一场，后场按原顺序重新放回队列。
- 一次要插上多条更靠前的段时，按成片顺序从后往前用 `front: true` 提交，保证号小的先算。不要把还没看过上一段结尾的段插到它的上一段前面。
- 用户写明「一段段生成」时，每段结束就停下等用户。不要把后场放进队列。
- 只提交这次授权清单里的段。失败的同一套参数不自动再交。`node_errors` 非空也停止，不自动再交。
- 生成成功仍是待验收，不代替采用。

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

云上没有可下载的工作流模板。不要探测 `/api/workflows`、`/api/templates`、`/userdata/workflows`，也不要让用户从浏览器导出 JSON。下面这张图就是提交体，直接 `POST /prompt`。

`1344×768`，24fps，不加 FL2VA，不接 `first_frame`。`PROMPT`、`LENGTH`、`SEED`、`PREFIX` 和 `UPLOADED_NAME` 换成当次的值。参考图每增加一张，就加一个 `LoadImage`，并在节点 `11` 上增加 `reference_image_1`、`reference_image_2`……连到对应节点。采样用的 latent 是节点 `11` 的输出 1，不是输出 0。

时长帧数用 `max(5, round(秒 × 24))`，再补到能被当前融合步长接受的长度：`帧 + (5 - 帧 % 17) % 17`。一次不超过规则里的上限。当前上限是 8 秒、192 帧。8 秒就是 192 帧。更长不要提交。

```json
{
  "prompt": {
    "1": {"class_type": "UNETLoader", "inputs": {"unet_name": "MiniMax/minimax_h3_fused_refdelta_r1024_turbo8_mystic07_int8_convrot.safetensors", "weight_dtype": "default"}},
    "2": {"class_type": "MiniMaxLowVRAMAttention", "inputs": {"model": ["1", 0], "head_chunks": 8}},
    "4": {"class_type": "VAELoader", "inputs": {"vae_name": "minimax-h3/minimax_h3_video_vae_fp16.safetensors"}},
    "5": {"class_type": "VAELoader", "inputs": {"vae_name": "minimax-h3/minimax_h3_audio_vae_fp32.safetensors"}},
    "6": {"class_type": "CLIPLoader", "inputs": {"clip_name": "minimax-h3/qwen3vl_32b_minimax_h3_int8_convrot.safetensors", "type": "minimax", "device": "default"}},
    "31": {"class_type": "LoadImage", "inputs": {"image": "UPLOADED_NAME"}},
    "11": {"class_type": "MiniMaxH3DirectorConditioning", "inputs": {
      "clip": ["6", 0], "vae": ["4", 0], "audio_vae": ["5", 0], "prompt": "PROMPT",
      "width": 1344, "height": 768, "length": "LENGTH", "ref_image_size": "match",
      "reference_image_0": ["31", 0]
    }},
    "12": {"class_type": "MiniMaxH3SigmaShift", "inputs": {"model": ["2", 0], "shift_video": 6.0, "shift_audio": 3.0}},
    "13": {"class_type": "RandomNoise", "inputs": {"noise_seed": "SEED"}},
    "14": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler"}},
    "15": {"class_type": "BasicScheduler", "inputs": {"model": ["12", 0], "scheduler": "simple", "steps": 8, "denoise": 1.0}},
    "16": {"class_type": "BasicGuider", "inputs": {"model": ["12", 0], "conditioning": ["11", 0]}},
    "17": {"class_type": "SamplerCustomAdvanced", "inputs": {"noise": ["13", 0], "guider": ["16", 0], "sampler": ["14", 0], "sigmas": ["15", 0], "latent_image": ["11", 1]}},
    "18": {"class_type": "VAEDecode", "inputs": {"samples": ["17", 0], "vae": ["4", 0]}},
    "19": {"class_type": "VAEDecodeAudio", "inputs": {"samples": ["17", 0], "vae": ["5", 0]}},
    "20": {"class_type": "CreateVideo", "inputs": {"images": ["18", 0], "fps": 24.0, "audio": ["19", 0], "bit_depth": 8}},
    "21": {"class_type": "SaveVideo", "inputs": {"video": ["20", 0], "filename_prefix": "PREFIX", "format": "mp4", "codec": "auto"}}
  },
  "client_id": "随机字符串"
}
```

`length` 和 `noise_seed` 必须是数字，不要保留引号。`node_errors` 非空则停止，不自动再交一次。不要再叠 LoRA。

## 取回

用返回的 `prompt_id` 轮询 `GET /history/{prompt_id}`，直到 `status_str` 为 `success` 或 `error`。轮询间隔约 12 秒，单次任务不超过 30 分钟。

`error` 时记下消息并停止，不换同一套参数自动重交。

成功后从输出里找 `.mp4`，用 `GET /view?filename&subfolder&type` 下载到项目里的人类可读路径。记录 `prompt_id`、`execution_start`、`execution_success`、本地文件路径和字节数。生成成功不等于采用。

上面的 JSON 就是完整工作流，不依赖本机脚本，也不依赖浏览器导出。Pod 地址只用用户当次确认仍在线的那一个。
