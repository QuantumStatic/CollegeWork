from myfunctions import execute_this
import timm


@execute_this
def main():
    model = timm.create_model('vit_base_patch16_224', pretrained=True)
    model.eval()

