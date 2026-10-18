# 画布执行

> **Seedance 使用边界：** 本文件只负责把已定稿成果放到画布上或执行已经逐次授权的 Toonflow 视频生成，不参与 Seedance prompt 的创作。只要已有可执行剧本/时间轴且目标进入视频制作/生成/修订，必须先由主 `SKILL.md` 的“Seedance 路由锁存”进入内嵌 PART A；**不得把五个画布读取工具或节点配置当作 Seedance 之前的入口步骤。** 正式提示词必须先由 PART A 规划/定稿；本文件不得重新分段、改写 A9.1/A9.2 格式、替换 Timeline、补表演/运镜/连续性规则。用户对画幅、分辨率、模式、音频等配置问题的回答只补充当前任务的执行参数，不解除或重置 Seedance 路由。

只用本轮实际提供的工具操作当前 Toonflow 画布。画布负责存放正文、建立连线、挂载媒体，并可在用户逐次明确授权后调用内置视频模型。不调用 `node:generateImage`、`node:generateAudio`，不用画布供应商出图或出音频。`listMediaModels`、视频节点 `node:setConfig`、`generateVideo` 或 `node:generateVideo` 仅用于本次已授权的视频片段、模型、数量和次数。制作流程见入口，版本和结果记录见[状态与交付](stateAndDelivery.md)。

## 发现与绑定

`getCanvas({})` 只返回激活画布概览；需要类型或画布列表时传 `include: ["nodeTypes"]` 或 `["canvases"]`。用 `findCanvasNodes` 按名称、类型或选择状态定位目标；已知节点 ID 时直接用 `getCanvasNodes` 读取必要字段，`getCanvasEdges` 读取局部连接，`getNodeTools` 发现函数与完整 schema。节点类型可能带运行时前缀，不硬编码。

五个画布读取工具受条数和 64 KiB 体积限制，按 `hasMore` / `nextCursor` 继续分页；节点和连线每页最多扫描 2000 项，空结果但 `hasMore: true` 仍需继续。`totalNodes/totalEdges` 是画布总量而非命中数；`selectedOnly` 现场筛选，不是冻结快照。保持原查询参数，仅替换游标；游标失效重新查询。全图任务分批处理，上下文仅保留当前批次、摘要和游标。`getCanvasNodes` 默认只读 `label/type/position`，端口、正文和输出须显式选择 `ports/data/outputs`；`dataKeys` 仅在选择 `data` 时筛选字段。详情和函数查询的 `nodeIds` 每批最多 20 个，须先去重；移动、重命名、删除和连接每批最多 64 项。

顶层 `nextCursor` 仅用于保持原参数继续节点分页。处理节点任一 `truncated` 时，仅查询所属节点，使用该项路径及偏移，不携带原 `cursor`：`text` 用该项 `path` 和 `nextOffset` 作为 `textOffset` 续读；`entries` 改用 `valueOffset`，没有 `nextOffset` 表示该路径已到末尾。`depth/budget` 沿该项 `path` 缩小范围重新查询，不携带旧 `cursor`；对象/数组的 `valueLimit` 最多 100，字符串的 `textLimit` 最多 4000，正偏移必须指定 `path`。路径最多 64 层和 2048 JSON UTF-8 字节，每段最多 256 字符；`pathDepthLimit/pathBytesLimit/circular` 不可靠重复请求补齐，`keyTooLong` 可用返回的 `nextOffset` 作为 `valueOffset` 跳过该键继续，但被跳过的值仍未读取。不把截断内容当完整证据。

默认复用当前项目和目标画布。有既有台账时核对绑定；用户已明确切换目标则按其授权操作，含糊的“继续”遇到不同绑定先澄清。新建、切换、重命名成功后使用返回的绑定，不沿用旧 ID。

| 工具 | 当前参数形状 |
|---|---|
| `getCanvas` | `{include?:["canvases","nodeTypes"],cursor?,limit?,canvasId?}` |
| `findCanvasNodes` | `{query?,types?,selectedOnly?,cursor?,limit?,canvasId?}` |
| `getCanvasNodes` | `{nodeIds:[...],fields?:["label","type","position","ports","data","outputs"],dataKeys?,path?,valueOffset?,valueLimit?,textOffset?,textLimit?,cursor?,canvasId?}` |
| `getCanvasEdges` | `{nodeIds?:[...],direction?:"incoming"/"outgoing"/"both",cursor?,limit?,canvasId?}` |
| `getNodeTools` | `{nodeIds:[...],names?,cursor?,limit?,canvasId?}` |
| `addNode` | `{type, position:{x,y}, label?}` |
| `nodeTools` | `{nodeId, name:"node:函数名", args:{...}}` |
| `connectNodes` | `{connections:[{source,sourceHandle,target,targetHandle}]}` |
| `moveNodes` | `{moves:[{nodeId,position:{x,y}}]}` |
| `renameNodes` | `{renames:[{nodeId,label}]}` |
| `deleteNodes` / `deleteEdges` | `{nodeIds:[...]}` / `{edgeIds:[...]}` |
| `addCanvas` / `switchCanvas` | `{name?}` / `{canvasId}` |
| `renameCanvas` | `{canvasId?,name}` |
| `fitCanvas` / `arrangeCanvas` | `{nodeIds?}` / `{}` |

批量修改按实际数量限制拆批。`addNode` 不接受任意 `data`、指定 ID 或正文；用返回的 `node.id` 查询 `getNodeTools`，再按完整 schema 用 `nodeTools` 填内容，新增回执不包含函数清单。不要调用旧版单数移动/重命名工具，不直接写画布 JSON。

结构操作的 ID 回执可能缩略为最多 100 项：`arrangeCanvas` 另给 `arrangedCount`，`fitCanvas` 给 `nodeCount`，`deleteNodes` 给 `removedEdgeCount`。`truncated` 只影响返回 ID 列表，不表示只完成预览部分，不为获取完整回执重复操作；改用只读工具核对。`nodeTools` 返回具体业务函数的结果，不受上述五个读取工具的 64 KiB 上限约束。

按现有布局从左到右放内容、资产、片段，同阶段纵向排列，避免覆盖用户节点。用 `fitCanvas` 展示本轮成果；`arrangeCanvas` 会整理全部顶层节点，只在整幅整理属于用户范围时调用。当前没有分组工具，不伪造分组接口。

## 内容与素材节点

- 文本使用该节点实际注册的 `node:setText({text})`。成功后用 `getCanvasNodes({ nodeIds: [目标ID], fields: ["data"], dataKeys: ["textPath"] })` 回读路径，读取对应正文核对并登记；`setText` 当前只返回正文，不返回路径。需要查看当前内存正文时用 `getCanvasNodes` 的 `path: ["outputs", "text", "value"]` 分段读取；持久化画布 JSON 不保存这份内联正文，不能据此判断文本为空。
- 正文由节点编辑与保存，不直接写其 `textPath` 绕过界面。状态文件和版本快照用实际文本文件工具保存；快照不作为第二份可编辑正文。
- 素材通过发现的 `node:setImage`、`node:setVideo`、`node:setAudio` 挂载，当前通常为 `{path,mimeType}`。`path` 使用工作区相对路径，指向本工作区实际存在、可读取的文件，不能填写预期输出或外部尚未导入的路径。
- 新图由当前 Agent 的图片工具生成，完成后用图片素材节点 `node:setImage` 挂载。已采用的图继续固定在图片素材节点。下一版新建素材节点，保留已采用节点和连接；不为重生成替换仍被下游引用的源节点。
- 文字由当前 Agent 写完后用 `node:setText` 写入。不调用画布文本生成。文件工具不保证支持视频理解或二进制复制，具体边界见[交付](stateAndDelivery.md)。

## 画布上的引用

先用 `getCanvasNodes` 的 `ports` 检查源/目标端口的 ID、方向、类型，用 `getCanvasEdges` 检查已有连接。只把已经采用的媒体接给下游素材节点，不用连线表示阶段、批准或依赖索引。上游还在生成或未采用的候选不能成为正式参考。

提示词的权威正文在文本节点。传给媒体工具或已授权 Toonflow 视频节点的必须是该定稿正文和真实参考文件。参考图、首帧和尾帧按实际接口接受的参数传入；工具不支持的参考方式要先说明，不得静默改模式、改模型或丢弃参考。

## 段间交接执行

1. 每个正式视频交付必须已经包含主 `SKILL.md` A7.3/A9 要求的八项制片交接卡。调用模型前，以 `【制片交接卡｜不发送给模型】` 为边界，只提交前面的模型正文；交接卡不得进入供应商 prompt。
2. 生成下一段前，先按交接卡分别确认连续性关系、视觉切法、剪辑把手、尾帧策略、声音切法和执行归属。
3. 连续关联段必须以**上一段实际画面**为依据，记录人物世界位置、姿态、朝向、持物、动作进度、环境状态和持续声音。计划末态不能冒充实际结果。
4. 同一场戏的下一段提交前，先提取上一段结尾稳定帧。先检查运动模糊、闭眼、肢体变形、遮挡错误、人数和坐法；站位可用才把它作为当前模型的一张参考图。当前模型没有首帧入口时不换模型。结尾站位错误时停住。跨场硬切、闪回、场景重建或时间跳跃不绑定上一场尾帧。
5. 即使绑定尾帧，下一段仍传入完整绝对初态文字，并且这些文字必须和那张真实尾帧一致。
6. 前段正文负责生成可见的“怎么出去”，后段首个镜头/时间块负责生成可见的“怎么进来”。默认由后期完成硬切、叠化、淡入淡出、白闪、冻结帧和 J-cut/L-cut；模型只提供干净把手。只有依赖源剧情已有物理运动、遮挡、撞击或真实灯光变化时才由模型生成，且必须包含在授权时长内。
7. 同一场戏拆成先后两段分别生成时，两段文件落地后按 `stateAndDelivery.md` 做拼接抽帧：上一段结尾稳定帧和下一段开头稳定帧放在一起看。多人场景对人数、画面左右、并排还是隔桌对坐、机位和桌子朝向、脸朝向、持物和服装。单段单独通过不算拼接通过。对不上且剧本没有要求换机位时，后一段标拼接不通过，停在这一场。

## 配置询问不得截断 Seedance

- 本文件中的配置核实只允许发生在主 `SKILL.md` 已经锁存 Seedance 路由、并完成 A0 目标模型确认之后；若用户未指定 2.0/2.5，主 PART A 必须先用一次简短提问确认“Seedance 2.0 还是 2.5”。这个模型确认问题由主 PART A 负责，本文件不得自行选择默认模型，也不得重复询问。
- 若执行工具必须向用户确认画幅、分辨率、是否生成音频等参数，提问和用户回答都属于同一 Seedance 任务的执行参数补充。回答后继续使用 PART A 已规划/定稿的提示词，不重新进入通用工作流。
- 若用户在配置回答中明确把模型改为 2.0/2.5，这属于 A0 输入更新：回到 PART A 按新目标模型重新路由受影响的正式提示词，然后再回本文件挂载结果；不得仅在节点配置层换模型而继续使用另一模型的提示词外壳。
- 若当前 Agent 的视频工具不支持 PART A 目标模型，默认报告能力冲突并停在已批准提示词。只有用户针对本次片段、模型、数量和次数逐次明确授权，且 Toonflow 内置视频模型与 PART A 目标模型完全一致时，才可调用；不得使用节点默认模型或静默替换。

## 生成与挂载

1. 核对真实执行工具实际接受的模型、参考、画幅、尺寸、时长和声音参数。图片和音频不得改走 Toonflow 供应商；视频只有逐次明确授权后才可使用 Toonflow 内置模型。
2. 固定本次方案：片段、数量、完整提示词、模型、参数、参考文件与用途、执行次数；展示并取得本次算力授权。报价或额度可可靠查询时如实展示，无法查询时标记未知，但不阻止已获授权的 Toonflow 视频任务提交。
3. 用户批准后只执行授权范围。Toonflow 视频一次授权只提交约定次数，不自动重试、不扩大批次、不切换模型；参考必须使用工作区里真实存在且已确认的文件。
4. 任务提交后记录真实任务 ID 和返回状态。失败、超时或结果不明确时先查询同一任务，不重复提交；任何额外尝试必须重新展示方案并取得授权。
5. Toonflow 视频任务结束后记录任务 ID、实际模型、参数、状态和返回文件。不强制读取生成前后额度或计算损耗；接口主动返回额度信息时可据实附记。
6. 工具返回真实文件后，复制或保存到当前工作区的可读路径。画布模式用视频素材节点挂载或回读内置生成节点的真实输出；`path` 使用工作区相对路径。挂载后回读输出。
7. 不调用 `node:generateImage`、`node:generateAudio`。同一已授权批次里，不依赖彼此结果的对象可以继续；依赖基础图、变体或前段采用结果的对象必须等待。

生成失败先确认结果状态及原因。工具返回不明确时不盲重试，以免重复消耗算力；改变方案和额外尝试核对授权范围。

结果能读取时按实际能力检查；视频采用和下一片段接戏见[状态与交付](stateAndDelivery.md)。只有实际确认采用的文件才固定为素材节点。归属不清时询问这次输出对应哪次生成，先不下游采用。
