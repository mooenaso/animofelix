import torchvision
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def get_model(device='cpu', model_name='v2'):
    # Load the model.
    if model_name == 'v2':
        model = torchvision.models.detection.fasterrcnn_resnet50_fpn_v2(
            weights='DEFAULT'
        )
    elif model_name == 'v1':
        model = torchvision.models.detection.fasterrcnn_resnet50_fpn(
            weights='DEFAULT'
        )
    elif model_name == 'v3':
        model = torchvision.models.detection.fasterrcnn_mobilenet_v3_large_fpn(
            weights='DEFAULT')
    else:
        model = torchvision.models.detection.fasterrcnn_mobilenet_v3_large_320_fpn(
            weight='DEFAULT')
        
    # Load the model onto the computation device.
    model = model.eval().to(device)
    return model