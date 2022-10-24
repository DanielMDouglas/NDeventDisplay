import h5py
import numpy as np

from LarpixParser import event_parser as EvtParser
from LarpixParser import hit_parser as HitParser
from LarpixParser import geom_dict_loader as DictLoader
from LarpixParser import util as util

import matplotlib.pyplot as plt
from matplotlib import cm, colors
import mpl_toolkits.mplot3d.art3d as art3d

import detector

def draw_boundaries(ax):
    for it in range(0,detector.TPC_BORDERS.shape[0],2):
        anode1 = plt.Rectangle((detector.TPC_BORDERS[it][0][0], detector.TPC_BORDERS[it][1][0]),
                               detector.TPC_BORDERS[it][0][1]-detector.TPC_BORDERS[it][0][0], 
                               detector.TPC_BORDERS[it][1][1]-detector.TPC_BORDERS[it][1][0],
                               linewidth=1, fc='none',
                               edgecolor='gray')
        ax.add_patch(anode1)
        art3d.pathpatch_2d_to_3d(anode1, z=detector.TPC_BORDERS[0][2][0], zdir="y")

        anode2 = plt.Rectangle((detector.TPC_BORDERS[it][0][0], detector.TPC_BORDERS[it][1][0]),
                               detector.TPC_BORDERS[it][0][1]-detector.TPC_BORDERS[it][0][0], 
                               detector.TPC_BORDERS[it][1][1]-detector.TPC_BORDERS[it][1][0],
                               linewidth=1, fc='none',
                               edgecolor='gray')
        ax.add_patch(anode2)
        art3d.pathpatch_2d_to_3d(anode2, z=detector.TPC_BORDERS[it+1][2][0], zdir="y")

        cathode = plt.Rectangle((detector.TPC_BORDERS[it][0][0], detector.TPC_BORDERS[it][1][0]),
                                detector.TPC_BORDERS[it][0][1]-detector.TPC_BORDERS[it][0][0], 
                                detector.TPC_BORDERS[it][1][1]-detector.TPC_BORDERS[it][1][0],
                                linewidth=1, fc='gray', alpha=0.2,
                                edgecolor='gray')
        ax.add_patch(cathode)
        z_cathode = (detector.TPC_BORDERS[it][2][0]+detector.TPC_BORDERS[it+1][2][0])/2
        art3d.pathpatch_2d_to_3d(cathode, z=z_cathode, zdir="y")

        ax.plot((detector.TPC_BORDERS[it][0][0],detector.TPC_BORDERS[it][0][0]),(detector.TPC_BORDERS[it][2][0],detector.TPC_BORDERS[it+1][2][0]),
                (detector.TPC_BORDERS[it][1][0],detector.TPC_BORDERS[it][1][0]), lw=1,color='gray')
        
        ax.plot((detector.TPC_BORDERS[it][0][0],detector.TPC_BORDERS[it][0][0]),(detector.TPC_BORDERS[it][2][0],detector.TPC_BORDERS[it+1][2][0]),
                (detector.TPC_BORDERS[it][1][1],detector.TPC_BORDERS[it][1][1]), lw=1,color='gray')

        ax.plot((detector.TPC_BORDERS[it][0][1],detector.TPC_BORDERS[it][0][1]),(detector.TPC_BORDERS[it][2][0],detector.TPC_BORDERS[it+1][2][0]),
                (detector.TPC_BORDERS[it][1][0],detector.TPC_BORDERS[it][1][0]), lw=1,color='gray')

        ax.plot((detector.TPC_BORDERS[it][0][1],detector.TPC_BORDERS[it][0][1]),(detector.TPC_BORDERS[it][2][0],detector.TPC_BORDERS[it+1][2][0]),
                (detector.TPC_BORDERS[it][1][1],detector.TPC_BORDERS[it][1][1]), lw=1,color='gray')

    ax.set_xlim(detector.TPC_BORDERS[0][0][0],detector.TPC_BORDERS[-1][0][1])
    ax.set_ylim(detector.TPC_BORDERS[0][2][0],detector.TPC_BORDERS[-1][2][0])
    ax.set_zlim(detector.TPC_BORDERS[0][1][0],detector.TPC_BORDERS[-1][1][1])

    xSpan = np.max(detector.TPC_BORDERS[:,0,:]) - np.min(detector.TPC_BORDERS[:,0,:])
    ySpan = np.max(detector.TPC_BORDERS[:,2,:]) - np.min(detector.TPC_BORDERS[:,2,:])
    zSpan = np.max(detector.TPC_BORDERS[:,1,:]) - np.min(detector.TPC_BORDERS[:,1,:])

    ax.set_box_aspect((xSpan/100, ySpan/100, zSpan/100))
    ax.grid(False)
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    ax.yaxis.set_major_locator(plt.MaxNLocator(5))                                    

def plot_event(filename, event_id, configs): 
    f = h5py.File(filename, 'r')
    packets = f['packets']
 
    geom_dict = DictLoader.load_geom_dict(configs['geom'])
    run_config = util.get_run_config(configs['detprop'])

    detector.set_detector_properties(configs['detprop'],
                                     configs['pixel'])
    
    t0_grp = EvtParser.get_t0(packets)

    t0 = t0_grp[event_id][0]
    print("--------event_id: ", event_id)
    # pckt_mask = (packets['timestamp'] > t0) & (packets['timestamp'] < t0 + 50000)
    pckt_mask = (packets['timestamp'] > 0)
    packets_ev = packets[pckt_mask]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
        
    x,y,z,dQ = HitParser.hit_parser_charge(t0, packets_ev, geom_dict, run_config)

    draw_boundaries(ax)

    ax.scatter(np.array(z)/10, np.array(x)/10, np.array(y)/10, c = dQ)
        
    plt.show()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type = str,
                        help = "input LArPix file")
    parser.add_argument('-e', '--eventid', type = int,
                        default = 0,
                        help = "geometry layout pickle file")
    parser.add_argument('-g', '--geometry', type = str,
                        default = "../../larpix_readout_parser/config_repo/dict_repo/multi_tile_layout-3.0.40.pkl",
                        help = "geometry layout pickle file")
    parser.add_argument('-p', '--pixelfile', type = str,
                        default = "../../larpix_readout_parser/config_repo/multi_tile_layout-3.0.40.yaml",
                        help = "pixel layout yaml file")
    parser.add_argument('-d', '--detprop', type = str,
                        default = "../../larpix_readout_parser/config_repo/ndlar-module.yaml",
                        help = "detector properties yaml file")

    args = parser.parse_args()

    plot_event(args.infile, args.eventid,
               {'geom': args.geometry,
                'pixel': args.pixelfile,
                'detprop': args.detprop})
