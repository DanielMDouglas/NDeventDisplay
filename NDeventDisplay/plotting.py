import numpy as np

from LarpixParser import hit_parser as HitParser
from LarpixParser import event_parser as EvtParser
from LarpixParser.geom_to_dict import larpix_layout_to_dict
from LarpixParser import util

import matplotlib.pyplot as plt
from matplotlib import cm, colors
import mpl_toolkits.mplot3d.art3d as art3d

from SLACplots import colors

from . import detector, utils, voxelize

def evd_ndlar(larpixFile, eventid):

    packets = larpixFile['packets']
    tracks = larpixFile['tracks']
    assn = larpixFile['mc_packets_assn']
    
    t0_grp = EvtParser.get_t0(packets)

    config = utils.make_config({"detector": "ndlar"})
    geom_dict = larpix_layout_to_dict('multi_tile_layout-3.0.40',
                                      save_dict = False)
    run_config = util.get_run_config('ndlar-module.yaml',
                                     use_builtin = True)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')

    draw_boundaries(ax, config)
    plot_event(ax, packets, eventid, t0_grp, geom_dict, run_config)
    plot_tracks(ax, packets, tracks, assn, eventid, t0_grp, geom_dict, run_config)
    
def draw_boundaries(ax, config):

    detector.set_detector_properties(config['detpropFile'],
                                     config['pixelFile'])

    patchCollection = []

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

        edge1 = ax.plot((detector.TPC_BORDERS[it][0][0],detector.TPC_BORDERS[it][0][0]),
                        (detector.TPC_BORDERS[it][2][0],detector.TPC_BORDERS[it+1][2][0]),
                        (detector.TPC_BORDERS[it][1][0],detector.TPC_BORDERS[it][1][0]),
                        lw=1,color='gray')
        
        edge2 = ax.plot((detector.TPC_BORDERS[it][0][0],detector.TPC_BORDERS[it][0][0]),
                        (detector.TPC_BORDERS[it][2][0],detector.TPC_BORDERS[it+1][2][0]),
                        (detector.TPC_BORDERS[it][1][1],detector.TPC_BORDERS[it][1][1]),
                        lw=1,color='gray')

        edge3 = ax.plot((detector.TPC_BORDERS[it][0][1],detector.TPC_BORDERS[it][0][1]),
                        (detector.TPC_BORDERS[it][2][0],detector.TPC_BORDERS[it+1][2][0]),
                        (detector.TPC_BORDERS[it][1][0],detector.TPC_BORDERS[it][1][0]),
                        lw=1,color='gray')

        edge4 = ax.plot((detector.TPC_BORDERS[it][0][1],detector.TPC_BORDERS[it][0][1]),
                        (detector.TPC_BORDERS[it][2][0],detector.TPC_BORDERS[it+1][2][0]),
                        (detector.TPC_BORDERS[it][1][1],detector.TPC_BORDERS[it][1][1]),
                        lw=1,color='gray')

        patchCollection.append(anode1)
        patchCollection.append(anode2)
        patchCollection.append(cathode)
        patchCollection.append(edge1[0])
        patchCollection.append(edge2[0])
        patchCollection.append(edge3[0])
        patchCollection.append(edge4[0])

    return patchCollection
    
def plot_event(ax, packets, event_id, t0_grp, geom_dict, run_config):
    t0 = t0_grp[event_id][0]
    ti = t0 + run_config['time_interval'][0]/run_config['CLOCK_CYCLE']
    tf = t0 + run_config['time_interval'][1]/run_config['CLOCK_CYCLE']

    pckt_mask = (packets['timestamp'] > ti) & (packets['timestamp'] < tf)
    packets_ev = packets[pckt_mask]

    x,y,z,dQ = HitParser.hit_parser_charge(t0,
                                           packets_ev,
                                           geom_dict,
                                           run_config,
                                           drift_model = 1)

    hitCollection = []
    hitCollection.append(ax.scatter(np.array(z)/10,
                                    np.array(x)/10,
                                    np.array(y)/10,
                                    c = dQ,
                                    cmap = 'SLACjet'))

    return hitCollection

def plot_tracks(ax, packets, tracks, assn, event_id, t0_grp, geom_dict, run_config):
    t0 = t0_grp[event_id][0]
    ti = t0 + run_config['time_interval'][0]/run_config['CLOCK_CYCLE']
    tf = t0 + run_config['time_interval'][1]/run_config['CLOCK_CYCLE']

    pckt_mask = (packets['timestamp'] > ti) & (packets['timestamp'] < tf)
    track_ev_id = np.unique(EvtParser.packet_to_eventid(assn, tracks)[pckt_mask])
    
    track_mask = tracks['eventID'] == track_ev_id
    tracks_ev = tracks[track_mask]

    xStart = tracks_ev['x_start']
    yStart = tracks_ev['y_start']
    zStart = tracks_ev['z_start']

    xEnd = tracks_ev['x_end']
    yEnd = tracks_ev['y_end']
    zEnd = tracks_ev['z_end']

    xSegs = np.array([xStart, xEnd]).T
    ySegs = np.array([yStart, yEnd]).T
    zSegs = np.array([zStart, zEnd]).T

    segmentCollection = []
    for xSeg, ySeg, zSeg in zip(xSegs, ySegs, zSegs):
        segmentCollection.append(ax.plot(xSeg,
                                         zSeg,
                                         ySeg,
                                         color = colors.SLACred
                                         )[0])

    return segmentCollection

def plot_edep_voxels(ax, packets, tracks, assn, event_id, t0_grp, geom_dict, run_config):
    t0 = t0_grp[event_id][0]
    ti = t0 + run_config['time_interval'][0]/run_config['CLOCK_CYCLE']
    tf = t0 + run_config['time_interval'][1]/run_config['CLOCK_CYCLE']

    pckt_mask = (packets['timestamp'] > ti) & (packets['timestamp'] < tf)
    track_ev_id = np.unique(EvtParser.packet_to_eventid(assn, tracks)[pckt_mask])
    
    track_mask = tracks['eventID'] == track_ev_id
    tracks_ev = tracks[track_mask]

    coords, dE = voxelize.voxelize(tracks_ev)

    x = np.array([coord[0] for coord in coords])
    y = np.array([coord[1] for coord in coords])
    z = np.array([coord[2] for coord in coords])

    edepCollection = []
    edepCollection.append(ax.scatter(np.array(x),
                                     np.array(z),
                                     np.array(y),
                                     c = dE,
                                     cmap = 'SLACjet'))

    return edepCollection
