import os

def make_config(args):
    try:
        args = vars(args)
    except TypeError:
        pass
    
    if "pixellayout" in args and args["pixellayout"]:
        larpixlayout = args["pixellayout"]
        detprop = args["detprop"]
    elif args["detector"].lower() == "ndlar":
        larpixlayout = "multi_tile_layout-3.0.40"
        detprop = "ndlar-module.yaml"
    elif args["detector"].lower() == "module0":
        larpixlayout = "multi_tile_layout-2.3.16"
        detprop = "module0.yaml"

    larpixlayoutFile = os.path.join(os.path.dirname(__file__),
                                    "config",
                                    larpixlayout+".yaml")
    detpropFile = os.path.join(os.path.dirname(__file__),
                                    "config",
                                    detprop)
        
    config = {'larpix_layout_name': larpixlayout,
              'detprop_name': detprop,
              'pixelFile': larpixlayoutFile,
              'detpropFile': detpropFile,
              }

    return config
