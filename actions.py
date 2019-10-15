"""Actions."""

from qgis.core import (
    QgsProject,
    QgsLineSymbol,
    QgsFeatureRequest,
    Qgis,
    QgsProcessingException,
    QgsMessageLog,
)
from qgis.utils import iface

try:
    # QGIS >= 3.8
    from qgis import processing
except ImportError:
    # QGIS < 3.8
    import processing

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


def inverser_canalisation(*args):
    id_canalisation = int(args[0])
    id_layer = args[1]

    layer = QgsProject.instance().mapLayer(id_layer)

    # materialized feature in new layer
    request = QgsFeatureRequest()
    request.setFilterFids([id_canalisation])
    mat = layer.materialize(request)

    # run the processing alg "reverse line direction"
    params = {
        'INPUT': mat,
        'OUTPUT': 'memory:test'
    }
    try:
        out = processing.run('native:reverselinedirection', params)
    except QgsProcessingException:
        QgsMessageLog.logMessage('Error in the Processing/Postgis logs.', 'RAEPA', Qgis.Critical)
        iface.messageBar().pushMessage(
            'Error in Processing/Postgis logs.', level=Qgis.Critical, duration=2)
        return

    vout = out['OUTPUT']
    for feat in vout.getFeatures():
        if layer.changeGeometry(id_canalisation, feat.geometry()):
            # message
            iface.messageBar().pushMessage(
                "Line direction has been reversed",
                level=Qgis.Success,
                duration=2
            )
            iface.mapCanvas().refresh()
        else:
            iface.messageBar().pushMessage(
                "Line direction has NOT been reversed. Check if the layer is editable",
                level=Qgis.Critical,
                duration=2
            )


def annuler_la_derniere_modification(*args):
    id_ouvrage = args[0]
    id_layer = args[1]

    layer = QgsProject.instance().mapLayer(id_layer)

    # use processing alg cancel_last_modification
    params = {
        'SOURCE_LAYER': layer,
        'SOURCE_ID': id_ouvrage
    }
    try:
        processing.run('raepa:cancel_last_modification', params)
    except QgsProcessingException:
        QgsMessageLog.logMessage('Error in the Processing/Postgis logs.', 'RAEPA', Qgis.Critical)
        iface.messageBar().pushMessage(
            'Error in Processing/Postgis logs.', level=Qgis.Critical, duration=2)
        return

    # Refresh upstream and downstream
    for layername in [layer.name(), 'Canalisations']:
        gl = QgsProject.instance().mapLayersByName(layername)
        if gl:
            gl[0].triggerRepaint()


def couper_la_canalisation_sous_cet_ouvrage(*args):
    id_ouvrage = args[0]
    id_layer = args[1]

    layer = QgsProject.instance().mapLayer(id_layer)

    # Use alg to do cut_pipe_under_item
    sql = "SELECT raepa.decoupage_canalisation_par_ouvrage('{}');".format(id_ouvrage)
    params = {
        'INPUT_SQL': sql
    }
    try:
        processing.run('raepa:execute_sql', params)
    except QgsProcessingException:
        QgsMessageLog.logMessage('Error in the Processing/Postgis logs.', 'RAEPA', Qgis.Critical)
        iface.messageBar().pushMessage(
            'Error in Processing/Postgis logs.', level=Qgis.Critical, duration=2)
        return

    # Refresh layers
    for layername in [layer.name(), 'Canalisations']:
        gl = QgsProject.instance().mapLayersByName(layername)
        if gl:
            gl[0].triggerRepaint()


def parcourir_reseau_depuis_cet_ouvrage(*args):
    idouvrage = args[0]
    target_table = args[1]

    # Use alg get_downstream_route and get_upstream_route
    params = {
        'OUTPUT_LAYER_NAME': '',
        'SOURCE_ID': idouvrage,
        'TARGET_TABLE': target_table
    }
    try:
        down = processing.run('raepa:get_downstream_route', params)
    except QgsProcessingException:
        QgsMessageLog.logMessage('Error in the Processing/Postgis logs.', 'RAEPA', Qgis.Critical)
        iface.messageBar().pushMessage(
            'Error in Processing/Postgis logs.', level=Qgis.Critical, duration=2)
        return

    if down['OUTPUT_STATUS'] == 1:
        layer = down['OUTPUT_LAYER']
        layer.setName(down['OUTPUT_LAYER_RESULT_NAME'])
        symbol = QgsLineSymbol.createSimple(
            {
                'line_color': '255,50,50,255',
                'line_style': 'solid',
                'line_width': '1.8'
            }
        )
        layer.renderer().setSymbol(symbol)
        QgsProject.instance().addMapLayer(layer)

    params = {
        'OUTPUT_LAYER_NAME': '',
        'SOURCE_ID': idouvrage,
        'TARGET_TABLE': target_table
    }
    try:
        up = processing.run('raepa:get_upstream_route', params)
    except QgsProcessingException:
        QgsMessageLog.logMessage('Error in the Processing/Postgis logs.', 'RAEPA', Qgis.Critical)
        iface.messageBar().pushMessage(
            'Error in Processing/Postgis logs.', level=Qgis.Critical, duration=2)
        return

    if up['OUTPUT_STATUS'] == 1:
        layer = up['OUTPUT_LAYER']
        layer.setName(up['OUTPUT_LAYER_RESULT_NAME'])
        symbol = QgsLineSymbol.createSimple(
            {
                'line_color': '50,255,50,255',
                'line_style': 'solid',
                'line_width': '1.8'
            }
        )
        layer.renderer().setSymbol(symbol)
        QgsProject.instance().addMapLayer(layer)