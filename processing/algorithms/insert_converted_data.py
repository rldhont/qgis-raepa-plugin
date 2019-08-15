# -*- coding: utf-8 -*-

"""
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = '3liz'
__date__ = '2018-12-19'
__copyright__ = '(C) 2018 by 3liz'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from PyQt5.QtCore import QCoreApplication
from qgis.core import (
        QgsProcessing,
        QgsProcessingAlgorithm,
        QgsProcessingUtils,
        QgsProcessingException,
        QgsProcessingParameterString,
        QgsProcessingParameterBoolean,
        QgsProcessingOutputString
)
import os

class InsertConvertedData(QgsProcessingAlgorithm):
    """
    Insert imported and converted data into the schema raepa
    """

    PGSERVICE = 'PGSERVICE'
    SOURCE_HISTORIQUE = 'SOURCE_HISTORIQUE'
    CODE_CHANTIER = 'CODE_CHANTIER'
    NETTOYER_AVANT_INSERTION = 'NETTOYER_AVANT_INSERTION'
    OUTPUT_STRING = 'OUTPUT_STRING'

    def name(self):
        return 'insert_converted_data'

    def displayName(self):
        return self.tr('03 Insert converted data')

    def group(self):
        return self.tr('Import')

    def groupId(self):
        return 'raepa_import'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return self.__class__()

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        # INPUTS
        self.addParameter(
            QgsProcessingParameterString(
                self.PGSERVICE, 'PostgreSQL Service',
                defaultValue='raepa',
                optional=False
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.SOURCE_HISTORIQUE, 'Source historique',
                defaultValue='test',
                optional=False
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.CODE_CHANTIER, 'Code Chantier',
                defaultValue='test',
                optional=False
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.NETTOYER_AVANT_INSERTION, 'Nettoyer avant insertion',
                defaultValue=True,
                optional=False
            )
        )

        # OUTPUTS
        self.addOutput(
            QgsProcessingOutputString(
                self.OUTPUT_STRING, self.tr('Output message')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        import processing
        plugin_dir = os.path.dirname(os.path.abspath(__file__))

        msg = ''
        sql = '''
        SELECT raepa.import_tables_temporaires_dans_raepa(
            '%s', '%s', %s
        )
        ''' % (
            parameters[self.SOURCE_HISTORIQUE],
            parameters[self.CODE_CHANTIER],
            parameters[self.NETTOYER_AVANT_INSERTION]
        )
        feedback.pushInfo(sql)
        exec_result = processing.run("Raepa:raepa_execute_sql_on_service", {
            'PGSERVICE': parameters[self.PGSERVICE],
            'INPUT_SQL': sql
        }, context=context, feedback=feedback)

        feedback.pushInfo(exec_result['OUTPUT_STRING'])

        msg = exec_result['OUTPUT_STRING']
        return {
            self.OUTPUT_STRING: msg
        }