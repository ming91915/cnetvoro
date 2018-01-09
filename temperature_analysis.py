# -*- coding: utf-8 -*-
from __future__ import absolute_import
from sfepy.mechanics.matcoefs import stiffness_from_lame
import numpy as np
from scipy import spatial

def define(meshname, c):
    filename_mesh = meshname
    centroid = [float(coord) for coord in c.split(",")]
    def get_centroid(coors, domain=None):
        dis = np.array([spatial.distance.euclidean(c, centroid) for c in coors])
        return [dis.argsort()[0]]

    functions = {
        'get_centroid' : (get_centroid,),
    }

    regions = {
        'Omega' : 'all',
        'Surface' : ('vertices of surface','facet'),
        'Centroid' : 'cells by get_centroid',
    }

    materials = {
        'coef' : ({'val' : 1.0}, ),
    }

    fields = {
        'temperature': ('real', 1, 'Omega', 1),
    }

    integrals = {
        'i' : 1,
    }

    variables = {
        'T' : ('unknown field', 'temperature', 0),
        's' : ('test field', 'temperature', 'T'),
    }

    ebcs = {
        'T0' : ('Surface', {'T.0' : 1.0}),
        'T1' : ('Centroid', {'T.0' : 0.0}),
    }

    equations = {
        'balance_of_forces' :
        """dw_laplace.i.Omega( coef.val, s, T ) = 0""",
    }

    solvers = {
        'ls' : ('ls.scipy_direct', {}),
        'newton' : ('nls.newton', {
            'i_max'      : 1,
            'eps_a'      : 1e-10,
        }),
    }
    return locals()
