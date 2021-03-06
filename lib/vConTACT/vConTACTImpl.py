# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
from GenomeFileUtil.GenomeFileUtilClient import GenomeFileUtil as gfu
from KBaseDataObjectToFileUtils.KBaseDataObjectToFileUtilsClient import KBaseDataObjectToFileUtils as ofu
from vConTACT.vConTACT_utils.vConTACTUtils import vConTACTUtils
from vConTACT.kb_object_utils.KBObjectUtils import KBObjectUtils

from GenomeAnnotationAPI.GenomeAnnotationAPIClient import GenomeAnnotationAPI
from DataFileUtil.DataFileUtilClient import DataFileUtil as dfu

#END_HEADER

class vConTACT:
    '''
    Module Name:
    vConTACT

    Module Description:
    A KBase module: vConTACT
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/bolduc/vcontact"
    GIT_COMMIT_HASH = "ff92f754f02d757aa925d2327fc8ef2bf0af4b07"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.config = config
        #END_CONSTRUCTOR
        pass


    def run_vcontact(self, ctx, params):
        """
        :param params: instance of type "InParams" -> structure: parameter
           "genome" of type "obj_ref" (Insert your typespec information here.)
        """
        # ctx is the context object
        #BEGIN run_vcontact
        self.callback_url = os.environ['SDK_CALLBACK_URL']

        vc = vConTACTUtils(self.config)

        self.genome_api = GenomeAnnotationAPI(self.callback_url)
        genome = params['genome']
        genome_data = self.genome_api.get_genome_v1({"genomes": [{"ref": genome}]})

        gene2genome, sequences = vc.genome_to_inputs(genome_data)

        gene2genome_fp, sequences_fp = vc.write_inputs(gene2genome, sequences)

        params['gene2genome'] = gene2genome_fp
        params['sequences'] = sequences_fp

        returnVal = vc.run_vcontact(params)

        vc.vcontact_help()

        kbo = KBObjectUtils(self.config)
        kbo.create_report(params['workspace_name'])

        #END run_vcontact
        pass
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
