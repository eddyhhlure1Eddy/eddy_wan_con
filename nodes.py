AUTHOR = "eddy"
import os
import gc
import re
import hashlib
import torch
import sys
from comfy import model_management as mm

wrapper_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ComfyUI-WanVideoWrapper"))
if wrapper_path not in sys.path:
    sys.path.insert(0, wrapper_path)

import importlib.util
spec = importlib.util.spec_from_file_location("wan_utils", os.path.join(wrapper_path, "utils.py"))
wan_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wan_utils)
log = wan_utils.log
set_module_tensor_to_device = wan_utils.set_module_tensor_to_device

script_directory = os.path.dirname(os.path.abspath(__file__))
offload_device = mm.unet_offload_device()
cache_dir = os.path.join(script_directory, 'text_embed_cache')

def get_cache_path(prompt):
    cache_key = prompt.strip()
    cache_hash = hashlib.sha256(cache_key.encode('utf-8')).hexdigest()
    return os.path.join(cache_dir, f"{cache_hash}.pt")

def get_cached_text_embeds(positive_prompt, negative_prompt):
    os.makedirs(cache_dir, exist_ok=True)
    context = None
    context_null = None
    pos_cache_path = get_cache_path(positive_prompt)
    neg_cache_path = get_cache_path(negative_prompt)
    if os.path.exists(pos_cache_path):
        try:
            log.info(f"Loading prompt embeds from cache: {pos_cache_path}")
            context = torch.load(pos_cache_path)
        except Exception as e:
            log.warning(f"Failed to load cache: {e}, will re-encode.")
    if os.path.exists(neg_cache_path):
        try:
            log.info(f"Loading prompt embeds from cache: {neg_cache_path}")
            context_null = torch.load(neg_cache_path)
        except Exception as e:
            log.warning(f"Failed to load cache: {e}, will re-encode.")
    return context, context_null


class EddyWanVideoTextEncode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "positive_prompt": ("STRING", {"default": "", "multiline": True}),
                "negative_prompt": ("STRING", {"default": "", "multiline": True}),
            },
            "optional": {
                "t5": ("WANTEXTENCODER",),
                "model_to_offload": ("WANVIDEOMODEL", {"tooltip": "Model to move to offload_device before encoding"}),
                "enable_cinematic": ("BOOLEAN", {"default": True}),
                "visual_style": ([
                    "none",
                    "photorealistic / 写实",
                    "anime style / 二次元动画",
                    "cel-shaded / 三渲二",
                    "2.5D anime / 2.5D动漫",
                    "Chinese style / 国风",
                    "ink painting / 水墨画",
                    "pixel art / 像素风格",
                    "3D game / 3D游戏",
                    "puppet animation / 木偶动画",
                    "impressionist / 印象派",
                    "watercolor / 水彩",
                    "cyberpunk / 赛博朋克",
                    "steampunk / 蒸汽朋克",
                    "tilt-shift / 移轴摄影",
                    "time-lapse / 延时摄影",
                    "handheld camera / 手持",
                    "fashion magazine / 时尚杂志",
                    "vintage film / 复古电影",
                    "CGI stylized / CGI风格化"
                ], {"default": "none"}),
                "time": ([
                    "none",
                    "Day time / 白天",
                    "Night time / 夜晚",
                    "Dawn time / 黎明",
                    "Sunrise time / 日出"
                ], {"default": "none"}),
                "light_source": ([
                    "none",
                    "Daylight / 日光",
                    "Artificial lighting / 人工光",
                    "Moonlight / 月光",
                    "Practical lighting / 实用光",
                    "Firelight / 火光",
                    "Fluorescent lighting / 荧光",
                    "Overcast lighting / 阴天光",
                    "Sunny lighting / 晴天光"
                ], {"default": "none"}),
                "light_intensity": ([
                    "none",
                    "Soft lighting / 柔光",
                    "Hard lighting / 硬光",
                    "Diffused lighting / 漫射光",
                    "Dramatic lighting / 戏剧光",
                    "Ambient lighting / 环境光",
                    "Contrasty lighting / 对比光"
                ], {"default": "none"}),
                "light_angle": ([
                    "none",
                    "Top lighting / 顶光",
                    "Side lighting / 侧光",
                    "Underlighting / 底光",
                    "Edge lighting / 边缘光"
                ], {"default": "none"}),
                "color_tone": ([
                    "none",
                    "Warm colors / 暖色调",
                    "Cool colors / 冷色调",
                    "Mixed colors / 混合色调"
                ], {"default": "none"}),
                "shot_size": ([
                    "none",
                    "Medium shot / 中景",
                    "Medium close-up shot / 中近景",
                    "Wide shot / 全景",
                    "Medium wide shot / 中全景",
                    "Close-up shot / 近景",
                    "Extreme close-up shot / 特写",
                    "Extreme wide shot / 大全景"
                ], {"default": "none"}),
                "camera_angle": ([
                    "none",
                    "Over-the-shoulder shot / 过肩镜头",
                    "Low angle shot / 低角度",
                    "High angle shot / 高角度",
                    "Dutch angle shot / 倾斜角度",
                    "Aerial shot / 航拍",
                    "Overhead shot / 俯视"
                ], {"default": "none"}),
                "composition": ([
                    "none",
                    "Center composition / 中心构图",
                    "Balanced composition / 平衡构图",
                    "Right-heavy composition / 右侧重构图",
                    "Left-heavy composition / 左侧重构图",
                    "Symmetrical composition / 对称构图",
                    "Short-side composition / 短边构图"
                ], {"default": "none"}),
                "camera_motion": ([
                    "none",
                    "static / 静止 ✓",
                    "pan left / 左摇 ✓",
                    "pan right / 右摇 ✓",
                    "tilt up / 上倾 ✓",
                    "tilt down / 下倾 ✓",
                    "dolly in / 推进 ✓",
                    "dolly out / 拉远 ✓",
                    "pull back / 后退 ✓",
                    "zoom in / 放大 ✓",
                    "zoom out / 缩小 ✓",
                    "crash zoom / 快速变焦 ✓",
                    "crane up / 升起 ✓",
                    "crane down / 下降 ✓",
                    "orbital arc / 环绕弧线 ⚠",
                    "orbiting shot / 环绕镜头 ⚠",
                    "orbit left / 左环绕 (不推荐)",
                    "orbit right / 右环绕 (不推荐)",
                    "360 orbit / 360度环绕 (不稳定)",
                    "tracking shot / 跟踪镜头 ✓",
                    "track upward / 上跟踪 ✓",
                    "track downward / 下跟踪 ✓",
                    "camera roll / 镜头翻滚 ✓",
                    "slow-motion / 慢动作 ✓",
                    "slow-motion pan left / 慢动作左摇 (分开使用)",
                    "slow-motion pan right / 慢动作右摇 (分开使用)",
                    "rapid whip-pan / 快速甩镜 ✓",
                    "rapid whip-pan left / 快速左甩 (不必指定方向)",
                    "rapid whip-pan right / 快速右甩 (不必指定方向)",
                    "time-lapse / 延时摄影 ✓"
                ], {"default": "none"}),
                "color_grading": ([
                    "none",
                    "teal-and-orange / 橘蓝调色",
                    "bleach-bypass / 漂白旁路",
                    "kodak portra / 柯达Portra"
                ], {"default": "none"}),
                "lighting_style": ([
                    "none",
                    "volumetric dusk / 体积黄昏",
                    "harsh noon sun / 正午强光",
                    "neon rim light / 霓虹缘光",
                    "rembrandt lighting / 伦勃朗光",
                    "three-point lighting / 三点光",
                    "backlighting / 逆光",
                    "dappled sunlight / 斑驳阳光",
                    "golden hour / 黄金时刻",
                    "blue hour / 蓝色时刻",
                    "magic hour / 魔法时刻",
                    "high-key lighting / 高调光",
                    "low-key lighting / 低调光",
                    "chiaroscuro lighting / 明暗对照",
                    "butterfly lighting / 蝴蝶光",
                    "loop lighting / 环形光",
                    "split lighting / 分割光"
                ], {"default": "none"}),
                "lens_style": ([
                    "none",
                    "anamorphic bokeh / 变形宽银幕虚化",
                    "16mm grain / 16mm胶片颗粒",
                    "CGI stylized / CGI风格化"
                ], {"default": "none"}),
                "film_stock": ([
                    "none",
                    "Kodak Vision3 500T / 柯达500T",
                    "Kodak Ektachrome / 柯达Ektachrome",
                    "Cinestill 800T / Cinestill 800T",
                    "Fujifilm Velvia 50 / 富士Velvia 50",
                    "Fuji Eterna / 富士Eterna",
                    "Ilford HP5 / Ilford HP5"
                ], {"default": "none"}),
                "color_palette": ([
                    "none",
                    "high-contrast / 高对比度",
                    "low-contrast / 低对比度",
                    "low-saturation / 低饱和度",
                    "muted colors / 柔和色",
                    "pastel tones / 马卡龙色",
                    "monochrome / 单色",
                    "sepia tone / 棕褐色",
                    "duotone cyan-orange / 青橙双色"
                ], {"default": "none"}),
                "lighting_technique": ([
                    "none",
                    "key light / 主光",
                    "fill light / 补光",
                    "rim light / 轮廓光",
                    "hair light / 发光",
                    "background light / 背景光",
                    "practical light source / 实用光源"
                ], {"default": "none"}),
                "force_offload": ("BOOLEAN", {"default": True}),
                "use_disk_cache": ("BOOLEAN", {"default": False}),
                "device": (["gpu", "cpu"], {"default": "gpu"}),
            }
        }

    RETURN_TYPES = ("WANVIDEOTEXTEMBEDS",)
    RETURN_NAMES = ("text_embeds",)
    FUNCTION = "process"
    CATEGORY = "EddyWanCon"
    DESCRIPTION = "Eddy's standalone WanVideo TextEncode with integrated cinematic and motion controls"

    def process(self, positive_prompt, negative_prompt, t5=None, model_to_offload=None,
                enable_cinematic=True, visual_style="none", time="none", light_source="none",
                light_intensity="none", light_angle="none",
                color_tone="none", shot_size="none",
                camera_angle="none", composition="none",
                camera_motion="none", color_grading="none", lighting_style="none",
                lens_style="none", film_stock="none", color_palette="none",
                lighting_technique="none",
                force_offload=True, use_disk_cache=False, device="gpu"):

        if enable_cinematic:
            terms = []
            prefix_map = [
                ("视觉风格", visual_style),
                ("时间", time),
                ("光源", light_source),
                ("光线强度", light_intensity),
                ("光线角度", light_angle),
                ("色调", color_tone),
                ("镜头尺寸", shot_size),
                ("拍摄角度", camera_angle),
                ("构图", composition),
                ("运镜", camera_motion),
                ("调色", color_grading),
                ("光照风格", lighting_style),
                ("镜头风格", lens_style),
                ("胶片", film_stock),
                ("色彩母题", color_palette),
                ("打光技术", lighting_technique)
            ]
            
            for prefix_cn, value in prefix_map:
                if value != "none" and value:
                    # Extract English part only (before " / ")
                    value_en = value.split(" / ")[0] if " / " in value else value
                    # Remove UI annotations (✓, ⚠, and parentheses notes)
                    value_en = value_en.replace(" ✓", "").replace(" ⚠", "").strip()
                    # Remove any parentheses notes like (不推荐), (不稳定), etc.
                    if "(" in value_en:
                        value_en = value_en.split("(")[0].strip()
                    terms.append(f"{prefix_cn}：{value_en}")
            
            if terms:
                prefix = ", ".join(terms)
                positive_prompt = f"{prefix}, {positive_prompt}".strip()
                log.info(f"Applied cinematic prefix: {prefix}")

        echoshot = True if "[1]" in positive_prompt else False

        if use_disk_cache:
            context, context_null = get_cached_text_embeds(positive_prompt, negative_prompt)
            if context is not None and context_null is not None:
                return ({"prompt_embeds": context, "negative_prompt_embeds": context_null, "echoshot": echoshot},)
        
        if t5 is None:
            raise ValueError("T5 encoder is required for text encoding. Please provide a valid T5 encoder or enable disk cache.")

        if model_to_offload is not None and device == "gpu":
            try:
                log.info(f"Moving video model to {offload_device}")
                model_to_offload.model.to(offload_device)
            except:
                pass

        encoder = t5["model"]
        dtype = t5["dtype"]

        positive_prompts = []
        all_weights = []

        if "|" in positive_prompt:
            log.info("Multiple positive prompts detected, splitting by '|'")
            positive_prompts_raw = [p.strip() for p in positive_prompt.split('|')]
        elif "[1]" in positive_prompt:
            log.info("Multiple positive prompts detected, splitting by [#] and enabling EchoShot")
            segments = re.split(r'\[\d+\]', positive_prompt)
            positive_prompts_raw = [segment.strip() for segment in segments if segment.strip()]
            assert len(positive_prompts_raw) > 1 and len(positive_prompts_raw) < 7, 'Input shot num must between 2~6 !'
        else:
            positive_prompts_raw = [positive_prompt.strip()]

        for p in positive_prompts_raw:
            cleaned_prompt, weights = self.parse_prompt_weights(p)
            positive_prompts.append(cleaned_prompt)
            all_weights.append(weights)

        mm.soft_empty_cache()

        if device == "gpu":
            device_to = mm.get_torch_device()
        else:
            device_to = torch.device("cpu")

        if encoder.quantization == "fp8_e4m3fn":
            cast_dtype = torch.float8_e4m3fn
        else:
            cast_dtype = encoder.dtype

        params_to_keep = {'norm', 'pos_embedding', 'token_embedding'}
        for name, param in encoder.model.named_parameters():
            dtype_to_use = dtype if any(keyword in name for keyword in params_to_keep) else cast_dtype
            value = encoder.state_dict[name] if hasattr(encoder, 'state_dict') else encoder.model.state_dict()[name]
            set_module_tensor_to_device(encoder.model, name, device=device_to, dtype=dtype_to_use, value=value)

        if hasattr(encoder, 'state_dict'):
            del encoder.state_dict
            mm.soft_empty_cache()
            gc.collect()

        with torch.autocast(device_type=mm.get_autocast_device(device_to), dtype=encoder.dtype, enabled=encoder.quantization != 'disabled'):
            context = encoder(positive_prompts, device_to)
            for i, weights in enumerate(all_weights):
                for text, weight in weights.items():
                    log.info(f"Applying weight {weight} to prompt: {text}")
                    if len(weights) > 0:
                        context[i] = context[i] * weight
            context_null = encoder([negative_prompt], device_to)

        if force_offload:
            encoder.model.to(offload_device)
            mm.soft_empty_cache()
            gc.collect()

        if use_disk_cache:
            pos_cache_path = get_cache_path(positive_prompt)
            neg_cache_path = get_cache_path(negative_prompt)
            try:
                if not os.path.exists(pos_cache_path):
                    torch.save(context, pos_cache_path)
                    log.info(f"Saved prompt embeds to cache: {pos_cache_path}")
            except Exception as e:
                log.warning(f"Failed to save cache: {e}")
            try:
                if not os.path.exists(neg_cache_path):
                    torch.save(context_null, neg_cache_path)
                    log.info(f"Saved prompt embeds to cache: {neg_cache_path}")
            except Exception as e:
                log.warning(f"Failed to save cache: {e}")

        return ({"prompt_embeds": context, "negative_prompt_embeds": context_null, "echoshot": echoshot},)

    def parse_prompt_weights(self, prompt):
        pattern = r'\((.*?):([\d\.]+)\)'
        matches = re.findall(pattern, prompt)
        cleaned_prompt = prompt
        weights = {}
        for match in matches:
            text, weight = match
            orig_text = f"({text}:{weight})"
            cleaned_prompt = cleaned_prompt.replace(orig_text, text)
            weights[text] = float(weight)
        return cleaned_prompt, weights


NODE_CLASS_MAPPINGS = {
    "EddyWanVideoTextEncode": EddyWanVideoTextEncode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EddyWanVideoTextEncode": "Eddy WanVideo TextEncode (Cinematic)",
}
