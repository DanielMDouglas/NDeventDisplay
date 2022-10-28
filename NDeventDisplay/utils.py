import os

def make_config(args):
    if args.pixellayout:
        pixellayoutFile = args.pixellayout
        detpropFile = args.detprop
    elif args.detector.lower() == "ndlar":
        pixellayoutFile = os.path.join(os.path.dirname(__file__),
                                       "config",
                                       "multi_tile_layout-3.0.40.yaml")
        detpropFile = os.path.join(os.path.dirname(__file__),
                                   "config",
                                   "ndlar-module.yaml")
    elif args.detector.lower() == "module0":
        pixellayoutFile = os.path.join(os.path.dirname(__file__),
                                       "config",
                                       "multi_tile_layout-2.3.16.yaml")
        detpropFile = os.path.join(os.path.dirname(__file__),
                                   "config",
                                   "module0.yaml")

    config = {'pixel': pixellayoutFile,
              'detprop': detpropFile}

    return config
