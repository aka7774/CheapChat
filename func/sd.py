from diffusers import AutoPipelineForText2Image, AutoencoderKL, DPMSolverMultistepScheduler
import os
import torch
from torch.cuda import amp
import numpy as np
from PIL import Image
import importlib
import cv2
import shutil
import pathlib
import tqdm
import pytorch_lightning as pl
import base64
import gc
import io
from model import ISNetDIS, ISNetGTEncoder, U2NET, U2NET_full2, U2NET_lite2, MODNet

pipe = None

def model_load():
    global pipe

    if pipe:
        return

    pipe = AutoPipelineForText2Image.from_pretrained(
        "cagliostrolab/animagine-xl-3.0",
        torch_dtype=torch.float16,
        )
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(
        pipe.scheduler.config,
        algorithm_type="sde-dpmsolver++",
        use_karras_sigmas=True
        )
    pipe.to("cuda")
    pipe.enable_vae_slicing()

def model_unload():
    global pipe

    pipe = None
    gc.collect()
    torch.cuda.empty_cache()

def generate(add_prompt):
    prompt = f"""
    masterpiece, best quality, highres intricate detailed
    , 1girl, portrait
    , purple long twintail hair
    , cat ears headdress, frills lolita fashion
    , white background
    , {add_prompt}
    """
    negative_prompt  = "worst quality, low quality"
    # generator = torch.manual_seed(seed)
    image = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        guidance_scale=5.0,
        num_inference_steps=20,
        clip_skip=2,
        # generator=generator,
        ).images[0]

    return image

def pil_to_base64(img, format='webp'):
    buffer = BytesIO()
    img.save(buffer, format)
    img_b64 = base64.b64encode(buffer.getvalue()).decode('ascii')

    return img_b64

# pil_to_base64(image)

def get_mask(model, input_img):
    h, w = input_img.shape[0], input_img.shape[1]
    tmpImg = np.zeros([h, w, 3], dtype=np.float16)
    tmpImg[0:h, 0:w] = cv2.resize(input_img, (w, h)) / 255
    tmpImg = tmpImg.transpose((2, 0, 1))
    tmpImg = torch.from_numpy(tmpImg).unsqueeze(0).type(torch.FloatTensor).to(model.device)
    with torch.no_grad():
        pred = model(tmpImg)
        pred = pred[0, :, 0:h, 0:w]
        pred = cv2.resize(pred.cpu().numpy().transpose((1, 2, 0)), (w, h))[:, :, np.newaxis]
        return pred

def get_net(net_name):
    if net_name == "isnet":
        return ISNetDIS()
    elif net_name == "isnet_is":
        return ISNetDIS()
    elif net_name == "isnet_gt":
        return ISNetGTEncoder()
    elif net_name == "u2net":
        return U2NET_full2()
    elif net_name == "u2netl":
        return U2NET_lite2()
    elif net_name == "modnet":
        return MODNet()
    raise NotImplemented

# from anime-segmentation.train
class AnimeSegmentation(pl.LightningModule):
    def __init__(self, net_name):
        super().__init__()
        assert net_name in ["isnet_is", "isnet", "isnet_gt", "u2net", "u2netl", "modnet"]
        self.net = get_net(net_name)
        if net_name == "isnet_is":
            self.gt_encoder = get_net("isnet_gt")
            for param in self.gt_encoder.parameters():
                param.requires_grad = False
        else:
            self.gt_encoder = None

    @classmethod
    def try_load(cls, net_name, ckpt_path, map_location=None):
        state_dict = torch.load(ckpt_path, map_location=map_location)
        if "epoch" in state_dict:
            return cls.load_from_checkpoint(ckpt_path, net_name=net_name, map_location=map_location)
        else:
            model = cls(net_name)
            if any([k.startswith("net.") for k, v in state_dict.items()]):
                model.load_state_dict(state_dict)
            else:
                model.net.load_state_dict(state_dict)
            return model

    def forward(self, x):
        if isinstance(self.net, ISNetDIS):
            return self.net(x)[0][0].sigmoid()
        if isinstance(self.net, ISNetGTEncoder):
            return self.net(x)[0][0].sigmoid()
        elif isinstance(self.net, U2NET):
            return self.net(x)[0].sigmoid()
        elif isinstance(self.net, MODNet):
            return self.net(x, True)[2]
        raise NotImplemented

def pil_transparent(image):
    if not image:
        return None

    if torch.cuda.is_available():
        device = 'cuda'
    else:
        device = 'cpu'
    
    model = AnimeSegmentation.try_load('isnet_is', 'model/isnetis.ckpt', device)
    model.eval()
    model.to(device)

    imn = np.array(image, dtype=np.uint8)
    img = cv2.cvtColor(imn, cv2.COLOR_RGB2BGR)
    mask = get_mask(model, img)

    img = np.concatenate((mask * img + 1 - mask, mask * 255), axis=2).astype(np.uint8)

    # save
    result, n = cv2.imencode('.webp', img, params=[int(cv2.IMWRITE_WEBP_QUALITY), 85])
    return n.tobytes()

def pil_transparent2(image):
    if not image:
        return None

    img = np.array(image, dtype=np.uint8)

    # Point 2: 元画像をBGR形式からBGRA形式に変換
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGRA)
     
    # Point 1: 白色部分に対応するマスク画像を生成
    color_lower = np.array([248, 248, 248, 255])
    color_upper = np.array([255, 255, 255, 255])
    mask = cv2.inRange(img, color_lower, color_upper)
    img = cv2.bitwise_not(img, img, mask=mask)
    # mask = np.all(img[:,:,:] == [255, 255, 255], axis=-1)

    # Point3: マスク画像をもとに、白色部分を透明化
    #img[mask,3] = 0

    # save
    result, n = cv2.imencode('.webp', img, params=[int(cv2.IMWRITE_WEBP_QUALITY), 85])

    buffer = io.BytesIO()
    n.tofile(buffer)
    
    return buffer

def infer(args: dict):
    binary = raw(args)
    return base64.b64encode(binary).decode('ascii')

def raw(args: dict):
    model_load()
    image = generate(args['add_prompt'] if 'add_prompt' in args else '')
    return pil_transparent(image)
