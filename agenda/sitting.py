import ctypes
import numpy as np
from agenda.models import Event

def sitting_arrang(event,tables):
    sit = ctypes.CDLL("sitting.so")

    nb_attendees = len(event.attendees.members.all())
    aff = event.attendees.relationship_matrix()

    affc = np.array(aff, dtype=ctypes.c_int)

    tablec = np.array(tables, dtype=ctypes.c_int)

    sit.sitting.restype = ctypes.POINTER(ctypes.c_int)

    res = sit.sitting(nb_attendees, affc.ctypes.data, tablec.ctypes.data, len(tables))
    res = np.ctypeslib.as_array(res, (nb_attendees,))

    return res
